#!/usr/bin/env python3
"""Tests for scripts/verify_cassette_runner.py — WP-2.3 verify cassette runner.

Vectors: row-shape · all-five-PASS at writing · seed-name identity ·
verdict mapping · hermetic/stdin-free guarantee (+ self-test battery).
"""
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_cassette_runner as R  # noqa: E402

CASSETTE_PATH = os.path.join(ROOT, "evals", "verify_policies", "CASSETTE_WP23.json")
SEED_TRACES = {
    "WP-2.3-cassette-seed-required-SUB-001": "trace_required.json",
    "WP-2.3-cassette-seed-opt-in-SUB-002": "trace_opt_in.json",
    "WP-2.3-cassette-seed-opt-out-SUB-003": "trace_opt_out.json",
}


class TestVerifyCassetteRunner(unittest.TestCase):

    def setUp(self):
        with open(CASSETTE_PATH, encoding="utf-8") as fh:
            self.cassette = json.load(fh)
        self.rows = self.cassette["rows"]

    def test_row_shape(self):
        """Design B3: five rows, each id · question · expected · runner · verdict."""
        self.assertEqual(len(self.rows), 5)
        for row in self.rows:
            self.assertEqual(R.row_shape_findings(row), [], row.get("id"))
            self.assertIn(row["verdict"], R.VERDICTS)
            self.assertIn(row["runner"], R.RUNNERS)
        self.assertEqual(tuple(r["id"] for r in self.rows), R.EXPECTED_ROW_IDS)

    def test_all_five_pass_at_writing(self):
        results = R.run_cassette()
        self.assertEqual([r["verdict"] for r in results], ["PASS"] * 5,
                         [r["justification"] for r in results])
        self.assertEqual(R.summary_line(results), "verify cassette: 5/5 rows PASS")
        for row, res in zip(self.rows, results):
            self.assertEqual(res["verdict"], row["expected"])

    def test_seed_name_identity(self):
        """J1: the three seed rows consume the WP-1 traces by name — never rebuilt."""
        seed_rows = [r for r in self.rows if r["runner"] == "seed_trace"]
        self.assertEqual({r["id"] for r in seed_rows}, set(SEED_TRACES))
        for row in seed_rows:
            fname = SEED_TRACES[row["id"]]
            self.assertEqual(row["target"], f"evals/verify_policies/{fname}")
            with open(os.path.join(ROOT, row["target"]), encoding="utf-8") as fh:
                trace = json.load(fh)
            self.assertEqual(trace["cassette_seed"], row["id"])
            self.assertEqual(trace["verify"]["seed"], row["id"])
            self.assertEqual(trace["policy_class"], row["policy_class"])

    def test_verdict_mapping(self):
        self.assertEqual(R.map_verdict([]), ("PASS", "all deterministic checks held"))
        self.assertEqual(R.map_verdict(["a", "b"]), ("WARN-and-justify", "a; b"))
        bad_shape = {"id": "x", "expected": "PASS", "runner": "seed_trace", "verdict": "PASS"}
        self.assertEqual(R.evaluate_row(bad_shape)[0], "RETURNED")
        unknown = dict(bad_shape, question="q", runner="behavioral_grader")
        self.assertEqual(R.evaluate_row(unknown)[0], "RETURNED")
        bad_enum = dict(unknown, runner="seed_trace", verdict="FAIL")
        self.assertEqual(R.evaluate_row(bad_enum)[0], "RETURNED")
        drift = dict(self.rows[0], id="WP-2.3-cassette-seed-renamed")
        self.assertEqual(R.evaluate_row(drift)[0], "WARN-and-justify")

    def test_hermetic_stdin_free(self):
        """stdlib-only, no network imports, runs with stdin closed, writes nothing."""
        with open(os.path.join(ROOT, "scripts", "verify_cassette_runner.py"),
                  encoding="utf-8") as fh:
            src = fh.read()
        for banned in ("import urllib", "import socket", "import http", "import requests",
                       "from urllib", "from http", "input(", "sys.stdin"):
            self.assertNotIn(banned, src)
        before = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                                capture_output=True, text=True).stdout
        r = subprocess.run([sys.executable, "scripts/verify_cassette_runner.py"],
                           cwd=ROOT, capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("verify cassette: 5/5 rows PASS", r.stdout)
        after = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True).stdout
        self.assertEqual(before, after)

    def test_self_test_battery(self):
        r = subprocess.run([sys.executable, "scripts/verify_cassette_runner.py", "--self-test"],
                           cwd=ROOT, capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("-> FAIL", r.stdout)


if __name__ == "__main__":
    unittest.main()
