#!/usr/bin/env python3
"""
Test harness for push_preflight_check.py — P-12 LAW-5 Motor Preflight

Vectors ≥4 (happy path, wrong-HEAD base, extra-in-diff, extra-in-allowed), synthetic repos like gate's self-test harness.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def run(cmd, cwd=ROOT, check=False):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd failed {cmd}: {p.stdout} {p.stderr}")
    return p

class TestPushPreflight(unittest.TestCase):
    def make_temp_repo(self):
        tmp = tempfile.mkdtemp()
        run("git init -q", cwd=tmp, check=True)
        run("git config user.email test@test.com", cwd=tmp, check=True)
        run("git config user.name Test", cwd=tmp, check=True)
        pathlib.Path(tmp, "README.md").write_text("hi\n", encoding="utf-8")
        run("git add README.md && git commit -qm init", cwd=tmp, check=True)
        return tmp

    def test_happy_path(self):
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"happy path should pass, got {p.stdout} {p.stderr}")
            self.assertIn("0 finding", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_wrong_head_base(self):
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            # Create divergent branch so base is NOT ancestor of HEAD (true wrong base)
            run("git checkout -b other", cwd=tmp, check=True)
            pathlib.Path(tmp, "other.txt").write_text("other", encoding="utf-8")
            run("git add other.txt && git commit -qm other", cwd=tmp, check=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base_other = p.stdout.strip()
            run("git checkout main 2>/dev/null || git checkout master", cwd=tmp, check=True)
            pathlib.Path(tmp, "new.txt").write_text("new", encoding="utf-8")
            run("git add new.txt && git commit -qm new", cwd=tmp, check=True)
            exp = {
                "base_sha": base_other,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "new.txt", "kind": "A"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            p = run(f"python3 scripts/push_preflight_check.py --base {base_other}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0, "wrong HEAD base should fail when base not ancestor")
            self.assertIn("BASE-PIN", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_extra_in_diff(self):
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            pathlib.Path(tmp, "evil.txt").write_text("evil", encoding="utf-8")
            run("git add evil.txt && git commit -qm evil", cwd=tmp, check=True)
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "README.md", "kind": "M"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0, "extra in diff should fail")
            self.assertIn("DELTA", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_extra_in_allowed(self):
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "docs/RELEASE_TRUTH_GATE/EXPECTATION.json", "kind": "M"}, {"path": "extra_not_in_diff.txt", "kind": "M"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            run("git add . && git commit -qm add-expectation", cwd=tmp, check=True)
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0, "extra in allowed should fail")
            self.assertIn("DELTA", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_ci_hygiene(self):
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            pathlib.Path(tmp, "some_output.txt").write_text("diagnostic", encoding="utf-8")
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0, "CI hygiene should fail on untracked _output.txt")
            self.assertIn("CI-HYGIENE", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_whitespace_clean_pass(self):
        # LAW-6 control: clean tree → LAW-6 passes
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"clean whitespace should pass LAW-6, got {p.stdout}")
            self.assertIn("LAW-6 WHITESPACE", p.stdout)
            self.assertIn("OK", p.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_whitespace_trailing_blank_fail(self):
        # LAW-6 adversarial: tree carrying trailing-blank-at-EOF in tracked file → LAW-6 FAILS, finding names file and line (exact run-#97 shape)
        tmp = self.make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "docs").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Exact run-#97 shape: ROADMAP had blank line at EOF — inject trailing blank line
            tracked = pathlib.Path(tmp, "docs/ROADMAP.md")
            tracked.write_text("line1\nline2\n\n", encoding="utf-8")  # blank line at EOF
            run("git add docs/ROADMAP.md && git commit -qm add-roadmap-with-blank", cwd=tmp, check=True)
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "docs/ROADMAP.md", "kind": "A"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "push_preflight_check.py"), str(pathlib.Path(tmp, "scripts/push_preflight_check.py")))
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            self.assertNotEqual(p.returncode, 0, "trailing blank at EOF should fail LAW-6")
            self.assertIn("LAW-6 WHITESPACE", p.stdout)
            self.assertIn("ROADMAP", p.stdout)
        finally:
            shutil.rmtree(tmp)

if __name__ == "__main__":
    unittest.main()
