"""5500-closure Step 1 — replica tranche authority must be VISIBLE.

The 12 declared replica pairs are admitted while their ratification record
reads `commander-review-requested`. That state may never be indistinguishable
from a ratified PASS: validate must surface an OPEN GOVERNED EXCEPTION, and
the decision options must exist for the Commander. Fail-closed: a missing
ratification record is also open. Nobody self-ratifies.
"""
import importlib.util
import os
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load_validate():
    spec = importlib.util.spec_from_file_location(
        "radiation_validate", ROOT / "scripts" / "validate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestReplicaAuthority(unittest.TestCase):
    def test_01_decision_predicate_is_fail_closed(self):
        v = _load_validate()
        self.assertTrue(v._replica_open_exception("commander-review-requested"))
        self.assertTrue(v._replica_open_exception(None))
        self.assertTrue(v._replica_open_exception(""))
        self.assertTrue(v._replica_open_exception("ratified"))  # near-miss token
        self.assertFalse(v._replica_open_exception("commander-ratified"))

    @unittest.skipIf(
        os.environ.get("RADIATION_VALIDATION_CTX"),
        "validate.py is this suite's parent process — spawning it again is the "
        "validate→harness→validate recursion, not a test; run the suite "
        "directly for the live-output assertion")
    def test_02_live_validate_surfaces_the_open_exception(self):
        out = subprocess.run(
            ["python3", "scripts/validate.py"], capture_output=True,
            text=True, cwd=ROOT, stdin=subprocess.DEVNULL, timeout=600)
        self.assertEqual(out.returncode, 0)
        self.assertIn("OPEN GOVERNED EXCEPTION", out.stdout)
        self.assertIn("commander-review-requested", out.stdout)
        self.assertIn("11.6", out.stdout)

    def test_03_decision_brief_lists_every_declared_pair(self):
        import json
        manifest = json.loads(
            (ROOT / "scaffolding/neurons/REPLICA_MANIFEST.json").read_text())
        doc = (ROOT / "docs/REPLICA_DECISION.md").read_text(encoding="utf-8")
        self.assertIn("open governed exception", doc)
        for pair in manifest["pairs"]:
            self.assertIn(pair["canonical_path"], doc)
            self.assertIn(pair["replica_path"], doc)
        self.assertIn("Option A", doc)
        self.assertIn("Option B", doc)
        self.assertIn("No option deletes anything", doc)

    def test_04_no_self_ratification(self):
        import json
        manifest = json.loads(
            (ROOT / "scaffolding/neurons/REPLICA_MANIFEST.json").read_text())
        self.assertEqual(
            manifest["ratification"]["status"], "commander-review-requested",
            "an Architect must never flip ratification without a Commander order")


if __name__ == "__main__":
    unittest.main()
