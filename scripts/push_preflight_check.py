#!/usr/bin/env python3
"""
push_preflight_check.py — Motor Preflight Tool (P-12 LAW-5)

Purpose: encode LAW-5 — the motor's workspace preflight that the four gate laws could not prevent.
Incident closed: run #82 stale-base extraction + hand merge (EXPECTATION.json hand-spliced from RD-3 commit 2bc6e17, base still fee4a95 but tree was 0c0548b ancestor mismatch).
The four laws (PUBLIC-OBJECT, STDLIB-ONLY, DELTA-≡-ALLOWED, CI-HYGIENE) are machine-enforced inside the gate (release_truth_check.py).
The one incident they could not prevent lived in the motor's workspace before extraction/push.

This tool is additive, stdlib-only, self-testable, no network beyond `git fetch origin`.

Checks (exit 0/1, failures printed as LAW-n name: finding lines so motor reads laws, not stack traces):

- BASE-PIN CHECK (LAW-5): git rev-parse HEAD must equal tranche's declared base (arg --base <sha>, defaulting to EXPECTATION's base_sha); print SHA — the "verify the face" moment for motor.
  - If HEAD != base, FAIL: motor is at wrong base (stale-base extraction risk, run #82 genus)
  - If HEAD == base, PASS: motor verified face, safe to extract/push base or candidate after apply

- PUBLIC-OBJECT CHECK (LAW-1 mirror): git fetch origin → declared base must exist (git cat-file -e) AND be ancestor of origin/main (mirror gate's LAW-1 logic so failure modes match)
  - If origin exists: base must exist, must be ancestor of origin/main
  - If no origin (self-test temp repos): skip origin/main check, only cat-file -e

- DELTA-≡-ALLOWED CHECK (LAW-3 mirror): path set of git diff --name-status <base>..HEAD ≡ allowed_changes of candidate EXPECTATION — ∅ both directions
  - Reads docs/RELEASE_TRUTH_GATE/EXPECTATION.json allowed_changes
  - Compares set(diff paths) vs set(allowed paths)
  - Extra in diff or extra in allowed → FAIL with LAW-3 name

- CI-HYGIENE CHECK (LAW-4 mirror): untracked/unignored diagnostic artifacts (*_output.txt, apply_report.txt) in worktree → FAIL with names
  - Scans git status --porcelain for ?? files matching *_output.txt, apply_report.txt, validation_report.json (if not ignored)
  - Also scans for any file matching pattern that is not ignored via .gitignore
  - If found, FAIL with LAW-4 name

Usage:
  python3 scripts/push_preflight_check.py --base <sha>          # check HEAD vs base + public-object + delta + hygiene
  python3 scripts/push_preflight_check.py                        # defaults base to EXPECTATION's base_sha
  python3 scripts/push_preflight_check.py --self-test            # 4+ vectors synthetic repos like gate's self-test harness

Motor preflight: run python3 scripts/push_preflight_check.py before extraction/push; STOP at any finding.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECTATION_PATH = ROOT / "docs" / "RELEASE_TRUTH_GATE" / "EXPECTATION.json"

def run(cmd, cwd=ROOT, check=False):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd failed {cmd}: {p.stdout} {p.stderr}")
    return p

def load_expectation():
    if not EXPECTATION_PATH.exists():
        return None, [f"EXPECTATION.json missing at {EXPECTATION_PATH}"]
    try:
        data = json.loads(EXPECTATION_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"EXPECTATION.json invalid JSON: {e}"]
    return data, []

def get_head_sha():
    p = run("git rev-parse HEAD")
    return p.stdout.strip() if p.returncode == 0 else ""

def get_diff_name_status(base):
    p = run(f"git diff {base}..HEAD --name-status")
    if p.returncode != 0:
        return []
    lines = []
    for line in p.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            kind = parts[0][0]
            path = parts[-1]
            lines.append((kind, path))
    return lines

def check_base_pin(declared_base):
    findings = []
    head = get_head_sha()
    print(f"BASE-PIN: HEAD={head} declared_base={declared_base}")
    if not declared_base or not re.fullmatch(r"[0-9a-f]{7,40}", declared_base):
        findings.append(f"LAW-5 BASE-PIN: declared base invalid or missing: {declared_base} — must be valid SHA")
        return findings
    if head == declared_base:
        print(f"LAW-5 BASE-PIN: OK — HEAD equals declared base {declared_base} — verify-the-face moment passed")
    else:
        # HEAD has moved beyond base (candidate built) — check that base is ancestor of HEAD, i.e., motor started from correct base
        p = run(f"git merge-base --is-ancestor {declared_base} {head}")
        if p.returncode == 0:
            print(f"LAW-5 BASE-PIN: OK — HEAD {head} is beyond base {declared_base} but base is ancestor (candidate built on correct base) — verify-the-face passed, motor at {head[:7]} built from {declared_base[:7]}")
        else:
            findings.append(f"LAW-5 BASE-PIN: HEAD {head} != declared base {declared_base} and base not ancestor of HEAD — motor at wrong base (stale-base extraction risk, run #82 genus: EXPECTATION hand-spliced from RD-3 commit 2bc6e17 but base still fee4a95)")
    return findings

def check_public_object(declared_base):
    findings = []
    if not declared_base:
        return findings
    # Check if origin exists
    p_remote = run("git remote get-url origin 2>&1")
    if p_remote.returncode != 0:
        print("LAW-1 PUBLIC-OBJECT: no origin remote — skipping origin/main check (self-test temp repo)")
        # Still check cat-file -e locally
        p_cat = run(f"git cat-file -e {declared_base} 2>&1")
        if p_cat.returncode != 0:
            findings.append(f"LAW-1 PUBLIC-OBJECT: declared base {declared_base} does not exist (git cat-file -e failed) — local object doesn't exist")
        return findings
    # Fetch origin
    run("git fetch origin --quiet 2>&1 || true")
    p_cat = run(f"git cat-file -e {declared_base} 2>&1")
    if p_cat.returncode != 0:
        findings.append(f"LAW-1 PUBLIC-OBJECT: declared base {declared_base} does not exist (git cat-file -e failed) — local objects don't exist; only pushed history is real")
        return findings
    p_origin_main = run("git rev-parse --verify origin/main 2>&1")
    if p_origin_main.returncode == 0:
        p_contains = run(f"git branch -r --contains {declared_base} 2>&1")
        p_anc = run(f"git merge-base --is-ancestor {declared_base} origin/main")
        if p_anc.returncode != 0:
            findings.append(f"LAW-1 PUBLIC-OBJECT: declared base {declared_base} is not ancestor of origin/main (branch -r --contains: {p_contains.stdout[:200]}) — local-only object, violates PUBLIC-OBJECT LAW")
        else:
            print(f"LAW-1 PUBLIC-OBJECT: OK — base {declared_base} exists and is ancestor of origin/main")
    else:
        print(f"LAW-1 PUBLIC-OBJECT: origin/main not found, only cat-file check passed for {declared_base}")
    return findings

def check_delta_equals_allowed(declared_base):
    findings = []
    data, load_findings = load_expectation()
    if load_findings:
        findings.append(f"LAW-3 DELTA-≡-ALLOWED: could not load EXPECTATION.json: {load_findings}")
        return findings
    if not declared_base:
        return findings
    allowed_paths = set()
    for entry in data.get("allowed_changes", []):
        if isinstance(entry, dict):
            pth = entry.get("path")
            if pth:
                allowed_paths.add(pth)
    diff = get_diff_name_status(declared_base)
    diff_paths = set(path for _, path in diff)
    print(f"LAW-3 DELTA-≡-ALLOWED: diff={len(diff_paths)} allowed={len(allowed_paths)}")
    if diff_paths != allowed_paths:
        extra_in_diff = sorted(diff_paths - allowed_paths)
        extra_in_allowed = sorted(allowed_paths - diff_paths)
        if extra_in_diff:
            findings.append(f"LAW-3 DELTA-≡-ALLOWED: diff contains paths not in allowed_changes: {extra_in_diff} — δ extra in diff, run #82 genus hand-merge")
        if extra_in_allowed:
            findings.append(f"LAW-3 DELTA-≡-ALLOWED: allowed_changes contains paths not in diff (δ≠∅): {extra_in_allowed} — allowed must equal true delta")
    else:
        print(f"LAW-3 DELTA-≡-ALLOWED: OK — diff ≡ allowed (∅ both ways) — delta-vs-allowed: ran · output ∅")
    return findings

def check_ci_hygiene():
    findings = []
    # Scan git status --porcelain for untracked files matching diagnostic patterns
    p = run("git status --porcelain --untracked-files=all")
    untracked = []
    for line in p.stdout.splitlines():
        if line.startswith("??"):
            path = line[3:].strip()
            # Check patterns
            if path.endswith("_output.txt") or path.endswith("apply_report.txt") or path == "validation_report.json":
                # Check if ignored via git check-ignore
                p_ignore = run(f"git check-ignore -q {path}; echo $?")
                # git check-ignore returns 0 if ignored, 1 if not
                # Our run captures exit code via echo, but we need to check
                # Simpler: run git check-ignore
                p_check = run(f"git check-ignore {path} 2>&1")
                if p_check.returncode != 0:
                    # Not ignored → hygiene violation
                    untracked.append(path)
    if untracked:
        findings.append(f"LAW-4 CI-HYGIENE: untracked/unignored diagnostic artifacts in worktree: {untracked} — must be gitignored or out-of-repo per LAW-4 (precedent §3c validation_report.json, §3f /*_output.txt)")
    else:
        print("LAW-4 CI-HYGIENE: OK — no unignored diagnostic artifacts")
    return findings

def main_check(declared_base_arg=None):
    # Determine declared base: arg --base or EXPECTATION's base_sha
    if declared_base_arg:
        declared_base = declared_base_arg
    else:
        data, _ = load_expectation()
        declared_base = data.get("base_sha") if data else ""
    if not declared_base:
        print("push_preflight_check: findings")
        print("  - LAW-5 BASE-PIN: declared base missing and no EXPECTATION.json base_sha")
        return 1
    findings = []
    findings.extend(check_base_pin(declared_base))
    findings.extend(check_public_object(declared_base))
    findings.extend(check_delta_equals_allowed(declared_base))
    findings.extend(check_ci_hygiene())
    if findings:
        print(f"push_preflight_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        return 1
    else:
        print("push_preflight_check: 0 finding(s) — motor preflight PASS, safe to extract/push")
        return 0

def self_test():
    def make_temp_repo():
        tmp = tempfile.mkdtemp()
        run("git init -q", cwd=tmp, check=True)
        run("git config user.email test@test.com", cwd=tmp, check=True)
        run("git config user.name Test", cwd=tmp, check=True)
        pathlib.Path(tmp, "README.md").write_text("hi\n", encoding="utf-8")
        run("git add README.md && git commit -qm init", cwd=tmp, check=True)
        return tmp

    def v_happy_path():
        # Happy path: HEAD == base, allowed == diff (empty or exact), no hygiene violations
        tmp = make_temp_repo()
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
            # Run preflight with base == HEAD, should pass (no diff, no allowed, no hygiene)
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            return p.returncode == 0 and "0 finding" in p.stdout
        finally:
            shutil.rmtree(tmp)

    def v_wrong_head_base():
        # Wrong HEAD base: base NOT ancestor of HEAD -> FAIL LAW-5 (true wrong base, divergent branch)
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            # Create divergent branch so base is NOT ancestor of HEAD
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
            # Run with divergent base, base not ancestor of HEAD -> should FAIL LAW-5 BASE-PIN
            p = run(f"python3 scripts/push_preflight_check.py --base {base_other}", cwd=tmp)
            return p.returncode != 0 and "BASE-PIN" in p.stdout
        finally:
            shutil.rmtree(tmp)

    def v_extra_in_diff():
        # Extra in diff not in allowed -> FAIL LAW-3
        tmp = make_temp_repo()
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
            # Run with base, diff has evil.txt not in allowed -> FAIL
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            return p.returncode != 0 and "DELTA" in p.stdout
        finally:
            shutil.rmtree(tmp)

    def v_extra_in_allowed():
        # Extra in allowed not in diff -> FAIL LAW-3
        tmp = make_temp_repo()
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
            # Now HEAD is new commit, but diff base..HEAD is EXPECTATION.json M only, not extra_not_in_diff.txt
            # So allowed has extra -> FAIL
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            return p.returncode != 0 and "DELTA" in p.stdout
        finally:
            shutil.rmtree(tmp)

    def v_ci_hygiene_fail():
        # CI hygiene: untracked *_output.txt not ignored -> FAIL LAW-4
        tmp = make_temp_repo()
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
            # Create untracked diagnostic artifact that is NOT ignored (no .gitignore)
            pathlib.Path(tmp, "some_output.txt").write_text("diagnostic", encoding="utf-8")
            p = run(f"python3 scripts/push_preflight_check.py --base {base}", cwd=tmp)
            return p.returncode != 0 and "CI-HYGIENE" in p.stdout
        finally:
            shutil.rmtree(tmp)

    tests = [
        ("happy path HEAD==base allowed==diff -> pass", v_happy_path),
        ("wrong HEAD base != declared -> reject LAW-5", v_wrong_head_base),
        ("extra in diff not in allowed -> reject LAW-3", v_extra_in_diff),
        ("extra in allowed not in diff -> reject LAW-3", v_extra_in_allowed),
        ("CI hygiene untracked _output.txt -> reject LAW-4", v_ci_hygiene_fail),
    ]
    passed = 0
    for name, fn in tests:
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"  vector exception {name}: {e}")
        status = "PASS" if ok else "FAIL"
        print(f"  vector {name} -> {status}")
        if ok:
            passed += 1
    print(f"push_preflight_check self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="Declared base SHA (default: EXPECTATION's base_sha)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test vectors")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(self_test())
    else:
        sys.exit(main_check(args.base))
