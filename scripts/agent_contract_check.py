#!/usr/bin/env python3
"""
agent_contract_check.py — deterministic compile check for agent contracts catalog (Dim-1/G4)

Checks (house finding style, exit 0/1):
- catalog valid vs schema (radiation.agent_contract/1)
- profile_ref resolves (agents/<X>/CAPABILITY_PROFILE.md must exist)
- tier enum valid (primary|secondary|asserted|benchmark)
- no_simulated_commander_authority not exactly-true → FAIL (D4 law)
- unique ids
- status discipline (draft→note; deprecated→superseded_by)
- claim ≤200, provider non-empty, boundary_note non-empty, tests[] array, authority object
- tests[] entries resolve if they look like paths

--self-test ≥4 vectors:
- repo passes
- broken profile_ref → FAIL
- unknown tier → FAIL
- simulated-authority (no_simulated_commander_authority false) → FAIL
Plus: duplicate id, draft missing note, deprecated missing superseded_by, claim too long, missing authority

Stdlib only, deterministic, no network.
"""

import json
import os
import re
import sys
import pathlib
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTRACTS_DIR = ROOT / "agents" / "contracts"
SCHEMA_PATH = ROOT / "schemas" / "agent_contract.schema.json"

ID_PATTERN = re.compile(r"^AGT-[a-z0-9-]+$")
PROFILE_REF_PATTERN = re.compile(r"^agents/[A-Za-z0-9_]+/CAPABILITY_PROFILE\.md$")
TIER_ENUM = {"primary", "secondary", "asserted", "benchmark"}
STATUS_ENUM = {"active", "draft", "deprecated"}

