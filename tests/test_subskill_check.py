#!/usr/bin/env python3
"""
Test harness for subskill_check.py — P-18 Subskill Catalog + Hook Protocol (Dim-8/G4)

≥4 vectors: repo passes · broken parent FK → FAIL · missing scenario_ref → FAIL · illegal trigger → FAIL
"""
import json
import pathlib
import subprocess
import tempfile
import shutil
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKER_PATH = ROOT / "scripts" / "subskill_check.py"

def run_cmd(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

def make_skill(sid="SKILL-015"):
    return {
        "id": sid,
        "title": f"Skill {sid}",
        "entry_path": "agents/Arena_AI/BOOT.md",
        "kind": "agent",
        "description": "Test skill description valid ≤200.",
        "eval_ref": "evals/skills/SKILL-001.eval.md",
        "status": "active",
        "activation_note": "asserted",
        "tests": ["evals/skills/SKILL-001.eval.md"]
    }

def make_sub(sid="SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md", status="active"):
    return {
        "id": sid,
        "title": f"Test subskill {sid}",
        "parent_skill": parent,
        "entry_path": entry_path,
        "trigger": trigger,
        "condition": None,
        "description": f"Test description for subskill {sid} valid ≤200.",
        "scenario_ref": scenario_ref,
        "status": status,
        "tests": [scenario_ref]
    }

class TestSubskillCheck(unittest.TestCase):
    def test_live_repo_passes(self):
        """live repo passes — subskill_check exit 0"""
        p = run_cmd(f"python3 {CHECKER_PATH}")
        self.assertEqual(p.returncode, 0, f"subskill_check should pass on live repo, got {p.stdout} {p.stderr}")
        self.assertIn("0 finding", p.stdout)

    def test_broken_parent_fk_fail(self):
        """broken parent FK → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            (tr / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            src_schema = ROOT / "schemas" / "subskill_card.schema.json"
            if src_schema.exists():
                shutil.copy(src_schema, tr / "schemas" / "subskill_card.schema.json")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-999", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")]
            sub_path = tr / "subskills" / "SUBSKILL_CATALOG.json"
            skill_path = tr / "skills" / "SKILL_CATALOG.json"
            sub_path.write_text(json.dumps(sub_cat), encoding="utf-8")
            skill_path.write_text(json.dumps(skill_cat), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import subskill_check
findings = subskill_check.check_subskills(catalog_path=pathlib.Path('{sub_path}'), skill_catalog_path=pathlib.Path('{skill_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"broken parent FK should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("parent_skill", p.stdout)

    def test_missing_scenario_ref_fail(self):
        """missing scenario_ref → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            src_schema = ROOT / "schemas" / "subskill_card.schema.json"
            if src_schema.exists():
                shutil.copy(src_schema, tr / "schemas" / "subskill_card.schema.json")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/MISSING.scenario.json", entry_path="subskills/active/colony.md")]
            sub_path = tr / "subskills" / "SUBSKILL_CATALOG.json"
            skill_path = tr / "skills" / "SKILL_CATALOG.json"
            sub_path.write_text(json.dumps(sub_cat), encoding="utf-8")
            skill_path.write_text(json.dumps(skill_cat), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import subskill_check
findings = subskill_check.check_subskills(catalog_path=pathlib.Path('{sub_path}'), skill_catalog_path=pathlib.Path('{skill_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"missing scenario_ref should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("scenario_ref", p.stdout)

    def test_illegal_trigger_fail(self):
        """illegal trigger → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"illegal","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            (tr / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            src_schema = ROOT / "schemas" / "subskill_card.schema.json"
            if src_schema.exists():
                shutil.copy(src_schema, tr / "schemas" / "subskill_card.schema.json")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="bad_trigger", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")]
            sub_path = tr / "subskills" / "SUBSKILL_CATALOG.json"
            skill_path = tr / "skills" / "SKILL_CATALOG.json"
            sub_path.write_text(json.dumps(sub_cat), encoding="utf-8")
            skill_path.write_text(json.dumps(skill_cat), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import subskill_check
findings = subskill_check.check_subskills(catalog_path=pathlib.Path('{sub_path}'), skill_catalog_path=pathlib.Path('{skill_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"illegal trigger should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("trigger", p.stdout)

    def test_self_test_ran(self):
        """self-test ran — subskill_check --self-test ≥4 vectors pass"""
        p = run_cmd(f"python3 {CHECKER_PATH} --self-test")
        self.assertEqual(p.returncode, 0, f"self-test should pass, got {p.stdout} {p.stderr}")
        self.assertIn("passed", p.stdout)
        import re
        m = re.search(r"(\d+) passed", p.stdout)
        self.assertIsNotNone(m)
        passed = int(m.group(1))
        self.assertGreaterEqual(passed, 4, f"self-test should have ≥4 vectors, got {passed}")

if __name__ == "__main__":
    unittest.main()
