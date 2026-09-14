"""5500-closure Step 0 — CI semantics, pinned as tests.

What these tests prove (exactly):
  1. The workflow really runs steps under GitHub Actions' `shell: bash`
     semantics, which is `bash --noprofile --norc -eo pipefail` — so an
     upstream failure is NOT masked by `tee` (the 5300-era mask is dead).
  2. The workflow keeps the Python 3.11 pin AND keeps its failure diagnostics
     (public step summary + failure-only artifact a non-admin can download).
  3. Repo sources carry no 3.12+ nested-same-quote f-strings (the actual cause
     of the CI red at 2681ee3: radiation_core/relay.py parsed on 3.13 but was
     a SyntaxError on the pinned 3.11, killing BOTH jobs at their first step).

What these tests do NOT claim: they do not run GitHub Actions; the local
tripwire in test_06 is a heuristic line scan — the authoritative 3.11 grammar
guard is the workflow's byte-compile step executing under the pinned job
python. Public green runs remain the Commander-side post-push proof.
"""
import pathlib
import re
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


class TestCISemantics(unittest.TestCase):
    def test_01_workflow_declares_bash_shell(self):
        text = workflow_text()
        self.assertIn("defaults:", text)
        self.assertIn("shell: bash", text)

    def test_02_workflow_pins_python_3_11(self):
        self.assertIn('python-version: "3.11"', workflow_text())

    def test_03_upstream_failure_is_not_masked_by_tee(self):
        """Exact Actions semantics for shell: bash → `bash -eo pipefail`."""
        probe = pathlib.Path("/tmp") / "_radiation_tee_probe_fail.txt"
        cmd = f'python3 -c "import sys; sys.exit(3)" | tee {probe}'
        rc = subprocess.run(
            ["bash", "-eo", "pipefail", "-c", cmd], capture_output=True
        ).returncode
        self.assertNotEqual(rc, 0, "tee masked an upstream failure under -eo pipefail")

    def test_04_successful_pipeline_still_exits_zero(self):
        probe = pathlib.Path("/tmp") / "_radiation_tee_probe_ok.txt"
        cmd = f'python3 -c "pass" | tee {probe}'
        rc = subprocess.run(
            ["bash", "-eo", "pipefail", "-c", cmd], capture_output=True
        ).returncode
        self.assertEqual(rc, 0)

    def test_05_failure_diagnostics_and_artifact_steps_present(self):
        text = workflow_text()
        self.assertIn("if: failure()", text)
        self.assertIn("$GITHUB_STEP_SUMMARY", text)
        self.assertIn("actions/upload-artifact@v4", text)

    def test_06_no_312_plus_nested_quote_f_strings(self):
        """Heuristic tripwire for the 2681ee3 CI-red class.

        3.12's tokenizer accepts `{x.get("k")}` inside an f"..." literal;
        the pinned 3.11 raises SyntaxError. Flag any double quote that appears
        inside the braces of an f"..." literal (escaped-quote lines are
        skipped — those can be legal on 3.11).
        """
        offenders = []
        for path in sorted(ROOT.rglob("*.py")):
            parts = path.parts
            if ".git" in parts or "__pycache__" in parts:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for no, line in enumerate(lines, 1):
                if not re.search(r'(?:^|[^A-Za-z0-9_])f"', line) or '\\"' in line:
                    continue
                j, in_f, depth = 0, False, 0
                hit = False
                while j < len(line):
                    c = line[j]
                    if not in_f:
                        if c == "f" and j + 1 < len(line) and line[j + 1] == '"':
                            in_f = True
                            j += 2
                            continue
                        j += 1
                        continue
                    if c == "\\":
                        j += 2
                        continue
                    if c == '"':
                        if depth > 0:
                            offenders.append(f"{path.relative_to(ROOT)}:{no}")
                            hit = True
                            break
                        in_f = False
                        j += 1
                        continue
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth = max(0, depth - 1)
                    j += 1
        self.assertEqual(
            offenders,
            [],
            "3.12+ nested-quote f-strings found (SyntaxError under the CI 3.11 pin) — "
            "use single quotes inside f-string expressions",
        )


if __name__ == "__main__":
    unittest.main()
