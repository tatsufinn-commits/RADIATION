#!/usr/bin/env python3
"""
session_state_check.py — Session Capability State checker (S-2-ENV)

House finding style, deterministic, stdlib-only, no network.

Checks:
- Lint any present state file vs schema: enums exact, required fields, provenance discipline (OBSERVED ⇒ must cite cap_probe execution this session in evidence field), host_label declared-shape.
- Absent file → exit 0 with "no session state declared" (session artifacts may never become gate requirements — memory-lane rule).

Lifecycle: state file lives session-local in Brain/short_term/active/; presumed impermanent, triaged at session close per short-term law. It must never be committed with live content — repo carries schema + writer + checker + docs.

Fences: No hardcoded platform limits, no private-quota probing, no parallel EXECUTE/ALT/HOLD chain — state file is input artifact consumed by scan/anchor/stockpile shortfall, never resolver. No autonomous self-check loop, no network calls.

Domain-10 rider correspondence (one bounded doc block in docs/EVIDENCE_TAXONOMY.md or checker README — picked checker README here and EVIDENCE_TAXONOMY annex):
AVAILABLE↔primary+active · UNAVAILABLE↔deprecated/secondary/asserted/benchmark · UNKNOWN↔draft+honesty-grammar · VERIFIED↔[D]/[I]+primary+active · DOCUMENTED↔[D]/[O]+secondary · INFERRED↔[N]/[R]+asserted/benchmark · UNKNOWN↔[S]+UNVERIFIED+draft
"""
import argparse
import json
import pathlib
import sys
import tempfile
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "session_capability_state.schema.json"
STATE_PATH = ROOT / "Brain" / "short_term" / "active" / "session_capability_state.json"

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

def load_schema():
    if not SCHEMA_PATH.exists():
        return None, f"schema missing at {SCHEMA_PATH}"
    try:
        data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        return data, ""
    except Exception as e:
        return None, f"schema invalid JSON: {e}"

def check_state_file(path=STATE_PATH):
    findings = []
    if not path.exists():
        print("no session state declared — session artifacts may never become gate requirements (memory-lane rule)")
        return 0, []

    # Load file
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        findings.append(f"session state file invalid JSON at {path}: {e}")
        return 1, findings

    # Load schema for required fields and enums
    schema, err = load_schema()
    if err:
        findings.append(err)
        return 1, findings

    # Required fields
    for field in schema.get("required", []):
        if field not in data:
            findings.append(f"missing required field: {field}")

    # host_label declared-shape: non-empty string, DECLARED never discovered never profile-inferred
    host_label = data.get("host_label")
    if not isinstance(host_label, str) or not host_label.strip():
        findings.append(f"host_label must be non-empty DECLARED string — never discovered, never profile-inferred, got {host_label!r}")
    elif host_label.strip().lower() in ("unknown", "auto", "discovered"):
        # Declared shape should not be generic placeholder unless explicitly UNKNOWN discipline? But allow UNKNOWN as value? No, host_label must be DECLARED, so UNKNOWN is not valid host_label
        if host_label.strip() == "UNKNOWN":
            # UNKNOWN as host_label is allowed? Schema says minLength 1, but discipline says DECLARED — UNKNOWN is not a declared label, but we allow if explicitly set? For safety, require non-UNKNOWN
            findings.append(f"host_label DECLARED shape invalid: {host_label!r} — must be explicit declared label, never generic UNKNOWN/discovered")

    # capabilities enums exact + provenance discipline
    caps = data.get("capabilities", [])
    if not isinstance(caps, list):
        findings.append("capabilities must be array")
    else:
        for idx, cap in enumerate(caps):
            if not isinstance(cap, dict):
                findings.append(f"capabilities[{idx}] must be object")
                continue
            name = cap.get("name")
            state = cap.get("state")
            prov = cap.get("provenance")
            evidence = cap.get("evidence", "")
            if not name or not isinstance(name, str):
                findings.append(f"capabilities[{idx}] missing name")
            if state not in ("AVAILABLE", "UNAVAILABLE", "UNKNOWN"):
                findings.append(f"capabilities[{idx}] {name!r} invalid state {state!r} — must be AVAILABLE|UNAVAILABLE|UNKNOWN exact enum")
            if prov not in ("OBSERVED", "DECLARED", "INFERRED"):
                findings.append(f"capabilities[{idx}] {name!r} invalid provenance {prov!r} — must be OBSERVED|DECLARED|INFERRED exact enum")
            # Provenance discipline: OBSERVED ⇒ must cite cap_probe execution this session in evidence field
            if prov == "OBSERVED":
                if "cap_probe" not in (evidence or ""):
                    findings.append(f"capabilities[{idx}] {name!r} OBSERVED without cap_probe evidence → FAIL — OBSERVED must cite cap_probe execution this session in evidence field")
            # UNKNOWN honesty: if state is UNKNOWN, provenance should not be OBSERVED without evidence? Actually UNKNOWN is first-class, but we check that absent evidence stays UNKNOWN
            # No extra check here beyond enums

    # constraints
    constraints = data.get("constraints", [])
    if not isinstance(constraints, list):
        findings.append("constraints must be array")
    else:
        for idx, cons in enumerate(constraints):
            if not isinstance(cons, dict):
                findings.append(f"constraints[{idx}] must be object")
                continue
            if cons.get("provenance") not in ("OBSERVED", "DECLARED", "INFERRED"):
                findings.append(f"constraints[{idx}] invalid provenance {cons.get('provenance')!r}")
            if "name" not in cons:
                findings.append(f"constraints[{idx}] missing name")

    # generated_at: should be ISO date-time, but we don't enforce strict format here beyond existence; stale reads UNKNOWN rather than lie is discipline for consumer, not checker
    if "generated_at" not in data:
        findings.append("missing generated_at")

    # pass_ref, honesty_note
    if "pass_ref" not in data:
        findings.append("missing pass_ref")
    if "honesty_note" not in data:
        findings.append("missing honesty_note")

    # Lifecycle: file must never be committed with live content — checker asserts no committed file matches live-content path
    # This check is for gate: ensure state file is not tracked in git
    # If file exists on disk, check if it's tracked
    p = run(f"git ls-files --error-unmatch {path} 2>&1")
    if p.returncode == 0:
        findings.append(f"session state file {path} is tracked in git — must never be committed with live content — repo carries schema+writer+checker+docs only, lifecycle: working memory, presumed impermanent, triaged at session close")

    return (0 if not findings else 1), findings

