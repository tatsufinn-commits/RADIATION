#!/usr/bin/env python3
"""cap_verify — structural + semantic verifier for CAP capability-activation records.

    python3 scripts/cap_verify.py RECORD.json [--repo ROOT]
    python3 scripts/cap_verify.py --self-test

═══════════════════════════════════════════════════════════════════════════
 BOUNDARY (4700 research adoption): cap_verify VERIFIES capability records.
 Since the Commander's Product-2 ratification (5000, II.11), authority
 flows ONLY through radiation_core.control_plane: two-key resolver, bounded
 draft executor, hash-chained receipts. cap_verify still only VERIFIES
 records. canonical_apply stays the Commander's motor act.
═══════════════════════════════════════════════════════════════════════════

Checks performed on a record (radiation.cap/0.1):
  1. schema execution — schemas/cap_record.schema.json, recursively, using the
     SAME executor as every other contract schema (radiation_core.relay); a
     second implementation was the 4700 lesson and is not repeated here.
  2. identity binding — declared.model_identity must be null (the hidden
     model behind a host is unknowable; labels are labels).
  3. vocabularies — status, requested_effect, blockers, verifier names.
  4. seal digest — recomputed over canonical bytes with the digest zeroed;
     any later hand-edit of any field breaks the seal.
  5. honesty of outcomes — "verified" requires non-empty observation, all
     green registry checks, no blockers; "blocked" requires blockers.
  6. observed fidelity (--live default) — observed git_head/dirty are
     re-probed against the repository; claims must match reality.

Exit 0 iff zero findings. Findings always print (4700 law: verbose, never
exit-code-only).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from radiation_core.relay import _schema_check  # ONE executor, no second impl

SCHEMA = "cap_record.schema.json"
STATUSES = ("new", "limited", "ready", "blocked", "verified")
EFFECTS = ("read", "workspace_draft", "canonical_apply")
BLOCKERS = (
    "repository_not_mounted_or_not_a_git_worktree",
    "git_probe_failed",
    "auth_required",
    "read_only_surface",
    "canonical_apply_requires_commander_outside_agent_runtime",
    "effect_denied_by_tool_absence",
    "effect_denied_by_policy",
)
# Deterministic verifiers a record may cite — RADIATION's own CLI checks only.
VERIFIERS = {
    "relay-self-test": [sys.executable, "-m", "radiation_core.relay", "--self-test"],
    "nota-check": [sys.executable, "scripts/nota.py", "--check"],
    "knowledge-regression": [sys.executable, "scripts/knowledge_regression.py"],
    "render-docs-check": [sys.executable, "scripts/render_docs.py", "--check"],
    "validate-full": [sys.executable, "scripts/validate.py"],
}
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

# C-4 redaction policy (docs/CAP_RECORD_POLICY.md) — executed here, vector in
# self-test, check 35 in CI. Mechanical classes only; judgment classes are
# prose law (prompt bodies, model speculation, personal data).
REDACTION_PATTERNS = (
    ("github-pat-classic", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github-pat-fine", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer-token", re.compile(r"Bearer [A-Za-z0-9._\-]{15,}")),
    ("access-token-url", re.compile(r"x-access-token:")),
    ("embedded-password", re.compile(r"(?i)\bpassword\s*[=:]\s*\S+")),
)


def _record_strings(obj, where="record"):
    if isinstance(obj, str):
        yield where, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _record_strings(v, f"{where}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _record_strings(v, f"{where}[{i}]")


def check_redaction(doc: dict) -> list[str]:
    out: list[str] = []
    for where, s in _record_strings(doc):
        for name, pat in REDACTION_PATTERNS:
            if pat.search(s):
                out.append(f"redaction violation (C-4 policy): {name} pattern in {where}")
    return out


def canonical_bytes(doc: dict) -> bytes:
    d = json.loads(json.dumps(doc))          # deep copy, round-trip stable
    if "verified" in d:
        d["verified"] = {**d["verified"], "artifact_digest": ""}
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


def seal_digest(doc: dict) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(doc)).hexdigest()


def live_attestation(repo: str) -> dict:
    """Allowlisted read-only probe (the PoC's two-tool contract, CLI form)."""
    if not os.path.isdir(repo) or not os.path.exists(os.path.join(repo, ".git")):
        return {"mounted": False}
    head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=False, timeout=30)
    st = subprocess.run(["git", "-C", repo, "status", "--short"],
                        capture_output=True, text=True, check=False, timeout=30)
    return {"mounted": True,
            "git_head": head.stdout.strip() if head.returncode == 0 else None,
            "dirty": bool(st.stdout.strip()) if st.returncode == 0 else None}


