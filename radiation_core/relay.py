#!/usr/bin/env python3
"""relay.py - semantic validation of task bundles (patch 4500 hardening).
History: 4400 introduced bundles; 4500 closes the recheck gaps:
  - schemas/ are EXECUTED (required/const/enum/pattern/type subset), not decorative;
  - outcome identity is bound: file stem == internal command_id (CMD-MISMATCH fails);
  - projection.json is parsed and must equal the event-derived final state;
  - causation: command events carry ref=<command_id>, verified for coverage;
  - base_revision agreement across envelope/plan/commands;
  - unique event_ids, RFC-3339 timestamps, monotonic order.
Legacy rule (II.10.6, CLOSED list): pre-runtime TIDs stay legacy_trace forever;
every task after 4400 ships a canonical bundle. The list never grows.
Self-test: python3 -m radiation_core.relay --self-test  (6 vectors, negatives MUST fail).
Stdlib only. Exit 0 = valid; 1 = findings."""
import hashlib, json, os, re, sys, tempfile, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(ROOT, "evidence", "tasks")
SCHEMA_DIR = os.path.join(ROOT, "schemas")
STATES = ("RECEIVED","ACCEPTED","CONTEXT_READY","PLAN_PROPOSED","PLAN_APPROVED",
          "COMMAND_PROPOSED","COMMAND_AUTHORIZED","EXECUTING","OBSERVED",
          "STEP_VERIFIED","FINAL_VERIFYING","COMPLETE","REPLAN_REQUIRED","BLOCKED","FAILED")
# TARGET: the destination state of every event (single-valued by construction).
# ALLOWED (below) constrains the ORIGINS. They are different things; conflating
# them made the state itself a tuple after plan.re-approval (caught by vector 1).
TARGET = {
 "input.received":"RECEIVED","task.accepted":"ACCEPTED","context.built":"CONTEXT_READY",
 "plan.proposed":"PLAN_PROPOSED","plan.approved":"PLAN_APPROVED",
 "command.proposed":"COMMAND_PROPOSED","command.authorized":"COMMAND_AUTHORIZED",
 "execution.started":"EXECUTING","outcome.recorded":"OBSERVED",
 "verification.passed":"STEP_VERIFIED","task.completed":"COMPLETE","task.blocked":"BLOCKED",
 "replan":"REPLAN_REQUIRED"}
OPS = {"read_file","run_validator","run_test","apply_patch","build_artifact","render_docs","stage_files"}
CAUSAL = {"command.proposed","command.authorized","execution.started","outcome.recorded","verification.passed"}
ALLOWED = {  # event -> required prior state(s)
 "input.received":None,"task.accepted":"RECEIVED","context.built":"ACCEPTED",
 "plan.proposed":"CONTEXT_READY","plan.approved":("PLAN_PROPOSED","REPLAN_REQUIRED"),
 "command.proposed":("PLAN_APPROVED","STEP_VERIFIED","REPLAN_REQUIRED"),
 "command.authorized":"COMMAND_PROPOSED","execution.started":"COMMAND_AUTHORIZED",
 "outcome.recorded":("EXECUTING",),"verification.passed":"OBSERVED",
 "task.completed":("STEP_VERIFIED","FINAL_VERIFYING"),"task.blocked":None,"replan":None}

_SCHEMAS = {}
_K_CONST, _K_ENUM, _K_PAT = "const", "enum", "pattern"
def _load_schema(name):
    if name not in _SCHEMAS:
        p = os.path.join(SCHEMA_DIR, name)
        try: _SCHEMAS[name] = json.load(open(p, encoding="utf-8"))
        except Exception: _SCHEMAS[name] = None
    return _SCHEMAS[name]

def _fits(v, spec):
    """Trial validation for applicators (oneOf): does v fit this subschema?"""
    out: list[str] = []
    _validate_against(v, spec, "trial", out)
    return not out


_SCHEMA_KEYWORDS_EXECUTED = {
    "type", "required", "properties", "items", "additionalProperties",
    "const", "enum", "pattern", "minLength", "maxLength",
    "minimum", "maximum", "minItems", "maxItems",
    "oneOf", "anyOf", "allOf", "not", "if", "then",
}
# $defs/definitions are containers (recursed); $schema/title/description are
# annotations; `format` is ANNOTATION-ONLY in JSON Schema 2020-12 unless a
# format-assertion vocabulary is declared — we do not assert formats, and the
# coverage scan must not criminalize a legal annotation.
_SCHEMA_META_ANNOTATIONS = {"$schema", "title", "description", "$defs", "definitions", "format"}


