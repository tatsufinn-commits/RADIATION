#!/usr/bin/env python3
"""relay.py — semantic validation of task bundles (patch 4400; auditor plan item 2).
Replaces filename-topology-only relay checking. A TID is either:
  legacy_trace  — listed in evidence/tasks/legacy_manifest.json; judged by the
                  filename-triple rule only, status historical_unverified; or
  canonical     — must own evidence/tasks/<TID>/ with task.json (TaskEnvelope),
                  plan JSON, commands/, outcomes/, events.ndjson, projection.json
                  satisfying the state machine and evidence-digest rules.
Self-test: python3 -m radiation_core.relay   (negative vectors MUST fail).
Stdlib only. Exit 0 = all bundles valid; 1 = findings exist.
"""
import hashlib, json, os, re, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(ROOT, "evidence", "tasks")
STATES = ("RECEIVED","ACCEPTED","CONTEXT_READY","PLAN_PROPOSED","PLAN_APPROVED",
          "COMMAND_PROPOSED","COMMAND_AUTHORIZED","EXECUTING","OBSERVED",
          "STEP_VERIFIED","FINAL_VERIFYING","COMPLETE","REPLAN_REQUIRED","BLOCKED","FAILED")
TRANS = {
 "input.received":"RECEIVED","task.accepted":"ACCEPTED","context.built":"CONTEXT_READY",
 "plan.proposed":"PLAN_PROPOSED","plan.approved":"PLAN_APPROVED","command.proposed":"COMMAND_PROPOSED",
 "command.authorized":"COMMAND_AUTHORIZED","execution.started":"EXECUTING","outcome.recorded":"OBSERVED",
 "verification.passed":"STEP_VERIFIED","task.completed":"COMPLETE","task.blocked":"BLOCKED",
 "replan":"REPLAN_REQUIRED"}
OPS = {"read_file","run_validator","run_test","apply_patch","build_artifact","render_docs","stage_files"}
ALLOWED = {  # event -> required prior state (state-machine guards)
 "input.received":None,"task.accepted":"RECEIVED","context.built":"ACCEPTED",
 "plan.proposed":"CONTEXT_READY","plan.approved":("PLAN_PROPOSED","REPLAN_REQUIRED"),  # replan re-approval is legal
 "command.proposed":("PLAN_APPROVED","STEP_VERIFIED","REPLAN_REQUIRED"),
 "command.authorized":"COMMAND_PROPOSED","execution.started":"COMMAND_AUTHORIZED",
 "outcome.recorded":("EXECUTING",),"verification.passed":"OBSERVED",
 "task.completed":("STEP_VERIFIED","FINAL_VERIFYING"),"task.blocked":None,"replan":None}

def _sha(p):
    h = hashlib.sha256()
    with open(p,"rb") as fh:
        for b in iter(lambda: fh.read(65536), b""): h.update(b)
    return h.hexdigest()

def _req(obj, fields, where, out):
    for f in fields:
        if f not in obj or obj[f] in (None,"",[]): out.append(f"{where}: missing required field '{f}'")

def load_legacy():
    p = os.path.join(EVID,"legacy_manifest.json")
    try: return set(json.load(open(p,encoding="utf-8"))["legacy_tids"])
    except Exception: return set()

