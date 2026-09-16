#!/usr/bin/env python3
"""
Test harness for deck_verify.py — S-2-PPTX-B outline round-trip + receipt resolver

Vectors ≥5 + rider vector (TestCase law; discover 167 → ≥173)
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

class TestDeckVerify(unittest.TestCase):
    def make_temp_repo(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "schemas").mkdir(parents=True, exist_ok=True)
        (tmp / "decks").mkdir(parents=True, exist_ok=True)
        (tmp / "scripts").mkdir(parents=True, exist_ok=True)
        (tmp / "01-research").mkdir(parents=True, exist_ok=True)
        (tmp / "05-annotate").mkdir(parents=True, exist_ok=True)
        (tmp / "06-triangulate").mkdir(parents=True, exist_ok=True)
        (tmp / "09-nota").mkdir(parents=True, exist_ok=True)
        shutil.copy(str(ROOT / "schemas" / "deck_outline.schema.json"), str(tmp / "schemas" / "deck_outline.schema.json"))
        shutil.copy(str(ROOT / "decks" / "DECK_RULES.json"), str(tmp / "decks" / "DECK_RULES.json"))
        shutil.copy(str(ROOT / "scripts" / "deck_verify.py"), str(tmp / "scripts" / "deck_verify.py"))
        shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp / "scripts" / "deck_rules_check.py"))
        # Create minimal grounding files for receipt resolver
        (tmp / "01-research" / "REFERENCES.md").write_text("SRC-013 SRC-014 SRC-015 CARD_001 TRI_bp344", encoding="utf-8")
        (tmp / "09-nota" / "CARD_001_test.md").write_text("id: CARD_001", encoding="utf-8")
        (tmp / "06-triangulate" / "TRI_test.md").write_text("TRI_bp344-accessibility", encoding="utf-8")
        run(f"git init -q", cwd=tmp)
        run(f"git config user.email test@test.com", cwd=tmp)
        run(f"git config user.name Test", cwd=tmp)
        return tmp

    def make_outline(self, bullets=None, theme_name="anchor"):
        if bullets is None:
            bullets=[{"text": "Bullet one", "source_ref": "SRC-013"}, {"text": "Bullet two", "source_ref": "CARD_001"}]
        return {
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-TEST",
            "title": "Test Outline",
            "theme": {"name": theme_name, "theme_lock": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"]},
            "slides": [{"ref": "S-001", "type": "content", "bullets": bullets, "notes": None}],
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-16", "source_refs": ["SRC-013"]},
            "honesty_note": "test"
        }

    def test_true_match(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline()
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            # Compare with itself — should be MATCH
            p = run(f"python3 scripts/deck_verify.py {out_path} --compare {out_path}", cwd=tmp)
            self.assertIn("MATCH", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_drift_text(self):
        tmp = self.make_temp_repo()
        try:
            orig = self.make_outline()
            orig_path = tmp / "decks" / "OUTLINE_ORIG.json"
            orig_path.write_text(json.dumps(orig), encoding="utf-8")
            tamp = self.make_outline()
            tamp["slides"][0]["bullets"][0]["text"] = "Mutated text different"
            tamp_path = tmp / "decks" / "OUTLINE_TAMP.json"
            tamp_path.write_text(json.dumps(tamp), encoding="utf-8")
            p = run(f"python3 scripts/deck_verify.py {orig_path} --compare {tamp_path}", cwd=tmp)
            self.assertIn("DRIFT-text", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_drift_structure(self):
        tmp = self.make_temp_repo()
        try:
            orig = self.make_outline(bullets=[{"text": "One", "source_ref": "SRC-013"}, {"text": "Two", "source_ref": "CARD_001"}])
            orig_path = tmp / "decks" / "OUTLINE_ORIG.json"
            orig_path.write_text(json.dumps(orig), encoding="utf-8")
            tamp = self.make_outline(bullets=[{"text": "One", "source_ref": "SRC-013"}])
            tamp_path = tmp / "decks" / "OUTLINE_TAMP.json"
            tamp_path.write_text(json.dumps(tamp), encoding="utf-8")
            p = run(f"python3 scripts/deck_verify.py {orig_path} --compare {tamp_path}", cwd=tmp)
            self.assertIn("DRIFT-structure", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unresolved_receipt(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets=[{"text": "Test", "source_ref": "SRC-NONEXISTENT-999"}])
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_verify.py {out_path}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("UNRESOLVED-RECEIPT", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_canonical_idempotence(self):
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline()
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_verify.py {out_path}", cwd=tmp)
            # Should have canonical-idempotence PASS in INFO
            self.assertIn("canonical-idempotence PASS", p.stdout)
            self.assertIn("sha", p.stdout.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_receipt_resolved(self):
        # Real tree should resolve CARD_001
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline(bullets=[{"text": "Test", "source_ref": "CARD_001"}])
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_verify.py {out_path}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"known receipt should resolve: {p.stdout}")
            self.assertIn("0 finding", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_rider_truth_bearing_coverage(self):
        # Rider from PPTX-A: checked N outline file(s) — 0 findings truth-bearing
        tmp = self.make_temp_repo()
        try:
            outline = self.make_outline()
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            self.assertIn("checked 1 outline file(s)", p.stdout)
            self.assertIn("0 findings", p.stdout)
            # With 0 outlines present, allowed to say no outlines present
            tmp2 = pathlib.Path(tempfile.mkdtemp())
            (tmp2 / "schemas").mkdir(parents=True, exist_ok=True)
            (tmp2 / "decks").mkdir(parents=True, exist_ok=True)
            (tmp2 / "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "schemas" / "deck_outline.schema.json"), str(tmp2 / "schemas" / "deck_outline.schema.json"))
            shutil.copy(str(ROOT / "decks" / "DECK_RULES.json"), str(tmp2 / "decks" / "DECK_RULES.json"))
            shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp2 / "scripts" / "deck_rules_check.py"))
            p2 = run(f"python3 scripts/deck_rules_check.py", cwd=tmp2)
            self.assertIn("no outlines present", p2.stdout.lower())
            self.assertIn("checked 0 outline file(s)", p2.stdout.lower())
            shutil.rmtree(tmp2, ignore_errors=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_no_pptx_import(self):
        # No python-pptx import anywhere
        import re
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        for fp in (ROOT / "scripts").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(txt), f"{fp} must not import pptx per S-2-PPTX-B")
        for fp in (ROOT / "decks").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(pattern.search(txt))

if __name__ == "__main__":
    unittest.main()