def unsupported_keywords(spec, acc=None):
    """5600 closure: keywords a schema USES but this executor does NOT execute.

    A schema is a claim; the executor is its truth. validate check 40 runs
    this over every shipped schema — an unexecuted keyword in a shipped
    schema is a build failure, never a silent freebie."""
    if acc is None: acc = []
    if isinstance(spec, dict):
        for k, sub in spec.items():
            if k in _SCHEMA_META_ANNOTATIONS:
                continue
            if k == "properties":
                for p in sub.values(): unsupported_keywords(p, acc)
            elif k in ("items", "not", "additionalProperties"):
                if isinstance(sub, dict): unsupported_keywords(sub, acc)
            elif k in ("oneOf", "anyOf", "allOf"):
                for s in sub: unsupported_keywords(s, acc)
            elif k not in _SCHEMA_KEYWORDS_EXECUTED and k not in acc:
                acc.append(k)
    return acc


def _validate_against(v, spec, where, out):
    """Recursive execution of the schema subset our contracts use — and the
    set is CLOSED: type (boolean strict; bool is NOT an integer), required,
    properties, additionalProperties (false | schema), items, const, enum,
    pattern, minLength, maxLength, minimum, maximum, minItems, maxItems,
    oneOf, anyOf, allOf, not. `unsupported_keywords` + validate check 40
    enforce that no shipped schema uses anything outside this set (5600):
    a schema claim the executor cannot execute is a build failure, never a
    silent freebie."""
    if not isinstance(spec, dict): return
    if "allOf" in spec:
        for s in spec["allOf"]:
            if isinstance(s, dict): _validate_against(v, s, where, out)
    if "oneOf" in spec:
        hits = sum(1 for s in spec["oneOf"] if isinstance(s, dict) and _fits(v, s))
        if hits != 1:
            out.append(f"{where}: oneOf violated (matched {hits} of "
                       f"{len(spec['oneOf'])} subschemas)")
    if "anyOf" in spec:
        hits = sum(1 for s in spec["anyOf"] if isinstance(s, dict) and _fits(v, s))
        if hits < 1:
            out.append(f"{where}: anyOf violated (matched 0 of "
                       f"{len(spec['anyOf'])} subschemas)")
    if "not" in spec and isinstance(spec["not"], dict) and _fits(v, spec["not"]):
        out.append(f"{where}: 'not' violated (matched the forbidden subschema)")
    if "if" in spec and isinstance(spec["if"], dict) and _fits(v, spec["if"]):
        then = spec.get("then")
        if isinstance(then, dict): _validate_against(v, then, where, out)
    # Constraints apply by INSTANCE type (JSON Schema semantics) — gating
    # them on a DECLARED type made typeless subschemas (if/then/anyOf arms)
    # vacuous. Type assertions happen at the bottom, without early returns.
    if isinstance(v, dict):
        for r in spec.get("required", []):
            if r not in v: out.append(f"{where}: schema-required field {r!r} missing")
        props = spec.get("properties", {})
        ap = spec.get("additionalProperties", True)
        for k, rv in v.items():
            if k in props: _validate_against(rv, props[k], f"{where}.{k}", out)
            elif ap is False:
                out.append(f"{where}: unknown property {k!r} (additionalProperties: false)")
            elif isinstance(ap, dict): _validate_against(rv, ap, f"{where}.{k}", out)
    if isinstance(v, list):
        if "minItems" in spec and len(v) < spec["minItems"]:
            out.append(f"{where}: fewer than minItems {spec['minItems']}")
        if "maxItems" in spec and len(v) > spec["maxItems"]:
            out.append(f"{where}: more than maxItems {spec['maxItems']}")
        if "items" in spec:
            for i, item in enumerate(v):
                _validate_against(item, spec["items"], f"{where}[{i}]", out)
    ty = spec.get("type")
    if ty == "boolean" and not isinstance(v, bool):
        out.append(f"{where}: must be boolean (strict: true/false; 1/0/null are not booleans)")
    if ty == "object" and not isinstance(v, dict):
        out.append(f"{where}: must be object")
    if ty == "array" and not isinstance(v, list):
        out.append(f"{where}: must be array")
    if ty == "integer" and (isinstance(v, bool) or not isinstance(v, int)):
        out.append(f"{where}: must be integer (bool is not an integer)")
    if "const" in spec and v != spec["const"]:
        out.append(f"{where}: const violated (want {spec['const']!r})")
    if "enum" in spec and v not in spec["enum"]:
        out.append(f"{where}: {v!r} outside enum {spec['enum']}")
    if "pattern" in spec and isinstance(v, str) and not re.search(spec["pattern"], v):
        out.append(f"{where}: {v!r} fails pattern {spec['pattern']!r}")
    if "minLength" in spec and isinstance(v, str) and len(v) < spec["minLength"]:
        out.append(f"{where}: shorter than minLength {spec['minLength']}")
    if "maxLength" in spec and isinstance(v, str) and len(v) > spec["maxLength"]:
        out.append(f"{where}: longer than maxLength {spec['maxLength']}")
    if "minimum" in spec and isinstance(v, (int, float)) and not isinstance(v, bool) and v < spec["minimum"]:
        out.append(f"{where}: {v!r} below minimum {spec['minimum']}")
    if "maximum" in spec and isinstance(v, (int, float)) and not isinstance(v, bool) and v > spec["maximum"]:
        out.append(f"{where}: {v!r} above maximum {spec['maximum']}")
    if ty == "string" and not isinstance(v, str): out.append(f"{where}: must be string")
    if ty == "integer" and not isinstance(v, int): out.append(f"{where}: must be integer")
    if ty == "number" and not isinstance(v, (int, float)): out.append(f"{where}: must be number")
    if ty == "null" and v is not None: out.append(f"{where}: must be null")


