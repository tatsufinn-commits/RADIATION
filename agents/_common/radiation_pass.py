#!/usr/bin/env python3
"""radiation_pass — the RADIATION PASS state machine (5200; review E4).

    python3 agents/_common/radiation_pass.py --host "Arena Agent Mode" [--repo ROOT]
    python3 agents/_common/radiation_pass.py --self-test [--repo ROOT]

═══════════════════════════════════════════════════════════════════════════
 THE PASS IS A HANDOFF, NOT AN ELEVATION. "RADIATION PASS" tells a session
 to RUN this machine; it grants no powers. Deterministic, READ-ONLY: same
 inputs, same output; zero writes. It yields exactly five things:

   1. routing       — known provider folder or the generic CAP fallback
   2. observation   — probe attestation (mount/tools) or explicit
                      non-availability; recorded unknowns
   3. boundary      — the II.11 two-key resolver's answer for the read
                      effect (canonical_apply is NEVER routable: it answers
                      commander_motor_act at every source level)
   4. profile       — the host posture file, or its explicit absence
   5. proofs        — the verification commands a reviewer can run

 Honesty invariants (tested): no identity claims, no tool claims, no
 mutation, unknown host gets the safe neutral flow, Arena's declared
 posture is read-only. Limits: docs/THREAT_MODEL.md.
═══════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.dirname(HERE)
ROOT = os.path.dirname(AGENTS_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

PROVIDERS = ("Arena_AI", "ChatGPT", "Claude", "Gemini", "Grok")
HOST_ALIASES = {"Arena Agent Mode": "Arena_AI", "Arena_AI": "Arena_AI",
                "ChatGPT": "ChatGPT", "Claude": "Claude",
                "Gemini": "Gemini", "Grok": "Grok"}
IDENTITY_PATTERNS = (
    "i am gpt", "i am chatgpt", "i am claude", "i am gemini", "i am grok",
    "my underlying model", "my base model", "i can commit", "i can push",
    "my push access", "my tools are",
)


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _probe(repo: str):
    try:
        cp = _load("capprobe", os.path.join(ROOT, "scripts", "cap_probe.py"))
        return cp.capability_attestation(repo)
    except Exception as e:  # probe unavailable IS a result, not a crash
        return {"repository_status": "unknown", "git_head": None, "dirty": None,
                "repository_path": repo, "probe_error": str(e)[:120],
                "tools_exposed_by_this_server": [], "effects_exposed_by_this_server": []}


def route(host_label: str) -> dict:
    """Known host → provider folder; anything else → generic CAP fallback."""
    label = (host_label or "").strip()
    if label in HOST_ALIASES:
        prov = HOST_ALIASES[label]
        boot = os.path.join(AGENTS_DIR, prov, "BOOT.md")
        if os.path.isfile(boot):
            return {"route": "provider", "provider": prov,
                    "boot_path": os.path.relpath(boot, ROOT)}
    return {"route": "generic", "provider": None, "boot_path": None,
            "note": "unknown or ambiguous host — generic CAP path; declare the "
                    "uncertainty; never invent a provider profile"}


def run_pass(host_label: str, repo: str = ROOT) -> dict:
    # ── 5300 E5: one result, one root ──
    # A profile, the II.11 boundary and the proof commands belong to THIS
    # protocol tree. Observing a foreign --repo alongside them would stitch
    # two contexts into one handoff. Cross-root invocation is therefore
    # refused explicitly: no profile, no repository-relative proofs, and no
    # probe of the target at all. Zero writes either way.
    protocol_root = os.path.realpath(ROOT)
    target_root = os.path.realpath(repo or ".")
    if target_root != protocol_root:
        routed = route(host_label)
        routed["protocol_target_mismatch"] = True
        try:
            from radiation_core.control_plane import resolve
            b_read = resolve("read", "session_initiative", "TID-2026-01-01-passrun")
            b_canon = resolve("canonical_apply", "commander_order", "TID-2026-01-01-passrun")
            boundary = {"read": {"status": b_read["status"], "tool": b_read.get("tool")},
                        "canonical_apply": {"status": b_canon["status"],
                                            "tool": b_canon.get("tool"),
                                            "note": b_canon["reasons"][0]}}
        except Exception as e:
            boundary = {"error": f"resolver unavailable: {e}"[:120]}
        out = {
            "schema_name": "radiation.pass/0.1",
            "host_label_declared": host_label or "",
            "routing": routed,
            "observation": {"repository_path": repo,
                            "repository_status": "protocol_target_mismatch",
                            "note": "--repo is not this protocol's root; the pass "
                                    "observes, binds, and writes NOTHING on the target"},
            "boundary": boundary,
            "profile": None,
            "unknowns": ["protocol_target_mismatch: the pass only speaks for its own "
                         "protocol root — re-run inside the RADIATION checkout",
                         "host tool surface is session-contingent; only the probe's "
                         "catalog is real",
                         "model identity unknowable — the host label is not an identity claim"],
            "proofs": [],
            "pass_is": "a handoff (observation+bounds+proofs), not an elevation; "
                       "zero writes performed; cross-root invocation refused",
        }
        blob = json.dumps(out).lower()
        out["honesty_selfcheck"] = "clean" if not any(p in blob for p in IDENTITY_PATTERNS) \
            else "VIOLATION"
        return out
    routed = route(host_label)
    att = _probe(repo)
    mounted = att.get("repository_status") == "mounted"
    unknowns = []
    if not mounted:
        unknowns.append(f"repository {att.get('repository_status')!r} — no mount, no tools assumed")
    unknowns.append("host tool surface is session-contingent; only the probe's "
                    "catalog is real")
    unknowns.append("model identity unknowable — the host label is not an identity claim")
    try:
        from radiation_core.control_plane import resolve
        b_read = resolve("read", "session_initiative", "TID-2026-01-01-passrun")
        b_canon = resolve("canonical_apply", "commander_order", "TID-2026-01-01-passrun")
        boundary = {"read": {"status": b_read["status"], "tool": b_read.get("tool")},
                    "canonical_apply": {"status": b_canon["status"],
                                        "tool": b_canon.get("tool"),
                                        "note": b_canon["reasons"][0]}}
    except Exception as e:
        boundary = {"error": f"resolver unavailable: {e}"[:120]}
    profile = None
    # 5500 gate review: a posture profile binds to ITS provider only. The Arena
    # profile must never ride on a ChatGPT/Claude/Gemini/Grok route — other
    # providers get explicit declared absence until their own profile exists.
    if routed.get("provider") == "Arena_AI":
        pp = os.path.join(ROOT, "scaffolding", "hosts", "arena_agent_mode.json")
        if os.path.isfile(pp):
            try:
                profile = json.load(open(pp, encoding="utf-8"))
                profile.pop("notes", None)
            except Exception:
                profile = None
    if profile is None:
        unknowns.append("no host posture profile for this route (declared absence)")
    out = {
        "schema_name": "radiation.pass/0.1",
        "host_label_declared": host_label or "",
        "routing": routed,
        "observation": {k: att.get(k) for k in
                        ("repository_path", "repository_status", "git_head",
                         "dirty", "tools_exposed_by_this_server",
                         "effects_exposed_by_this_server")},
        "boundary": boundary,
        "profile": ({"host_label": profile.get("host_label"),
                     "requested_effects": profile.get("posture", {}).get("requested_effects"),
                     "model_identity": None} if profile else None),
        "unknowns": unknowns,
        "proofs": ["python3 -m radiation_core.relay --self-test",
                   "python3 scripts/cap_verify.py --tree",
                   "python3 -m radiation_core.control_plane verify"],
        "pass_is": "a handoff (observation+bounds+proofs), not an elevation; "
                   "zero writes performed",
    }
    blob = json.dumps(out).lower()
    out["honesty_selfcheck"] = "clean" if not any(p in blob for p in IDENTITY_PATTERNS) \
        else "VIOLATION"
    return out


def self_test(repo: str = ROOT) -> int:
    import subprocess
    import tempfile
    vecs: list[tuple[str, bool, str]] = []

    def vec(name, ok, detail=""):
        vecs.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'} {name}" + (f" -> {detail}" if detail and not ok else ""))

    r = run_pass("Arena Agent Mode", repo)
    vec("known host routes to its provider folder",
        r["routing"]["route"] == "provider" and r["routing"]["provider"] == "Arena_AI",
        str(r["routing"]))
    vec("pass yields all five sections",
        all(k in r for k in ("observation", "boundary", "profile", "proofs", "unknowns")))
    vec("no identity/access claims in output", r["honesty_selfcheck"] == "clean",
        r["honesty_selfcheck"])
    vec("Arena declared posture is read-only",
        (r["profile"] or {}).get("requested_effects") == ["read"],
        str((r["profile"] or {}).get("requested_effects")))
    vec("canonical_apply unroutable in the pass boundary",
        r["boundary"]["canonical_apply"]["status"] == "commander_motor_act"
        and r["boundary"]["canonical_apply"]["tool"] is None)

    ru = run_pass("Definitely-Unknown-Host-42", repo)
    vec("unknown host gets safe neutral fallback (no invented profile)",
        ru["routing"]["route"] == "generic" and ru["routing"]["provider"] is None
        and ru["profile"] is None and "uncertainty" in ru["routing"]["note"])
    vec("unknown-host output also claim-free", ru["honesty_selfcheck"] == "clean")

    ghost = tempfile.mkdtemp(prefix="pass-crossroot-")
    rg = run_pass("Arena Agent Mode", ghost)
    vec("cross-root --repo -> explicit protocol_target_mismatch (no profile, no repo-relative proofs)",
        rg["routing"].get("protocol_target_mismatch") is True
        and rg["observation"]["repository_status"] == "protocol_target_mismatch"
        and rg["profile"] is None and rg["proofs"] == []
        and rg["honesty_selfcheck"] == "clean",
        str(rg["observation"])[:80])
    for label, prov in (("ChatGPT", "ChatGPT"), ("Claude", "Claude"),
                        ("Gemini", "Gemini"), ("Grok", "Grok"),
                        ("Arena Agent Mode", "Arena_AI")):
        rp = run_pass(label, repo)
        want_profile = prov == "Arena_AI"
        vec(f"table: {prov} routes to its folder with correct profile discipline",
            rp["routing"]["route"] == "provider" and rp["routing"]["provider"] == prov
            and ((rp["profile"] or {}).get("host_label") == "Arena Agent Mode") is want_profile
            and rp["honesty_selfcheck"] == "clean"
            and any(("declared absence" in u) == (not want_profile) for u in rp["unknowns"]),
            str({"provider": rp["routing"]["provider"], "profile": rp["profile"]}))
    amb = run_pass("gpt? claude? maybe?", repo)
    vec("table: ambiguous label takes the generic path (no invented profile)",
        amb["routing"]["route"] == "generic" and amb["profile"] is None
        and amb["honesty_selfcheck"] == "clean")
    ru2 = run_pass("Definitely-Unknown-Host-42", ghost)
    vec("cross-root + unknown host still refused, uncertainty declared",
        ru2["routing"]["route"] == "generic"
        and ru2["routing"].get("protocol_target_mismatch") is True
        and ru2["profile"] is None and ru2["honesty_selfcheck"] == "clean",
        str(ru2["routing"])[:80])

    # zero-write proof on a disposable COPY (works on any root, git or not)
    try:
        import shutil
        tmp = tempfile.mkdtemp(prefix="pass-nowrite-")
        dst = os.path.join(tmp, "copy")
        shutil.copytree(repo, dst,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                        dirs_exist_ok=True)
        n0 = sum(len(fs) for _, _, fs in os.walk(dst))
        run_pass("Arena Agent Mode", dst)
        n1 = sum(len(fs) for _, _, fs in os.walk(dst))
        vec("pass performs zero writes (copy census unchanged)",
            n0 == n1, f"files {n0}->{n1}")
    except Exception as e:
        vec("pass performs zero writes (copy census unchanged)", False, str(e)[:80])

    ok = sum(1 for _, p, _ in vecs if p)
    for name, p, d in vecs:
        if not p:
            print(f"  FAIL {name} -> {d}")
    print(f"radiation_pass self-test: {ok}/{len(vecs)} vectors")
    print("the pass is a handoff, not an elevation — limits: docs/THREAT_MODEL.md")
    return 0 if ok == len(vecs) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="")
    ap.add_argument("--repo", default=ROOT)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test(a.repo)
    print(json.dumps(run_pass(a.host, a.repo), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