def verify_record(doc: dict, repo: str = ROOT, live: bool = True) -> list[str]:
    out: list[str] = []
    _schema_check(doc, SCHEMA, "cap_record", out)
    dec = doc.get("declared", {})
    obs = doc.get("observed", {})
    ver = doc.get("verified", {})
    status = doc.get("status")
    blockers = doc.get("blockers", [])
    if dec.get("model_identity") is not None:
        out.append("identity binding: declared.model_identity must be null "
                   "(no hidden-model claims)")
    if status not in STATUSES:
        out.append(f"status invalid: {status!r}")
    for b in blockers:
        if b not in BLOCKERS:
            out.append(f"blocker not in vocabulary: {b!r}")
    for c in ver.get("checks", []):
        if isinstance(c, dict) and c.get("name") not in VERIFIERS:
            out.append(f"invalid verification reference: {c.get('name')!r} "
                       "not in verifier registry")
    dg = ver.get("artifact_digest", "")
    if status in ("ready", "verified"):
        if not (isinstance(dg, str) and DIGEST_RE.match(dg)):
            out.append("seal digest missing/malformed (want sha256:<64 hex>)")
        elif dg != seal_digest(doc):
            out.append("seal digest does not bind record content "
                       "(hand-edited after seal — re-render, never hand-edit)")
    if status == "verified":
        if not ver.get("checks"):
            out.append("fabricated success: verified with zero deterministic checks")
        elif any(c.get("exit_code") != 0 for c in ver.get("checks", [])):
            out.append("fabricated success: verified with failing checks")
        if blockers:
            out.append(f"fabricated success: verified while blockers present: {blockers}")
        if not (obs.get("repository") or {}).get("path"):
            out.append("fabricated success: verified without any observation")
    if status == "blocked" and not blockers:
        out.append("blocked record must name its blockers (unavailability is "
                   "first-class, not silent)")
    if live and status == "verified" and (obs.get("repository") or {}).get("path"):
        att = live_attestation(repo)
        pre = len(out)
        r = obs.get("repository", {})
        if not att.get("mounted"):
            out.append("observed fidelity: repository no longer mounted")
        else:
            if r.get("git_head") != att["git_head"]:
                out.append(f"observed fidelity: git_head drifts "
                           f"(record={r.get('git_head')!r} live={att['git_head']!r})")
            if "dirty" in r and r.get("dirty") != att["dirty"]:
                out.append(f"observed fidelity: dirty bit drifts "
                           f"(record={r.get('dirty')!r} live={att['dirty']!r})")
            if len(out) > pre:
                out.append("fabricated success: verified record contradicts live observation")
    out += check_redaction(doc)
    return out


# ------------------------------------------------------------------ self-test
def _fixture_tampered(repo: str, att: dict) -> dict:
    d = _fixture_verified_unchecked(att)
    d["task_id"] = "CAP-SELFTEST-3"
    d["status"] = "verified"
    d["observed"]["repository"]["git_head"] = "0" * 40                   # fake head
    d["verified"]["checks"] = [{"name": "unit-tests", "exit_code": 0}]  # not in registry
    d["verified"]["artifact_digest"] = "sha256:" + "a" * 64              # stale seal
    return d


def _fixture_verified(repo: str) -> dict:
    att = live_attestation(repo)
    r = subprocess.run(VERIFIERS["nota-check"], cwd=repo, capture_output=True,
                       text=True, check=False, timeout=120)
    doc = _fixture_verified_unchecked(att)
    doc["task_id"] = "CAP-SELFTEST-1"
    doc["verified"]["checks"] = [{"name": "nota-check", "exit_code": r.returncode,
                                  "detail": ""}]
    doc["verified"]["artifact_digest"] = seal_digest(doc)
    return doc


def _fixture_verified_unchecked(att: dict) -> dict:
    doc = {
        "schema_name": "radiation.cap/0.1", "task_id": "CAP-SELFTEST",
        "declared": {"host_label": "self-test", "adapter_path": "scripts/cap_verify.py",
                     "requested_effect": "read", "model_identity": None},
        "observed": {"repository": {"path": os.path.abspath(os.getcwd()),
                                    "git_head": att.get("git_head"),
                                    "dirty": att.get("dirty"), "status": "mounted"},
                     "tools": ["capability_attestation", "read_file_digest"],
                     "allowed_effects": [], "probes": []},
        "verified": {"policy_paths_loaded": [], "artifact_digest": "", "checks": []},
        "status": "verified", "blockers": [], "events": [],
    }
    return doc