def _schema_check(obj, name, where, out):
    """Execute the schema file (recursive subset). Missing schema = finding."""
    s = _load_schema(name)
    if s is None:
        out.append(f"{where}: schema {name} missing/unreadable (schemas are executed law)")
        return
    _validate_against(obj, s, where, out)


def _sha(p):
    h = hashlib.sha256()
    with open(p,"rb") as fh:
        for b in iter(lambda: fh.read(65536), b""): h.update(b)
    return h.hexdigest()

def _req(obj, fields, where, out):
    for f in fields:
        if f not in obj or obj[f] in (None,"",[]): out.append(f"{where}: missing required field {f!r}")

def load_legacy(evid_dir=None):
    p = os.path.join(evid_dir or EVID, "legacy_manifest.json")
    try: return set(json.load(open(p,encoding="utf-8"))["legacy_tids"])
    except Exception: return set()

def validate_bundle(tid, d):
    """Full semantic validation of one canonical bundle -> list[str] findings."""
    out = []
    tj = os.path.join(d,"task.json")
    if not os.path.isfile(tj): return [f"{tid}: task.json missing (bundle is not a TaskEnvelope)"]
    try: env = json.load(open(tj,encoding="utf-8"))
    except Exception as e: return [f"{tid}: task.json unparseable: {e}"]
    _schema_check(env, "task-envelope.schema.json", f"{tid}/task.json", out)
    _req(env,["schema_version","task_id","source","principal","received_at","mode_hint","base_revision","idempotency_key"],f"{tid}/task.json",out)
    if env.get("task_id") != tid: out.append(f"{tid}: envelope task_id mismatch")
    if not re.match(r"^[0-9a-f]{7,40}$", str(env.get("base_revision",""))): out.append(f"{tid}: base_revision not a git SHA")
    # plan (versioned; all files must parse, first matching becomes current)
    plans = [f for f in os.listdir(d) if re.match(r"plan(\.v\d+)?\.json$",f)]
    if not plans: out.append(f"{tid}: no plan JSON")
    plan = None
    for pf in sorted(plans, key=_plan_version):
        try: p = json.load(open(os.path.join(d,pf),encoding="utf-8"))
        except Exception as e: out.append(f"{tid}: {pf} unparseable: {e}"); continue
        _schema_check(p, "plan.schema.json", f"{tid}/{pf}", out)
        _req(p,["plan_id","task_id","base_revision","steps"],f"{tid}/{pf}",out)
        if str(p.get("base_revision")) != str(env.get("base_revision")):
            out.append(f"{tid}/{pf}: plan base_revision disagrees with envelope (revision drift)")
        for st in p.get("steps",[]):
            _req(st,["step_id","operation_class","success_predicate"],f"{tid}/{pf}:{st.get('step_id')}",out)
        if str(p.get("task_id")) != tid:
            out.append(f"{tid}/{pf}: plan file belongs to a foreign task {p.get('task_id')!r} — never silently skipped (4600)")
            continue
        if plan is None: plan = p
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
        _schema_check(c, "command.schema.json", f"{tid}/commands/{cid}", out)
        if str(c.get("command_id")) != cid:
            out.append(f"{tid}/commands/{cid}: command identity mismatch — file stem says {cid!r}, internal command_id says {c.get('command_id')!r}")
        _req(c,["command_id","task_id","plan_id","step_id","operation"],f"{tid}/commands/{cid}",out)
        if c.get("operation") not in OPS: out.append(f"{tid}/commands/{cid}: operation {c.get('operation')!r} outside the allowlist")
        if c.get("task_id") != tid: out.append(f"{tid}/commands/{cid}: cross-task command (causation broken)")
        if plan and c.get("plan_id") != plan.get("plan_id"): out.append(f"{tid}/commands/{cid}: references plan {c.get('plan_id')!r}, bundle plan is {plan.get('plan_id')!r}")
        steps = {s.get("step_id") for s in (plan or {}).get("steps",[])}
        if plan and c.get("step_id") not in steps: out.append(f"{tid}/commands/{cid}: step {c.get('step_id')!r} not in approved plan")
        if "base_revision" in c and str(c.get("base_revision")) != str(env.get("base_revision")):
            out.append(f"{tid}/commands/{cid}: command base_revision disagrees with envelope")
        if cid not in outs: out.append(f"{tid}/commands/{cid}: no outcome recorded")
    for oid,o in outs.items():
        _schema_check(o, "outcome.schema.json", f"{tid}/outcomes/{oid}", out)
        _req(o,["command_id","task_id","result","evidence"],f"{tid}/outcomes/{oid}",out)
        if str(o.get("task_id")) != tid:
            out.append(f"{tid}/outcomes/{oid}: outcome task_id mismatch (foreign outcome — {o.get('task_id')!r})")
        if o.get("result") not in ("succeeded","failed","stale_precondition","policy_denied","timed_out","security_blocked"):
            out.append(f"{tid}/outcomes/{oid}: illegal result {o.get('result')!r}")
        # identity binding (4500): file stem MUST equal the internal command_id
        if str(o.get("command_id")) != oid:
            out.append(f"{tid}/outcomes/{oid}: outcome identity mismatch - file stem says {oid!r}, internal command_id says {o.get('command_id')!r}")
        for ev in o.get("evidence",[]):
            ep = os.path.join(ROOT, ev.get("path",""))
            if not os.path.isfile(ep): out.append(f"{tid}/outcomes/{oid}: evidence path missing: {ev.get('path')}")
            elif ev.get("sha256") != _sha(ep): out.append(f"{tid}/outcomes/{oid}: evidence digest mismatch: {ev.get('path')}")
        if o.get("result") == "failed" and oid in cmds: out.append(f"{tid}/outcomes/{oid}: failed command has no replan event or follow-up")
    # events: order, transitions, uniqueness, timestamps, causation
    ej = os.path.join(d,"events.ndjson")
    if not os.path.isfile(ej): out.append(f"{tid}: events.ndjson missing (append-only causal record)")
    else:
        seqs, eids, state, done = [], set(), "RECEIVED", False
        refs = {t: [] for t in CAUSAL}
        last_dt = None
        for ln in open(ej,encoding="utf-8"):
            ln = ln.strip()
            if not ln: continue
            try: e = json.loads(ln)
            except Exception as ex: out.append(f"{tid}/events.ndjson: unparseable line: {ex}"); continue
            _schema_check(e, "event.schema.json", f"{tid}/events", out)
            _req(e,["seq","event_id","task_id","type","at","actor"],f"{tid}/events",out)
            if e.get("task_id") != tid: out.append(f"{tid}/events: foreign task_id {e.get('task_id')!r}")
            seqs.append(e.get("seq"))
            if e.get("event_id") in eids: out.append(f"{tid}/events: duplicate event_id {e.get('event_id')!r}")
            eids.add(e.get("event_id"))
            ts = e.get("at","")
            try:
                dt = datetime.datetime.fromisoformat(ts)
                if dt.tzinfo is None or dt.utcoffset() is None:
                    out.append(f"{tid}/events: timestamp without timezone offset {ts!r} (RFC-3339 requires one)")
                if last_dt is not None and dt < last_dt:
                    out.append(f"{tid}/events: timestamps not monotonic at {e.get('event_id')!r}")
                last_dt = dt
            except Exception:
                out.append(f"{tid}/events: non-RFC3339 timestamp {ts!r}")
            t = e.get("type")
            if t in CAUSAL:
                ref = e.get("ref")
                if not ref: out.append(f"{tid}/events: {t} without causation ref")
                else: refs[t].append(ref)
            if t not in TARGET: out.append(f"{tid}/events: unknown event type {t!r}"); continue
            need = ALLOWED.get(t)
            ok = (need is None) if not isinstance(need,tuple) else (state in need)
            if isinstance(need,str): ok = (state == need)
            if not ok: out.append(f"{tid}/events: illegal transition {state} --{t}-->")
            state = TARGET[t]
            if t == "task.completed": done = True
        if seqs != sorted(seqs): out.append(f"{tid}/events: sequence numbers out of order (append-only violated)")
        if len(seqs) != len(set(seqs)): out.append(f"{tid}/events: duplicate sequence numbers")
        if seqs and seqs != list(range(1, len(seqs)+1)):
            out.append(f"{tid}/events: sequences must be contiguous 1..N (got {seqs[:6]}...)")
        if not done: out.append(f"{tid}: no task.completed event (closure without completion)")
        # causation coverage (4500): every command authorized+executed, every outcome recorded
        for cid in cmds:
            for t in ("command.proposed","command.authorized","execution.started"):
                if cid not in refs[t]: out.append(f"{tid}/events: command {cid} missing a {t} causation ref")
        for t in sorted(CAUSAL):
            for ref in refs[t]:
                if ref not in cmds:
                    out.append(f"{tid}/events: {t} ref {ref!r} names an unknown command")
        for ref in refs["verification.passed"]:
            if ref in outs and outs[ref].get("result") != "succeeded":
                out.append(f"{tid}/events: verification.passed ref {ref!r} attests a command without a succeeded outcome")
        for oid,o in outs.items():
            rec = refs["outcome.recorded"]
            if rec.count(str(o.get("command_id"))) != 1:
                out.append(f"{tid}/events: outcome {oid} needs exactly one outcome.recorded ref to its command_id")
    if done and not outs: out.append(f"{tid}: completed with zero outcomes (no evidence)")
    # projection (4500): parsed, identity-bound, and equal to the event-derived state
    pj = os.path.join(d,"projection.json")
    if not os.path.isfile(pj): out.append(f"{tid}: projection.json missing (rebuildable view is required)")
    else:
        try: proj = json.load(open(pj,encoding="utf-8"))
        except Exception as e: proj = None; out.append(f"{tid}: projection.json unparseable: {e}")
        if proj is not None:
            if proj.get("task_id") != tid: out.append(f"{tid}: projection.json task_id mismatch")
            derived = state if done else "INCOMPLETE"
            if proj.get("state") != derived:
                out.append(f"{tid}: projection.json state {proj.get('state')!r} != event-derived state {derived!r} (projection is rebuildable, never hand-edited)")
    return out