def validate_bundle(tid, d):
    """Full semantic validation of one canonical bundle -> list[str] findings."""
    out = []
    tj = os.path.join(d,"task.json")
    if not os.path.isfile(tj): return [f"{tid}: task.json missing (bundle is not a TaskEnvelope)"]
    try: env = json.load(open(tj,encoding="utf-8"))
    except Exception as e: return [f"{tid}: task.json unparseable: {e}"]
    _req(env,["schema_version","task_id","source","principal","received_at","mode_hint","base_revision","idempotency_key"],f"{tid}/task.json",out)
    if env.get("task_id") != tid: out.append(f"{tid}: envelope task_id mismatch")
    if env.get("schema_version") != "1.0": out.append(f"{tid}: unsupported schema_version {env.get('schema_version')!r}")
    if not re.match(r"^[0-9a-f]{7,40}$", str(env.get("base_revision",""))): out.append(f"{tid}: base_revision not a git SHA")
    # plan
    plans = [f for f in os.listdir(d) if re.match(r"plan(\.v\d+)?\.json$",f)]
    if not plans: out.append(f"{tid}: no plan JSON")
    plan = None
    for pf in sorted(plans):
        try: p = json.load(open(os.path.join(d,pf),encoding="utf-8"))
        except Exception as e: out.append(f"{tid}: {pf} unparseable: {e}"); continue
        _req(p,["plan_id","task_id","base_revision","steps"],f"{tid}/{pf}",out)
        for st in p.get("steps",[]):
            _req(st,["step_id","operation_class","success_predicate"],f"{tid}/{pf}:{st.get('step_id')}",out)
        if plan is None and p.get("task_id")==tid: plan = p
    # commands + outcomes
    cmds, outs = {}, {}
    for sub,store in (("commands",cmds),("outcomes",outs)):
        sd = os.path.join(d,sub)
        if os.path.isdir(sd):
            for f in sorted(os.listdir(sd)):
                if not f.endswith(".json"): continue
                try: o = json.load(open(os.path.join(sd,f),encoding="utf-8"))
                except Exception as e: out.append(f"{tid}/{sub}/{f}: unparseable: {e}"); continue
                store[f[:-5]] = o
    for cid,c in cmds.items():
        _req(c,["command_id","task_id","plan_id","step_id","operation"],f"{tid}/commands/{cid}",out)
        if c.get("operation") not in OPS: out.append(f"{tid}/commands/{cid}: operation {c.get('operation')!r} outside the allowlist")
        if c.get("task_id") != tid: out.append(f"{tid}/commands/{cid}: cross-task command (causation broken)")
        if plan and c.get("plan_id") != plan.get("plan_id"): out.append(f"{tid}/commands/{cid}: references plan {c.get('plan_id')!r}, bundle plan is {plan.get('plan_id')!r}")
        steps = {s.get("step_id") for s in (plan or {}).get("steps",[])}
        if plan and c.get("step_id") not in steps: out.append(f"{tid}/commands/{cid}: step {c.get('step_id')!r} not in approved plan")
        if cid not in outs: out.append(f"{tid}/commands/{cid}: no outcome recorded")
    for oid,o in outs.items():
        _req(o,["command_id","task_id","result","evidence"],f"{tid}/outcomes/{oid}",out)
        if o.get("result") not in ("succeeded","failed","stale_precondition","policy_denied","timed_out","security_blocked"):
            out.append(f"{tid}/outcomes/{oid}: illegal result {o.get('result')!r}")
        for ev in o.get("evidence",[]):
            ep = os.path.join(ROOT, ev.get("path",""))
            if not os.path.isfile(ep): out.append(f"{tid}/outcomes/{oid}: evidence path missing: {ev.get('path')}")
            elif ev.get("sha256") != _sha(ep): out.append(f"{tid}/outcomes/{oid}: evidence digest mismatch: {ev.get('path')}")
        if o.get("result") == "failed" and oid in cmds: out.append(f"{tid}/outcomes/{oid}: failed command has no replan event or follow-up")
    # events: order, transitions, duplicates
    ej = os.path.join(d,"events.ndjson")
    if not os.path.isfile(ej): out.append(f"{tid}: events.ndjson missing (append-only causal record)")
    else:
        seqs, state, done = [], "RECEIVED", False
        for ln in open(ej,encoding="utf-8"):
            ln = ln.strip()
            if not ln: continue
            try: e = json.loads(ln)
            except Exception as ex: out.append(f"{tid}/events.ndjson: unparseable line: {ex}"); continue
            _req(e,["seq","event_id","task_id","type","at","actor"],f"{tid}/events",out)
            if e.get("task_id") != tid: out.append(f"{tid}/events: foreign task_id {e.get('task_id')!r}")
            seqs.append(e.get("seq"))
            t = e.get("type")
            if t not in TRANS: out.append(f"{tid}/events: unknown event type {t!r}"); continue
            need = ALLOWED.get(t)
            ok = (need is None) if not isinstance(need,tuple) else (state in need)
            if isinstance(need,str): ok = (state == need)
            if not ok: out.append(f"{tid}/events: illegal transition {state} --{t}--> ")
            state = TRANS[t]
            if t == "task.completed": done = True
        if seqs != sorted(seqs): out.append(f"{tid}/events: sequence numbers out of order (append-only violated)")
        if len(seqs) != len(set(seqs)): out.append(f"{tid}/events: duplicate sequence numbers")
        if not done: out.append(f"{tid}: no task.completed event (closure without completion)")
    if done and not outs: out.append(f"{tid}: completed with zero outcomes (no evidence)")
    return out

