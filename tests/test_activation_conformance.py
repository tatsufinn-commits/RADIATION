#!/usr/bin/env python3
"""Contract and limitation regressions for MAS-SCAN-NOTES revision 1.

Target tests for scripts/activation_conformance.py: the six-value truth boundary,
sole custody selection, the UNKNOWN default, and every limitation the contract
document discloses. These tests exercise FIXTURE records only; a fixture can prove
a shape, never a live authenticated disposition, a caller identity, or a permission.
"""
import ast
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import activation_conformance as A  # noqa: E402


def live_custody():
    with open(ROOT / A.CUSTODY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def mutant(**changes):
    obj = copy.deepcopy(live_custody())
    for dotted, value in changes.items():
        node = obj
        parts = dotted.split("__")
        for part in parts[:-1]:
            node = node[part]
        node[parts[-1]] = value
    return obj


def fixture(custody=None, **changes):
    return A.declaration_fixture(custody or live_custody(), **changes)


class TestActivationConformance(unittest.TestCase):

    def test_01_live_custody_plus_bound_declaration_is_satisfied(self):
        receipt = A.evaluate(fixture())
        self.assertEqual(receipt["result"], "SATISFIED")
        self.assertEqual(A._schema_findings(receipt, "receipt"), [])
        self.assertEqual(receipt["custody_path"], A.CUSTODY_PATH)
        self.assertEqual(receipt["persisted"], False)
        self.assertEqual(receipt["authority"], "none")
        self.assertEqual(receipt["authentication"], "none")
        self.assertEqual(set(receipt["limits"]), set(A.LIMITS))
        self.assertIn("structural conformance only", " ".join(receipt["reasons"]))

    def test_02_absent_empty_and_placeholder_notes_are_missing(self):
        for value, present in ((None, False), ("", True), ("   \n\t", True), ("none", True),
                               ("N/A", True), ("—", True)):
            with self.subTest(value=value, present=present):
                self.assertEqual(A.evaluate(fixture(value=value, present=present))["result"],
                                 "MISSING")

    def test_03_false_predicate_is_not_applicable(self):
        receipt = A.evaluate(fixture(), custody_obj=mutant(declaration__declaration_required=False))
        self.assertEqual(receipt["result"], "NOT APPLICABLE")

    def test_04_malformed_and_unknown_custody_are_unknown(self):
        self.assertEqual(A.evaluate(fixture(), custody_obj={"schema_name": "wrong"})["result"],
                         "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            validity={"state": "UNKNOWN", "invalidated_reason": None}))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            context__cutoff_recorded_on="2026-02-31"))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=None, root=str(ROOT / "no-such-root"))["result"],
                         "UNKNOWN")

    def test_05_stale_or_mismatched_custody_digests_are_unknown(self):
        original = live_custody()["digests"]
        for field in ("rule_digest_sha256", "contract_digest_sha256"):
            with self.subTest(field=field):
                digests = dict(original, **{field: "0" * 64})
                self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(digests=digests))["result"],
                                 "UNKNOWN")

    def test_06_missing_or_disallowed_history_is_unknown(self):
        self.assertEqual(A.evaluate(dict(fixture(), history=None))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(history={
            "basis": "declared-by-supplier",
            "entries": [{"result": "SATISFIED", "persisted": True}]}))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(history={
            "basis": "declared-by-supplier",
            "entries": [{"result": "COMMANDER DISPOSITION", "persisted": False}]}))["result"],
            "UNKNOWN")

    def test_07_invalid_or_superseded_custody_is_unknown(self):
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            validity={"state": "INVALIDATED", "invalidated_reason": "desk hold"}))["result"],
            "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(validity={
            "state": "VALID", "invalidated_reason": "stale reason"}))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            supersession={"superseded": True, "superseded_by": "rev2"}))["result"], "UNKNOWN")

    def test_08_forged_labels_and_non_canonical_paths_are_unknown(self):
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(identity={
            "custodian_label": "THE COMMANDER", "custodian_class": "commander_label_assertion",
            "identity_proven": True}))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            sole_path="scaffolding/activation_rules/SUBSTITUTE.v1.json"))["result"], "UNKNOWN")
        self.assertEqual(A.evaluate(fixture(), custody_obj=mutant(
            identity__custodian_label="NOT-THE-COMMANDER"))["result"], "SATISFIED",
            "a label is a label: renaming the custodian label changes nothing factual")

    def test_09_dynamic_disposition_is_unknown_and_never_a_live_result(self):
        for authenticated in (False, True):
            with self.subTest(authenticated=authenticated):
                receipt = A.evaluate(fixture(disposition={
                    "kind": "commander_disposition", "authenticated": authenticated,
                    "statement": "fixture-only disposition record"}))
                self.assertEqual(receipt["result"], "UNKNOWN")
                self.assertNotEqual(receipt["result"], "COMMANDER DISPOSITION")
        self.assertIn("COMMANDER DISPOSITION", A.RESULTS)
        source = (ROOT / "scripts/activation_conformance.py").read_text(encoding="utf-8")
        self.assertNotIn('_receipt("COMMANDER DISPOSITION"', source)

    def test_10_conflict_fixtures_are_conflict(self):
        self.assertEqual(A.evaluate(fixture(present=False, value="text while absent"))["result"],
                         "CONFLICT")
        self.assertEqual(A.evaluate(fixture(declaration_revision=99))["result"], "CONFLICT")
        self.assertEqual(A.evaluate(fixture(task_id="TID-2026-01-01-z"))["result"], "CONFLICT")
        self.assertEqual(A.evaluate(fixture(rule_revision=2))["result"], "UNKNOWN",
                         "an off-enum revision fails the closed schema before semantics")

    def test_11_no_permission_elevation_on_any_result(self):
        results = [A.evaluate(fixture()),
                   A.evaluate(fixture(value=None, present=False)),
                   A.evaluate(fixture(), custody_obj=mutant(declaration__declaration_required=False)),
                   A.evaluate({"schema_name": "x"})]
        for receipt in results:
            with self.subTest(result=receipt["result"]):
                self.assertEqual(receipt["authority"], "none")
                self.assertEqual(receipt["authentication"], "none")
                self.assertEqual(receipt["persisted"], False)
                self.assertIn("no_activation_or_permission_grant", receipt["limits"])

    def test_12_no_persistence_no_network_no_subprocess(self):
        source = (ROOT / "scripts/activation_conformance.py").read_text(encoding="utf-8")
        imports = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse(source))
                   if isinstance(n, ast.Import)}
        imports |= {n.module.split(".")[0] for n in ast.walk(ast.parse(source))
                    if isinstance(n, ast.ImportFrom) and n.module}
        self.assertFalse(imports - {"hashlib", "json", "os", "sys", "radiation_core", "copy"}, imports)
        for forbidden in ("subprocess", "socket", "urllib", "requests", "tempfile", "shutil",
                          "os.environ", "getenv"):
            self.assertNotIn(forbidden, source)
        writes = [n for n in ast.walk(ast.parse(source))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                  and n.func.id == "open" and len(n.args) > 1
                  and isinstance(n.args[1], ast.Constant) and n.args[1].value != "rb"]
        self.assertEqual(writes, [], "the evaluator opens files read-only")
        before = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                                capture_output=True, text=True).stdout
        A.evaluate(fixture())
        after = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True).stdout
        self.assertEqual(before, after, "an evaluation must leave the worktree untouched")

    def test_13_repeat_evaluation_is_idempotent_and_claims_no_first_use(self):
        first, second = A.evaluate(fixture()), A.evaluate(fixture())
        self.assertEqual(first, second)
        self.assertNotIn("first use", " ".join(first["reasons"]).lower())
        self.assertIn("no_cross_invocation_replay_protection", first["limits"])

    def test_14_schema_invalid_records_are_rejected_before_semantics(self):
        self.assertTrue(A._schema_findings(dict(live_custody(), rogue=1), "custody"))
        self.assertTrue(A._schema_findings(dict(fixture(), field="MODE"), "submission"))
        self.assertTrue(A._schema_findings(dict(fixture(), disposition={"kind": "other",
                                                                        "authenticated": True,
                                                                        "statement": "x"*3}),
                                           "submission"))
        receipt = A.evaluate(fixture())
        self.assertTrue(A._schema_findings(dict(receipt, result="PROBABLY"), "receipt"))
        self.assertTrue(A._schema_findings(dict(receipt, limits=A.LIMITS[:5]), "receipt"))
        self.assertEqual(A._schema_findings(receipt, "receipt"), [])

    def test_15_sole_custody_selection_cannot_be_redirected(self):
        source = (ROOT / "scripts/activation_conformance.py").read_text(encoding="utf-8")
        self.assertEqual(A.CUSTODY_PATH, "scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json")
        self.assertNotIn("os.environ", source)
        argv_reads = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Attribute)
                      and isinstance(n.value, ast.Name) and n.value.id == "sys"
                      and n.attr == "argv"]
        self.assertLessEqual(len(argv_reads), 1, "argv is read once, in main only")
        for bogus in (["--custody", "elsewhere.json"], ["--path", A.CUSTODY_PATH],
                      ["--submission"], ["--rule", "MAS-SCAN-NOTES"]):
            with self.subTest(flag=bogus[0]):
                proc = subprocess.run([sys.executable, "scripts/activation_conformance.py", *bogus],
                                      cwd=ROOT, capture_output=True, text=True, timeout=120,
                                      env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                                      stdin=subprocess.DEVNULL)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)

    def test_16_cli_live_evaluation_binds_only_its_custody_and_reports_honestly(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "submission.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(fixture(), fh)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run([sys.executable, "scripts/activation_conformance.py",
                                   "--submission", path, "--json"], cwd=ROOT, capture_output=True,
                                  text=True, timeout=120, env=env, stdin=subprocess.DEVNULL)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            receipt = json.loads(proc.stdout)
            self.assertEqual(receipt["result"], "SATISFIED")
            self.assertEqual(receipt["custody_path"], A.CUSTODY_PATH)
            empty = os.path.join(td, "empty.json")
            with open(empty, "w", encoding="utf-8") as fh:
                json.dump(fixture(value=None, present=False), fh)
            proc = subprocess.run([sys.executable, "scripts/activation_conformance.py",
                                   "--submission", empty], cwd=ROOT, capture_output=True,
                                  text=True, timeout=120, env=env, stdin=subprocess.DEVNULL)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("MISSING", proc.stdout)
            bare = subprocess.run([sys.executable, "scripts/activation_conformance.py"], cwd=ROOT,
                                  capture_output=True, text=True, timeout=120, env=env,
                                  stdin=subprocess.DEVNULL)
            self.assertEqual(bare.returncode, 1)
            self.assertIn("UNKNOWN", bare.stdout)


if __name__ == "__main__":
    unittest.main()
