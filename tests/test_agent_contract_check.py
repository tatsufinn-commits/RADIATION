#!/usr/bin/env python3
"""
test_agent_contract_check.py — ≥4 vectors for agent contracts catalog (Dim-1/G4)

Vectors:
- repo passes
- broken profile_ref → FAIL
- unknown tier → FAIL
- simulated-authority (no_simulated_commander_authority false) → FAIL
Plus self-test ran.

Discover 130 + yours OK.
"""

import json
import pathlib
import tempfile
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from agent_contract_check import check_contracts

def test_repo_passes():
    findings = check_contracts()
    assert len(findings) == 0, f"repo should pass, got findings: {findings}"

def test_broken_profile_ref():
    with tempfile.TemporaryDirectory() as td:
        tr = pathlib.Path(td)
        (tr / "agents" / "contracts").mkdir(parents=True, exist_ok=True)
        (tr / "schemas").mkdir(parents=True, exist_ok=True)
        src_schema = ROOT / "schemas" / "agent_contract.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, tr / "schemas" / "agent_contract.schema.json")
        # valid contracts to meet ≥5 count
        def make_valid(cid, provider, profile):
            return {
                "id": cid,
                "provider": provider,
                "profile_ref": profile,
                "capabilities": [{"claim": "Test claim valid", "tier": "primary", "receipt_ref": "O10"}],
                "boundary_note": "Host session-contingent; model identity unknowable; canonical_apply outside II.11",
                "authority": {"no_simulated_commander_authority": True},
                "status": "active",
                "tests": []
            }
        # create 4 valid dummy profiles
        for i in range(1, 5):
            pr = f"agents/Dummy{i}/CAPABILITY_PROFILE.md"
            pr_path = tr / pr
            pr_path.parent.mkdir(parents=True, exist_ok=True)
            pr_path.write_text("# dummy\n", encoding="utf-8")
        # broken one
        broken = make_valid("AGT-broken-ref", "Broken", "agents/MISSING/CAPABILITY_PROFILE.md")
        contracts = []
        for i in range(1, 5):
            contracts.append(make_valid(f"AGT-dummy-{i}", f"Dummy{i}", f"agents/Dummy{i}/CAPABILITY_PROFILE.md"))
        contracts.append(broken)
        for c in contracts:
            (tr / "agents" / "contracts" / f"{c['id']}.json").write_text(json.dumps(c), encoding="utf-8")
        findings = check_contracts(contracts_dir=tr / "agents" / "contracts", root=tr)
        assert any("profile_ref does not resolve" in f for f in findings), f"should detect broken profile_ref, got {findings}"

def test_unknown_tier():
    with tempfile.TemporaryDirectory() as td:
        tr = pathlib.Path(td)
        (tr / "agents" / "contracts").mkdir(parents=True, exist_ok=True)
        (tr / "schemas").mkdir(parents=True, exist_ok=True)
        src_schema = ROOT / "schemas" / "agent_contract.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, tr / "schemas" / "agent_contract.schema.json")
        def make_valid(cid, tier="primary"):
            pr = f"agents/Dummy{cid}/CAPABILITY_PROFILE.md"
            pr_path = tr / pr
            pr_path.parent.mkdir(parents=True, exist_ok=True)
            pr_path.write_text("# dummy\n", encoding="utf-8")
            return {
                "id": cid,
                "provider": "Dummy",
                "profile_ref": pr,
                "capabilities": [{"claim": "Test claim", "tier": tier, "receipt_ref": None}],
                "boundary_note": "Host session-contingent",
                "authority": {"no_simulated_commander_authority": True},
                "status": "active",
                "tests": []
            }
        contracts = [make_valid(f"AGT-dummy-{i}") for i in range(1, 5)]
        bad = make_valid("AGT-bad-tier", tier="superprimary")
        contracts.append(bad)
        for c in contracts:
            (tr / "agents" / "contracts" / f"{c['id']}.json").write_text(json.dumps(c), encoding="utf-8")
        findings = check_contracts(contracts_dir=tr / "agents" / "contracts", root=tr)
        assert any("tier enum" in f for f in findings), f"should detect unknown tier, got {findings}"

def test_simulated_authority():
    with tempfile.TemporaryDirectory() as td:
        tr = pathlib.Path(td)
        (tr / "agents" / "contracts").mkdir(parents=True, exist_ok=True)
        (tr / "schemas").mkdir(parents=True, exist_ok=True)
        src_schema = ROOT / "schemas" / "agent_contract.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, tr / "schemas" / "agent_contract.schema.json")
        def make_valid(cid, auth_true=True):
            pr = f"agents/Dummy{cid}/CAPABILITY_PROFILE.md"
            pr_path = tr / pr
            pr_path.parent.mkdir(parents=True, exist_ok=True)
            pr_path.write_text("# dummy\n", encoding="utf-8")
            return {
                "id": cid,
                "provider": "Dummy",
                "profile_ref": pr,
                "capabilities": [{"claim": "Test claim", "tier": "primary", "receipt_ref": None}],
                "boundary_note": "Host session-contingent",
                "authority": {"no_simulated_commander_authority": auth_true},
                "status": "active",
                "tests": []
            }
        contracts = [make_valid(f"AGT-dummy-{i}") for i in range(1, 5)]
        bad = make_valid("AGT-bad-auth", auth_true=False)
        contracts.append(bad)
        for c in contracts:
            (tr / "agents" / "contracts" / f"{c['id']}.json").write_text(json.dumps(c), encoding="utf-8")
        findings = check_contracts(contracts_dir=tr / "agents" / "contracts", root=tr)
        assert any("no_simulated_commander_authority" in f for f in findings), f"should detect simulated authority false, got {findings}"

def test_self_test_ran():
    # Ensure the checker's self-test passes
    import subprocess
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "agent_contract_check.py"), "--self-test"], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"self-test should pass: {result.stdout}\n{result.stderr}"
    assert "8 passed" in result.stdout, f"self-test should show 8 passed, got {result.stdout}"

if __name__ == "__main__":
    test_repo_passes()
    test_broken_profile_ref()
    test_unknown_tier()
    test_simulated_authority()
    test_self_test_ran()
    print("tests/test_agent_contract_check.py: 5 vectors PASS")