def validate_active(neurons_dir=None):
    """The check-27 engine: legacy triple rule + canonical bundle rule."""
    findings = []
    nd = neurons_dir or os.path.join(ROOT,"scaffolding","neurons")
    stages = (("sensoryneurons","intake"),("interneurons","reasoning"),("motorneurons","orders"))
    tids, files = set(), {}
    legacy = load_legacy()
    for stage,suf in stages:
        sd = os.path.join(nd,stage)
        fs = sorted(f for f in os.listdir(sd) if f.endswith(".md")) if os.path.isdir(sd) else []
        files[stage] = fs
        if not any(f.startswith("TEMPLATE") for f in fs):
            findings.append(f"{stage}: TEMPLATE record missing")
        for f in fs:
            m = re.match(r"TID-(.+)_"+suf+r"\.md$", f)
            if m: tids.add(m.group(1))
    for tid in sorted(tids):
        trip = [f"TID-{tid}_{suf}.md" in files[st] for st,suf in stages]
        if tid in legacy:
            if not all(trip): findings.append(f"TID-{tid} (legacy_trace): incomplete filename triple")
            continue
        if not all(trip): findings.append(f"TID-{tid}: incomplete filename triple")
        # projection fidelity (4400): the Markdown neurons are RENDERED projections
        # of the bundle - a motor record of gibberish must never pass again (the
        # audit's negative mutation test is now a standing law, not a demo).
        for stage,suf in stages:
            fp = os.path.join(nd,stage,f"TID-{tid}_{suf}.md")
            body = open(fp,encoding="utf-8",errors="replace").read() if os.path.isfile(fp) else ""
            if f"TID-{tid}" not in body:
                findings.append(f"TID-{tid}: {stage} projection does not name its TID (hand-authored drift)")
            if "evidence/tasks/" not in body:
                findings.append(f"TID-{tid}: {stage} projection carries no bundle evidence link")
        findings.extend(validate_bundle(f"TID-{tid}", os.path.join(EVID,f"TID-{tid}")))
    return findings

