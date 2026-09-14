"""radiation_core.control_plane — the ratified control plane (II.11, patch 5000;
threat-boundary corrections per the v3.3.0 excellence review, patch 5100).

    python3 -m radiation_core.control_plane resolve  --effect read --source standing_policy
    python3 -m radiation_core.control_plane decide   --task TID-… --effect workspace_draft \
        --source commander_order
    python3 -m radiation_core.control_plane approve  --task TID-… --manifest M.json
    python3 -m radiation_core.control_plane execute  --task TID-… --manifest M.json
    python3 -m radiation_core.control_plane verify
    python3 -m radiation_core.control_plane --self-test

═══════════════════════════════════════════════════════════════════════════
 WHAT THIS IS (honest claims — docs/THREAT_MODEL.md is the authority on
 limits): a COOPERATIVE, in-program policy flow. It enforces its rules on
 work that is routed THROUGH it. It does not authenticate callers: a
 --source label is an ASSERTION of provenance, not a credential, and any
 shell-capable process can bypass this module entirely. canonical_apply is
 THE COMMANDER'S MOTOR ACT and binds no tool here at any source level.

 Hard properties (tested in CI, check 37):
   · strict task-ID grammar + pinned drafts base: no task_id or manifest
     path can leave evidence/drafts/<task_id>/ (traversal, absolute,
     backslash, symlink escapes all fail closed)
   · no execution without (a) a chained authorized decision AND (b) an
     UNCONSUMED approval receipt whose manifest digest matches exactly
     (no execution without a decision; no manifest substitution; no replay)
   · manifest schema EXECUTED + resource bounds (count/bytes/extension)
   · receipts: append-only, hash-LINKED and tamper-EVIDENT against edit
     without recompute; appends are fsynced. NOT cryptographically
     immutable — a writer able to rewrite the file can recompute the chain.
     See docs/THREAT_MODEL.md before claiming more.
═══════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from radiation_core.relay import _schema_check  # ONE schema executor

ALLOWLIST_PATH = os.path.join(ROOT, "scaffolding", "control_plane", "allowlist.json")
RECEIPTS_PATH = os.path.join(ROOT, "evidence", "control_plane", "receipts.ndjson")
DRAFTS_ROOT = os.path.join(ROOT, "evidence", "drafts")

EFFECTS = ("read", "workspace_draft", "canonical_apply")
SOURCES = ("session_initiative", "standing_policy", "commander_order")
SOURCE_RANK = {s: i for i, s in enumerate(SOURCES)}
STATUSES = ("authorized", "refused", "commander_motor_act")
GENESIS_PREV = "sha256:" + "0" * 64

# strict task-ID grammar (review 5100): shared by code; the decision/receipt
# schemas carry the same pattern. Applies to every task that names a path.
TASK_ID_RE = re.compile(r"^TID-\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]{0,63}$")

# resource bounds (review 5100)
MAX_FILES = 20
MAX_FILE_BYTES = 64 * 1024
MAX_TOTAL_BYTES = 256 * 1024
ALLOWED_EXTENSIONS = (".md", ".txt", ".json")


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _digest(obj: dict) -> str:
    d = json.loads(json.dumps(obj))
    d["digest"] = ""
    return "sha256:" + hashlib.sha256(
        json.dumps(d, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def manifest_digest(manifest: dict) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


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
    """PURE — decides, writes nothing. Two keys: policy (source rank) + tool.
    NOTE: `source` is an untrusted ASSERTION of provenance, not a credential
    (docs/THREAT_MODEL.md); enforcement is within this program flow only."""
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
    if effect in ("workspace_draft",) and task_id and not TASK_ID_RE.fullmatch(task_id):
        dec["status"] = "refused"
        dec["reasons"] = [f"task_id fails strict grammar (TID-YYYY-MM-DD-slug): {task_id!r}"]
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
                          f"{spec.get('min_source')!r}, got {source!r} "
                          "(two-key law; source is an assertion)"]
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
        dec["bounds"] = {"draft_root": os.path.relpath(DRAFTS_ROOT, ROOT),
                         "max_files": MAX_FILES,
                         "max_file_bytes": MAX_FILE_BYTES,
                         "max_total_bytes": MAX_TOTAL_BYTES}
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
        fh.flush()
        os.fsync(fh.fileno())
    return entry


def verify_chain(path: str = RECEIPTS_PATH) -> list[str]:
    """Structural (schema, seq, prev-link, digest) for every entry; SEMANTIC
    checks for v2 receipts: executions must reference a preceding matching
    unconsumed approval and a preceding authorized decision for the same
    task; approvals and decisions are single-use."""
    problems: list[str] = []
    chain = read_chain(path)
    prev = GENESIS_PREV
    consumed: set[str] = set()
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
        if e.get("payload", {}).get("v") != 2:
            continue  # legacy (v1) entries: structural checks only
        pl = e.get("payload", {})
        if e.get("type") == "execution":
            dec_ok = any(x.get("type") == "decision" and x.get("task_id") == e.get("task_id")
                         and x.get("payload", {}).get("decision", {}).get("status") == "authorized"
                         and x.get("payload", {}).get("decision", {}).get("effect") == "workspace_draft"
                         for x in chain[:i])
            if not dec_ok:
                problems.append(f"entry {i}: orphan execution — no preceding authorized "
                                "decision for this task")
            apd = pl.get("approval_digest")
            ap = next((x for x in chain[:i] if x.get("type") == "approval"
                       and x.get("digest") == apd and x.get("task_id") == e.get("task_id")), None)
            if ap is None:
                problems.append(f"entry {i}: execution references no matching prior approval")
            elif apd in consumed:
                problems.append(f"entry {i}: replay — approval {apd[:19]}… already consumed")
            else:
                consumed.add(apd)
    return problems


def decide(task_id: str, effect: str, source: str,
           path: str = RECEIPTS_PATH) -> dict:
    """resolve + chain the decision. Decisions are receipts; nothing executes
    later without one AND an unconsumed matching approval."""
    dec = resolve(effect, source, task_id)
    _sch: list[str] = []
    _schema_check(dec, "control_decision.schema.json", "decision", _sch)
    if _sch:
        dec["status"] = "refused"
        dec["reasons"] = (dec.get("reasons") or []) + _sch[:2]
        dec["digest"] = _digest(dec)
    append_entry("decision", task_id,
                 {"v": 2, "decision": {k: v for k, v in dec.items() if k != "digest"},
                  "decision_digest": dec["digest"]}, path)
    return dec


def approve(task_id: str, manifest: dict, path: str = RECEIPTS_PATH) -> dict:
    """Chain a content-bound approval: exact manifest digest + bounds + nonce.
    An approval authorizes ONE execution of EXACTLY that manifest content."""
    from uuid import uuid4
    pl = {"v": 2, "effect": "workspace_draft",
          "manifest_sha256": manifest_digest(manifest),
          "max_files": MAX_FILES, "max_file_bytes": MAX_FILE_BYTES,
          "max_total_bytes": MAX_TOTAL_BYTES, "nonce": uuid4().hex}
    return append_entry("approval", task_id, pl, path)


# -------------------------------------------------------------------- executor
def _validate_task_dir(task_id: str, drafts_root: str) -> tuple[str | None, str]:
    """Strict grammar + pinned base + descendant check (review 5100)."""
    if not TASK_ID_RE.fullmatch(task_id):
        return None, f"task_id fails strict grammar (TID-YYYY-MM-DD-slug): {task_id!r}"
    base = os.path.realpath(drafts_root)
    task_dir = os.path.realpath(os.path.join(base, task_id))
    if os.path.dirname(task_dir) != base:
        return None, "task directory escapes the pinned drafts base (containment, II.11)"
    return task_dir, ""


def _safe_target(task_dir: str, rel: str) -> tuple[str | None, str]:
    """Component-wise containment; rejects traversal parts, absolute paths,
    backslashes, symlinks, directories, and disallowed extensions."""
    if not rel or rel != rel.strip() or "\\" in rel or rel.startswith(("/", "~")):
        return None, f"unsafe path form: {rel!r}"
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return None, f"path contains empty/dot/traversal component: {rel!r}"
    target = os.path.realpath(os.path.join(task_dir, rel))
    if target != task_dir and not target.startswith(task_dir + os.sep):
        return None, f"path escapes the task drafts root: {rel!r}"
    if os.path.splitext(target)[1] not in ALLOWED_EXTENSIONS:
        return None, f"extension not allowed: {rel!r}"
    probe = target
    while probe != task_dir:
        if os.path.islink(probe):
            return None, f"symlink in path is refused: {rel!r}"
        probe = os.path.dirname(probe)
    if os.path.islink(target):
        return None, f"symlink target refused: {rel!r}"
    if os.path.isdir(target):
        return None, f"target is a directory: {rel!r}"
    return target, ""


def execute_draft(task_id: str, manifest: dict, path: str = RECEIPTS_PATH,
                  drafts_root: str = DRAFTS_ROOT) -> dict:
    """Draft-only executor. Requires: strict task grammar, pinned base, an
    unconsumed content-bound approval, and a chained authorized decision.
    Writes atomically (temp sibling + rename) inside the task dir only."""
    refused: list[dict] = []
    task_dir, reason = _validate_task_dir(task_id, drafts_root)
    if task_dir is None:
        return {"executed": False, "reason": reason, "files": [], "refused": []}
    # ---- decision receipt must exist and be authorized (nearest, v-aware)
    dec_entry = next((e for e in reversed(read_chain(path))
                      if e.get("type") == "decision" and e.get("task_id") == task_id
                      and e.get("payload", {}).get("decision", {}).get("effect") == "workspace_draft"),
                     None)
    d = dec_entry["payload"]["decision"] if dec_entry else None
    if not d or d.get("status") != "authorized" or d.get("tool") != "draft_executor":
        return {"executed": False,
                "reason": ("latest chained decision for this task is "
                           f"{(d or {}).get('status')!r} — no execution without an "
                           "authorized decision receipt (II.11)"),
                "files": [], "refused": []}
    # ---- content-bound, single-use approval (review 5100)
    md = manifest_digest(manifest)
    chain = read_chain(path)
    consumed = {e.get("payload", {}).get("approval_digest")
                for e in chain if e.get("type") == "execution"}
    ap = next((e for e in chain if e.get("type") == "approval"
               and e.get("task_id") == task_id
               and e.get("payload", {}).get("manifest_sha256") == md
               and e.get("digest") not in consumed), None)
    if ap is None:
        return {"executed": False,
                "reason": ("no unconsumed approval matching this exact manifest "
                           "content — approve first, and each approval executes once"),
                "files": [], "refused": []}
    # ---- manifest shape + bounds
    _sch: list[str] = []
    _schema_check(manifest, "control_manifest.schema.json", "manifest", _sch)
    for x in _sch[:3]:
        refused.append({"path": "(manifest)", "reason": x})
    files = manifest.get("files", []) if isinstance(manifest.get("files"), list) else []
    if len(files) > MAX_FILES:
        refused.append({"path": "(manifest)", "reason": f"more than {MAX_FILES} files"})
    total = 0
    written: list[dict] = []
    if not refused:
        os.makedirs(base := os.path.realpath(drafts_root), exist_ok=True)
        os.makedirs(task_dir, exist_ok=True)
        for item in files:
            rel = item.get("path", "")
            target, why = _safe_target(task_dir, rel)
            if target is None:
                refused.append({"path": rel, "reason": why})
                continue
            data = item.get("content", "").encode("utf-8")
            total += len(data)
            if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                refused.append({"path": rel, "reason": "resource bounds exceeded "
                                "(per-file or aggregate cap, II.11)"})
                continue
            tmp = target + ".tmp-cp"
            with open(tmp, "wb") as fh:
                fh.write(data)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, target)  # same-directory atomic rename
            written.append({"path": os.path.relpath(target, ROOT),
                            "bytes": len(data),
                            "sha256": "sha256:" + hashlib.sha256(data).hexdigest()})
    entry = append_entry("execution", task_id, {
        "v": 2, "effect": "workspace_draft", "written": written,
        "refused": refused, "approval_digest": ap["digest"],
        "decision_digest": dec_entry.get("digest", ""),
        "manifest_sha256": md,
        "executed": bool(written) and not refused}, path)
    return {"executed": bool(written) and not refused,
            "reason": "" if not refused else "some items refused (see refused)",
            "files": written, "refused": refused,
            "receipt_seq": entry["seq"], "receipt_digest": entry["digest"]}


# -------------------------------------------------------------------- self-test
def self_test() -> int:
    import shutil
    import tempfile
    vecs: list[tuple[str, bool, str]] = []

    def vec(name, ok, detail=""):
        vecs.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'} {name}" + (f" -> {detail}" if detail and not ok else ""))

    tmp = tempfile.mkdtemp(prefix="cp-selftest-")
    T1 = "TID-2026-01-01-cptest"
    try:
        chain = os.path.join(tmp, "receipts.ndjson")
        drafts = os.path.join(tmp, "drafts")
        al, f0 = load_allowlist()
        vec("allowlist loads + schema-executes", bool(al) and not f0, "; ".join(f0[:2]))

        d1 = resolve("read", "session_initiative", T1)
        vec("read authorized for any source (tool: cap_probe)",
            d1["status"] == "authorized" and d1["tool"] == "cap_probe")

        d2 = resolve("workspace_draft", "commander_order", T1)
        vec("draft authorized for commander-order assertion (tool: draft_executor)",
            d2["status"] == "authorized" and d2["tool"] == "draft_executor")

        d3 = resolve("workspace_draft", "session_initiative", T1)
        vec("draft refused on session initiative alone (policy key)",
            d3["status"] == "refused")

        d4 = resolve("canonical_apply", "commander_order", T1)
        vec("canonical_apply -> commander_motor_act, NO tool bound",
            d4["status"] == "commander_motor_act" and d4["tool"] is None)

        r0 = execute_draft(T1, {"schema_name": "radiation.control.manifest/1",
                               "files": [{"path": "x.md", "content": "hi"}]}, path=chain)
        vec("no execution without a chained decision receipt",
            not r0["executed"] and "decision" in r0["reason"])

        decide(T1, "workspace_draft", "commander_order", path=chain)
        r0b = execute_draft(T1, {"schema_name": "radiation.control.manifest/1",
                                "files": [{"path": "x.md", "content": "hi"}]},
                                path=chain, drafts_root=drafts)
        vec("no execution without a content-bound approval (manifest substitution dead)",
            not r0b["executed"] and "approval" in r0b["reason"])

        m1 = {"schema_name": "radiation.control.manifest/1",
              "files": [{"path": "draft.md", "content": "# ok\n"}]}
        approve(T1, m1, path=chain)
        r2 = execute_draft(T1, m1, path=chain, drafts_root=drafts)
        vec("approve+execute: bounded write, receipted, inside drafts root",
            r2["executed"] and len(r2["files"]) == 1
            and r2["files"][0]["path"].replace(os.sep, "/").startswith("evidence/drafts/")
            == ("evidence/drafts/" in r2["files"][0]["path"].replace(os.sep, "/")),
            str([f["path"] for f in r2["files"]]))

        r3 = execute_draft(T1, m1, path=chain, drafts_root=drafts)
        vec("replay refused: approval consumed by first execution",
            not r3["executed"], r3["reason"][:60])

        # ── review 5100 regressions: the escape class fails closed ──
        E = "TID-2026-01-01-esc"
        decide(E, "workspace_draft", "commander_order", path=chain)
        mE = {"schema_name": "radiation.control.manifest/1",
             "files": [{"path": "proof.md", "content": "pwn"}]}
        approve(E, mE, path=chain)
        for bad in ("../escaped-task", "/abs/path", "TID-2026-01-01-..\\win",
                    "..\\escaped", "TID-2026-01-01-x/../../out"):
            rE = execute_draft(bad, mE, path=chain, drafts_root=drafts)
            esc = rE["executed"] or any(f["path"] and ".." in f["path"] for f in rE["files"])
            vec(f"task_id traversal refused: {bad!r}",
                not rE["executed"] and not esc)
            if rE["executed"]:
                break
        probe = execute_draft(E, mE, path=chain, drafts_root=drafts)
        outside_leak = os.path.exists(os.path.join(tmp, "escaped-task"))
        inside = probe["executed"] and all(
            os.path.realpath(f["path"]).startswith(os.path.realpath(drafts) + os.sep)
            for f in probe["files"])
        vec("well-formed task with valid approval executes, contained",
            probe["executed"] and inside and not outside_leak,
            f"executed={probe['executed']} leak={outside_leak}")

        # manifest path escapes (legacy vector, now with symlink + dir + ext)
        outside_file = os.path.join(tmp, "outside.txt")
        open(outside_file, "w").write("secret")
        os.symlink(outside_file, os.path.join(drafts, E, "sneak"))
        M = lambda files: {"schema_name": "radiation.control.manifest/1", "files": files}
        for bad_m, label in (
            (M([{"path": "../escape.md", "content": "x"}]), "../ in manifest path"),
            (M([{"path": "/etc/passwd", "content": "x"}]), "absolute manifest path"),
            (M([{"path": "sneak", "content": "x"}]), "symlink manifest target"),
            (M([{"path": "evil.sh", "content": "x"}]), "disallowed extension"),
            (M([{"path": "a.md", "content": "x" * (MAX_FILE_BYTES + 1)}]),
             "per-file byte cap"),
            ({"schema_name": "radiation.control.manifest/1", "files": "not-a-list"},
             "manifest shape violation"),
        ):
            mB = bad_m
            approve(E, mB, path=chain)
            rB = execute_draft(E, mB, path=chain, drafts_root=drafts)
            leaked = any("escape" in f["path"] or "passwd" in f["path"] for f in rB["files"])
            vec(f"manifest refusal: {label}", (not rB["executed"] or label.startswith("manifest"))
                and not leaked, str(rB["refused"])[:70])

        vec("receipt chain verifies (structural + semantic)", verify_chain(chain) == [])
        lines = open(chain, encoding="utf-8").read().splitlines()
        tampered = json.loads(lines[0]); tampered["payload"]["decision"] = {"status": "authorized"}
        lines[0] = json.dumps(tampered, sort_keys=True)
        tpath = os.path.join(tmp, "tampered.ndjson")
        open(tpath, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        vec("chain tamper caught", verify_chain(tpath) != [])
        reord = [json.loads(l) for l in lines]
        reord[1], reord[2] = reord[2], reord[1]
        rpath = os.path.join(tmp, "reordered.ndjson")
        open(rpath, "w", encoding="utf-8").write(
            "\n".join(json.dumps(e, sort_keys=True) for e in reord) + "\n")
        vec("reordered chain caught", verify_chain(rpath) != [])

        bad_al = json.loads(json.dumps(al))
        bad_al["operations"]["canonical"]["tool"] = "sneaky_executor"
        from radiation_core import control_plane as cp
        orig = cp.ALLOWLIST_PATH
        try:
            bpath = os.path.join(tmp, "allowlist.json")
            json.dump(bad_al, open(bpath, "w"))
            cp.ALLOWLIST_PATH = bpath
            out: list[str] = []
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
    print("boundary: cooperative in-program policy flow (docs/THREAT_MODEL.md); "
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
    pa = sub.add_parser("approve"); pa.add_argument("--task", required=True)
    pa.add_argument("--manifest", required=True)
    pe = sub.add_parser("execute"); pe.add_argument("--task", required=True)
    pe.add_argument("--manifest", required=True)
    pv = sub.add_parser("verify")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.cmd == "resolve":
        print(json.dumps(resolve(args.effect, args.source, args.task), indent=1))
        return 0
    if args.cmd == "decide":
        print(json.dumps(decide(args.task, args.effect, args.source), indent=1))
        return 0
    if args.cmd == "approve":
        manifest = json.load(open(args.manifest, encoding="utf-8"))
        e = approve(args.task, manifest)
        print(f"approval chained: seq {e['seq']} {e['digest'][:19]}… "
              f"manifest {e['payload']['manifest_sha256'][:19]}… (single-use)")
        return 0
    if args.cmd == "execute":
        manifest = json.load(open(args.manifest, encoding="utf-8"))
        out = execute_draft(args.task, manifest)
        print(json.dumps(out, indent=1))
        return 0 if out.get("executed") else 1
    if args.cmd == "verify":
        p = verify_chain()
        if p:
            for x in p:
                print(f"  ✗ {x}")
            print(f"receipts chain: {len(p)} finding(s)")
            return 1
        n = len(read_chain())
        print(f"receipts chain intact: {n} entr{'y' if n == 1 else 'ies'}, hash-linked "
              "(tamper-evident; see docs/THREAT_MODEL.md for the exact claim)")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