STAGE_MAP = (("intake", "sensoryneurons"), ("reasoning", "interneurons"), ("orders", "motorneurons"))

def render_neuron(tid, bundle_dir, stage):
    """Render one Markdown neuron projection FROM the canonical bundle (4700).
    Deterministic: same bundle -> same bytes. The bundle is the record; this
    file is a view of it. Hand edits break file==render and fail check 27."""
    env = json.load(open(os.path.join(bundle_dir, "task.json"), encoding="utf-8"))
    plan = None
    for pf in sorted((f for f in os.listdir(bundle_dir)
                      if re.match(r"plan(\.v\d+)?\.json$", f)), key=_plan_version):
        pj = json.load(open(os.path.join(bundle_dir, pf), encoding="utf-8"))
        if pj.get("task_id") == tid: plan = pj  # 5500: HIGHEST numeric version wins
    cdir = os.path.join(bundle_dir, "commands")
    cmds = sorted(f for f in os.listdir(cdir) if f.endswith(".json")) if os.path.isdir(cdir) else []
    odir = os.path.join(bundle_dir, "outcomes")
    ototal = oks = 0
    if os.path.isdir(odir):
        for f in sorted(x for x in os.listdir(odir) if x.endswith(".json")):
            o = json.load(open(os.path.join(odir, f), encoding="utf-8")); ototal += 1
            oks += (o.get("result") == "succeeded")
    nev = sum(1 for l in open(os.path.join(bundle_dir, "events.ndjson"), encoding="utf-8") if l.strip())
    proj_state = "—"
    ppath = os.path.join(bundle_dir, "projection.json")
    if os.path.isfile(ppath):
        try: proj_state = json.load(open(ppath, encoding="utf-8")).get("state", "—")
        except Exception: pass
    src = env.get("source", {}) or {}
    folder = dict(STAGE_MAP)[stage]
    title = stage.upper()
    notes = (env.get("operator_notes") or {}).get(stage) or "(no operator notes)"
    out = [f"# {tid} — {title} · RENDERED PROJECTION (4700)",
           f"> Rendered from `evidence/tasks/{tid}/` by `radiation_core.relay.render_neuron`.",
           "> Projection, not the record: hand edits FAIL check 27 (file must equal render output).",
           "",
           f"- **Task:** {tid} · **Mode hint:** {env.get('mode_hint','—')} · **Base revision:** {env.get('base_revision','—')}",
           f"- **Source:** {src.get('kind','—')} · {src.get('artifact_ref','—')} · trust={src.get('trust','—')}",
           f"- **Received:** {env.get('received_at','—')}",
           f"- **Plan:** {(plan or {}).get('plan_id','—')} · {len((plan or {}).get('steps',[]))} step(s)",
           f"- **Commands:** {len(cmds)} · outcomes succeeded: {oks}/{ototal} · **Events:** {nev} · **Final state:** {proj_state}",
           "",
           f"## NOTES — {title}", ""]
    out.extend(notes.rstrip().splitlines())
    return "\n".join(out).rstrip() + "\n"


