#!/usr/bin/env python3
"""
Test harness for deck_rules_check.py — S-2-PPTX-A stage 1

Vectors ≥4 TestCase law: clean pass, R-001 violation, R-002 violation, schema-invalid, UNBACKED-BULLET WARN
Discover 158 → ≥162
"""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

class TestDeckRulesCheck(unittest.TestCase):
    def make_temp_repo(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "schemas").mkdir(parents=True, exist_ok=True)
        (tmp / "decks").mkdir(parents=True, exist_ok=True)
        (tmp / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy(str(ROOT / "schemas" / "deck_outline.schema.json"), str(tmp / "schemas" / "deck_outline.schema.json"))
        shutil.copy(str(ROOT / "decks" / "DECK_RULES.json"), str(tmp / "decks" / "DECK_RULES.json"))
        shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp / "scripts" / "deck_rules_check.py"))
        run(f"git init -q", cwd=tmp)
        run(f"git config user.email test@test.com", cwd=tmp)
        run(f"git config user.name Test", cwd=tmp)
        return tmp

    def make_outline(self, bullets_per_slide=3, chars_per_bullet=20, theme_name="anchor", unbacked=False, invalid_schema=False, theme_lock_override=None):
        registry_hexes = {
            "anchor": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"],
            "slate": ["#1E293B", "#E2E8F0", "#818CF8", "#F472B6", "#22D3EE"]
        }
        tlock = theme_lock_override if theme_lock_override is not None else registry_hexes.get(theme_name, registry_hexes["anchor"])
        bullets=[]
        for i in range(bullets_per_slide):
            txt = "x" * chars_per_bullet if chars_per_bullet>0 else f"Bullet {i+1}"
            sref = None if unbacked and i==0 else f"SRC-00{i+1}"
            bullets.append({"text": txt, "source_ref": sref})
        slides=[{"ref": "S-001", "type": "content", "bullets": bullets, "notes": None}]
        outline={
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-TEST",
            "title": "Test Outline",
            "theme": {"name": theme_name, "theme_lock": tlock},
            "slides": slides,
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-16", "source_refs": ["SRC-001"]},
            "honesty_note": "test"
        }
        if invalid_schema:
            outline.pop("title", None)
        return outline

    def test_clean_pass(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets_per_slide=3, chars_per_bullet=20)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"clean should pass: {p.stdout}")
            self.assertIn("0 finding", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_r001_violation(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets_per_slide=7, chars_per_bullet=10)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("R-001", p.stdout)
            self.assertIn("7 bullets vs threshold 6", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_r002_violation(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets_per_slide=5, chars_per_bullet=100)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("R-002", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_r003_violation(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets_per_slide=1, chars_per_bullet=100)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("R-003", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_schema_invalid(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(invalid_schema=True)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("schema-invalid", p.stdout.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unbacked_bullet_warn(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets_per_slide=2, chars_per_bullet=20, unbacked=True)
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"UNBACKED should be WARN not FAIL: {p.stdout}")
            self.assertIn("UNBACKED-BULLET", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_example_card001_lint_clean(self):
        # Example derived from CARD_001 should be lint-clean
        tmp = self.make_temp_repo()
        try:
            # Copy example file
            example_src = ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"
            self.assertTrue(example_src.exists(), "example outline must exist")
            out_path = tmp / "decks" / "OUTLINE_example_card001.json"
            shutil.copy(str(example_src), str(out_path))
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"example CARD001 should be lint-clean: {p.stdout}")
            self.assertIn("0 finding", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_theme_registry_provisional(self):
        # Theme registry must have exactly two palettes marked PROVISIONAL, 5 hexes each
        rules_path = ROOT / "decks" / "DECK_RULES.json"
        data = json.loads(rules_path.read_text(encoding="utf-8"))
        registry = data.get("theme_registry", {})
        self.assertEqual(set(registry.keys()), {"anchor", "slate"})
        for name, entry in registry.items():
            self.assertEqual(entry.get("status"), "PROVISIONAL")
            self.assertEqual(len(entry.get("hexes", [])), 5)

    def test_no_pptx_import(self):
        # No python-pptx import anywhere (import pptx = policy FAIL-class)
        # Check for actual import statements, not substring in comments/docstrings
        import re
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        for fp in (ROOT / "scripts").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(txt), f"{fp} must not import pptx per S-2-PPTX-A")
        for fp in (ROOT / "decks").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(txt), f"{fp} must not import pptx per S-2-PPTX-A")

if __name__ == "__main__":
    unittest.main()
