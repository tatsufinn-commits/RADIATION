#!/usr/bin/env python3
"""
Test harness for scaffold_check.py — P-16 Scaffolding Contract Spine (Dim-3/G4)

≥4 vectors: live repo passes · broken depends_on → FAIL · uncontracted file → FAIL · cycle → FAIL
"""
import json
import pathlib
import subprocess
import tempfile
import shutil
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKER_PATH = ROOT / "scripts" / "scaffold_check.py"

def run_cmd(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

class TestScaffoldCheck(unittest.TestCase):
    def test_live_repo_passes(self):
        """live repo passes — scaffold_check exit 0"""
        p = run_cmd(f"python3 {CHECKER_PATH}")
        self.assertEqual(p.returncode, 0, f"scaffold_check should pass on live repo, got {p.stdout} {p.stderr}")
        self.assertIn("0 finding", p.stdout)

    def test_broken_depends_on_fail(self):
        """broken depends_on → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            # Copy schema
            schema_src = ROOT / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "test.md"
            sf.write_text("# test\n", encoding="utf-8")
            contract = {
                "id": "SCAFFOLD-core-test-md",
                "file": "scaffolding/core/test.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-nonexistent"],
                "effects": ["read"],
                "tests": []
            }
            (tr / "scaffolding" / "core" / "test.md.contract.json").write_text(json.dumps(contract), encoding="utf-8")
            # Run checker with temp root via env? We'll run via python with modified ROOT by importing
            # Simpler: run checker script with temp root by monkey-patching via subprocess that sets env? We'll reuse logic from scaffold_check self-test
            # Instead, directly run the checker file with temp dir as ROOT by creating a wrapper script
            # For simplicity, we run the checker via python -c that imports and overrides ROOT
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import scaffold_check
scaffold_check.ROOT = pathlib.Path('{tr}')
scaffold_check.SCAFF_DIR = pathlib.Path('{tr / 'scaffolding'}')
scaffold_check.SCHEMA_PATH = pathlib.Path('{tr / 'schemas' / 'scaffold_contract.schema.json'}')
findings = scaffold_check.check_scaffolding()
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            # Should have findings and exit 1
            self.assertNotEqual(p.returncode, 0, f"broken depends_on should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("depends_on", p.stdout)

    def test_uncontracted_file_fail(self):
        """uncontracted file → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = ROOT / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "orphan.md"
            sf.write_text("# orphan\n", encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import scaffold_check
scaffold_check.ROOT = pathlib.Path('{tr}')
scaffold_check.SCAFF_DIR = pathlib.Path('{tr / 'scaffolding'}')
scaffold_check.SCHEMA_PATH = pathlib.Path('{tr / 'schemas' / 'scaffold_contract.schema.json'}')
findings = scaffold_check.check_scaffolding()
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"uncontracted file should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("uncontracted", p.stdout)

    def test_cycle_fail(self):
        """cycle → FAIL"""
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = ROOT / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf1 = tr / "scaffolding" / "core" / "a.md"
            sf1.write_text("# a\n", encoding="utf-8")
            sf2 = tr / "scaffolding" / "core" / "b.md"
            sf2.write_text("# b\n", encoding="utf-8")
            c1 = {
                "id": "SCAFFOLD-core-a-md",
                "file": "scaffolding/core/a.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-b-md"],
                "effects": ["read"],
                "tests": []
            }
            c2 = {
                "id": "SCAFFOLD-core-b-md",
                "file": "scaffolding/core/b.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-a-md"],
                "effects": ["read"],
                "tests": []
            }
            (tr / "scaffolding" / "core" / "a.md.contract.json").write_text(json.dumps(c1), encoding="utf-8")
            (tr / "scaffolding" / "core" / "b.md.contract.json").write_text(json.dumps(c2), encoding="utf-8")
            code = f"""
import pathlib, sys
sys.path.insert(0, '{ROOT / 'scripts'}')
import scaffold_check
scaffold_check.ROOT = pathlib.Path('{tr}')
scaffold_check.SCAFF_DIR = pathlib.Path('{tr / 'scaffolding'}')
scaffold_check.SCHEMA_PATH = pathlib.Path('{tr / 'schemas' / 'scaffold_contract.schema.json'}')
findings = scaffold_check.check_scaffolding()
print(findings)
sys.exit(1 if findings else 0)
"""
            p = subprocess.run(f"python3 -c \"{code}\"", shell=True, capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0, f"cycle should FAIL, got {p.stdout} {p.stderr}")
            self.assertIn("cycle", p.stdout.lower())

    def test_self_test_ran(self):
        """self-test ran — scaffold_check --self-test ≥4 vectors pass"""
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
