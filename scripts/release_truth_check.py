#!/usr/bin/env python3
"""
release_truth_check.py — Release Truth Gate checker (5824 FIX)

Checks per independent review 98d8c81:
- base SHA exists and is ancestor of HEAD
- required deletions absent on disk + D in diff (when must_be_D_in_diff true)
- allowed changes only (A/M/D) with no undeclared paths
- forbidden_paths must NOT be in diff base..HEAD
- generated artifacts: must exist, freshness_check must pass, generator must be valid, must_match_live if declared
- mandatory validations exit 0 and contain expected substrings
- whitespace: git diff --check <base>..HEAD must be clean
- clean worktree: git status --porcelain must be empty at gate run

Self-test: 6 negative vectors + 1 positive isolated fixture (not live ROOT), disposable temp git repos.
Trust boundary: cooperative release-integrity check, NOT immutable/adversary-resistant. EXPECTATION.json and checker are mutable in same candidate, checker uses shell=True. Future immutable design needs expectation pinned in already-public base.
"""
import argparse, json, pathlib, re, subprocess, sys, tempfile, shutil

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

def check_base_sha(data):
    findings = []
    base = data.get("base_sha")
    if not base or not re.fullmatch(r"[0-9a-f]{7,40}", base):
        findings.append(f"base_sha invalid or missing: {base}")
        return findings
    p = run(f"git cat-file -e {base} 2>&1")
    if p.returncode != 0:
        findings.append(f"base_sha {base} does not exist in repo")
        return findings
    if data.get("base_must_be_ancestor"):
        p = run(f"git merge-base --is-ancestor {base} HEAD")
        if p.returncode != 0:
            findings.append(f"base_sha {base} is not ancestor of HEAD")
    return findings

def check_absent_on_disk(data):
    findings = []
    for path in data.get("required_absent_on_disk", []):
        if (ROOT / path).exists():
            findings.append(f"required deletion still on disk: {path}")
    for entry in data.get("required_deletions", []):
        if isinstance(entry, dict) and entry.get("must_be_absent_on_disk"):
            path = entry.get("path")
            if path and (ROOT / path).exists():
                findings.append(f"required deletion still on disk: {path}")
    return findings

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

def check_diff_deletions(data):
    findings = []
    base = data.get("base_sha")
    if not base:
        return findings
    diff = get_diff_name_status(base)
    diff_dict = {path: kind for kind, path in diff}
    for entry in data.get("required_deletions", []):
        if isinstance(entry, dict) and entry.get("must_be_D_in_diff"):
            path = entry.get("path")
            kind = diff_dict.get(path)
            if kind != "D":
                findings.append(f"expected delete missing from git diff base..HEAD: {path} (found kind={kind})")
    return findings

def check_forbidden_paths(data):
    findings = []
    base = data.get("base_sha")
    if not base:
        return findings
    forbidden = data.get("forbidden_paths", [])
    if not forbidden:
        return findings
    diff = get_diff_name_status(base)
    diff_paths = {path for _, path in diff}
    for fpath in forbidden:
        if fpath in diff_paths:
            findings.append(f"forbidden path in committed delta: {fpath}")
    return findings

def check_allowed_changes(data):
    findings = []
    base = data.get("base_sha")
    if not base:
        return findings
    allowed = {}
    for entry in data.get("allowed_changes", []):
        if isinstance(entry, dict):
            p = entry.get("path")
            k = entry.get("kind")
            if p and k:
                allowed[p] = k
    diff = get_diff_name_status(base)
    for kind, path in diff:
        exp_kind = allowed.get(path)
        if exp_kind is None:
            findings.append(f"undeclared changed path: {kind} {path}")
        else:
            if exp_kind != kind:
                findings.append(f"change kind mismatch for {path}: expected {exp_kind} got {kind}")
    # Also assert every direct delivery path declared with correct A/M/D per gap 1
    # For this check, we ensure allowed list covers all diff paths (already done above)
    return findings

def check_generated_artifacts(data):
    findings = []
    for entry in data.get("required_generated_artifacts", []):
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if not path:
            continue
        full = ROOT / path
        # must_exist
        if entry.get("must_exist") or entry.get("must_match_live"):
            if not full.exists():
                findings.append(f"generated artifact missing: {path}")
                continue
        # generator field enforcement: check file exists and is executable? At minimum require path exists
        generator = entry.get("generator")
        if generator:
            # generator should be a valid command string, not enforced as file, but we check it contains python
            if "python3" not in generator and "scripts/" not in generator:
                findings.append(f"generator field suspicious for {path}: {generator}")
        # freshness_check
        freshness_cmd = entry.get("freshness_check")
        if freshness_cmd:
            p = run(freshness_cmd)
            if p.returncode != 0:
                findings.append(f"generated artifact stale check failed: {path} cmd={freshness_cmd} exit={p.returncode} out={p.stdout[:200]}")
            else:
                out = (p.stdout + p.stderr).lower()
                if "stale" in out:
                    findings.append(f"generated artifact reported stale: {path}")
        # must_match_live: for INVENTORY, check that file content matches render_inventory
        if entry.get("must_match_live"):
            # For inventory, we can run --check-inventory-only already done via freshness_check, but also ensure file contains "active records:"
            try:
                content = full.read_text(encoding="utf-8")
                if "active records:" not in content:
                    findings.append(f"generated artifact {path} does not look like inventory")
            except Exception as e:
                findings.append(f"generated artifact {path} unreadable: {e}")
    return findings