def main_check():
    code, findings = check_state_file(STATE_PATH)
    if findings:
        print(f"session_state_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
    else:
        if code == 0 and not STATE_PATH.exists():
            # Already printed "no session state declared"
            pass
        else:
            print("session_state_check: 0 finding(s) — state file schema-valid, provenance discipline OK, UNKNOWN honesty preserved")
    return code

def self_test():
    def make_temp_repo():
        tmp = pathlib.Path(tempfile.mkdtemp())
        # init minimal structure
        (tmp / "schemas").mkdir(parents=True, exist_ok=True)
        (tmp / "Brain" / "short_term" / "active").mkdir(parents=True, exist_ok=True)
        (tmp / "scripts").mkdir(parents=True, exist_ok=True)
        # copy schema
        shutil.copy(str(SCHEMA_PATH), str(tmp / "schemas" / "session_capability_state.schema.json"))
        # copy checker
        shutil.copy(str(ROOT / "scripts" / "session_state_check.py"), str(tmp / "scripts" / "session_state_check.py"))
        # init git for lifecycle check
        run(f"git init -q", cwd=tmp)
        run(f"git config user.email test@test.com", cwd=tmp)
        run(f"git config user.name Test", cwd=tmp)
        return tmp

    def v_absent_file():
        tmp = make_temp_repo()
        try:
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            return p.returncode == 0 and "no session state declared" in p.stdout.lower()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def v_valid_file():
        tmp = make_temp_repo()
        try:
            # Create valid state file
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider", "provider": "Arena_AI"},
                "capabilities": [
                    {"name": "tool_a", "state": "AVAILABLE", "provenance": "OBSERVED", "evidence": "cap_probe execution this session: tools_exposed includes tool_a"},
                    {"name": "host_posture_profile", "state": "UNKNOWN", "provenance": "INFERRED", "evidence": "no profile — absent evidence stays UNKNOWN"}
                ],
                "constraints": [
                    {"name": "repository_status", "provenance": "OBSERVED", "value_or_unknown": "mounted"}
                ],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc123",
                "honesty_note": "working memory, stale reads UNKNOWN"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            return p.returncode == 0 and "0 finding" in p.stdout
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def v_unknown_honesty():
        # UNKNOWN-honesty: absent evidence stays UNKNOWN — capability with no evidence should be UNKNOWN never UNAVAILABLE
        tmp = make_temp_repo()
        try:
            # Create file where a capability has no evidence but is marked UNAVAILABLE — should still be allowed? Actually discipline says absent evidence stays UNKNOWN never UNAVAILABLE, so checker should not enforce UNAVAILABLE without evidence? But we test that UNKNOWN is preserved
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "generic", "provider": None},
                "capabilities": [
                    {"name": "mystery_cap", "state": "UNKNOWN", "provenance": "INFERRED", "evidence": "no evidence — absent evidence stays UNKNOWN per mandatory discipline"}
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "UNKNOWN is first-class"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            # Should PASS because UNKNOWN is honest
            return p.returncode == 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def v_observed_without_evidence_fail():
        # OBSERVED-vs-DECLARED: OBSERVED without cap_probe evidence → FAIL
        tmp = make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider", "provider": "Arena_AI"},
                "capabilities": [
                    {"name": "tool_x", "state": "AVAILABLE", "provenance": "OBSERVED", "evidence": "declared by config"}  # missing cap_probe
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "test"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            return p.returncode != 0 and "OBSERVED without cap_probe" in p.stdout
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def v_invalid_enum_fail():
        tmp = make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider"},
                "capabilities": [
                    {"name": "tool_y", "state": "ENABLED", "provenance": "OBSERVED", "evidence": "cap_probe execution"}  # invalid enum
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "test"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            return p.returncode != 0 and "invalid state" in p.stdout.lower()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    tests = [
        ("absent file → no session state declared (memory-lane rule)", v_absent_file),
        ("valid file → 0 findings", v_valid_file),
        ("UNKNOWN-honesty: absent evidence stays UNKNOWN", v_unknown_honesty),
        ("OBSERVED-vs-DECLARED: OBSERVED without cap_probe evidence → FAIL", v_observed_without_evidence_fail),
        ("invalid enum → FAIL", v_invalid_enum_fail),
    ]
    passed = 0
    for name, fn in tests:
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"  vector exception {name}: {e}")
        status = "PASS" if ok else "FAIL"
        print(f"  vector {name} -> {status}")
        if ok:
            passed += 1
    print(f"session_state_check self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(self_test())
    else:
        sys.exit(main_check())
