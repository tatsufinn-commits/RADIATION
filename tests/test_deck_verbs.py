#!/usr/bin/env python3
"""
test_deck_verbs.py — ≥5 vectors for S-2-PPTX-C guardrailed verbs + optional adapter

Vectors:
- plan exemplar budgets
- verify chains green
- fill_template with ABSENT adapter reports blocked-at-WP-D never crash never fake
- unconditional-pptx-import guard walk ship-files asserting no raw import pptx outside guarded probe block
- budgets re-asserted at plan time truth lines + receipts audit

Unittest.TestCase only — bare functions not tests per P-19 fix.

Battery: discover 175→≥180, registry 35→36
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def run(cmd, cwd=ROOT):
    return subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)

class TestDeckVerbs(unittest.TestCase):

    def test_01_plan_exemplar_budgets(self):
        """plan of exemplar emits budgets · truth lines · receipts audit"""
        p = run(f"python3 scripts/deck_verbs.py plan_slide decks/examples/OUTLINE_example_card001.json")
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        self.assertIn("budgets re-asserted at plan time", p.stdout)
        self.assertIn("source_ref audit", p.stdout)
        self.assertIn("truth:", p.stdout)
        self.assertIn("backed", p.stdout)

    def test_02_verify_chains_green(self):
        """verify chains green: deck_rules_check + deck_verify + adapter status line"""
        p = run(f"python3 scripts/deck_verbs.py verify_deck decks/examples/OUTLINE_example_card001.json")
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        self.assertIn("checked", p.stdout.lower())
        self.assertIn("canonical", p.stdout.lower())
        self.assertIn("chained gate green", p.stdout)
        self.assertIn("adapter:", p.stdout)

    def test_03_fill_template_absent_adapter_blocked_at_wp_d(self):
        """fill_template with ABSENT adapter reports blocked-at-WP-D never crash never fake"""
        p = run(f"python3 scripts/deck_verbs.py fill_template decks/examples/OUTLINE_example_card001.json --adapter null")
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        self.assertIn("ABSENT-UNKNOWN", p.stdout)
        self.assertIn("blocked_at", p.stdout)
        self.assertIn("WP-D", p.stdout)
        self.assertIn("would_render", p.stdout)
        # Never fake — must not claim rendered
        self.assertNotIn("rendered pptx", p.stdout.lower())
        # Structured report contains sha
        self.assertIn("sha", p.stdout.lower())

    def test_04_unconditional_pptx_import_guard(self):
        """fence law extended: no raw import pptx outside guarded probe block"""
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        for fp in (ROOT / "scripts").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            if fp.name == "deck_pptx_adapter.py":
                # Only allowed inside probe function — no top-level unconditional
                if "def probe_pptx_capability" not in txt:
                    self.fail(f"{fp} missing probe function")
                lines = txt.splitlines()
                def_idx = txt.find("def probe_pptx_capability")
                for line in lines:
                    if re.match(r"^\s*(import\s+pptx|from\s+pptx)", line):
                        line_idx = txt.find(line)
                        if line_idx < def_idx:
                            self.fail(f"{fp} has unconditional pptx import at module level — policy FAIL-class")
                continue
            if pattern.search(txt):
                self.fail(f"{fp} contains raw import pptx outside guarded probe block — fence law violation")

    def test_05_plan_budgets_reasserted_per_slide(self):
        """plan re-check per slide vs DECK_RULES budgets re-asserted at plan time, source_ref audit {backed,unbacked-warn}, per-slide truth lines ref·type·bullets·chars·receipts"""
        # Use exemplar — should have 6 truth lines
        p = run(f"python3 scripts/deck_verbs.py plan_slide decks/examples/OUTLINE_example_card001.json")
        self.assertEqual(p.returncode, 0)
        # Count truth lines
        truth_count = p.stdout.count("truth:")
        self.assertEqual(truth_count, 6, msg=f"expected 6 truth lines, got {truth_count} — {p.stdout}")
        # Each truth line must contain ref·type·bullets·chars·receipts pattern
        for line in p.stdout.splitlines():
            if "truth:" in line:
                self.assertIn("·", line)
                self.assertIn("bullets", line)
                self.assertIn("chars", line)
                self.assertIn("receipts", line)

    def test_06_fill_template_dry_run_evidence_deterministic(self):
        """fill_template deterministic sha — same input → same sha, no actual rendering"""
        p1 = run(f"python3 scripts/deck_verbs.py fill_template decks/examples/OUTLINE_example_card001.json --adapter null")
        p2 = run(f"python3 scripts/deck_verbs.py fill_template decks/examples/OUTLINE_example_card001.json --adapter null")
        self.assertEqual(p1.returncode, 0)
        self.assertEqual(p2.returncode, 0)
        # Extract sha
        import json as js
        # Find json block — first { to last }
        def extract_json(s):
            start = s.find("{")
            end = s.rfind("}")
            if start == -1 or end == -1:
                return None
            try:
                return js.loads(s[start:end+1])
            except Exception:
                # Try line-by-line — the report is first JSON
                # The script prints JSON then a line — so first JSON block ends before fill_template:
                # We'll parse up to blocked_at line? Simpler: find sha via regex
                m = re.search(r'"sha"\s*:\s*"([a-f0-9]+)"', s)
                if m:
                    return {"sha": m.group(1)}
                return None
        j1 = extract_json(p1.stdout)
        j2 = extract_json(p2.stdout)
        self.assertIsNotNone(j1)
        self.assertIsNotNone(j2)
        self.assertEqual(j1.get("sha"), j2.get("sha"), msg="deterministic sha must be same across runs")

    def test_07_self_test_vectors(self):
        """deck_verbs self-test ≥5 vectors"""
        p = run(f"python3 scripts/deck_verbs.py --self-test")
        self.assertEqual(p.returncode, 0, msg=p.stdout + p.stderr)
        self.assertIn("5/5", p.stdout)
        self.assertIn("vectors", p.stdout)

    def test_08_adapter_probe_contract_grammar(self):
        """adapter probe contract grammar ABSENT≠UNAVAILABLE≠UNKNOWN declared stamped, never claimed absent-by-proxy"""
        p = run(f"python3 scripts/deck_pptx_adapter.py")
        self.assertEqual(p.returncode, 0)
        data = json.loads(p.stdout)
        self.assertIn("pptx", data)
        self.assertIn(data["pptx"], ["AVAILABLE", "ABSENT-UNKNOWN"])
        # Must have note about observed
        self.assertIn("probe observed", data.get("note",""))

if __name__ == "__main__":
    unittest.main()