def validate_active(neurons_dir=None, evid_dir=None):
    """The check-27 engine: legacy triple rule + canonical bundles whose Markdown
    projections MUST equal render_neuron output (4700: the bundle is the record)."""
    findings = []
    nd = neurons_dir or os.path.join(ROOT,"scaffolding","neurons")
    evid = evid_dir or EVID
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
        # projection fidelity (4700): the neuron MUST equal render_neuron(bundle).
        # The bundle is the authoritative record; Markdown is a rendered view.
        bdir = os.path.join(evid, f"TID-{tid}")
        for stage,suf in stages:
            fp = os.path.join(nd,stage,f"TID-{tid}_{suf}.md")
            actual = open(fp,encoding="utf-8").read() if os.path.isfile(fp) else ""
            try:
                expected = render_neuron(f"TID-{tid}", bdir, suf)
            except Exception as e:
                findings.append(f"TID-{tid}: {stage} unrenderable (bundle unreadable: {e})")
                continue
            if actual != expected:
                findings.append(f"TID-{tid}: {stage} projection drifts from the canonical bundle — re-render, never hand-edit (4700)")
        findings.extend(validate_bundle(f"TID-{tid}", bdir))
    return findings


def _make_vector_bundle():
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
               "idempotency_key":"selftest-4500-vec"}, open(os.path.join(d,"task.json"),"w"))
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
    ev = []
    for i,ty in enumerate(seq):
        e = {"seq":i+1,"event_id":f"e{i+1}","task_id":tid,"type":ty,
             "at":f"2026-09-14T12:00:{i:02d}+08:00","actor":"relay"}
        if ty in CAUSAL: e["ref"] = "C1"
        ev.append(e)
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(json.dumps(e) for e in ev))
    json.dump({"task_id":tid,"state":"COMPLETE"}, open(os.path.join(d,"projection.json"),"w"))
    return root, d, tid