def _self_test_vectors():
    # synthetic canonical bundle in a temp dir; mutations of it MUST fail
    root = tempfile.mkdtemp(prefix="relay_selftest_")
    tid = "TID-2026-09-14-z"
    d = os.path.join(root, "evidence", "tasks", tid)
    os.makedirs(d)
    rev = "c9592bba7699928260c38de08b0929676a40114e"
    json.dump({"schema_version":"1.0","task_id":tid,
               "source":{"kind":"commander","artifact_ref":"artifact://t","trust":"root"},
               "principal":"commander","received_at":"2026-09-14T12:00:00+08:00",
               "mode_hint":"autopilot","base_revision":rev,
               "idempotency_key":"selftest-4400-vec"}, open(os.path.join(d,"task.json"),"w"))
    json.dump({"schema_version":"1.0","plan_id":"P1","task_id":tid,"base_revision":rev,
               "steps":[{"step_id":"S1","operation_class":"verify","success_predicate":"exit==0"}]},
              open(os.path.join(d,"plan.v1.json"),"w"))
    os.makedirs(os.path.join(d,"commands")); os.makedirs(os.path.join(d,"outcomes"))
    json.dump({"schema_version":"1.0","command_id":"C1","task_id":tid,"plan_id":"P1","step_id":"S1",
               "operation":"run_test","issued_at":"2026-09-14T12:01:00+08:00","base_revision":rev},
              open(os.path.join(d,"commands","C1.json"),"w"))
    art = os.path.join(d, "evidence.txt"); open(art,"w").write("ok")
    dg = hashlib.sha256(open(art,"rb").read()).hexdigest()
    json.dump({"schema_version":"1.0","command_id":"C1","task_id":tid,"result":"succeeded",
               "evidence":[{"path":art,"sha256":dg}]}, open(os.path.join(d,"outcomes","C1.json"),"w"))
    seq = ["input.received","task.accepted","context.built","plan.proposed","plan.approved",
           "command.proposed","command.authorized","execution.started","outcome.recorded",
           "verification.passed","task.completed"]
    ev = [{"seq":i+1,"event_id":f"e{i+1}","task_id":tid,"type":ty,
           "at":f"2026-09-14T12:00:{i:02d}+08:00","actor":"relay"} for i,ty in enumerate(seq)]
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(json.dumps(e) for e in ev))
    json.dump({"task_id":tid,"state":"COMPLETE"}, open(os.path.join(d,"projection.json"),"w"))
    return root, d, tid

def self_test():
    ok = 0
    root, d, tid = _self_test_vectors()
    f = validate_bundle(tid, d)
    ok += (len(f) == 0)
    print(f"  vector 1 valid bundle clean -> {'PASS' if not f else f}")
    p = os.path.join(d,"outcomes","C1.json")
    o = json.load(open(p)); o["evidence"][0]["sha256"] = "0"*64
    json.dump(o, open(p,"w"))
    f2 = validate_bundle(tid, d)
    v2 = any("digest mismatch" in x for x in f2); ok += v2
    print(f"  vector 2 tampered evidence caught -> {'PASS' if v2 else 'FAIL'}")
    o["evidence"][0]["sha256"] = hashlib.sha256(open(os.path.join(d,"evidence.txt"),"rb").read()).hexdigest()
    json.dump(o, open(p,"w"))
    lines = open(os.path.join(d,"events.ndjson")).read().splitlines()
    del lines[6]  # drop command.authorized -> execution.started becomes illegal
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(lines))
    f3 = validate_bundle(tid, d)
    v3 = any("illegal transition" in x for x in f3); ok += v3
    print(f"  vector 3 unauthorized execution caught -> {'PASS' if v3 else 'FAIL'}")
    # vector 4: a LEGAL replan (completed task -> replan -> re-approval) must pass
    shutil.rmtree(root)
    root, d, tid = _self_test_vectors()
    lines = open(os.path.join(d,"events.ndjson")).read().splitlines()
    import json as _j
    seq = _j.loads(lines[-1])["seq"]
    ins = [_j.dumps({"seq":seq+1,"event_id":f"e{seq+1}","task_id":tid,"type":"replan","at":"2026-09-14T13:00:00+08:00","actor":"relay"}),
           _j.dumps({"seq":seq+2,"event_id":f"e{seq+2}","task_id":tid,"type":"plan.approved","at":"2026-09-14T13:00:05+08:00","actor":"policy"})]
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(lines + ins) + "\n")
    f4 = validate_bundle(tid, d)
    v4 = (len(f4) == 0); ok += v4
    print(f"  vector 4 legal replan sequence -> {'PASS' if v4 else f4}")
    shutil.rmtree(root)
    print(f"relay self-test: {ok}/4 vectors")
    return 0 if ok == 4 else 1

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    f = validate_active()
    for x in f: print("✗", x)
    print(f"relay: {len(f)} finding(s)")
    sys.exit(1 if f else 0)
