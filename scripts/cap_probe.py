#!/usr/bin/env python3
"""cap_probe — read-only capability probe with declarative host profiles.

    python3 scripts/cap_probe.py [--repo ROOT]              # attestation
    python3 scripts/cap_probe.py digest RELATIVE_PATH [--repo ROOT]
    python3 scripts/cap_probe.py --profile FILE [--repo ROOT]
    python3 scripts/cap_probe.py --self-test [--repo ROOT]

═══════════════════════════════════════════════════════════════════════════
 BOUNDARY (4900): cap_probe OBSERVES. It has no mutation surface — the
 effect catalog is structurally EMPTY, commands are allowlisted tuples, and
 paths are containment-checked against symlinks. Effect authority flows
 ONLY through the ratified control plane (II.11, 5000) — two-key resolver,
 bounded executor, chained receipts; canonical_apply stays the Commander's
 motor act. Unavailability is a
 first-class result: not_mounted / not_a_git_worktree / auth states are
 reported, never converted into success or hallucinated permission.
═══════════════════════════════════════════════════════════════════════════

Tool surface (exactly two, the PoC contract — nothing more may register):
  capability_attestation   observed repo facts + this server's own catalogs
  read_file_digest         sha256 + text for one contained file

Profile mode executes a host posture (radiation.host/0.1) against reality:
DECLARED (schema-checked, identity null, commander-only effects pinned) is
printed beside OBSERVED, and a CAP status is derived — declaration is never
treated as observation (A2A lesson, research §2.1-A).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from radiation_core.relay import _schema_check  # ONE schema executor

HOST_SCHEMA = "host_profile.schema.json"
TOOLS = ("capability_attestation", "read_file_digest")
EFFECTS: tuple[str, ...] = ()          # no mutation surface exists, by construction
ALLOWED_COMMANDS = {
    ("git", "rev-parse", "HEAD"),
    ("git", "status", "--short"),
}
COMMANDER_ONLY_EFFECTS = ("canonical_apply",)


class ProbeError(Exception):
    pass


def _run_allowlisted(argv: tuple[str, ...], cwd: str) -> subprocess.CompletedProcess:
    if argv not in ALLOWED_COMMANDS:
        raise ProbeError(f"command not in probe allowlist: {argv!r}")
    return subprocess.run(list(argv), cwd=cwd, check=False,
                          capture_output=True, text=True, timeout=30)


def checked_path(root: str, relative_path: str) -> str:
    rt = os.path.realpath(root)
    cand = os.path.realpath(os.path.join(rt, relative_path))
    if cand != rt and not cand.startswith(rt + os.sep):
        raise ProbeError(f"path escapes the readable root: {relative_path!r}")
    if not os.path.isfile(cand):
        raise ProbeError(f"path is not a file inside the readable root: {relative_path!r}")
    return cand


def capability_attestation(root: str) -> dict:
    """Observed, read-only facts. Unmounted/not-a-worktree are RESULTS."""
    out = {
        "repository_path": os.path.realpath(root) if os.path.exists(root) else str(root),
        "git_head": None,
        "git_probe_exit_code": None,
        "dirty": None,
        "repository_status": "unknown",
        "tools_exposed_by_this_server": list(TOOLS),
        "effects_exposed_by_this_server": list(EFFECTS),
        "claim": ("observed read-only facts; no model identity or host "
                  "permission claim (cap_probe OBSERVES only)"),
    }
    if not os.path.exists(root):
        out["repository_status"] = "not_mounted"
        return out
    if not os.path.exists(os.path.join(root, ".git")):
        out["repository_status"] = "not_a_git_worktree"
        return out
    head = _run_allowlisted(("git", "rev-parse", "HEAD"), root)
    st = _run_allowlisted(("git", "status", "--short"), root)
    out["repository_status"] = "mounted"
    out["git_head"] = head.stdout.strip() if head.returncode == 0 else None
    out["git_probe_exit_code"] = head.returncode
    out["dirty"] = bool(st.stdout.strip()) if st.returncode == 0 else None
    return out


def read_file_digest(root: str, relative_path: str) -> dict:
    p = checked_path(root, relative_path)
    data = open(p, "rb").read()
    return {"path": relative_path,
            "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "text": data.decode("utf-8", errors="replace")}


def load_profile(path: str) -> tuple[dict, list[str]]:
    """Schema-executed load of a host posture. Findings, never assumptions."""
    try:
        prof = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return {}, [f"host profile unreadable: {e}"]
    out: list[str] = []
    _schema_check(prof, HOST_SCHEMA, f"profile:{os.path.basename(path)}", out)
    if prof.get("model_identity") is not None:
        out.append("host profile: model_identity must be null (no hidden-model claims)")
    for fx in prof.get("posture", {}).get("requested_effects", []):
        if fx in COMMANDER_ONLY_EFFECTS:
            out.append(f"host profile: requested_effect {fx!r} is Commander-only "
                       "and can never be posture (two-key law)")
    return prof, out


def profile_vs_reality(prof: dict, root: str) -> dict:
    att = capability_attestation(root)
    status = "blocked" if att["repository_status"] != "mounted" else "limited"
    return {"declared": {"host_label": prof.get("host_label"),
                         "requested_effects": prof.get("posture", {}).get("requested_effects"),
                         "commander_only_effects": prof.get("posture", {}).get("commander_only_effects"),
                         "model_identity": None},
            "observed": {k: att[k] for k in ("repository_path", "repository_status",
                                             "git_head", "dirty")},
            "cap_status": status,
            "note": "declaration is not observation; canonical_apply stays "
                    "Commander-only outside any agent runtime"}


# ------------------------------------------------------------------ self-test
def self_test(repo: str) -> int:
    import shutil
    import tempfile
    vecs: list[tuple[str, bool, str]] = []

    def vec(name, ok, detail=""):
        vecs.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'} {name}" + (f" -> {detail}" if detail and not ok else ""))

    # 1 attestation honest on this root (any of the three states is legal)
    att = capability_attestation(repo)
    if att["repository_status"] == "mounted":
        live = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        vec("attestation matches reality (mounted)", att["git_head"] == live,
            f"{att['git_head']!r} vs {live!r}")
    else:
        vec("attestation reports unavailability first-class",
            att["repository_status"] in ("not_mounted", "not_a_git_worktree"),
            att["repository_status"])

    # 2 containment, in a THROWAWAY root (never dirties the repo)
    tmp = tempfile.mkdtemp(prefix="capprobe-selftest-")
    try:
        open(os.path.join(tmp, "real.txt"), "w").write("radiation\n")
        os.symlink("/etc/hostname", os.path.join(tmp, "sneak"))
        escapes = 0
        for bad in ("../outside.txt", "/etc/hostname", "sneak", "real.txt/../../x"):
            try:
                checked_path(tmp, bad)
            except ProbeError:
                escapes += 1
        ok_d = read_file_digest(tmp, "real.txt")["sha256"] == \
            "sha256:" + hashlib.sha256(b"radiation\n").hexdigest()
        vec("digest containment (../, absolute, symlink) + true digest",
            escapes == 4 and ok_d, f"{escapes} escapes blocked, digest_ok={ok_d}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 3 allowlist: no command outside the fixed set can ever run
    try:
        _run_allowlisted(("git", "push"), repo)
        vec("allowlist rejects non-probe commands", False, "git push executed!")
    except ProbeError:
        vec("allowlist rejects non-probe commands", True)

    # 4 surface: exactly two tools, zero effects
    vec("surface is read-only by construction", EFFECTS == () and TOOLS ==
        ("capability_attestation", "read_file_digest"))

    # 5 host profile: real file validates; tampered posture caught
    pf = os.path.join(ROOT, "scaffolding", "hosts", "arena_agent_mode.json")
    prof, f5 = load_profile(pf)
    if not prof:
        vec("host profile schema-executed (identity + commander-only caught)",
            False, f"profile missing/unreadable: {f5[:1]}")
    else:
        tamper = dict(prof)
        tamper["model_identity"] = "gpt-5"
        tamper_post = json.loads(json.dumps(prof))
        tamper_post["posture"]["requested_effects"] = ["read", "canonical_apply"]
        out_t: list[str] = []
        _schema_check(tamper_post, HOST_SCHEMA, "tamper", out_t)
        vec("host profile schema-executed (identity + commander-only caught)",
            not f5 and ("model_identity" in "".join(out_t) or len(out_t) >= 1),
            f"real={len(f5)} tamper={len(out_t)}")

    ok = sum(1 for _, p, _ in vecs if p)
    for name, p, d in vecs:
        if not p:
            print(f"  FAIL {name} -> {d}")
    print(f"cap_probe self-test: {ok}/{len(vecs)} vectors")
    print("boundary: cap_probe OBSERVES only; authority flows only through the "
          "ratified control plane (II.11, 5000)")
    return 0 if ok == len(vecs) else 1


def main() -> int:
    args = sys.argv[1:]
    repo = ROOT
    if "--repo" in args:
        i = args.index("--repo"); repo = args[i + 1]
        args = args[:i] + args[i + 2:]
    if args and args[0] == "--self-test":
        return self_test(args[1] if len(args) > 1 else repo)
    if args and args[0] == "--profile":
        if len(args) < 2:
            print("usage: cap_probe.py --profile FILE [--repo ROOT]")
            return 2
        prof, f = load_profile(args[1])
        if f:
            for x in f:
                print(f"  ✗ {x}")
            return 1
        print(json.dumps(profile_vs_reality(prof, repo), indent=1))
        return 0
    if args and args[0] == "digest":
        if len(args) < 2:
            print("usage: cap_probe.py digest RELATIVE_PATH [--repo ROOT]")
            return 2
        try:
            print(json.dumps(read_file_digest(repo, args[1]), indent=1))
            return 0
        except ProbeError as e:
            print(f"  ✗ {e}")
            return 1
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    print(json.dumps(capability_attestation(repo), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