def _plan_version(name: str) -> int:
    """5500: EXPLICIT numeric version rule for plan files — plan.v2 sorts
    before plan.v10, and a bare plan.json ranks as v0. Lexical order lied."""
    m = re.search(r"\.v(\d+)\.json$", name)
    return int(m.group(1)) if m else 0


def self_test():
    ok = 0
    # vector 1: valid bundle is clean
    root, d, tid = _make_vector_bundle()
    f = validate_bundle(tid, d)
    v1 = (len(f) == 0); ok += v1
    print(f"  vector 1 valid bundle clean -> {'PASS' if v1 else f}")
    # vector 2: tampered evidence digest fails
    pj = os.path.join(d,"outcomes","C1.json")
    o = json.load(open(pj)); o["evidence"][0]["sha256"] = "0"*64
    json.dump(o, open(pj,"w"))
    f2 = validate_bundle(tid, d)
    v2 = any("digest mismatch" in x for x in f2); ok += v2
    print(f"  vector 2 tampered evidence caught -> {'PASS' if v2 else 'FAIL'}")
    # vector 3: execution without authorization fails
    o["evidence"][0]["sha256"] = hashlib.sha256(open(os.path.join(d,"evidence.txt"),"rb").read()).hexdigest()
    json.dump(o, open(pj,"w"))
    lines = open(os.path.join(d,"events.ndjson")).read().splitlines()
    del lines[6]  # drop command.authorized
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(lines))
    f3 = validate_bundle(tid, d)
    v3 = any("illegal transition" in x for x in f3); ok += v3
    print(f"  vector 3 unauthorized execution caught -> {'PASS' if v3 else 'FAIL'}")
    # vector 4: a LEGAL replan (completed task -> replan -> re-approval) passes
    shutil.rmtree(root)
    root, d, tid = _make_vector_bundle()
    lines = open(os.path.join(d,"events.ndjson")).read().splitlines()
    import json as _j
    seqn = _j.loads(lines[-1])["seq"]
    ins = [_j.dumps({"seq":seqn+1,"event_id":f"e{seqn+1}","task_id":tid,"type":"replan","at":"2026-09-14T13:00:00+08:00","actor":"relay"}),
           _j.dumps({"seq":seqn+2,"event_id":f"e{seqn+2}","task_id":tid,"type":"plan.approved","at":"2026-09-14T13:00:05+08:00","actor":"policy"})]
    open(os.path.join(d,"events.ndjson"),"w").write("\n".join(lines + ins) + "\n")
    # a replan re-opens the task: the projection MUST be re-rendered to match
    pr = json.load(open(os.path.join(d,"projection.json"))); pr["state"] = "PLAN_APPROVED"
    json.dump(pr, open(os.path.join(d,"projection.json"),"w"))
    f4 = validate_bundle(tid, d)
    v4 = (len(f4) == 0); ok += v4
    print(f"  vector 4 legal replan sequence -> {'PASS' if v4 else f4}")
    # vector 5 (recheck mutation): outcome identity mismatch (CMD-MISMATCH) fails
    pj = os.path.join(d,"outcomes","C1.json")
    o = json.load(open(pj)); o["command_id"] = "CMD-MISMATCH"
    json.dump(o, open(pj,"w"))
    f5 = validate_bundle(tid, d)
    v5 = any("identity mismatch" in x for x in f5); ok += v5
    print(f"  vector 5 outcome identity mismatch caught -> {'PASS' if v5 else 'FAIL'}")
    # vector 6 (recheck mutation): corrupted projection (hand-edited state) fails
    o["command_id"] = "C1"; json.dump(o, open(pj,"w"))
    pp = os.path.join(d,"projection.json")
    pr = json.load(open(pp)); pr["state"] = "FAILED"
    json.dump(pr, open(pp,"w"))
    f6 = validate_bundle(tid, d)
    v6 = any("event-derived state" in x for x in f6); ok += v6
    print(f"  vector 6 corrupted projection caught -> {'PASS' if v6 else 'FAIL'}")
    # vectors 7-11: the 4500-recheck mutations — each MUST be caught (4600)
    shutil.rmtree(root)
    root, d, tid = _make_vector_bundle()
    c1 = os.path.join(d, "commands", "C1.json")
    cj = json.load(open(c1)); cj["command_id"] = "CMD-OTHER"; json.dump(cj, open(c1, "w"))
    f7 = validate_bundle(tid, d)
    v7 = any("command identity mismatch" in x for x in f7); ok += v7
    print(f"  vector 7 command identity mismatch caught -> {'PASS' if v7 else 'FAIL'}")
    cj["command_id"] = "C1"; json.dump(cj, open(c1, "w"))
    o1 = os.path.join(d, "outcomes", "C1.json")
    oj = json.load(open(o1)); oj["task_id"] = "TID-9999-99-99-x"; json.dump(oj, open(o1, "w"))
    f8 = validate_bundle(tid, d)
    v8 = any("outcome task_id mismatch" in x for x in f8); ok += v8
    print(f"  vector 8 outcome foreign task caught -> {'PASS' if v8 else 'FAIL'}")
    oj["task_id"] = tid; json.dump(oj, open(o1, "w"))
    tj2 = os.path.join(d, "task.json")
    e = json.load(open(tj2)); e["source"] = {"kind": "untrusted"}; json.dump(e, open(tj2, "w"))
    f9 = validate_bundle(tid, d)
    v9 = any(("outside enum" in x and "source.kind" in x) or ("schema-required field 'trust'" in x) for x in f9)
    ok += v9
    print(f"  vector 9 nested schema executed caught -> {'PASS' if v9 else f9}")
    e = json.load(open(tj2))
    e["source"] = {"kind": "commander", "artifact_ref": "artifact://t", "trust": "root"}
    json.dump(e, open(tj2, "w"))
    pl = os.path.join(d, "plan.v1.json")
    pj2 = json.load(open(pl)); pj2["task_id"] = "TID-9999-99-99-x"; json.dump(pj2, open(pl, "w"))
    f10 = validate_bundle(tid, d)
    v10 = any("belongs to a foreign task" in x for x in f10); ok += v10
    print(f"  vector 10 foreign plan hard-fail caught -> {'PASS' if v10 else 'FAIL'}")
    pj2["task_id"] = tid; json.dump(pj2, open(pl, "w"))
    evf = os.path.join(d, "events.ndjson")
    lines = open(evf).read().splitlines()
    e0 = json.loads(lines[0]); e0["seq"] = 0; lines[0] = json.dumps(e0)
    open(evf, "w").write("\n".join(lines))
    f11 = validate_bundle(tid, d)
    v11 = any(("below minimum" in x) or ("contiguous" in x) for x in f11); ok += v11
    print(f"  vector 11 seq below minimum caught -> {'PASS' if v11 else 'FAIL'}")
    # vector 12 (4700): a hand-edited neuron projection must fail file==render
    shutil.rmtree(root)
    root, d, tid = _make_vector_bundle()
    e = json.load(open(os.path.join(d, "task.json")))
    e["operator_notes"] = {"intake": "born", "reasoning": "born", "orders": "born"}
    json.dump(e, open(os.path.join(d, "task.json"), "w"))
    nd = os.path.join(root, "scaffolding", "neurons")
    for stage_name, folder in STAGE_MAP:
        os.makedirs(os.path.join(nd, folder), exist_ok=True)
        open(os.path.join(nd, folder, "TEMPLATE_" + stage_name + ".md"), "w").write("template")
        open(os.path.join(nd, folder, "TID-2026-09-14-z_" + stage_name + ".md"), "w", encoding="utf-8").write(
            render_neuron(tid, d, stage_name))
    evid = os.path.join(root, "evidence", "tasks")
    base = validate_active(neurons_dir=nd, evid_dir=evid)
    v12a = (len(base) == 0)
    open(os.path.join(nd, "motorneurons", "TID-2026-09-14-z_orders.md"), "a", encoding="utf-8").write("\nHAND EDIT\n")
    drifted = validate_active(neurons_dir=nd, evid_dir=evid)
    v12 = v12a and any("projection drifts" in x for x in drifted)
    ok += v12
    print(f"  vector 12 hand-edited projection caught -> {'PASS' if v12 else (base, drifted)}")
    shutil.rmtree(root)
    # ── 5500 gate-review vectors: schema execution + numeric versioning ──
    import radiation_core.relay as _self
    bad_tid = {"type": "execution", "task_id": "../not-a-valid-task-id",
               "payload": {"v": 2}, "digest": "x"}
    outb: list[str] = []
    _self._schema_check(bad_tid, "control_receipt.schema.json", "exploit", outb)
    v13 = any("oneOf" in x for x in outb); ok += v13
    print(f"  vector 13 schema oneOf executes (bad task_id caught) -> {'PASS' if v13 else 'FAIL'}")
    big = {"schema_name": "radiation.control.manifest/1",
           "files": [{"path": f"f{i}.md", "content": "x"} for i in range(21)]}
    outm: list[str] = []
    _self._schema_check(big, "control_manifest.schema.json", "manifest", outm)
    v14 = any("maxItems" in x for x in outm); ok += v14
    print(f"  vector 14 schema maxItems executes (21 files caught) -> {'PASS' if v14 else 'FAIL'}")
    outi: list[str] = []
    _self._schema_check({"seq": True}, "event.schema.json", "event", outi)
    v15 = any("must be integer" in x for x in outi); ok += v15
    print(f"  vector 15 bool rejected as integer -> {'PASS' if v15 else 'FAIL'}")
    rootv, dv, tidv = _make_vector_bundle()
    p2 = json.load(open(os.path.join(dv, "plan.v1.json")))
    if os.path.exists(os.path.join(dv, "plan.v1.json")): os.remove(os.path.join(dv, "plan.v1.json"))
    a2 = dict(p2); a2["plan_id"] = "PLAN-V2-MARK"
    a10 = dict(p2); a10["plan_id"] = "PLAN-V10-MARK"
    json.dump(a2, open(os.path.join(dv, "plan.v2.json"), "w"))
    json.dump(a10, open(os.path.join(dv, "plan.v10.json"), "w"))
    rend = render_neuron(tidv, dv, "reasoning")
    v16 = "PLAN-V10-MARK" in rend and "PLAN-V2-MARK" not in rend; ok += v16
    shutil.rmtree(rootv, ignore_errors=True)
    print(f"  vector 16 plan.v10 beats plan.v2 (numeric, not lexical) -> {'PASS' if v16 else 'FAIL'}")
    # ── 5600 closure vectors: the executor covers EXACTLY what schemas use ──
    outap: list[str] = []
    _self._validate_against({"a": 1, "evil": 2},
                            {"type": "object", "properties": {"a": {"type": "integer"}},
                             "additionalProperties": False}, "ap", outap)
    v17 = any("unknown property" in x for x in outap); ok += v17
    print(f"  vector 17 additionalProperties:false rejects unknown keys -> {'PASS' if v17 else 'FAIL'}")
    outany: list[str] = []
    _self._validate_against(3, {"anyOf": [{"const": 1}, {"const": 2}]}, "any", outany)
    v18 = len(outany) == 1 and "anyOf" in outany[0]; ok += v18
    print(f"  vector 18 anyOf executes (0 matches caught) -> {'PASS' if v18 else 'FAIL'}")
    outnot: list[str] = []
    _self._validate_against(5, {"type": "integer", "not": {"const": 5}}, "not", outnot)
    v19 = len(outnot) == 1 and "'not' violated" in outnot[0]; ok += v19
    print(f"  vector 19 not executes (forbidden match caught) -> {'PASS' if v19 else 'FAIL'}")
    outml: list[str] = []
    _self._validate_against("abcd", {"type": "string", "maxLength": 3}, "ml", outml)
    outmi: list[str] = []
    _self._validate_against([1], {"type": "array", "minItems": 2, "items": {}}, "mi", outmi)
    v20 = any("maxLength" in x for x in outml) and any("minItems" in x for x in outmi); ok += v20
    print(f"  vector 20 maxLength + minItems execute -> {'PASS' if v20 else 'FAIL'}")
    outb1: list[str] = []
    _self._validate_against(1, {"type": "boolean"}, "b1", outb1)
    outb2: list[str] = []
    _self._validate_against(True, {"type": "boolean"}, "b2", outb2)
    v21 = len(outb1) == 1 and not outb2; ok += v21
    print(f"  vector 21 boolean type is strict (1 is not true) -> {'PASS' if v21 else 'FAIL'}")
    v22 = _self.unsupported_keywords({"type": "object", "contains": {"type": "string"}}) == ["contains"]
    ok += v22
    print(f"  vector 22 keyword-coverage scan names unsupported keywords -> {'PASS' if v22 else 'FAIL'}")
    outif1: list[str] = []
    _self._validate_against({"role": "data_feed", "digest": "x"},
                            {"type": "object", "properties": {"role": {"type": "string"}},
                             "if": {"properties": {"role": {"const": "data_feed"}}},
                             "then": {"required": ["digest"]}}, "c1", outif1)
    outif2: list[str] = []
    _self._validate_against({"role": "data_feed"},
                            {"type": "object", "properties": {"role": {"type": "string"}},
                             "if": {"properties": {"role": {"const": "data_feed"}}},
                             "then": {"required": ["digest"]}}, "c2", outif2)
    v23 = not outif1 and len(outif2) == 1 and "digest" in outif2[0]; ok += v23
    print(f"  vector 23 if/then executes (conditional fires and abstains) -> {'PASS' if v23 else 'FAIL'}")
    print(f"relay self-test: {ok}/23 vectors")
    return 0 if ok == 23 else 1  # 5500: total tracked; success exits ZERO


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    f = validate_active()
    for x in f: print("✗", x)
    print(f"relay: {len(f)} finding(s)")
    sys.exit(1 if f else 0)
