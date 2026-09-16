#!/usr/bin/env python3
"""
Test harness for skill_check.py — P-17 Skill Catalog Spine (Dim-7/G4)

≥4 vectors: repo passes · broken eval_ref→FAIL · eval-free active→FAIL · unknown status→FAIL
"""
import json
import pathlib
import subprocess
import tempfile
import shutil
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKER_PATH = ROOT / "scripts" / "skill_check.py"

def run_cmd(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

def make_entry(suffix="001", status="active", eval_ref="evals/skills/SKILL-001.eval.md", entry_path="agents/Arena_AI/BOOT.md", extra=None):
    base = {
        "id": f"SKILL-{suffix}",
        "title": f"Test skill {suffix}",
        "entry_path": entry_path,
        "kind": "agent",
        "description": f"Test description for skill {suffix} valid ≤200.",
        "eval_ref": eval_ref,
        "status": status,
        "activation_note": "asserted",
        "tests": [eval_ref] if eval_ref else []
    }
    if extra:
        base.update(extra)
    return base

class TestSkillCheck(unittest.TestCase):
    def test_live_repo_passes(self):
        """live repo passes — skill_check exit 0"""
        p = run_cmd(f"python3 {CHECKER_PATH}")
        self.assertEqual(p.returncode, 0, f"skill_check should pass on live repo, got {p.stdout} {p.stderr}")
        self.assertIn("0 finding", p.stdout)

    def test_broken_eval_ref_fail(self):
        """broken eval_ref → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            schema_src = ROOT / "schemas" / "skill_card.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "skill_card.schema.json")
            entry = make_entry("001", status="active", eval_ref="evals/skills/missing.eval.md", entry_path="agents/Arena_AI/BOOT.md")
            cat_path = tr / "skills" / "SKILL_CATALOG.json"
            cat_path.write_text(json.dumps([entry]), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import skill_check
skill_check.ROOT = pathlib.Path('{tr}')
findings = skill_check.check_skills(catalog_path=pathlib.Path('{cat_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"broken eval_ref should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("eval_ref", p.stdout)

    def test_eval_free_active_fail(self):
        """eval-free active → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            schema_src = ROOT / "schemas" / "skill_card.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "skill_card.schema.json")
            entry = make_entry("001", status="active", eval_ref="", entry_path="agents/Arena_AI/BOOT.md")
            entry["eval_ref"] = ""
            entry["tests"] = []
            cat_path = tr / "skills" / "SKILL_CATALOG.json"
            cat_path.write_text(json.dumps([entry]), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import skill_check
skill_check.ROOT = pathlib.Path('{tr}')
findings = skill_check.check_skills(catalog_path=pathlib.Path('{cat_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"eval-free active should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("eval_ref", p.stdout)

    def test_unknown_status_fail(self):
        """unknown status → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            (tr / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "schemas").mkdir(parents=True, exist_ok=True)
            schema_src = ROOT / "schemas" / "skill_card.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "skill_card.schema.json")
            entry = make_entry("001", status="active", eval_ref="evals/skills/SKILL-001.eval.md", entry_path="agents/Arena_AI/BOOT.md")
            entry["status"] = "bogus"
            cat_path = tr / "skills" / "SKILL_CATALOG.json"
            cat_path.write_text(json.dumps([entry]), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import skill_check
skill_check.ROOT = pathlib.Path('{tr}')
findings = skill_check.check_skills(catalog_path=pathlib.Path('{cat_path}'), root=pathlib.Path('{tr}'))
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"unknown status should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("status", p.stdout)

    def test_self_test_ran(self):
        """self-test ran — skill_check --self-test ≥4 vectors pass"""
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