def load_json(path):
    if not path.exists():
        return None, [f"file missing: {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"unparseable JSON {path}: {e}"]
    return data, []

def validate_contract_schema(entry, idx):
    errors = []
    required = ["id", "provider", "profile_ref", "capabilities", "boundary_note", "authority", "status", "tests"]
    for field in required:
        if field not in entry:
            errors.append(f"[{idx}] missing required field '{field}'")
    if errors:
        return errors

    cid = entry.get("id", f"idx-{idx}")
    if not isinstance(cid, str) or not ID_PATTERN.match(cid):
        errors.append(f"[{cid}] id pattern mismatch '{cid}' must match {ID_PATTERN.pattern}")

    provider = entry.get("provider", "")
    if not isinstance(provider, str) or not provider.strip():
        errors.append(f"[{cid}] provider must be non-empty")

    profile_ref = entry.get("profile_ref", "")
    if not isinstance(profile_ref, str) or not PROFILE_REF_PATTERN.match(profile_ref):
        errors.append(f"[{cid}] profile_ref pattern mismatch '{profile_ref}' must match {PROFILE_REF_PATTERN.pattern}")

    caps = entry.get("capabilities")
    if not isinstance(caps, list) or len(caps) < 1:
        errors.append(f"[{cid}] capabilities must be array minItems 1")
    else:
        for c_idx, cap in enumerate(caps):
            if not isinstance(cap, dict):
                errors.append(f"[{cid}] capabilities[{c_idx}] must be object")
                continue
            claim = cap.get("claim")
            if not isinstance(claim, str) or not claim.strip():
                errors.append(f"[{cid}] capabilities[{c_idx}] claim must be non-empty")
            elif len(claim) > 200:
                errors.append(f"[{cid}] capabilities[{c_idx}] claim length {len(claim)} exceeds 200")

            tier = cap.get("tier")
            if tier not in TIER_ENUM:
                errors.append(f"[{cid}] capabilities[{c_idx}] tier enum mismatch '{tier}' not in {TIER_ENUM}")

            if "receipt_ref" not in cap:
                errors.append(f"[{cid}] capabilities[{c_idx}] missing receipt_ref")
            else:
                rr = cap["receipt_ref"]
                if not (isinstance(rr, str) or rr is None):
                    errors.append(f"[{cid}] capabilities[{c_idx}] receipt_ref must be string or null")

    boundary = entry.get("boundary_note", "")
    if not isinstance(boundary, str) or not boundary.strip():
        errors.append(f"[{cid}] boundary_note must be non-empty")

    authority = entry.get("authority")
    if not isinstance(authority, dict):
        errors.append(f"[{cid}] authority must be object")
    else:
        if "no_simulated_commander_authority" not in authority:
            errors.append(f"[{cid}] authority missing no_simulated_commander_authority")
        else:
            val = authority["no_simulated_commander_authority"]
            if val is not True:
                errors.append(f"[{cid}] authority.no_simulated_commander_authority must be exactly true (D4) — false impossible")

    status = entry.get("status")
    if status not in STATUS_ENUM:
        errors.append(f"[{cid}] status enum mismatch '{status}' not in {STATUS_ENUM}")

    tests = entry.get("tests")
    if not isinstance(tests, list) or not all(isinstance(t, str) for t in tests):
        errors.append(f"[{cid}] tests must be array of strings")

    if status == "draft" and "note" not in entry:
        errors.append(f"[{cid}] draft status must carry note")
    if status == "deprecated" and "superseded_by" not in entry:
        errors.append(f"[{cid}] deprecated status must carry superseded_by")
    if status == "deprecated" and "superseded_by" in entry:
        sb = entry["superseded_by"]
        if not isinstance(sb, str) or not ID_PATTERN.match(sb):
            errors.append(f"[{cid}] superseded_by pattern mismatch '{sb}' must match {ID_PATTERN.pattern}")

    allowed = {"id", "provider", "profile_ref", "capabilities", "boundary_note", "authority", "status", "tests", "note", "superseded_by"}
    for k in entry.keys():
        if k not in allowed:
            errors.append(f"[{cid}] additional property '{k}' not allowed")

    return errors

def check_contracts(contracts_dir=CONTRACTS_DIR, root=ROOT):
    findings = []

    if not contracts_dir.exists():
        findings.append(f"contracts directory missing: {contracts_dir.relative_to(root).as_posix() if contracts_dir.is_relative_to(root) else str(contracts_dir)}")
        return findings

    files = sorted(contracts_dir.glob("AGT-*.json"))
    if len(files) == 0:
        findings.append(f"no contracts found in {contracts_dir}")
        return findings

    seen_ids = set()
    for fpath in files:
        data, errs = load_json(fpath)
        if errs:
            findings.extend([f"{fpath.relative_to(root).as_posix()}: {e}" for e in errs])
            continue
        if not isinstance(data, dict):
            findings.append(f"{fpath.relative_to(root).as_posix()}: contract must be object")
            continue

        idx = fpath.name
        errs = validate_contract_schema(data, idx)
        for e in errs:
            findings.append(f"{fpath.relative_to(root).as_posix()}: schema violation: {e}")

        cid = data.get("id")
        if cid in seen_ids:
            findings.append(f"duplicate id '{cid}'")
        if cid:
            seen_ids.add(cid)

        # profile_ref resolves
        pr = data.get("profile_ref")
        if isinstance(pr, str) and pr.strip():
            pr_path = root / pr
            if not pr_path.exists():
                findings.append(f"{cid or fpath.name}: profile_ref does not resolve: '{pr}'")

        # tests[] resolve if they look like paths (contain /)
        tests = data.get("tests", [])
        if isinstance(tests, list):
            for t in tests:
                if isinstance(t, str) and "/" in t:
                    tp = root / t
                    if not tp.exists():
                        findings.append(f"{cid or fpath.name}: tests entry does not resolve: '{t}'")

    # At least 5 contracts expected (one per provider)
    if len(files) < 5:
        findings.append(f"catalog must have ≥5 contracts or all found, got {len(files)}")

    return findings

# ---------------- self-test vectors ----------------

def self_test():
    """
    ≥4 vectors: repo passes · broken profile_ref → FAIL · unknown tier → FAIL · simulated-authority → FAIL
    Plus: duplicate id, draft missing note, deprecated missing superseded_by, claim too long
    """
    def run_in_temp(temp_root: pathlib.Path, contracts):
        (temp_root / "agents" / "contracts").mkdir(parents=True, exist_ok=True)
        (temp_root / "schemas").mkdir(parents=True, exist_ok=True)
        # copy schema
        src_schema = ROOT / "schemas" / "agent_contract.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, temp_root / "schemas" / "agent_contract.schema.json")
        # create dummy profiles for valid refs (skip intentionally broken ones containing MISSING)
        for contract in contracts:
            pr = contract.get("profile_ref")
            if pr and "MISSING" not in pr:
                pr_path = temp_root / pr
                pr_path.parent.mkdir(parents=True, exist_ok=True)
                if not pr_path.exists():
                    pr_path.write_text("# dummy profile\n", encoding="utf-8")
            # create tests files if needed
            for t in contract.get("tests", []):
                if "/" in t:
                    tp = temp_root / t
                    tp.parent.mkdir(parents=True, exist_ok=True)
                    if not tp.exists():
                        tp.write_text("# test\n", encoding="utf-8")
        # write contracts - use index to preserve duplicate ids as separate files
        for idx, contract in enumerate(contracts):
            cid = contract.get("id", f"AGT-test-{idx}")
            # Use unique filename but keep id inside JSON same to test duplicate detection
            cpath = temp_root / "agents" / "contracts" / f"AGT-{idx:03d}-{cid}.json"
            # Ensure filename matches AGT-*.json pattern required by checker glob
            # The checker globs AGT-*.json, so we keep prefix AGT-
            # Our filename AGT-000-AGT-dup.json matches AGT-*.json, ok
            cpath.write_text(json.dumps(contract), encoding="utf-8")
        findings = check_contracts(contracts_dir=temp_root / "agents" / "contracts", root=temp_root)
        return findings

    def make_contract(cid="AGT-test", provider="Test", profile_ref="agents/Arena_AI/CAPABILITY_PROFILE.md", tier="primary", claim="Test capability claim valid", receipt_ref="O10", authority_true=True, status="active", extra=None, capabilities_override=None):
        if capabilities_override is not None:
            caps = capabilities_override
        else:
            caps = [{"claim": claim, "tier": tier, "receipt_ref": receipt_ref}]
        base = {
            "id": cid,
            "provider": provider,
            "profile_ref": profile_ref,
            "capabilities": caps,
            "boundary_note": "Host session-contingent; model identity unknowable; tool surface session-specific; canonical_apply outside agent runtime II.11",
            "authority": {"no_simulated_commander_authority": authority_true},
            "status": status,
            "tests": ["tests/test_agent_contract_check.py"]
        }
        if extra:
            base.update(extra)
        return base

    def vector_repo_passes():
        findings = check_contracts()
        ok = len(findings) == 0
        return ok, findings

    def make_valid_set(base_contracts):
        """Ensure at least 5 contracts total to satisfy catalog size check."""
        # base_contracts is list of contracts that include the failing one
        # If less than 5, pad with valid dummies
        valid_needed = max(0, 5 - len(base_contracts))
        dummies = []
        for i in range(valid_needed):
            dummies.append(make_contract(cid=f"AGT-dummy-{i+100}", provider=f"Dummy{i}", profile_ref=f"agents/Dummy{i+100}/CAPABILITY_PROFILE.md"))
        return base_contracts + dummies

    def vector_broken_profile_ref():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            contract = make_contract(cid="AGT-broken-ref", profile_ref="agents/MISSING/CAPABILITY_PROFILE.md")
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("profile_ref does not resolve" in f for f in findings)
            return ok, findings

    def vector_unknown_tier():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            contract = make_contract(cid="AGT-bad-tier", tier="superprimary")
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("tier enum" in f for f in findings)
            return ok, findings

    def vector_simulated_authority():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            contract = make_contract(cid="AGT-bad-auth", authority_true=False)
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("no_simulated_commander_authority" in f and "exactly true" in f for f in findings)
            return ok, findings

    def vector_duplicate_id():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            c1 = make_contract(cid="AGT-dup")
            c2 = make_contract(cid="AGT-dup")
            all_contracts = make_valid_set([c1, c2])
            findings = run_in_temp(tr, all_contracts)
            ok = any("duplicate id" in f for f in findings)
            return ok, findings

    def vector_draft_missing_note():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            contract = make_contract(cid="AGT-draft", status="draft")
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("draft" in f and "note" in f for f in findings)
            return ok, findings

    def vector_deprecated_missing_superseded():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            contract = make_contract(cid="AGT-depr", status="deprecated")
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("deprecated" in f and "superseded_by" in f for f in findings)
            return ok, findings

    def vector_claim_too_long():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            long_claim = "x" * 201
            contract = make_contract(cid="AGT-long", claim=long_claim)
            all_contracts = make_valid_set([contract])
            findings = run_in_temp(tr, all_contracts)
            ok = any("exceeds 200" in f for f in findings)
            return ok, findings

    tests = [
        ("repo passes (positive)", vector_repo_passes),
        ("broken profile_ref → FAIL", vector_broken_profile_ref),
        ("unknown tier → FAIL", vector_unknown_tier),
        ("simulated-authority false → FAIL", vector_simulated_authority),
        ("duplicate id → FAIL", vector_duplicate_id),
        ("draft missing note → FAIL", vector_draft_missing_note),
        ("deprecated missing superseded_by → FAIL", vector_deprecated_missing_superseded),
        ("claim too long → FAIL", vector_claim_too_long),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        ok, findings = fn()
        if ok:
            print(f"  ✅ self-test vector PASS: {name}")
            passed += 1
        else:
            print(f"  ❌ self-test vector FAIL: {name} — findings: {findings}")
            failed += 1

    print(f"\nagent_contract_check self-test: {passed} passed, {failed} failed — {len(tests)} vectors")
    return failed == 0

def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    findings = check_contracts()
    if findings:
        print(f"agent_contract_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("agent_contract_check: 0 finding(s) — catalog valid, profile_ref resolves, tier enum valid, authority D4 ok, unique ids, status discipline ok")
        sys.exit(0)

if __name__ == "__main__":
    main()
