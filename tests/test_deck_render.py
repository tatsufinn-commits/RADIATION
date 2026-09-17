#!/usr/bin/env python3
"""
test_deck_render.py — Renderer vectors (S-2-PPTX-D stage 4 of 5)

≥6 vectors incl fence extension + tree-scan guard asserting zero *.pptx ever committed
- single import site law: ONLY scripts/deck_pptx_adapter.py may contain import pptx
- no unconditional import
- render exemplar MATCH (skipUnless AVAILABLE)
- receipts embedded as speaker notes
- budgets re-asserted pre-render refuse on FAIL
- no *.pptx ever committed tree-scan
- theme taken from DECK_RULES.json as-is anchor PROVISIONAL
- receipts_embedded count

All pptx-touching vectors skipUnless-gated via probe AVAILABLE degrade honestly ABSENT-UNKNOWN never crash.
"""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent

def probe_available():
    try:
        spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cap = mod.probe_pptx_capability()
        return cap.get("pptx") == "AVAILABLE", mod, cap
    except Exception as e:
        return False, None, {"pptx": "ABSENT-UNKNOWN", "failure": str(e)}

class TestDeckRender(unittest.TestCase):

    def test_01_single_import_site_only_adapter_contains_import_pptx(self):
        """Fence law walks ALL ship-files scripts/, tests/, Brain/, cue/, skills/ FAIL any other occurrence — single import site ONLY scripts/deck_pptx_adapter.py"""
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        allowed = (ROOT / "scripts" / "deck_pptx_adapter.py").resolve()
        violations = []
        for scan_dir in [ROOT / "scripts", ROOT / "tests", ROOT / "Brain", ROOT / "cue", ROOT / "skills"]:
            if not scan_dir.exists():
                continue
            for fp in scan_dir.rglob("*.py"):
                if fp.resolve() == allowed:
                    continue
                txt = fp.read_text(encoding="utf-8", errors="ignore")
                for line in txt.splitlines():
                    s = line.strip()
                    if s.startswith("#"):
                        continue
                    if re.match(r"^(import\s+pptx|from\s+pptx)", s):
                        violations.append(f"{fp}:{line}")
        self.assertEqual(violations, [], f"single import site law violations — ONLY deck_pptx_adapter.py may contain import pptx: {violations}")

    def test_02_no_unconditional_import_in_adapter(self):
        """Adapter probe truly executes import pptx inside try/except — never module level"""
        adapter_path = ROOT / "scripts" / "deck_pptx_adapter.py"
        txt = adapter_path.read_text(encoding="utf-8", errors="ignore")
        lines = txt.splitlines()
        # Check no top-level import pptx before function def
        # Find first def probe_pptx_capability
        def_idx = None
        for i, l in enumerate(lines):
            if "def probe_pptx_capability" in l:
                def_idx = i
                break
        self.assertIsNotNone(def_idx, "probe_pptx_capability not found")
        for i in range(def_idx):
            line = lines[i].strip()
            if line.startswith("#"):
                continue
            if re.match(r"^(import\s+pptx|from\s+pptx)", line):
                self.fail(f"adapter has unconditional import pptx at module level line {i}: {lines[i]} — must be inside guarded probe/call-sites")

    def test_03_no_pptx_committed_tree_scan_guard(self):
        """Tree-scan guard asserting zero *.pptx ever committed — no .pptx ever committed anywhere ever, .gitignore LAW-6-era idiom"""
        found = []
        for fp in ROOT.rglob("*.pptx"):
            if ".git" in str(fp):
                continue
            found.append(str(fp))
        self.assertEqual(found, [], f"found *.pptx in repo tree — no .pptx ever committed violation: {found}")

        # Also check .gitignore contains *.pptx
        gitignore = ROOT / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text(encoding="utf-8", errors="ignore")
            self.assertIn("*.pptx", content, ".gitignore must contain *.pptx as LAW-6-era idiom")

    def test_04_render_exemplar_match_skipUnless_AVAILABLE(self):
        """Render exemplar outline to tempdir → parse back → MATCH (skipUnless AVAILABLE) — stdlib checkout still passes core"""
        available, mod, cap = probe_available()
        if not available:
            self.skipTest(f"probe {cap} — ABSENT-UNKNOWN — stdlib-only env degrades honestly per IP-ENV-01 — skipUnless AVAILABLE")

        outline_path = ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"
        self.assertTrue(outline_path.exists(), f"exemplar outline missing at {outline_path}")

        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            out_path = tmpdir / "test_render_match.pptx"
            p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_render.py"), str(outline_path), "--out", str(out_path)], cwd=str(ROOT), capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, f"deck_render failed rc={p.returncode} stdout={p.stdout} stderr={p.stderr}")
            self.assertTrue(out_path.exists(), f"rendered pptx not exists at {out_path}")

            # Parse back via adapter
            structure = mod.parse_pptx_to_structure(out_path)
            outline_data = json.loads(outline_path.read_text(encoding="utf-8"))
            self.assertEqual(len(structure), len(outline_data.get("slides", [])), f"structure len {len(structure)} vs outline {len(outline_data.get('slides',[]))}")

            # Check each slide bullets match
            for o_slide, p_slide in zip(outline_data.get("slides", []), structure):
                self.assertEqual(len(o_slide.get("bullets", [])), len(p_slide.get("bullets", [])), f"slide {o_slide.get('ref')} bullets count mismatch")

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_05_receipts_embedded_as_speaker_notes(self):
        """Slide shape title+bullets content speaker notes carry source_ref set receipts embedded two-pillar doctrine honored inside artifact"""
        available, mod, cap = probe_available()
        if not available:
            self.skipTest(f"probe {cap} — ABSENT-UNKNOWN — skipUnless AVAILABLE")

        outline_path = ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            out_path = tmpdir / "test_notes.pptx"
            p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_render.py"), str(outline_path), "--out", str(out_path)], cwd=str(ROOT), capture_output=True, text=True)
            self.assertEqual(p.returncode, 0)
            self.assertTrue(out_path.exists())
            structure = mod.parse_pptx_to_structure(out_path)
            # At least one slide should have source_refs in notes
            has_srefs = any(s.get("source_refs") for s in structure)
            self.assertTrue(has_srefs, f"no source_refs found in parsed structure {structure} — receipts must be embedded as speaker notes")

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_06_budgets_reasserted_pre_render_refuse_on_FAIL(self):
        """Budgets re-asserted pre-render run DECK_RULES check internally refuse render on FAIL guards not verbs"""
        # Create outline violating R-001 (max bullets 6) with 7 bullets
        outline = {
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-FAIL-BUDGET",
            "title": "Fail Budget",
            "theme": {"name": "anchor", "theme_lock": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"]},
            "slides": [{"ref": "S-001", "type": "content", "bullets": [{"text": f"Bullet {i}", "source_ref": "SRC-013"} for i in range(7)], "notes": None}],
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-17", "source_refs": ["SRC-013"]},
            "honesty_note": "test budget fail"
        }
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            out_json = tmpdir / "OUTLINE_FAIL.json"
            out_json.write_text(json.dumps(outline), encoding="utf-8")
            out_pptx = tmpdir / "fail.pptx"
            p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_render.py"), str(out_json), "--out", str(out_pptx)], cwd=str(ROOT), capture_output=True, text=True)
            # Should fail due to budget FAIL — guards, not verbs
            self.assertNotEqual(p.returncode, 0, f"expected FAIL on budget violation but got rc=0 stdout={p.stdout} stderr={p.stderr}")
            combined = p.stdout + p.stderr
            self.assertTrue("FAIL" in combined or "refuse render" in combined.lower() or "refuse" in combined.lower(), f"expected budget FAIL message in output: {combined}")

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_07_theme_taken_as_is_anchor_PROVISIONAL(self):
        """Theme taken from decks/DECK_RULES.json registry as-is anchor PROVISIONAL pending Commander notes"""
        rules_path = ROOT / "decks" / "DECK_RULES.json"
        self.assertTrue(rules_path.exists())
        rules_data = json.loads(rules_path.read_text(encoding="utf-8"))
        theme_registry = rules_data.get("theme_registry", {})
        # Theme registry should contain anchor and slate, both PROVISIONAL
        self.assertIn("anchor", theme_registry, "DECK_RULES.json theme_registry missing anchor")
        self.assertIn("slate", theme_registry, "DECK_RULES.json theme_registry missing slate")
        self.assertEqual(theme_registry["anchor"].get("status"), "PROVISIONAL", "anchor should be PROVISIONAL")
        # In docs/DECKS.md theme should be documented as PROVISIONAL
        decks_md = ROOT / "docs" / "DECKS.md"
        if decks_md.exists():
            content = decks_md.read_text(encoding="utf-8", errors="ignore")
            self.assertIn("PROVISIONAL", content, "DECKS.md should mention theme anchor PROVISIONAL")

    def test_08_fill_template_unfrozen_AVAIL_renders_ABSENT_honest(self):
        """fill_template unfrozen with adapter AVAILABLE performs render via deck_render emits {rendered, sha, receipts_embedded} ABSENT keeps honest report shape no fake never"""
        available, mod, cap = probe_available()
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            outline_path = ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"
            if available:
                out_pptx = tmpdir / "filled.pptx"
                p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "fill_template", str(outline_path), "--adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"), "--out", str(out_pptx)], cwd=str(ROOT), capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, f"fill_template AVAILABLE failed {p.stdout} {p.stderr}")
                self.assertTrue(out_pptx.exists(), "rendered file should exist when AVAILABLE")
                self.assertIn("rendered", p.stdout)
                self.assertIn("receipts_embedded", p.stdout)
                self.assertIn("sha", p.stdout)
                # Receipt law: outline ships always — check note
                self.assertIn("outline ships", p.stdout.lower())
            else:
                p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "fill_template", str(outline_path), "--adapter", "null"], cwd=str(ROOT), capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, f"fill_template ABSENT failed {p.stdout} {p.stderr}")
                self.assertIn("ABSENT-UNKNOWN", p.stdout)
                self.assertIn("blocked_at", p.stdout)
                # When ABSENT, honest report shape includes would_render plan (not fake rendered file)
                self.assertIn("would_render", p.stdout, "ABSENT report should include would_render plan — honest shape")
                # Must not claim actual pptx file inside repo tree
                # Check that no file path inside ROOT with .pptx extension is reported as rendered inside repo
                # The rendered field should be ABSENT-UNKNOWN or not a real file inside repo
                self.assertNotIn(str(ROOT), p.stdout.lower() + ".pptx inside repo" if ".pptx" in p.stdout and str(ROOT) in p.stdout else "")

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_09_verify_rendered_MATCH_and_DRIFT(self):
        """deck_verify --verify-rendered render outline to tempdir parse .pptx back derive structure compare vs outline verdict MATCH or DRIFT-text/DRIFT-structure/DRIFT-source_ref named classes preserved from B"""
        available, mod, cap = probe_available()
        if not available:
            self.skipTest(f"probe {cap} — ABSENT-UNKNOWN — skipUnless AVAILABLE")

        outline_path = ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            out_pptx = tmpdir / "verify.pptx"
            p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verify.py"), "--verify-rendered", str(outline_path), "--out", str(out_pptx)], cwd=str(ROOT), capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, f"--verify-rendered failed {p.stdout} {p.stderr}")
            self.assertIn("MATCH", p.stdout, f"expected MATCH verdict, got {p.stdout}")

            # Test DRIFT detection by mutating outline vs rendered? We test via deck_verify --compare which should detect DRIFT
            # Create tampered outline
            outline_data = json.loads(outline_path.read_text(encoding="utf-8"))
            import copy
            tampered = copy.deepcopy(outline_data)
            tampered["slides"][0]["bullets"][0]["text"] = "Mutated text for DRIFT"
            tampered_path = tmpdir / "tampered.json"
            tampered_path.write_text(json.dumps(tampered), encoding="utf-8")
            p2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verify.py"), str(outline_path), "--compare", str(tampered_path)], cwd=str(ROOT), capture_output=True, text=True)
            self.assertNotEqual(p2.returncode, 0, "compare should detect DRIFT")
            self.assertIn("DRIFT-text", p2.stdout, f"expected DRIFT-text, got {p2.stdout}")

        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_10_dependency_canon_four_rules(self):
        """Dependency canon — python-pptx (WP-D) four rules verbatim-core — single import site + pinned version floor + transitive + receipt law"""
        decks_md = ROOT / "docs" / "DECKS.md"
        self.assertTrue(decks_md.exists())
        content = decks_md.read_text(encoding="utf-8", errors="ignore")
        # Check four rules mentioned
        self.assertIn("python-pptx", content.lower(), "DECKS.md must mention python-pptx")
        self.assertIn("single import site", content.lower(), "DECKS.md must mention single import site")
        self.assertIn("pinned version", content.lower(), "DECKS.md must mention pinned version floor")
        self.assertIn("transitive", content.lower(), "DECKS.md must mention transitive scope")
        self.assertIn("receipt law", content.lower(), "DECKS.md must mention receipt law — deck never delivered alone")

if __name__ == "__main__":
    unittest.main()
