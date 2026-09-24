#!/usr/bin/env python3
"""B4.2 R0 T1–T14: ten live IO contracts, adapters, fences and Option-A WARN.

The live suite runs after the candidate has a committed HEAD. Nested suites
(from validate, a bound tool, or the release gate) use deterministic synthetic
output to avoid a validator/test/verify_apply recursion. No skips are added.
"""
import ast
from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import verify_tool_io as V


class TestVerifyToolIO(unittest.TestCase):
    @staticmethod
    def fixture_invoke(tool, argv):
        name = tool["id"]
        if name == "validate":
            stdout = json.dumps({
                "schema_version": "radiation.validation/1",
                "results": [{"check": 1, "severity": "FAIL", "ok": True, "msg": "clean"}],
                "summary": {"checks": 1, "pass": 1, "warn": 0, "fail": 0},
            })
        elif name == "verify_cassette_runner":
            stdout = json.dumps({
                "rows": [{"id": "seed", "verdict": "PASS", "expected": "PASS",
                          "justification": "deterministic fixture"}],
                "summary": "verify cassette: 1/1 rows PASS",
            })
        else:
            spec = json.loads((ROOT / "schemas/tool_io" /
                               f"{name}.outputs.schema.json").read_text(encoding="utf-8"))
            stdout = f"{spec['properties']['needle']['const']}\n"
        return subprocess.CompletedProcess([name, *argv], 0, stdout, "")

    @classmethod
    def setUpClass(cls):
        # On the real top-level discover, exercise all ten live CLIs ONCE.
        # validate's test harness and the release gate inherit these guards;
        # nested test runs still assert the real schemas on fixture output.
        cls.nested = bool(os.environ.get("RADIATION_VALIDATION_CTX") or
                          os.environ.get(V.CHILD_ENV))
        if cls.nested:
            with mock.patch.object(V, "_invoke", side_effect=cls.fixture_invoke):
                cls.report = V.run_io()
        else:
            cls.report = V.run_io()

    def test_t01_all_ten_live_contracts(self):
        self.assertEqual(len(self.report["rows"]), 10)
        self.assertEqual(tuple(r["id"] for r in self.report["rows"]), V.BOUND)
        self.assertEqual([r["verdict"] for r in self.report["rows"]], ["PASS"] * 10,
                         self.report["rows"])
        self.assertEqual(self.report["summary"], "verify tool_io: 10/10 tools PASS")
        self.assertFalse(self.report["scope_findings"])

    def test_t02_both_json_envelopes_are_existing_contracts(self):
        self.assertEqual(V.JSON_EMITTERS, {"validate", "verify_cassette_runner"})
        for name in V.JSON_EMITTERS:
            result = self.fixture_invoke({"id": name}, V.ARGV[name])
            payload = json.loads(result.stdout)
            self.assertEqual(V._schema_findings(payload,
                             f"tool_io/{name}.outputs.schema.json", name), [])
            self.assertEqual(V.ARGV[name], ("--json",))

    def test_t03_eight_prose_adapters_execute_as_prose(self):
        self.assertEqual(len(V.PROSE), 8)
        for name in V.PROSE:
            self.assertNotIn("--json", V.ARGV[name], name)
            spec = json.loads((ROOT / "schemas/tool_io" /
                               f"{name}.outputs.schema.json").read_text())
            payload = V._prose_adapter(name, self.fixture_invoke({"id": name}, ()), spec)
            self.assertEqual(V._schema_findings(payload,
                             f"tool_io/{name}.outputs.schema.json", name), [])
            self.assertTrue(payload["ok"], name)

    def test_t04_closed_and_required_schema_properties(self):
        base = {"schema_name": "radiation.tool_io.validate.inputs/1",
                "cwd": "repo-root", "argv": ["--json"]}
        schema = "tool_io/validate.inputs.schema.json"
        self.assertFalse(V._schema_findings(base, schema, "input"))
        self.assertIn("unknown property", " ".join(V._schema_findings(
            dict(base, intruder=1), schema, "input")))
        self.assertIn("schema-required", " ".join(V._schema_findings(
            {"cwd": "repo-root", "argv": []}, schema, "input")))
        self.assertIn("outside enum", " ".join(V._schema_findings(
            dict(base, argv=["--json-new"]), schema, "input")))
        output = {"schema_name": "radiation.tool_io.docs_index_check.outputs/1",
                  "ok": True, "exit": 0, "findings": [], "needle": "0 finding"}
        self.assertIn("unknown property", " ".join(V._schema_findings(
            dict(output, rogue=0), "tool_io/docs_index_check.outputs.schema.json", "output")))
        self.assertIn("schema-required", " ".join(V._schema_findings(
            {k: v for k, v in output.items() if k != "needle"},
            "tool_io/docs_index_check.outputs.schema.json", "output")))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "schemas/tool_io/validate.inputs.schema.json"
            path.parent.mkdir(parents=True)
            path.write_text("[]", encoding="utf-8")
            with mock.patch.object(V, "ROOT", Path(tmp)):
                findings = V._schema_findings(base, schema, "input")
            self.assertIn("schema must be an object", " ".join(findings))

    def test_t05_prose_needle_failure_is_actionable(self):
        spec = json.loads((ROOT / "schemas/tool_io/docs_index_check.outputs.schema.json").read_text())
        good = self.fixture_invoke({"id": "docs_index_check"}, ())
        self.assertTrue(V._prose_adapter("docs_index_check", good, spec)["ok"])
        silent = subprocess.CompletedProcess([], 0, "generic success\n", "")
        report = V._prose_adapter("docs_index_check", silent, spec)
        self.assertFalse(report["ok"])
        self.assertIn("success needle", report["findings"][0])
        self.assertEqual(V._schema_findings(report,
                         "tool_io/docs_index_check.outputs.schema.json", "output"), [])

    def test_t06_nonzero_exit_carries_source_findings(self):
        spec = json.loads((ROOT / "schemas/tool_io/docs_index_check.outputs.schema.json").read_text())
        failing = subprocess.CompletedProcess([], 1, "  - broken link in README\n", "")
        report = V._prose_adapter("docs_index_check", failing, spec)
        self.assertFalse(report["ok"])
        self.assertEqual(report["exit"], 1)
        self.assertIn("broken link", " ".join(report["findings"]))
        self.assertEqual(V._schema_findings(report,
                         "tool_io/docs_index_check.outputs.schema.json", "output"), [])

    def test_t07_json_failure_is_returned_or_warned_not_swallowed(self):
        row = next(t for t in V._load_registry()["tools"] if t["id"] == "validate")
        for output, verdict, phrase in (("not JSON", "RETURNED", "unreadable"),
                                        ("{}", "WARN-and-justify", "schema-required")):
            with self.subTest(output=output):
                result = subprocess.CompletedProcess([], 0, output, "")
                with mock.patch.object(V, "_invoke", return_value=result):
                    got = V._run_one("validate", row)
                self.assertEqual(got["verdict"], verdict)
                self.assertIn(phrase, got["justification"])
                self.assertTrue(got["findings"])
        with mock.patch.object(V, "_invoke", side_effect=subprocess.TimeoutExpired(["validate"], 1)):
            timed_out = V._run_one("validate", row)
        self.assertEqual(timed_out["verdict"], "RETURNED")
        self.assertIn("TimeoutExpired", timed_out["justification"])

    def test_t08_scope_fence_exact_ten_bound_thirty_other_metadata(self):
        reg = V._load_registry()
        by_id, findings = V._scope(reg)
        self.assertFalse(findings)
        self.assertEqual(len(by_id), 41)
        mutant = deepcopy(reg)
        next(t for t in mutant["tools"] if t["id"] == "relay")["outputs_schema"] = (
            "schemas/tool_io/validate.outputs.schema.json")
        self.assertIn("schema-bound scope", " ".join(V._scope(mutant)[1]))
        with mock.patch.object(V, "_load_registry", return_value=mutant), \
             mock.patch.object(V, "_invoke") as invoke:
            report = V.run_io()
        invoke.assert_not_called()
        self.assertEqual(len(report["rows"]), 10)
        self.assertTrue(all(r["verdict"] == "RETURNED" for r in report["rows"]))

    def test_t09_executor_remains_metadata_only_and_nonrecursive(self):
        reg = V._load_registry()
        row = next(t for t in reg["tools"] if t["id"] == "verify_tool_io")
        self.assertIsNone(row["inputs_schema"])
        self.assertIsNone(row["outputs_schema"])
        self.assertNotIn("verify_tool_io", V.BOUND)
        mutant = deepcopy(reg)
        next(t for t in mutant["tools"] if t["id"] == "verify_tool_io")["inputs_schema"] = (
            "schemas/tool_io/validate.inputs.schema.json")
        self.assertIn("METADATA-ONLY", " ".join(V._scope(mutant)[1]))

    def test_t10_all_twenty_schema_keywords_have_one_executor(self):
        from radiation_core.relay import _schema_check, unsupported_keywords
        self.assertIs(V._schema_check, _schema_check)
        for name in V.BOUND:
            for direction in ("inputs", "outputs"):
                spec = json.loads((ROOT / "schemas/tool_io" /
                                   f"{name}.{direction}.schema.json").read_text())
                self.assertEqual(unsupported_keywords(spec), [], f"{name}.{direction}")

    def test_t11_self_test_cli_is_synthetic_and_hermetic(self):
        child_env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, "scripts/verify_tool_io.py", "--self-test"],
                              cwd=ROOT, env=child_env, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("verify tool_io self-test: 10/10 PASS", proc.stdout)

    def test_t12_json_cli_report_and_rejected_extra_flags(self):
        with mock.patch.object(V, "run_io", return_value=self.report):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(V.main(["--json"]), 0)
            doc = json.loads(stdout.getvalue())
            self.assertEqual(doc["summary"], "verify tool_io: 10/10 tools PASS")
            self.assertEqual(len(doc["rows"]), 10)
        with redirect_stderr(io.StringIO()):
            self.assertEqual(V.main(["--json", "--self-test"]), 2)
            self.assertEqual(V.main(["--base", "X"]), 2)

    def test_t13_offline_stdlib_only_and_no_eight_tool_json_flag(self):
        source = (ROOT / "scripts/verify_tool_io.py").read_text(encoding="utf-8")
        imports = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse(source))
                   if isinstance(n, ast.Import)}
        imports |= {n.module.split(".")[0] for n in ast.walk(ast.parse(source))
                    if isinstance(n, ast.ImportFrom) and n.module}
        self.assertFalse(imports - {"json", "os", "pathlib", "subprocess", "sys",
                                    "radiation_core", "copy"}, imports)
        with mock.patch.object(V.subprocess, "run", return_value=None) as spawn:
            V._invoke({"entrypoint": "scripts/docs_index_check.py", "timeout_seconds": 10}, ())
        kwargs = spawn.call_args.kwargs
        self.assertEqual(kwargs["env"]["GIT_ALLOW_PROTOCOL"], "file")
        self.assertEqual(kwargs["env"]["GIT_CONFIG_COUNT"], "0")
        self.assertNotIn("GIT_CONFIG_VALUE_0", kwargs["env"])
        self.assertEqual(kwargs["env"]["RADIATION_ONLINE"], "0")
        self.assertEqual(kwargs["env"][V.CHILD_ENV], "1")
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(V.PROSE, set(V.BOUND) - V.JSON_EMITTERS)
        for name in V.PROSE:
            self.assertNotIn("--json", V.ARGV[name])

    def test_t14_option_a_through_live_apply_plugin_never_fail_class(self):
        import validate
        import verify_apply as A
        import verify_cassette_runner as C
        report = deepcopy(self.report)
        def invoke(report_or_error, marker=""):
            out = io.StringIO()
            patch = (mock.patch.object(V, "run_io", side_effect=report_or_error)
                     if isinstance(report_or_error, BaseException) else
                     mock.patch.object(V, "run_io", return_value=report_or_error))
            with patch as run_mock, mock.patch.object(validate, "run_all", return_value=[]), \
                 mock.patch.object(validate, "_summary", return_value=([], [])), \
                 mock.patch.object(A, "vehicle_audit", return_value=[]), \
                 mock.patch.object(A, "corpus_contract_findings", return_value=[]), \
                 mock.patch.object(A, "head_date", return_value=None), \
                 mock.patch.object(C, "run_cassette", return_value=[{"id": "c", "verdict": "PASS"}]), \
                 mock.patch.dict(os.environ, {V.CHILD_ENV: marker}), \
                 mock.patch.object(sys, "argv", ["verify_apply.py", "--strict"]), \
                 redirect_stdout(out):
                result = A.main()
            return result, out.getvalue(), run_mock.call_count

        rc, output, calls = invoke(report)
        self.assertEqual(rc, 0)
        self.assertEqual(calls, 1)
        self.assertNotIn("tool_io : ADVISORY", output)
        report["rows"][0] = dict(report["rows"][0], verdict="WARN-and-justify",
                                 justification="required property missing")
        rc, output, calls = invoke(report)
        self.assertEqual(rc, 0)
        self.assertEqual(calls, 1)
        self.assertIn("tool_io : ADVISORY", output)
        self.assertIn("WARN-CLASS :", output)
        self.assertIn("tool_io advisory", output)
        self.assertIn("FAIL-CLASS : none", output)
        rc, output, calls = invoke(RuntimeError("module unavailable"))
        self.assertEqual(rc, 0)
        self.assertEqual(calls, 1)
        self.assertIn("executor unavailable: RuntimeError: module unavailable", output)
        rc, output, calls = invoke(report, marker="1")
        self.assertEqual(rc, 0)
        self.assertEqual(calls, 0)
        self.assertNotIn("tool_io : ADVISORY", output)


if __name__ == "__main__":
    unittest.main()
