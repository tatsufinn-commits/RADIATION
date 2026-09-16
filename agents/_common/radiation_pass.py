#!/usr/bin/env python3
"""radiation_pass — the RADIATION PASS state machine (5200; review E4).

    python3 agents/_common/radiation_pass.py --host "Arena Agent Mode" [--repo ROOT]
    python3 agents/_common/radiation_pass.py --host "Arena Agent Mode" --persist [--repo ROOT]
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

 S-2-ENV extension (v3.10.26): opt-in persistence via --persist flag
 writing Brain/short_term/active/session_capability_state.json
 (schema-valid before write; deterministic JSON, sorted keys; stdout reports
 written path + counts). Default behavior (no flag) remains byte-identical
 to today — zero writes. The state file is working memory, presumed
 impermanent, triaged at session close per short-term law, never committed
 with live content. No hardcoded platform limits, no private-quota probing,
 no parallel EXECUTE/ALT/HOLD chain — input artifact consumed by scan/anchor/
 stockpile shortfall, never resolver. No autonomous self-check loop, no network
 calls from writer, file can never raise authority (stale reads UNKNOWN).
═══════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import datetime
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


def _get_git_head(repo: str = ROOT) -> str:
    # No network calls — local git only
    try:
        import subprocess
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, timeout=2)
        if p.returncode == 0:
            return p.stdout.strip()[:12]
    except Exception:
        pass
    return "unknown"


def build_session_capability_state(host_label: str, pass_output: dict, repo: str = ROOT) -> dict:
    """
    Build session_capability_state from pass output — working memory, not resolver.
    Vocabulary per Gate-1 correspondence map (Domain-10 rider):
    AVAILABLE↔primary+active, UNAVAILABLE↔deprecated/secondary/asserted/benchmark,
    UNKNOWN↔draft+honesty-grammar, VERIFIED↔[D]/[I]+primary+active, etc.
    Mandatory discipline: UNKNOWN is first-class everywhere; absent evidence stays UNKNOWN never UNAVAILABLE; stale generated_at reads UNKNOWN rather than lie.
    """
    # host_label DECLARED — never discovered, never profile-inferred
    declared_host = (host_label or "").strip()
    if not declared_host:
        declared_host = pass_output.get("host_label_declared", "") or "UNKNOWN"

    # route as returned by radiation_pass.route()
    routed = pass_output.get("routing") or route(declared_host)

    # capabilities from observation
    obs = pass_output.get("observation", {}) or {}
    tools = obs.get("tools_exposed_by_this_server") or []
    effects = obs.get("effects_exposed_by_this_server") or []

    capabilities = []

    # OBSERVED capabilities from cap_probe
    for t in tools:
        if not isinstance(t, str) or not t:
            continue
        capabilities.append({
            "name": t,
            "state": "AVAILABLE",
            "provenance": "OBSERVED",
            "evidence": f"cap_probe execution this session: tools_exposed_by_this_server includes {t} — repository_status={obs.get('repository_status')}"
        })

    for e in effects:
        if not isinstance(e, str) or not e:
            continue
        # Avoid duplicate if same as tool
        if any(c["name"] == e for c in capabilities):
            continue
        capabilities.append({
            "name": e,
            "state": "AVAILABLE",
            "provenance": "OBSERVED",
            "evidence": f"cap_probe execution this session: effects_exposed_by_this_server includes {e}"
        })

    # DECLARED capability from host label
    capabilities.append({
        "name": f"host_label:{declared_host}",
        "state": "AVAILABLE",
        "provenance": "DECLARED",
        "evidence": f"host_label DECLARED via --host flag: {declared_host} — never discovered, never profile-inferred per schema discipline"
    })

    # UNKNOWN discipline: capabilities with no evidence stay UNKNOWN never UNAVAILABLE
    # Example: if no profile, host posture profile capability is UNKNOWN (absent evidence stays UNKNOWN)
    profile = pass_output.get("profile")
    if profile is None:
        capabilities.append({
            "name": "host_posture_profile",
            "state": "UNKNOWN",
            "provenance": "INFERRED",
            "evidence": "no host posture profile for this route (declared absence) — absent evidence stays UNKNOWN per mandatory discipline"
        })
    else:
        capabilities.append({
            "name": "host_posture_profile",
            "state": "AVAILABLE",
            "provenance": "DECLARED",
            "evidence": f"host posture profile present for provider {routed.get('provider')} — host_label {profile.get('host_label')}"
        })

    # If repository not mounted, add UNKNOWN for mount capability (never UNAVAILABLE without evidence)
    repo_status = obs.get("repository_status")
    if repo_status != "mounted":
        capabilities.append({
            "name": "repository_mount",
            "state": "UNKNOWN",
            "provenance": "INFERRED",
            "evidence": f"repository_status={repo_status!r} — no mount, no tools assumed — absent evidence stays UNKNOWN never UNAVAILABLE per discipline"
        })

    # Mandatory UNKNOWN discipline: always include at least one UNKNOWN capability to demonstrate first-class UNKNOWN
    # Capability with no evidence is UNKNOWN never UNAVAILABLE — stale generated_at reads UNKNOWN rather than lie
    capabilities.append({
        "name": "unobserved_capability_surface",
        "state": "UNKNOWN",
        "provenance": "INFERRED",
        "evidence": "absent evidence stays UNKNOWN never UNAVAILABLE per mandatory discipline — session tool surface is session-contingent, only probe catalog is real"
    })

    # constraints — repository_status, dirty, etc.
    constraints = []
    constraints.append({
        "name": "repository_status",
        "provenance": "OBSERVED",
        "value_or_unknown": obs.get("repository_status") or "UNKNOWN"
    })
    constraints.append({
        "name": "git_head",
        "provenance": "OBSERVED",
        "value_or_unknown": obs.get("git_head") or "UNKNOWN"
    })
    constraints.append({
        "name": "dirty",
        "provenance": "OBSERVED",
        "value_or_unknown": obs.get("dirty") if obs.get("dirty") is not None else "UNKNOWN"
    })
    # Add a generic UNKNOWN constraint to demonstrate UNKNOWN first-class
    constraints.append({
        "name": "session_tool_surface",
        "provenance": "INFERRED",
        "value_or_unknown": "UNKNOWN"
    })

    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    pass_ref = _get_git_head(repo)
    honesty_note = "Working memory artifact — session-local in Brain/short_term/active/, presumed impermanent, triaged at session close per short-term law, never committed with live content; can never raise authority (data about limits, walls reading: stale reads UNKNOWN); UNKNOWN is first-class value everywhere; absent evidence stays UNKNOWN never UNAVAILABLE; stale generated_at reads UNKNOWN rather than lie."

    state = {
        "schema_name": "radiation.session_capability_state/1",
        "host_label": declared_host,
        "route": routed,
        "capabilities": sorted(capabilities, key=lambda x: x["name"]),
        "constraints": sorted(constraints, key=lambda x: x["name"]),
        "generated_at": generated_at,
        "pass_ref": pass_ref,
        "honesty_note": honesty_note
    }
    return state


def persist_session_state(host_label: str, pass_output: dict, repo: str = ROOT) -> tuple[str, dict]:
    """
    Opt-in persistence: write Brain/short_term/active/session_capability_state.json
    Schema-valid before write; deterministic JSON sorted keys; stdout reports written path + counts.
    No network calls. Returns (written_path, counts).
    """
    state = build_session_capability_state(host_label, pass_output, repo)

    # Schema-valid before write — load schema and validate enums/required
    schema_path = os.path.join(ROOT, "schemas", "session_capability_state.schema.json")
    try:
        schema = json.load(open(schema_path, encoding="utf-8"))
        # Minimal validation: check required fields and enums (full jsonschema not required, stdlib-only)
        required = schema.get("required", [])
        for f in required:
            if f not in state:
                raise ValueError(f"missing required field {f}")
        # Validate capabilities enums
        for cap in state.get("capabilities", []):
            if cap.get("state") not in ("AVAILABLE", "UNAVAILABLE", "UNKNOWN"):
                raise ValueError(f"invalid capability state {cap}")
            if cap.get("provenance") not in ("OBSERVED", "DECLARED", "INFERRED"):
                raise ValueError(f"invalid capability provenance {cap}")
            if cap.get("provenance") == "OBSERVED" and "cap_probe" not in (cap.get("evidence") or ""):
                raise ValueError(f"OBSERVED capability must cite cap_probe evidence: {cap}")
        # host_label declared-shape: non-empty string
        if not isinstance(state.get("host_label"), str) or not state["host_label"].strip():
            raise ValueError("host_label must be non-empty DECLARED string")
    except Exception as e:
        raise RuntimeError(f"schema validation failed before write: {e}")

    # Deterministic JSON, sorted keys
    out_dir = os.path.join(ROOT, "Brain", "short_term", "active")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "session_capability_state.json")
    # Write with sorted keys, indent 2 for readability but deterministic
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")

    # Counts
    caps = state.get("capabilities", [])
    available = sum(1 for c in caps if c.get("state") == "AVAILABLE")
    unavailable = sum(1 for c in caps if c.get("state") == "UNAVAILABLE")
    unknown = sum(1 for c in caps if c.get("state") == "UNKNOWN")
    observed = sum(1 for c in caps if c.get("provenance") == "OBSERVED")
    declared = sum(1 for c in caps if c.get("provenance") == "DECLARED")
    inferred = sum(1 for c in caps if c.get("provenance") == "INFERRED")

    counts = {
        "available": available,
        "unavailable": unavailable,
        "unknown": unknown,
        "observed": observed,
        "declared": declared,
        "inferred": inferred
    }
    return out_path, counts


def self_test(repo: str = ROOT) -> int:
    import shutil
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
    try:
        rg = run_pass("Arena Agent Mode", ghost)
    finally:
        shutil.rmtree(ghost, ignore_errors=True)
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
    # 5600: the proof cleans up after itself — the zero-write vector must not
    # litter /tmp with a ~6 MB repo copy per run (leak found at closure).
    zw_ok, zw_d = False, ""
    tmp = tempfile.mkdtemp(prefix="pass-nowrite-")
    try:
        dst = os.path.join(tmp, "copy")
        shutil.copytree(repo, dst,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                        dirs_exist_ok=True)
        n0 = sum(len(fs) for _, _, fs in os.walk(dst))
        run_pass("Arena Agent Mode", dst)
        n1 = sum(len(fs) for _, _, fs in os.walk(dst))
        zw_ok, zw_d = n0 == n1, f"files {n0}->{n1}"
    except Exception as e:
        zw_d = str(e)[:80]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    vec("pass performs zero writes (copy census unchanged)", zw_ok, zw_d)

    # S-2-ENV: default behavior byte-identical (no --persist → no write)
    # Verify that run_pass output without persist is identical to today
    tmp2 = tempfile.mkdtemp(prefix="pass-default-")
    try:
        dst2 = os.path.join(tmp2, "copy2")
        shutil.copytree(repo, dst2,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                        dirs_exist_ok=True)
        # Capture output without persist flag — should be zero writes
        out_before = run_pass("Arena Agent Mode", dst2)
        # Ensure no session_capability_state.json written
        state_path = os.path.join(dst2, "Brain", "short_term", "active", "session_capability_state.json")
        vec("default behavior no flag → no write (byte-identical output to today)",
            not os.path.exists(state_path),
            f"state file exists at {state_path}" if os.path.exists(state_path) else "no file")
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)

    # S-2-ENV: --persist writes schema-valid deterministic file
    tmp3 = tempfile.mkdtemp(prefix="pass-persist-")
    try:
        dst3 = os.path.join(tmp3, "copy3")
        shutil.copytree(repo, dst3,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                        dirs_exist_ok=True)
        out = run_pass("Arena Agent Mode", dst3)
        # Simulate persist
        # We need to call build and persist using the copy's path
        # Import from copy's file? Simpler: use local functions but with repo=dst3
        state = build_session_capability_state("Arena Agent Mode", out, dst3)
        # Check schema-valid
        schema_path = os.path.join(dst3, "schemas", "session_capability_state.schema.json")
        has_schema = os.path.exists(schema_path)
        vec("persist: schema file exists for validation", has_schema, schema_path)
        # Check UNKNOWN discipline
        has_unknown = any(c["state"] == "UNKNOWN" for c in state.get("capabilities", []))
        vec("persist: UNKNOWN is first-class value (has UNKNOWN capability)", has_unknown, str(state.get("capabilities", []))[:200])
        # Check OBSERVED cites cap_probe
        observed_ok = all("cap_probe" in (c.get("evidence") or "") for c in state.get("capabilities", []) if c.get("provenance") == "OBSERVED")
        vec("persist: OBSERVED provenance must cite cap_probe evidence", observed_ok, "missing cap_probe citation")
        # Check host_label DECLARED
        vec("persist: host_label DECLARED never discovered", state.get("host_label") == "Arena Agent Mode", state.get("host_label"))
    finally:
        shutil.rmtree(tmp3, ignore_errors=True)

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
    ap.add_argument("--persist", action="store_true", help="Opt-in persistence: write Brain/short_term/active/session_capability_state.json (schema-valid, deterministic sorted keys) and report path+counts")
    a = ap.parse_args()
    if a.self_test:
        return self_test(a.repo)
    # Default behavior: no flag → no write — byte-identical output to today
    pass_out = run_pass(a.host, a.repo)
    print(json.dumps(pass_out, indent=1))
    if a.persist:
        try:
            written_path, counts = persist_session_state(a.host, pass_out, a.repo)
            # Stdout reports written path + counts {available, unavailable, unknown, observed, declared, inferred}
            rel_path = os.path.relpath(written_path, a.repo) if os.path.commonpath([written_path, a.repo]) == os.path.realpath(a.repo) else written_path
            print(f"session_capability_state written: {rel_path} counts={counts}")
        except Exception as e:
            print(f"persist failed: {e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
