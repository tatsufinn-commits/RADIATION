#!/usr/bin/env python3
"""T5 — check 1 reports the complete unresolved-path list (no bad[:6] truncation)."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate as V  # noqa: E402

SEVEN = [
    "missing/one.md",
    "missing/two.md",
    "missing/three.md",
    "missing/four.md",
    "missing/five.md",
    "missing/six.md",
    "missing/seven.md",
]


class TestValidateCheck1FullDiagnostics(unittest.TestCase):
    def setUp(self):
        self._root = V.ROOT
        self._is_ex = V.IS_EX
        self._results = list(V.RESULTS)
        self._tmpdir = tempfile.TemporaryDirectory()
        tmp = self._tmpdir.name
        (Path(tmp) / "probe.md").write_text(
            "\n".join(f"`{p}`" for p in SEVEN) + "\n",
            encoding="utf-8",
        )

        def _no_ex(path):
            return False

        _no_ex.paths = set()
        V.ROOT = tmp
        V.IS_EX = _no_ex
        V.RESULTS = []

    def tearDown(self):
        V.ROOT = self._root
        V.IS_EX = self._is_ex
        V.RESULTS = self._results
        self._tmpdir.cleanup()

    def test_check1_reports_all_seven_unresolved_internal_md_refs(self):
        V.c1()
        c1 = next(r for r in V.RESULTS if r["check"] == 1)
        self.assertFalse(c1["ok"])
        self.assertEqual(c1["severity"], "FAIL")
        msg = c1["msg"]
        for ident in SEVEN:
            self.assertIn(ident, msg, f"truncated or missing {ident} in: {msg}")
        self.assertIn("missing/seven.md", msg)


if __name__ == "__main__":
    unittest.main()
