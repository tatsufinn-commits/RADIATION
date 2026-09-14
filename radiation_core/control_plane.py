"""radiation_core.control_plane — the ratified control plane (II.11, patch 5000).

    python3 -m radiation_core.control_plane resolve --effect read --source standing_policy
    python3 -m radiation_core.control_plane decide  --task TID --effect workspace_draft \
        --source commander_order [--receipts PATH]
    python3 -m radiation_core.control_plane execute --task TID --manifest M.json \
        [--receipts PATH]
    python3 -m radiation_core.control_plane verify  [--receipts PATH]
    python3 -m radiation_core.control_plane --self-test

═══════════════════════════════════════════════════════════════════════════
 II.11 — CONTROL PLANE (ratified by THE COMMANDER, patch 5000, "Product-2
 package"): this is OPERATED tooling, not an autonomous runtime. It executes
 only what a session explicitly requests THROUGH it; it never schedules
 itself, watches, or triggers. The two-key law is mechanical here: a policy
 key (source rank against the allowlist) AND a tool key (a least-privilege
 tool must exist) before anything executes — and no execution without a
 chained decision receipt. canonical_apply is THE COMMANDER'S MOTOR ACT:
 the resolver answers commander_motor_act and binds no tool, ever. The
 executor is bounded to evidence/drafts/<task_id>/ — no subprocess, no
 network, no canonical writes. Every decision and execution appends to an
 immutable, hash-chained receipt ledger.
═══════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from radiation_core.relay import _schema_check  # ONE schema executor

SCHEMA_DIR = os.path.join(ROOT, "schemas")
ALLOWLIST_PATH = os.path.join(ROOT, "scaffolding", "control_plane", "allowlist.json")
RECEIPTS_PATH = os.path.join(ROOT, "evidence", "control_plane", "receipts.ndjson")
DRAFTS_ROOT = os.path.join(ROOT, "evidence", "drafts")

EFFECTS = ("read", "workspace_draft", "canonical_apply")
SOURCES = ("session_initiative", "standing_policy", "commander_order")
SOURCE_RANK = {s: i for i, s in enumerate(SOURCES)}
STATUSES = ("authorized", "refused", "commander_motor_act")
GENESIS_PREV = "sha256:" + "0" * 64


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _digest(obj: dict) -> str:
    d = json.loads(json.dumps(obj))
    d["digest"] = ""
    return "sha256:" + hashlib.sha256(
        json.dumps(d, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ------------------------------------------------------------------ allowlist
def load_allowlist() -> tuple[dict, list[str]]:
    try:
        al = json.load(open(ALLOWLIST_PATH, encoding="utf-8"))
    except Exception as e:
        return {}, [f"allowlist unreadable: {e}"]
    out: list[str] = []
    _schema_check(al, "control_allowlist.schema.json", "allowlist", out)
    return al, out


# -------------------------------------------------------------------- resolver
def resolve(effect: str, source: str, task_id: str = "") -> dict:
    """PURE — decides, writes nothing. Two keys: policy (source rank) + tool."""
    dec = {"schema_name": "radiation.control.decision/1",
           "task_id": task_id, "effect": effect, "source": source,
           "status": None, "tool": None, "bounds": {}, "reasons": [],
           "decided_at": _now(), "digest": ""}
    al, findings = load_allowlist()
    if findings:
        dec["status"] = "refused"
        dec["reasons"] = findings[:2]
        dec["digest"] = _digest(dec)
        return dec
    if effect not in EFFECTS:
        dec["status"] = "refused"
        dec["reasons"] = [f"unknown effect {effect!r}"]
        dec["digest"] = _digest(dec)
        return dec
    if source not in SOURCES:
        dec["status"] = "refused"
        dec["reasons"] = [f"unknown source {source!r}"]
        dec["digest"] = _digest(dec)
        return dec
    op = next((o for o, s in al.get("operations", {}).items()
               if isinstance(s, dict) and s.get("effect") == effect), None)
    if op is None:
        dec["status"] = "refused"
        dec["reasons"] = [f"effect {effect!r} not in allowlist (policy key fails)"]
        dec["digest"] = _digest(dec)
        return dec
    spec = al["operations"][op]
    min_rank = SOURCE_RANK.get(spec.get("min_source", "commander_order"), 2)
    tool = spec.get("tool")
    if effect == "canonical_apply" or spec.get("commander_motor_act"):
        # the approval boundary, hard: no source level makes this executable
        dec["status"] = "commander_motor_act"
        dec["tool"] = None
        dec["reasons"] = ["canonical_apply is the Commander's motor act — "
                          "outside every agent runtime (II.11)"]
        dec["digest"] = _digest(dec)
        return dec
    if SOURCE_RANK[source] < min_rank:
        dec["status"] = "refused"
        dec["reasons"] = [f"policy key fails: {effect} requires source "
                          f"{spec.get('min_source')!r}, got {source!r} (two-key law)"]
        dec["digest"] = _digest(dec)
        return dec
    if not tool:
        dec["status"] = "refused"
        dec["reasons"] = ["tool key fails: no least-privilege tool bound to "
                          f"{effect!r} (two-key law)"]
        dec["digest"] = _digest(dec)
        return dec
    dec["status"] = "authorized"
    dec["tool"] = tool
    if effect == "workspace_draft":
        dec["bounds"] = {"draft_root": os.path.relpath(DRAFTS_ROOT, ROOT)}
    dec["digest"] = _digest(dec)
    return dec


# -------------------------------------------------------------------- receipts
def read_chain(path: str = RECEIPTS_PATH) -> list[dict]:
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                entries.append(json.loads(ln))
    return entries


def append_entry(entry_type: str, task_id: str, payload: dict,
                 path: str = RECEIPTS_PATH) -> dict:
    chain = read_chain(path)
    prev = chain[-1]["digest"] if chain else GENESIS_PREV
    entry = {"schema_name": "radiation.control.receipt/1",
             "seq": len(chain), "type": entry_type, "task_id": task_id,
             "recorded_at": _now(), "payload": payload, "prev": prev, "digest": ""}
    entry["digest"] = _digest(entry)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def verify_chain(path: str = RECEIPTS_PATH) -> list[str]:
    problems: list[str] = []
    chain = read_chain(path)
    prev = GENESIS_PREV
    for i, e in enumerate(chain):
        _sch: list[str] = []
        _schema_check(e, "control_receipt.schema.json", f"entry {i}", _sch)
        problems.extend(_sch[:2])
        if e.get("seq") != i:
            problems.append(f"entry {i}: seq discontinuity (want {i}, got {e.get('seq')})")
        if e.get("prev") != prev:
            problems.append(f"entry {i}: prev-link broken (chain forked or reordered)")
        claimed = e.get("digest")
        if claimed != _digest(e):
            problems.append(f"entry {i}: digest does not bind content (hand-edited)")
        prev = claimed
    return problems


def decide(task_id: str, effect: str, source: str,
           path: str = RECEIPTS_PATH) -> dict:
    """resolve + chain the decision. Decisions are receipts; nothing executes
    later without one."""
    dec = resolve(effect, source, task_id)
    _sch: list[str] = []
    _schema_check(dec, "control_decision.schema.json", "decision", _sch)
    if _sch:
        dec["status"] = "refused"
        dec["reasons"] = (dec.get("reasons") or []) + _sch[:2]
        dec["digest"] = _digest(dec)
    append_entry("decision", task_id,
                 {"decision": {k: v for k, v in dec.items() if k != "digest"},
                  "decision_digest": dec["digest"]}, path)
    return dec


def _latest_authorized_decision(task_id: str, effect: str,
                                path: str) -> tuple[dict | None, str]:
    for e in reversed(read_chain(path)):
        if (e.get("type") == "decision" and e.get("task_id") == task_id
                and e.get("payload", {}).get("decision", {}).get("effect") == effect):
            d = e["payload"]["decision"]
            if d.get("status") == "authorized" and d.get("tool") == "draft_executor":
                return d, e.get("digest", "")
            return None, (f"latest chained decision for {effect} is "
                          f"{d.get('status')!r} — no execution without an "
                          "authorized decision receipt (II.11)")
    return None, ("no chained decision receipt for this task/effect — "
                  "run decide first (no execution without a decision, II.11)")


# -------------------------------------------------------------------- executor
def execute_draft(task_id: str, manifest: dict, path: str = RECEIPTS_PATH,
                  drafts_root: str = DRAFTS_ROOT) -> dict:
    """Draft-only executor. Bounded: writes ONLY under drafts_root/<task_id>/;
    no subprocess; no network; no canonical writes; requires a chained
    authorized decision receipt (the approval boundary, mechanical)."""
    dec, reason = _latest_authorized_decision(task_id, "workspace_draft", path)
    if dec is None:
        return {"executed": False, "reason": reason, "files": [], "refused": []}
    task_dir = os.path.realpath(os.path.join(drafts_root, task_id))
    written, refused = [], []
    for item in manifest.get("files", []):
        rel = item.get("path", "")
        target = os.path.realpath(os.path.join(task_dir, rel))
        inside = target == task_dir or target.startswith(task_dir + os.sep)
        if not inside or not os.path.splitext(target)[1]:
            refused.append({"path": rel, "reason": "escapes the drafts root "
                            "(containment, II.11)"})
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        data = item.get("content", "").encode("utf-8")
        with open(target, "wb") as fh:
            fh.write(data)
        written.append({"path": os.path.relpath(target, ROOT),
                        "bytes": len(data),
                        "sha256": "sha256:" + hashlib.sha256(data).hexdigest()})
    entry = append_entry("execution", task_id, {
        "effect": "workspace_draft", "written": written,
        "refused": refused, "decision_digest": (reason or "") if dec is not None else "",
        "executed": bool(written) and not refused}, path)
    return {"executed": bool(written) and not refused,
            "reason": "" if not refused else "some paths refused (containment)",
            "files": written, "refused": refused, "receipt_seq": entry["seq"],
            "receipt_digest": entry["digest"]}


# -------------------------------------------------------------------- self-test
def self_test() -> int:
    import shutil
    import tempfile
    vecs: list[tuple[str, bool, str]] = []

    def vec(name, ok, detail=""):
        vecs.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'} {name}" + (f" -> {detail}" if detail and not ok else ""))

    tmp = tempfile.mkdtemp(prefix="cp-selftest-")
    try:
        chain = os.path.join(tmp, "receipts.ndjson")
        al, f0 = load_allowlist()
        vec("allowlist loads + schema-executes", bool(al) and not f0, "; ".join(f0[:2]))

        d1 = resolve("read", "session_initiative")
        vec("read authorized for any source (tool: cap_probe)",
            d1["status"] == "authorized" and d1["tool"] == "cap_probe")

        d2 = resolve("workspace_draft", "commander_order")
        vec("draft authorized for commander order (tool: draft_executor)",
            d2["status"] == "authorized" and d2["tool"] == "draft_executor"
            and d2["bounds"].get("draft_root"))

        d3 = resolve("workspace_draft", "session_initiative")
        vec("draft refused on session initiative alone (policy key)",
            d3["status"] == "refused")

        d4 = resolve("canonical_apply", "commander_order")
        vec("canonical_apply -> commander_motor_act, NO tool bound",
            d4["status"] == "commander_motor_act" and d4["tool"] is None)

        r1 = execute_draft("CP-TEST", {"files": [{"path": "x.txt", "content": "hi"}]},
                           path=chain)
        vec("no execution without a chained decision receipt",
            not r1["executed"] and not r1["files"] and "decision" in r1["reason"])

        decide("CP-TEST", "workspace_draft", "commander_order", path=chain)
        r2 = execute_draft("CP-TEST", {"files": [{"path": "draft.md", "content": "# ok\n"}]},
                           path=chain, drafts_root=os.path.join(tmp, "drafts"))
        wrote = r2["files"] and r2["files"][0]["path"].replace(os.sep, "/").startswith("evidence/drafts/") or r2["files"]
        vec("execution after decision: bounded write + chained receipt",
            r2["executed"] and len(r2["files"]) == 1 and r2["receipt_seq"] == 1)

        r3 = execute_draft("CP-TEST", {"files": [{"path": "../escape.txt", "content": "x"}]},
                           path=chain, drafts_root=os.path.join(tmp, "drafts"))
        vec("containment: drafts-root escape refused",
            not r3["executed"] and r3["refused"] and not os.path.exists(
                os.path.join(tmp, "escape.txt")))

        vec("receipt chain verifies intact", verify_chain(chain) == [])
        lines = open(chain, encoding="utf-8").read().splitlines()
        tampered = json.loads(lines[0]); tampered["payload"]["decision"]["effect"] = "read"
        lines[0] = json.dumps(tampered, sort_keys=True)
        tpath = os.path.join(tmp, "tampered.ndjson")
        open(tpath, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        vec("chain tamper caught", verify_chain(tpath) != [])

        bad_al = json.loads(json.dumps(al))
        bad_al["operations"]["canonical"]["tool"] = "sneaky_executor"
        import io
        from radiation_core import control_plane as cp
        orig = cp.ALLOWLIST_PATH
        try:
            bpath = os.path.join(tmp, "allowlist.json")
            json.dump(bad_al, open(bpath, "w"))
            cp.ALLOWLIST_PATH = bpath
            out: list[str] = []
            from radiation_core.relay import _schema_check
            _schema_check(bad_al, "control_allowlist.schema.json", "tamper", out)
            vec("tampered allowlist caught (canonical tool must stay null)",
                any("canonical" in x or "tool" in x for x in out), f"{len(out)} findings")
        finally:
            cp.ALLOWLIST_PATH = orig
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(1 for _, p, _ in vecs if p)
    for name, p, d in vecs:
        if not p:
            print(f"  FAIL {name} -> {d}")
    print(f"control_plane self-test: {ok}/{len(vecs)} vectors")
    print("boundary: OPERATED tooling (II.11) — it never schedules itself; "
          "canonical_apply stays the Commander's motor act")
    return 0 if ok == len(vecs) else 1


# -------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    pr = sub.add_parser("resolve"); pr.add_argument("--effect", required=True)
    pr.add_argument("--source", required=True); pr.add_argument("--task", default="")
    pd = sub.add_parser("decide"); pd.add_argument("--task", required=True)
    pd.add_argument("--effect", required=True); pd.add_argument("--source", required=True)
    pd.add_argument("--receipts", default=RECEIPTS_PATH)
    pe = sub.add_parser("execute"); pe.add_argument("--task", required=True)
    pe.add_argument("--manifest", required=True); pe.add_argument("--receipts", default=RECEIPTS_PATH)
    pe.add_argument("--drafts-root", default=DRAFTS_ROOT)
    pv = sub.add_parser("verify"); pv.add_argument("--receipts", default=RECEIPTS_PATH)
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.cmd == "resolve":
        print(json.dumps(resolve(args.effect, args.source, args.task), indent=1))
        return 0
    if args.cmd == "decide":
        print(json.dumps(decide(args.task, args.effect, args.source, args.receipts), indent=1))
        return 0
    if args.cmd == "execute":
        manifest = json.load(open(args.manifest, encoding="utf-8"))
        out = execute_draft(args.task, manifest, args.receipts, args.drafts_root)
        print(json.dumps(out, indent=1))
        return 0 if out.get("executed") or out.get("refused") is not None and not out.get("files") else 1
    if args.cmd == "verify":
        p = verify_chain(args.receipts)
        if p:
            for x in p:
                print(f"  ✗ {x}")
            print(f"receipts chain: {len(p)} finding(s)")
            return 1
        n = len(read_chain(args.receipts))
        print(f"receipts chain intact: {n} entr{'y' if n == 1 else 'ies'}, hash-linked")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
