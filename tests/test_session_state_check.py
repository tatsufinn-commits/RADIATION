#!/usr/bin/env python3
"""
Test harness for session_state_check.py — S-2-ENV Session Capability State

Vectors ≥4 (TestCase law): absent file, valid file, UNKNOWN-honesty, OBSERVED-vs-DECLARED
Discover 152 → ≥156
"""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

class TestSessionStateCheck(unittest.TestCase):
    def make_temp_repo(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "schemas").mkdir(parents=True, exist_ok=True)
        (tmp / "Brain" / "short_term" / "active").mkdir(parents=True, exist_ok=True)
        (tmp / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy(str(ROOT / "schemas" / "session_capability_state.schema.json"), str(tmp / "schemas" / "session_capability_state.schema.json"))
        shutil.copy(str(ROOT / "scripts" / "session_state_check.py"), str(tmp / "scripts" / "session_state_check.py"))
        run(f"git init -q", cwd=tmp)
        run(f"git config user.email test@test.com", cwd=tmp)
        run(f"git config user.name Test", cwd=tmp)
        return tmp

    def test_absent_file(self):
        tmp = self.make_temp_repo()
        try:
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertEqual(p.returncode, 0)
            self.assertIn("no session state declared", p.stdout.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_valid_file(self):
        tmp = self.make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider", "provider": "Arena_AI"},
                "capabilities": [
                    {"name": "tool_a", "state": "AVAILABLE", "provenance": "OBSERVED", "evidence": "cap_probe execution this session: tools_exposed includes tool_a"},
                    {"name": "host_posture_profile", "state": "UNKNOWN", "provenance": "INFERRED", "evidence": "no profile — absent evidence stays UNKNOWN"}
                ],
                "constraints": [
                    {"name": "repository_status", "provenance": "OBSERVED", "value_or_unknown": "mounted"}
                ],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc123",
                "honesty_note": "working memory, stale reads UNKNOWN"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"valid file should pass, got {p.stdout}")
            self.assertIn("0 finding", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unknown_honesty(self):
        # UNKNOWN-honesty: absent evidence stays UNKNOWN never UNAVAILABLE
        tmp = self.make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "generic", "provider": None},
                "capabilities": [
                    {"name": "mystery_cap", "state": "UNKNOWN", "provenance": "INFERRED", "evidence": "no evidence — absent evidence stays UNKNOWN per mandatory discipline"}
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "UNKNOWN is first-class value everywhere"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertEqual(p.returncode, 0, f"UNKNOWN honesty should pass, got {p.stdout}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_observed_without_cap_probe_fail(self):
        # OBSERVED-vs-DECLARED: OBSERVED without cap_probe evidence → FAIL
        tmp = self.make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider", "provider": "Arena_AI"},
                "capabilities": [
                    {"name": "tool_x", "state": "AVAILABLE", "provenance": "OBSERVED", "evidence": "declared by config"}
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "test"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("OBSERVED without cap_probe", p.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_invalid_enum_fail(self):
        tmp = self.make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider"},
                "capabilities": [
                    {"name": "tool_y", "state": "ENABLED", "provenance": "OBSERVED", "evidence": "cap_probe execution"}
                ],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "test"
            }
            (tmp / "Brain" / "short_term" / "active" / "session_capability_state.json").write_text(json.dumps(state), encoding="utf-8")
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("invalid state", p.stdout.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_lifecycle_no_commit(self):
        # Lifecycle: state file must never be committed with live content
        tmp = self.make_temp_repo()
        try:
            state = {
                "schema_name": "radiation.session_capability_state/1",
                "host_label": "Arena Agent Mode",
                "route": {"route": "provider"},
                "capabilities": [],
                "constraints": [],
                "generated_at": "2026-09-16T12:00:00Z",
                "pass_ref": "abc",
                "honesty_note": "test"
            }
            sp = tmp / "Brain" / "short_term" / "active" / "session_capability_state.json"
            sp.write_text(json.dumps(state), encoding="utf-8")
            # Track it in git
            run(f"git add {sp} && git commit -qm add-state", cwd=tmp)
            p = run(f"python3 scripts/session_state_check.py", cwd=tmp)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("must never be committed", p.stdout.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