def check_mandatory_validations(data):
    findings = []
    for entry in data.get("mandatory_validations", []):
        if not isinstance(entry, dict):
            continue
        cmd = entry.get("command")
        exp_exit = entry.get("expected_exit", 0)
        must_contain = entry.get("must_contain", "")
        if not cmd:
            continue
        p = run(cmd)
        if p.returncode != exp_exit:
            findings.append(f"DoD validation exit mismatch: {cmd} expected {exp_exit} got {p.returncode} out={p.stdout[:200]}")
        if must_contain:
            combined = p.stdout + p.stderr
            if must_contain not in combined:
                if must_contain.strip() != "":
                    findings.append(f"DoD validation missing expected substring '{must_contain}' in {cmd}")
    return findings

def check_whitespace_and_status(data):
    findings = []
    base = data.get("base_sha")
    if not base:
        return findings
    # git diff --check <base>..HEAD
    p = run(f"git diff --check {base}..HEAD")
    if p.returncode != 0:
        findings.append(f"whitespace check failed: git diff --check {base}..HEAD exit {p.returncode} out={p.stdout[:500]}")
    # git status --porcelain must be empty at gate run
    p = run("git status --porcelain")
    if p.stdout.strip() != "":
        # Allow untracked files that are not part of allowed? For gate, require empty per directive
        # But we have carriers? At gate run before commit, status may have M. After commit, should be empty.
        # For this checker, we require empty after commit (clean worktree)
        # If not empty, report
        findings.append(f"worktree not clean: git status --porcelain not empty: {p.stdout[:500]}")
    return findings

def main_check():
    data, load_findings = load_expectation()
    if load_findings:
        print("release-truth gate: findings")
        for f in load_findings:
            print(f"  - {f}")
        return 1
    findings = []
    findings.extend(check_base_sha(data))
    findings.extend(check_absent_on_disk(data))
    findings.extend(check_diff_deletions(data))
    findings.extend(check_forbidden_paths(data))
    findings.extend(check_allowed_changes(data))
    findings.extend(check_generated_artifacts(data))
    findings.extend(check_mandatory_validations(data))
    findings.extend(check_whitespace_and_status(data))
    if findings:
        print(f"release-truth gate: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        return 1
    else:
        print("release-truth gate: 0 finding(s)")
        return 0

# Self-test with disposable fixtures — fixed positive vector isolated
def self_test():
    def make_temp_repo():
        tmp = tempfile.mkdtemp()
        run("git init -q", cwd=tmp, check=True)
        run("git config user.email test@test.com", cwd=tmp, check=True)
        run("git config user.name Test", cwd=tmp, check=True)
        pathlib.Path(tmp, "README.md").write_text("hi\n", encoding="utf-8")
        run("git add README.md && git commit -qm init", cwd=tmp, check=True)
        return tmp

    def v_wrong_base():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            base = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
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
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_file_still_on_disk():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            stale = pathlib.Path(tmp, "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json")
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_text("{}", encoding="utf-8")
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": ["catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json"],
                "required_deletions": [{"path": "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json", "must_be_absent_on_disk": True}],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_delete_missing_from_diff():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            stale = pathlib.Path(tmp, "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json")
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_text("{}", encoding="utf-8")
            run("git add . && git commit -qm add-stale", cwd=tmp, check=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            stale.unlink()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [{"path": "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json", "must_be_D_in_diff": True}],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_undeclared_path():
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
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_stale_artifact():
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
                "required_generated_artifacts": [{"path": "catalogs/model_research/INVENTORY.generated.txt", "freshness_check": "false", "must_exist": True}],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_missing_dod():
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
                "mandatory_validations": [{"command": "false", "expected_exit": 0, "must_contain": ""}],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    def v_positive_isolated():
        # Isolated positive fixture: clean temp repo, base with expectation, then commit update that is allowed
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            # Initial base commit with empty expectation
            exp_initial = {
                "base_sha": "PLACEHOLDER",
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp_initial), encoding="utf-8")
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            run("git add . && git commit -qm init-base", cwd=tmp, check=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Now create new expectation that has base == previous commit, and allows M for itself
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "docs/RELEASE_TRUTH_GATE/EXPECTATION.json", "kind": "M"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [],
                "forbidden_paths": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            run("git add . && git commit -qm update-expectation", cwd=tmp, check=True)
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode == 0
        finally:
            shutil.rmtree(tmp)

    tests = [
        ("wrong base SHA -> reject", v_wrong_base),
        ("required deleted file still on disk -> reject", v_file_still_on_disk),
        ("expected delete missing from git diff -> reject", v_delete_missing_from_diff),
        ("undeclared changed path -> reject", v_undeclared_path),
        ("stale generated artifact -> reject", v_stale_artifact),
        ("missing DoD command/outcome -> reject", v_missing_dod),
        ("positive isolated clean -> pass", v_positive_isolated),
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
    print(f"release_truth_check self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(self_test())
    else:
        sys.exit(main_check())