def _fixture_blocked() -> dict:
    return {"schema_name": "radiation.cap/0.1", "task_id": "CAP-SELFTEST-2",
            "declared": {"host_label": "self-test", "adapter_path": "scripts/cap_verify.py",
                         "requested_effect": "read", "model_identity": None},
            "observed": {"repository": {}, "tools": [], "allowed_effects": [], "probes": []},
            "verified": {"policy_paths_loaded": [], "checks": [], "artifact_digest": ""},
            "status": "blocked",
            "blockers": ["repository_not_mounted_or_not_a_git_worktree"], "events": []}


def _fixture_identity(repo: str) -> dict:
    att = live_attestation(repo)
    d = _fixture_verified_unchecked(att)
    d["task_id"] = "CAP-SELFTEST-4"
    d["declared"]["model_identity"] = "gpt-5"                 # forbidden claim
    d["verified"]["artifact_digest"] = seal_digest(d)         # otherwise well-formed
    return d


def self_test(repo: str) -> int:
    att = live_attestation(repo)
    mounted = bool(att.get("mounted"))
    vecs: list[tuple[str, bool, str]] = []
    if mounted:
        f1 = verify_record(_fixture_verified(repo), repo, live=True)
        vecs.append(("honest verified record passes (live probe + real check)", not f1,
                     "; ".join(f1[:2])))
    else:
        f1 = verify_record(_fixture_blocked(), repo, live=True)
        vecs.append(("honest blocked record passes (unmounted root)", not f1,
                     "; ".join(f1[:2])))
        # a "verified" record about an unmounted root must be caught
        bad = _fixture_verified_unchecked(att)
        bad["task_id"] = "CAP-SELFTEST-NOMOUNT"
        f1b = verify_record(bad, repo, live=True)
        vecs.append(("verified-without-mount caught as fabricated", len(f1b) >= 2,
                     f"{len(f1b)} findings"))
    f2 = verify_record(_fixture_blocked(), repo, live=True)
    vecs.append(("honest blocked record passes", not f2, "; ".join(f2[:2])))
    f3 = verify_record(_fixture_tampered(repo, att), repo, live=True)
    vecs.append(("tampered record caught (head/verifier/seal)", len(f3) >= 3,
                 f"{len(f3)} findings"))
    f4 = verify_record(_fixture_identity(repo), repo, live=False)
    vecs.append(("identity claim caught", any("model_identity" in x for x in f4),
                 f"{len(f4)} findings"))
    leak = _fixture_blocked()
    leak["task_id"] = "CAP-SELFTEST-REDACT"
    leak["events"] = [{"state": "probe", "output": "token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"}]
    f5 = verify_record(leak, repo, live=False)
    vecs.append(("credential leak caught (C-4 redaction)",
                 any(x.startswith("redaction violation") for x in f5),
                 f"{len(f5)} findings"))
    ok = 0
    for name, passed, detail in vecs:
        ok += passed
        print(f"  {'PASS' if passed else 'FAIL'} {name}" + (f" -> {detail}" if detail and not passed else ""))
    print(f"cap_verify self-test: {ok}/{len(vecs)} vectors")
    print("boundary: cap_verify VERIFIES records; authority flows only through "
          "the ratified control plane (II.11, 5000)")
    return 0 if ok == len(vecs) else 1


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "--self-test":
        repo = args[1] if len(args) > 1 else ROOT
        return self_test(repo)
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if not args:
        print(__doc__)
        return 2
    record_path = args[0]
    repo, live = ROOT, True
    rest = args[1:]
    if "--repo" in rest:
        i = rest.index("--repo"); repo = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
    if "--no-live" in rest:
        live = False
    with open(record_path, encoding="utf-8") as fh:
        doc = json.load(fh)
    findings = verify_record(doc, repo, live=live)
    if findings:
        for x in findings:
            print(f"  ✗ {x}")
        print(f"cap_verify: {len(findings)} finding(s) — {record_path}")
        return 1
    print(f"cap_verify: 0 findings — {record_path} "
          f"(status={doc.get('status')!r}, sealed={bool(doc.get('verified', {}).get('artifact_digest'))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
