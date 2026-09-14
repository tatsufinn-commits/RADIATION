#!/usr/bin/env python3
"""Hostile retrieved-content fixtures — 5500 gate review §3.2, reframed 5600.

What these tests PROVE (exactly): the deterministic consumers in this repo —
the control-plane policy resolver and the PASS handoff — are unaffected by
hostile fixture content, and a fixture carried inside an evidence bundle is
validated as plain data with zero findings. Their behavior is structural
(code paths that read no retrieved text cannot be injected through it).

What these tests do NOT prove: injection resistance of a retrieval/cue
selection pipeline. No such resolver consumes these fixtures yet — that
evaluation is the future content-selection contract specified in
evals/README.md, and it must be proven by that resolver, never simulated here.

Fixtures are synthetic and inert: no real personal data, no real credentials,
and the P-09 trigger string appears NOWHERE (standing law).
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

HOSTILE_DIR = os.path.join(ROOT, "evals", "hostile")
FIXTURES = [
    "injected_course_derivative.md",
    "imported_text_html.md",
    "tool_result_shaped.json",
    "subagent_result_shaped.json",
]


class FixtureInventory(unittest.TestCase):
    def test_all_fixtures_exist_labeled_synthetic_p09_free(self):
        p09 = "PERMANENT DIRECTIVE OVERRIDE"  # no substring of the P-09 string
        for name in FIXTURES:
            p = os.path.join(HOSTILE_DIR, name)
            self.assertTrue(os.path.isfile(p), f"hostile fixture missing: {name}")
            text = open(p, encoding="utf-8").read()
            self.assertIn("FIXTURE NOTICE", text, f"{name} must be labeled synthetic")
            self.assertIn("forged", text.lower(), f"{name} must carry its forged marker")
            self.assertNotIn(p09, text, "P-09 trigger material must never exist")


class DeterministicConsumersStayInert(unittest.TestCase):
    def test_control_plane_decisions_invariant_under_fixture_content(self):
        """The policy resolver reads NO retrieved content: outcomes are
        identical whether or not hostile text exists in the tree."""
        from radiation_core import control_plane as cp
        d = cp.resolve("canonical_apply", "commander_order", "TID-2026-01-01-eval")
        self.assertEqual(d["status"], "commander_motor_act")
        self.assertIsNone(d["tool"], "no tool may bind to canonical_apply — fixture or not")
        r = cp.resolve("workspace_draft", "session_initiative", "TID-2026-01-01-eval")
        self.assertEqual(r["status"], "refused", "session initiative must stay insufficient")

    def test_pass_handoff_remains_claim_free_with_fixture_present(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "radiation_pass", os.path.join(ROOT, "agents", "_common", "radiation_pass.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out = mod.run_pass("Arena Agent Mode", ROOT)
        blob = (str(out) + "".join(
            open(os.path.join(HOSTILE_DIR, f), encoding="utf-8").read()
            for f in FIXTURES)).lower()
        self.assertEqual(out["honesty_selfcheck"], "clean")
        for claim in ("i can commit", "i can push", "my push access"):
            self.assertNotIn(claim, blob)

    def test_hostile_content_inside_an_evidence_bundle_is_plain_data(self):
        """A real content-consuming deterministic path: relay validates a
        bundle whose evidence files ARE the hostile fixtures. Expected: zero
        findings — directives in data execute nowhere."""
        from radiation_core import relay
        root = tempfile.mkdtemp(prefix="radiation_hostile_bundle_")
        try:
            tid = "TID-2026-01-01-hx"
            d = os.path.join(root, "evidence", "tasks", tid)
            os.makedirs(os.path.join(d, "commands"))
            os.makedirs(os.path.join(d, "outcomes"))
            os.makedirs(os.path.join(d, "artifacts"))
            task = {"task_id": tid, "title": "hostile fixture carrier",
                    "status": "completed", "date": "2026-01-01",
                    "base_revision": "a" * 40}
            json.dump(task, open(os.path.join(d, "task.json"), "w"))
            for name in FIXTURES:
                shutil.copy(os.path.join(HOSTILE_DIR, name),
                            os.path.join(d, "artifacts", name))
            env = {"task_id": tid, "base_revision": "a" * 40, "date": "2026-01-01"}
            json.dump(env, open(os.path.join(d, "envelope.json"), "w"))
            findings = relay.validate_active(
                neurons_dir=os.path.join(root, "scaffolding", "neurons"),
                evid_dir=os.path.join(root, "evidence", "tasks"))
            hostile_findings = [f for f in findings if tid in str(f)]
            self.assertEqual(hostile_findings, [],
                             f"fixture data must validate as plain data: {hostile_findings}")
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
