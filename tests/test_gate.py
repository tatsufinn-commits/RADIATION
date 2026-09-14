#!/usr/bin/env python3
"""5500 gate review — the discoverable unit-test harness.

Zero-test discovery is an explicit failure (validate check 39). These tests
wrap the deep CLI self-tests as subprocess gates and add direct unit probes
over the 5300/5500 contract cores and the 5500 control-plane semantics.
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))


class DeepSelfTests(unittest.TestCase):
    """Every shipped tool's own vector suite, gated from the harness."""

    def _run(self, args):
        import subprocess
        r = subprocess.run([sys.executable] + args, cwd=ROOT,
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(r.returncode, 0, (r.stdout + r.stderr)[-900:])
        return r.stdout

    def test_relay_self_test(self):
        out = self._run(["-m", "radiation_core.relay", "--self-test"])
        self.assertIn("23/23", out)

    def test_control_plane_self_test(self):
        out = self._run(["-m", "radiation_core.control_plane", "--self-test"])
        self.assertIn("38/38", out)

    def test_radiation_pass_self_test(self):
        out = self._run([os.path.join("agents", "_common", "radiation_pass.py"),
                         "--self-test"])
        self.assertIn("16/16", out)

    def test_contract_tests(self):
        out = self._run(["scripts/contract_tests.py"])
        self.assertIn("11/11", out)

    def test_verify_apply_self_test(self):
        self._run(["scripts/verify_apply.py", "--self-test"])

    def test_cap_verify_self_test(self):
        self._run(["scripts/cap_verify.py", "--self-test"])

    def test_cap_probe_self_test(self):
        self._run(["scripts/cap_probe.py", "--self-test"])


class DirectUnits(unittest.TestCase):
    """Fast in-process probes over the factored cores (no subprocess)."""

    def test_plan_version_numeric(self):
        from radiation_core.relay import _plan_version
        self.assertLess(_plan_version("plan.v2.json"), _plan_version("plan.v10.json"))
        self.assertEqual(_plan_version("plan.json"), 0)
        self.assertEqual(_plan_version("plan.v3.json"), 3)

    def test_schema_rejects_bad_task_id(self):
        from radiation_core.relay import _schema_check
        out: list[str] = []
        _schema_check({"type": "execution", "task_id": "../not-a-task",
                       "payload": {"v": 2}, "digest": "x"},
                      "control_receipt.schema.json", "u", out)
        self.assertTrue(any("oneOf" in x for x in out))

    def test_corpus_cores_exist_and_run(self):
        import tempfile
        import validate as V
        with tempfile.TemporaryDirectory() as tmp:
            bad, declared = V._corpus_contract_violations(tmp)
            self.assertTrue(any("missing" in b for b in bad))
            self.assertEqual(declared, set())

    def test_control_plane_transactional_semantics_available(self):
        from radiation_core import control_plane as cp
        self.assertTrue(callable(cp.verify_chain))
        self.assertTrue(callable(cp.execute_draft))


if __name__ == "__main__":
    unittest.main()
