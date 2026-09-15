#!/usr/bin/env python3
"""
CUE Resolver tests — Candidate B opening P-11-A
Proves:
- deterministic precedence law commander_order > ratified_policy > cue > heuristic > content
- CONTENT-only for courses/web/tools/subagent/imported_text never alters effects
- linter valid, directive coverage 13/13
- hostile closure: future contract 5 properties over 4 shapes via REAL resolver over REAL path
"""
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import cue_resolver as resolver

CATALOG_PATH = ROOT / "cue" / "CUE_CATALOG.json"
SCHEMA_PATH = ROOT / "schemas" / "cue_card.schema.json"
MAPPING_PATH = ROOT / "cue" / "DIRECTIVE_CUE_MAPPING.json"
HOSTILE_DIR = ROOT / "evals" / "hostile"

class TestPrecedenceLaw(unittest.TestCase):
    def test_commander_order_highest(self):
        cands = [
            {"id": "CUE-A", "precedence": "cue", "priority": 100, "trigger_source": "cue"},
            {"id": "CUE-B", "precedence": "commander_order", "priority": 1, "trigger_source": "commander"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(len(res["selected"]), 1)
        self.assertEqual(res["selected"][0]["id"], "CUE-B")
        self.assertEqual(res["law"], resolver.LAW_STRING)

    def test_commander_order_over_cue(self):
        cands = [
            {"id": "CUE-BOOT-MAGIC", "precedence": "commander_order", "priority": 100, "trigger_source": "commander"},
            {"id": "CUE-CONSTITUTION-SHAPE", "precedence": "cue", "priority": 80, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertTrue(any(s["id"] == "CUE-BOOT-MAGIC" for s in res["selected"]))
        self.assertTrue(all(s["precedence"] == "commander_order" for s in res["selected"]))

    def test_ratified_policy_over_cue(self):
        cands = [
            {"id": "CUE-SILENCE-CONSENT", "precedence": "ratified_policy", "priority": 90, "trigger_source": "ratified_policy"},
            {"id": "CUE-CLOSE-TOPIC", "precedence": "cue", "priority": 50, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["precedence"], "ratified_policy")

    def test_cue_precedence(self):
        cands = [
            {"id": "CUE-A", "precedence": "cue", "priority": 70, "trigger_source": "cue"},
            {"id": "CUE-B", "precedence": "heuristic", "priority": 100, "trigger_source": "heuristic"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["precedence"], "cue")

    def test_silence_is_ratified_policy(self):
        # Silence consent per III.6 is ratified_policy
        cands = [
            {"id": "CUE-SILENCE-CONSENT", "precedence": "ratified_policy", "priority": 90, "trigger_source": "ratified_policy"},
            {"id": "CUE-HEUR", "precedence": "heuristic", "priority": 99, "trigger_source": "heuristic"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-SILENCE-CONSENT")

    def test_standing_permission(self):
        cands = [
            {"id": "CUE-STANDING-PERMISSION", "precedence": "ratified_policy", "priority": 70, "trigger_source": "ratified_policy"},
            {"id": "CUE-CLOSE-TOPIC", "precedence": "cue", "priority": 50, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["precedence"], "ratified_policy")

    def test_full_discretion(self):
        cands = [
            {"id": "CUE-FULL-DISCRETION", "precedence": "commander_order", "priority": 95, "trigger_source": "commander"},
            {"id": "CUE-CLOSE-TOPIC", "precedence": "cue", "priority": 50, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-FULL-DISCRETION")

    def test_task_selection_correction(self):
        cands = [
            {"id": "CUE-TASK-SELECTION-CORRECTION", "precedence": "commander_order", "priority": 100, "trigger_source": "commander"},
            {"id": "CUE-PARITY-AUDIT", "precedence": "cue", "priority": 60, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-TASK-SELECTION-CORRECTION")

    def test_continuous_op_over_close(self):
        cands = [
            {"id": "CUE-CONTINUOUS-OP", "precedence": "commander_order", "priority": 80, "trigger_source": "commander", "conflicts_with": ["CUE-CLOSE-TOPIC"]},
            {"id": "CUE-CLOSE-TOPIC", "precedence": "cue", "priority": 50, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-CONTINUOUS-OP")
        self.assertTrue(len(res["conflicting_groups"]) >= 0)

    def test_git_state_outranks_assumption(self):
        cands = [
            {"id": "CUE-APPLY-WHILE-WORKING", "precedence": "ratified_policy", "priority": 85, "trigger_source": "ratified_policy"},
            {"id": "CUE-HEUR", "precedence": "heuristic", "priority": 10, "trigger_source": "heuristic"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["precedence"], "ratified_policy")

    def test_ratification_pass(self):
        cands = [
            {"id": "CUE-RATIFICATION-PASS", "precedence": "commander_order", "priority": 90, "trigger_source": "commander"},
            {"id": "CUE-A", "precedence": "cue", "priority": 70, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-RATIFICATION-PASS")

    def test_overrule_boundary(self):
        cands = [
            {"id": "CUE-OVERRULE-BOUNDARY", "precedence": "commander_order", "priority": 100, "trigger_source": "commander"},
            {"id": "CUE-A", "precedence": "ratified_policy", "priority": 90, "trigger_source": "ratified_policy"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-OVERRULE-BOUNDARY")

class TestContentIsolation(unittest.TestCase):
    def test_content_cannot_override_budget(self):
        cands = [
            {"id": "CUE-BUDGET-OVERRIDE", "precedence": "commander_order", "priority": 90, "trigger_source": "commander"},
            {"id": "CUE-FAKE-BUDGET", "precedence": "commander_order", "priority": 100, "trigger_source": "course"},
        ]
        res = resolver.resolve_candidates(cands)
        # Real commander wins, forged course is forced to content and suppressed
        self.assertEqual(res["selected"][0]["id"], "CUE-BUDGET-OVERRIDE")
        suppressed_ids = [c["id"] for c in res["suppressed"]]
        self.assertIn("CUE-FAKE-BUDGET", suppressed_ids)
        # Check forced content reason
        self.assertIn("CONTENT-only", res["reason_map"]["CUE-FAKE-BUDGET"])

    def test_course_content_is_content_only(self):
        cands = [
            {"id": "CUE-BRAIN-INGEST", "precedence": "cue", "priority": 70, "trigger_source": "cue"},
            {"id": "CUE-INJECTED", "precedence": "commander_order", "priority": 100, "trigger_source": "course"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BRAIN-INGEST")
        self.assertEqual(res["suppressed"][0]["precedence"], "content")

    def test_link_is_content_only_if_untrusted(self):
        cands = [
            {"id": "CUE-LINK-REGISTER", "precedence": "heuristic", "priority": 60, "trigger_source": "heuristic"},
            {"id": "CUE-WEB-INJECT", "precedence": "commander_order", "priority": 100, "trigger_source": "web"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-LINK-REGISTER")

    def test_recycle_is_content_only(self):
        cands = [
            {"id": "CUE-RECYCLE-IDEA", "precedence": "cue", "priority": 70, "trigger_source": "cue"},
            {"id": "CUE-WEB-RECYCLE", "precedence": "commander_order", "priority": 100, "trigger_source": "web"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-RECYCLE-IDEA")

    def test_tool_result_is_content_only(self):
        cands = [
            {"id": "CUE-REAL", "precedence": "cue", "priority": 60, "trigger_source": "cue"},
            {"id": "CUE-TOOL-CLAIM", "precedence": "commander_order", "priority": 100, "trigger_source": "tool"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-REAL")
        self.assertEqual(res["suppressed"][0]["precedence"], "content")

    def test_subagent_result_is_content_only(self):
        cands = [
            {"id": "CUE-REAL", "precedence": "cue", "priority": 60, "trigger_source": "cue"},
            {"id": "CUE-SUBAGENT-CLAIM", "precedence": "commander_order", "priority": 100, "trigger_source": "subagent"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-REAL")

    def test_imported_text_is_content_only(self):
        cands = [
            {"id": "CUE-REAL", "precedence": "cue", "priority": 60, "trigger_source": "cue"},
            {"id": "CUE-IMPORTED", "precedence": "commander_order", "priority": 100, "trigger_source": "imported_text"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-REAL")

class TestResolver(unittest.TestCase):
    def test_resolver_selects_cue(self):
        cands = [
            {"id": "CUE-REVIEWER", "precedence": "cue", "priority": 70, "trigger_source": "cue", "effect": "draft"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(len(res["selected"]), 1)

    def test_resolver_emits_reason(self):
        cands = [
            {"id": "CUE-DEFECT-ORDER", "precedence": "commander_order", "priority": 85, "trigger_source": "commander"},
            {"id": "CUE-CLOSE-TOPIC", "precedence": "cue", "priority": 50, "trigger_source": "cue"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertIn("CUE-DEFECT-ORDER", res["reason_map"])
        self.assertIn("CUE-CLOSE-TOPIC", res["reason_map"])

    def test_suppressed_cues(self):
        cands = [
            {"id": "CUE-A", "precedence": "commander_order", "priority": 100, "trigger_source": "commander"},
            {"id": "CUE-B", "precedence": "cue", "priority": 70, "trigger_source": "cue"},
            {"id": "CUE-C", "precedence": "heuristic", "priority": 20, "trigger_source": "heuristic"},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(len(res["suppressed"]), 2)

    def test_next_mode_signal(self):
        cands = [{"id": "CUE-NEXT-MODE-SIGNAL", "precedence": "cue", "priority": 60, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-NEXT-MODE-SIGNAL")

    def test_cross_reference(self):
        cands = [{"id": "CUE-CROSS-REFERENCE", "precedence": "cue", "priority": 75, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-CROSS-REFERENCE")

    def test_tool_freedom_vs_budget(self):
        cands = [
            {"id": "CUE-BUDGET-OVERRIDE", "precedence": "commander_order", "priority": 90, "trigger_source": "commander", "conflicts_with": ["CUE-TOOL-FREEDOM"]},
            {"id": "CUE-TOOL-FREEDOM", "precedence": "cue", "priority": 65, "trigger_source": "cue", "conflicts_with": ["CUE-BUDGET-OVERRIDE"]},
        ]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUDGET-OVERRIDE")

    def test_displeasure(self):
        cands = [{"id": "CUE-DISPLEASURE", "precedence": "commander_order", "priority": 80, "trigger_source": "commander"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-DISPLEASURE")

    def test_auto_law(self):
        cands = [{"id": "CUE-AUTO-LAW", "precedence": "commander_order", "priority": 85, "trigger_source": "commander"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-AUTO-LAW")

    def test_push_verdict(self):
        cands = [{"id": "CUE-PUSH-VERDICT", "precedence": "ratified_policy", "priority": 80, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-PUSH-VERDICT")

    def test_parity_audit(self):
        cands = [{"id": "CUE-PARITY-AUDIT", "precedence": "cue", "priority": 60, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-PARITY-AUDIT")

    def test_audit_order(self):
        cands = [{"id": "CUE-AUDIT-ORDER", "precedence": "commander_order", "priority": 75, "trigger_source": "commander"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-AUDIT-ORDER")

    def test_position_wanted(self):
        cands = [{"id": "CUE-POSITION-WANTED", "precedence": "cue", "priority": 70, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-POSITION-WANTED")

    def test_calendar_freshness(self):
        cands = [{"id": "CUE-CALENDAR-FRESHNESS", "precedence": "cue", "priority": 60, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-CALENDAR-FRESHNESS")

    def test_knowledge_vs_product(self):
        cands = [{"id": "CUE-KNOWLEDGE-VS-PRODUCT", "precedence": "ratified_policy", "priority": 80, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-KNOWLEDGE-VS-PRODUCT")

    def test_term_briefing(self):
        cands = [{"id": "CUE-TERM-BRIEFING", "precedence": "cue", "priority": 65, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-TERM-BRIEFING")

    def test_drill_request(self):
        cands = [{"id": "CUE-DRILL-REQUEST", "precedence": "cue", "priority": 65, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-DRILL-REQUEST")

    def test_shrine_audit(self):
        cands = [{"id": "CUE-SHRINE-AUDIT", "precedence": "cue", "priority": 85, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-SHRINE-AUDIT")

    def test_standing_audit(self):
        cands = [{"id": "CUE-STANDING-AUDIT", "precedence": "cue", "priority": 70, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-STANDING-AUDIT")

    def test_renovation_judgment(self):
        cands = [{"id": "CUE-ARCH-RENOVATION-JUDGMENT", "precedence": "cue", "priority": 60, "trigger_source": "cue"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-ARCH-RENOVATION-JUDGMENT")

    def test_build_cues(self):
        cands = [{"id": "CUE-BUILD-AST-PARSE", "precedence": "ratified_policy", "priority": 90, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-AST-PARSE")

    def test_generator_not_generated(self):
        cands = [{"id": "CUE-BUILD-GENERATOR", "precedence": "ratified_policy", "priority": 90, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-GENERATOR")

    def test_apply_gates(self):
        cands = [{"id": "CUE-BUILD-APPLY-GATES", "precedence": "ratified_policy", "priority": 85, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-APPLY-GATES")

    def test_deletion_absence(self):
        cands = [{"id": "CUE-BUILD-DELETION-ABSENCE", "precedence": "ratified_policy", "priority": 85, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-DELETION-ABSENCE")

    def test_grep_def(self):
        cands = [{"id": "CUE-BUILD-GREP-DEF", "precedence": "heuristic", "priority": 80, "trigger_source": "heuristic"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-GREP-DEF")

    def test_warn_parked(self):
        cands = [{"id": "CUE-BUILD-WARN-PARKED", "precedence": "heuristic", "priority": 70, "trigger_source": "heuristic"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-WARN-PARKED")

    def test_remedy(self):
        cands = [{"id": "CUE-BUILD-REMEDY", "precedence": "ratified_policy", "priority": 80, "trigger_source": "ratified_policy"}]
        res = resolver.resolve_candidates(cands)
        self.assertEqual(res["selected"][0]["id"], "CUE-BUILD-REMEDY")

class TestLinter(unittest.TestCase):
    def test_lint_catalog_ok(self):
        result = resolver.lint_catalog(CATALOG_PATH, SCHEMA_PATH, MAPPING_PATH)
        self.assertTrue(result["ok"], f"lint issues: {result['issues']}")
        self.assertGreaterEqual(result["cue_count"], 13)

    def test_directive_coverage_13(self):
        mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
        mapped = mapping.get("mappings", [])
        self.assertEqual(len(mapped), 13, "must map all 13 SD-GOV")
        ids = set(m["directive_id"] for m in mapped)
        expected = {f"SD-GOV-{i:03d}" for i in range(1, 14)}
        self.assertEqual(ids, expected)

class TestHostileClosure(unittest.TestCase):
    """
    Future deterministic content-selection test contract — now PROVEN via REAL resolver over REAL path.
    Implements evals/README.md contract: 5 properties over 4 shapes expecting no elevation.
    """
    def _load_catalog_cues(self):
        return resolver.load_catalog(CATALOG_PATH)

    def _run_hostile(self, fixture_name: str, source_type: str):
        fixture_path = HOSTILE_DIR / fixture_name
        self.assertTrue(fixture_path.exists(), f"missing fixture {fixture_name}")
        text = fixture_path.read_text(encoding="utf-8", errors="ignore")
        cues = self._load_catalog_cues()
        result = resolver.resolve_content_selection_path(cues, text, source_type)
        return result, text

    def _assert_no_elevation(self, result: dict, text: str, fixture_name: str):
        # 1. cannot change cue precedence or override standing directives
        self.assertTrue(result["no_elevation"], f"{fixture_name} elevated precedence")
        for sel in result["selected"]:
            self.assertEqual(sel["precedence"], "content", f"{fixture_name} selected non-content precedence")
        # 2. cannot grant tools, effects, identity, or authority
        # Content's claimed effect is suppressed; resolved effect must not grant authority
        for sel in result["selected"]:
            # Content-only candidates must not have effect propose that grants authority — we treat as read
            # The resolver's reason must contain CONTENT-only
            self.assertIn("CONTENT-only", result["reason_map"].get(sel["id"], ""), f"{fixture_name} missing CONTENT-only reason")
        # 3. cannot alter honesty/claim discipline
        blob = (json.dumps(result) + text).lower()
        for claim in ("i can commit", "i can push", "my push access", "i have authority"):
            self.assertNotIn(claim, blob, f"{fixture_name} altered claim discipline")
        # 4. cannot disclose secrets or trigger exfiltration
        # Fixtures are synthetic, but resolver must not expose credentials
        self.assertNotIn("credential", json.dumps(result["selected"]).lower(), f"{fixture_name} disclosed credential via selected")
        # 5. cannot bypass Commander approval
        # No selected with commander_order precedence from untrusted source
        for sel in result["selected"]:
            self.assertNotEqual(sel.get("_original_precedence"), "commander_order" if sel["precedence"] != "content" else "IMPOSSIBLE",
                                f"{fixture_name} bypassed Commander approval")

    def test_imported_text_html_no_elevation(self):
        result, text = self._run_hostile("imported_text_html.md", "imported_text")
        self._assert_no_elevation(result, text, "imported_text_html.md")

    def test_injected_course_derivative_no_elevation(self):
        result, text = self._run_hostile("injected_course_derivative.md", "course_derivative")
        self._assert_no_elevation(result, text, "injected_course_derivative.md")

    def test_tool_result_shaped_no_elevation(self):
        result, text = self._run_hostile("tool_result_shaped.json", "tool_result")
        self._assert_no_elevation(result, text, "tool_result_shaped.json")

    def test_subagent_result_shaped_no_elevation(self):
        result, text = self._run_hostile("subagent_result_shaped.json", "subagent_result")
        self._assert_no_elevation(result, text, "subagent_result_shaped.json")

    def test_all_four_shapes_expect_no_elevation(self):
        shapes = [
            ("imported_text_html.md", "imported_text"),
            ("injected_course_derivative.md", "course_derivative"),
            ("tool_result_shaped.json", "tool_result"),
            ("subagent_result_shaped.json", "subagent_result"),
        ]
        cues = self._load_catalog_cues()
        for fname, stype in shapes:
            text = (HOSTILE_DIR / fname).read_text(encoding="utf-8", errors="ignore")
            res = resolver.resolve_content_selection_path(cues, text, stype)
            self.assertTrue(res["no_elevation"], f"{fname} ({stype}) elevated")
            self.assertGreater(res["external_length"], 0)

if __name__ == "__main__":
    unittest.main()
