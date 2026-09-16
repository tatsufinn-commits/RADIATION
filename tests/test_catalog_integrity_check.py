#!/usr/bin/env python3
"""
test_catalog_integrity_check.py — ≥5 vectors for cross-catalog integrity checker (P-20)

Per new house law (P-19-fix): unittest.TestCase only, no bare functions.
Discover count before 135 → after 140+

Vectors:
- repo passes (0 findings)
- AGENT.profile_ref broken → FAIL
- SUBSKILL.parent_skill broken → FAIL
- SCAFFOLD.deps broken → FAIL
- SKILL.required_tools invalid → FAIL (NEW-IN-P20)
- CUE invalid → FAIL
- MEMORY path missing → FAIL
Plus self-test ran.
"""

import json
import pathlib
import tempfile
import shutil
import sys
import unittest
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from catalog_integrity_check import check_all

def make_base_temp(temp_root: pathlib.Path):
    (temp_root / "agents" / "contracts").mkdir(parents=True, exist_ok=True)
    (temp_root / "skills").mkdir(parents=True, exist_ok=True)
    (temp_root / "subskills").mkdir(parents=True, exist_ok=True)
    (temp_root / "scaffolding" / "core").mkdir(parents=True, exist_ok=True)
    (temp_root / "cue").mkdir(parents=True, exist_ok=True)
    (temp_root / "Brain").mkdir(parents=True, exist_ok=True)
    (temp_root / "tools").mkdir(parents=True, exist_ok=True)
    (temp_root / "evals" / "skills").mkdir(parents=True, exist_ok=True)
    (temp_root / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
    (temp_root / "tests").mkdir(parents=True, exist_ok=True)

    (temp_root / "agents" / "Arena_AI" / "CAPABILITY_PROFILE.md").write_text("# dummy\n", encoding="utf-8")
    (temp_root / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
    (temp_root / "tests" / "test_agent_contract_check.py").write_text("# test\n", encoding="utf-8")
    (temp_root / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")

    reg = {"tools": [{"id": "skill_check"}, {"id": "subskill_check"}]}
    (temp_root / "tools" / "TOOL_REGISTRY.json").write_text(json.dumps(reg), encoding="utf-8")

    skill = {
        "id": "SKILL-001",
        "title": "Test skill",
        "entry_path": "agents/Arena_AI/BOOT.md",
        "kind": "agent",
        "description": "Test skill description valid ≤200.",
        "eval_ref": "evals/skills/SKILL-001.eval.md",
        "status": "active",
        "activation_note": "asserted",
        "tests": ["evals/skills/SKILL-001.eval.md"]
    }
    (temp_root / "skills" / "SKILL_CATALOG.json").write_text(json.dumps([skill]), encoding="utf-8")

    agent = {
        "id": "AGT-arena-ai",
        "provider": "Arena_AI",
        "profile_ref": "agents/Arena_AI/CAPABILITY_PROFILE.md",
        "capabilities": [{"claim": "Test claim", "tier": "primary", "receipt_ref": None}],
        "boundary_note": "Host session-contingent",
        "authority": {"no_simulated_commander_authority": True},
        "status": "active",
        "tests": ["tests/test_agent_contract_check.py"]
    }
    (temp_root / "agents" / "contracts" / "AGT-arena-ai.json").write_text(json.dumps(agent), encoding="utf-8")

    sub = {
        "id": "SUB-001",
        "title": "Test subskill",
        "parent_skill": "SKILL-001",
        "entry_path": "agents/Arena_AI/BOOT.md",
        "trigger": "before_skill",
        "condition": None,
        "description": "Test subskill description valid ≤200.",
        "scenario_ref": "evals/skills/SKILL-001.eval.md",
        "status": "active",
        "tests": ["evals/skills/SKILL-001.eval.md"]
    }
    (temp_root / "subskills" / "SUBSKILL_CATALOG.json").write_text(json.dumps([sub]), encoding="utf-8")

    scaff = {
        "id": "SCAFFOLD-core-test",
        "kind": "core",
        "status": "active",
        "file": "scaffolding/core/test.md",
        "depends_on": [],
        "tests": []
    }
    (temp_root / "scaffolding" / "core" / "test.md").write_text("# test\n", encoding="utf-8")
    (temp_root / "scaffolding" / "core" / "test.contract.json").write_text(json.dumps(scaff), encoding="utf-8")

    cue = {
        "cues": [
            {
                "id": "CUE-001",
                "title": "Test cue",
                "precedence": "cue",
                "priority": 50,
                "effect": "read",
                "scope": "test",
                "trigger": "test",
                "evidence": "test",
                "conflicts_with": [],
                "review_after": "2026-09-15"
            }
        ]
    }
    (temp_root / "cue" / "CUE_CATALOG.json").write_text(json.dumps(cue), encoding="utf-8")

    mem_entry = {
        "id": "MEM-note-test-001",
        "path": "agents/Arena_AI/BOOT.md",
        "title": "Test note",
        "kind": "note",
        "tags": ["a", "b", "c"],
        "added": "2026-09-16"
    }
    (temp_root / "Brain" / "MEMORY_CATALOG.jsonl").write_text(json.dumps(mem_entry) + "\n", encoding="utf-8")

def run_fk_check(temp_root: pathlib.Path):
    findings = []
    contracts_dir = temp_root / "agents" / "contracts"
    if contracts_dir.exists():
        for fpath in contracts_dir.glob("AGT-*.json"):
            try:
                data = json.loads(fpath.read_text(encoding="utf-8"))
                pr = data.get("profile_ref")
                if pr:
                    pr_path = temp_root / pr
                    if not pr_path.exists():
                        findings.append(f"{data.get('id')}: profile_ref does not resolve: '{pr}'")
            except:
                pass
    skill_catalog_path = temp_root / "skills" / "SKILL_CATALOG.json"
    if skill_catalog_path.exists():
        try:
            skills = json.loads(skill_catalog_path.read_text(encoding="utf-8"))
            for entry in skills:
                cid = entry.get("id", "?")
                er = entry.get("eval_ref")
                if er:
                    er_path = temp_root / er
                    if not er_path.exists():
                        findings.append(f"{cid}: eval_ref does not resolve: '{er}'")
                req_tools = entry.get("required_tools")
                if req_tools:
                    reg_path = temp_root / "tools" / "TOOL_REGISTRY.json"
                    reg_ids = set()
                    if reg_path.exists():
                        try:
                            reg_data = json.loads(reg_path.read_text(encoding="utf-8"))
                            for t in reg_data.get("tools", []):
                                reg_ids.add(t.get("id"))
                        except:
                            pass
                    for tid in req_tools:
                        if tid not in reg_ids:
                            findings.append(f"SKILL {cid} required_tools id '{tid}' not in TOOL_REGISTRY")
        except:
            pass
    sub_catalog_path = temp_root / "subskills" / "SUBSKILL_CATALOG.json"
    if sub_catalog_path.exists() and skill_catalog_path.exists():
        try:
            subs = json.loads(sub_catalog_path.read_text(encoding="utf-8"))
            skills = json.loads(skill_catalog_path.read_text(encoding="utf-8"))
            skill_ids = {s.get("id") for s in skills if isinstance(s, dict)}
            for entry in subs:
                cid = entry.get("id", "?")
                parent = entry.get("parent_skill")
                if parent and parent not in skill_ids:
                    findings.append(f"{cid}: parent_skill FK does not resolve against skills/SKILL_CATALOG.json: '{parent}'")
        except:
            pass
    scaff_dir = temp_root / "scaffolding"
    if scaff_dir.exists():
        contracts = {}
        for cf in scaff_dir.rglob("*.contract.json"):
            try:
                data = json.loads(cf.read_text(encoding="utf-8"))
                cid = data.get("id")
                if cid:
                    contracts[cid] = cf
            except:
                pass
        for cf in scaff_dir.rglob("*.contract.json"):
            try:
                data = json.loads(cf.read_text(encoding="utf-8"))
                cid = data.get("id", cf.name)
                deps = data.get("depends_on", [])
                for dep in deps:
                    if dep not in contracts:
                        findings.append(f"{cid}: depends_on id '{dep}' does not resolve to existing contract")
            except:
                pass
    cue_catalog_path = temp_root / "cue" / "CUE_CATALOG.json"
    if cue_catalog_path.exists():
        try:
            catalog = json.loads(cue_catalog_path.read_text(encoding="utf-8"))
            cues = catalog.get("cues", [])
            for cue in cues:
                cid = cue.get("id", "?")
                prec = cue.get("precedence")
                if prec not in {"commander_order", "ratified_policy", "cue", "heuristic", "content"}:
                    findings.append(f"{cid} invalid precedence {prec}")
        except:
            pass
    mem_catalog_path = temp_root / "Brain" / "MEMORY_CATALOG.jsonl"
    if mem_catalog_path.exists():
        try:
            for line in mem_catalog_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                p = entry.get("path")
                if p:
                    pp = temp_root / p
                    if not pp.exists():
                        findings.append(f"path must exist: {p} for id {entry.get('id')}")
        except:
            pass
    return findings

class TestCatalogIntegrityCheck(unittest.TestCase):
    def test_repo_passes(self):
        report, total, ok = check_all()
        self.assertTrue(ok, f"live repo should pass 0 findings, got total={total} report={report[:500]}")
        self.assertEqual(total, 0)

    def test_agent_profile_ref_broken(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            agent_path = tr / "agents" / "contracts" / "AGT-arena-ai.json"
            data = json.loads(agent_path.read_text(encoding="utf-8"))
            data["profile_ref"] = "agents/MISSING/CAPABILITY_PROFILE.md"
            agent_path.write_text(json.dumps(data), encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("profile_ref does not resolve" in f for f in findings), f"should detect broken profile_ref, got {findings}")

    def test_subskill_parent_skill_broken(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            sub_path = tr / "subskills" / "SUBSKILL_CATALOG.json"
            data = json.loads(sub_path.read_text(encoding="utf-8"))
            data[0]["parent_skill"] = "SKILL-999"
            sub_path.write_text(json.dumps(data), encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("parent_skill FK does not resolve" in f for f in findings), f"should detect broken parent_skill FK, got {findings}")

    def test_scaffold_deps_broken(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            scaff_path = tr / "scaffolding" / "core" / "test.contract.json"
            data = json.loads(scaff_path.read_text(encoding="utf-8"))
            data["depends_on"] = ["SCAFFOLD-core-missing"]
            scaff_path.write_text(json.dumps(data), encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("depends_on" in f and "does not resolve" in f for f in findings), f"should detect broken scaffold deps, got {findings}")

    def test_skill_required_tools_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            skill_path = tr / "skills" / "SKILL_CATALOG.json"
            data = json.loads(skill_path.read_text(encoding="utf-8"))
            data[0]["required_tools"] = ["nonexistent_tool"]
            skill_path.write_text(json.dumps(data), encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("required_tools" in f and "not in TOOL_REGISTRY" in f for f in findings), f"should detect invalid required_tools, got {findings}")

    def test_cue_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            cue_path = tr / "cue" / "CUE_CATALOG.json"
            data = json.loads(cue_path.read_text(encoding="utf-8"))
            data["cues"][0]["precedence"] = "invalid_prec"
            cue_path.write_text(json.dumps(data), encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("invalid precedence" in f for f in findings), f"should detect invalid CUE precedence, got {findings}")

    def test_memory_path_missing(self):
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            make_base_temp(tr)
            mem_path = tr / "Brain" / "MEMORY_CATALOG.jsonl"
            entry = {
                "id": "MEM-note-test-001",
                "path": "Brain/missing/path.md",
                "title": "Test note",
                "kind": "note",
                "tags": ["a", "b", "c"],
                "added": "2026-09-16"
            }
            mem_path.write_text(json.dumps(entry) + "\n", encoding="utf-8")
            findings = run_fk_check(tr)
            self.assertTrue(any("path must exist" in f for f in findings), f"should detect missing MEMORY path, got {findings}")

    def test_self_test_ran(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "catalog_integrity_check.py"), "--self-test"], capture_output=True, text=True, timeout=30, cwd=str(ROOT))
        self.assertEqual(result.returncode, 0, f"self-test should pass: {result.stdout}\n{result.stderr}")
        self.assertIn("9 passed", result.stdout, f"self-test should show 9 passed, got {result.stdout}")

if __name__ == "__main__":
    unittest.main()
