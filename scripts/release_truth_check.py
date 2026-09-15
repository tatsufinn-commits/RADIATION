#!/usr/bin/env python3
"""
release_truth_check.py — Release Truth Gate checker (5824)

Checks:
- base SHA exists and is ancestor of HEAD
- required deletions absent on disk + D in diff
- allowed changes only (A/M/D) with no undeclared paths
- generated artifacts fresh
- mandatory validations exit 0 and contain expected substrings

Self-test: 6 negative vectors + 1 positive, disposable temp git repos.
"""
import argparse, json, os, pathlib, re, subprocess, sys, tempfile, shutil

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
    # Check exists
    p = run(f"git cat-file -e {base} 2>&1")
    if p.returncode != 0:
        findings.append(f"base_sha {base} does not exist in repo")
        return findings
    # Check ancestor if required
    if data.get("base_must_be_ancestor"):
        # git merge-base --is-ancestor base HEAD
        p = run(f"git merge-base --is-ancestor {base} HEAD")
        if p.returncode != 0:
            findings.append(f"base_sha {base} is not ancestor of HEAD")
    return findings

def check_absent_on_disk(data):
    findings = []
    for path in data.get("required_absent_on_disk", []):
        full = ROOT / path
        if full.exists():
            findings.append(f"required deletion still on disk: {path}")
    for entry in data.get("required_deletions", []):
        if isinstance(entry, dict) and entry.get("must_be_absent_on_disk"):
            path = entry.get("path")
            if path and (ROOT / path).exists():
                findings.append(f"required deletion still on disk: {path}")
    return findings

def get_diff_name_status(base):
    # git diff base..HEAD --name-status
    p = run(f"git diff {base}..HEAD --name-status")
    if p.returncode != 0:
        # fallback to diff --cached if no base..HEAD?
        return []
    lines = []
    for line in p.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            kind = parts[0][0]  # A, M, D, R etc
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
            # Check if path is in allowed as prefix? No, exact match required
            findings.append(f"undeclared changed path: {kind} {path}")
        else:
            # Kind check: allow M when expected A? Strict: kind must match expected or be compatible?
            # For simplicity, require exact kind match, but allow M for A? We require exact.
            if exp_kind != kind:
                # Allow A vs M flexibility? For this gate, we expect exact, but warn if mismatch
                findings.append(f"change kind mismatch for {path}: expected {exp_kind} got {kind}")
    return findings

def check_generated_artifacts(data):
    findings = []
    for entry in data.get("required_generated_artifacts", []):
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        freshness_cmd = entry.get("freshness_check")
        if not path:
            continue
        if freshness_cmd:
            p = run(freshness_cmd)
            if p.returncode != 0:
                findings.append(f"generated artifact stale check failed: {path} cmd={freshness_cmd} exit={p.returncode}")
            else:
                # Optionally check output contains "current" or "0 finding"
                out = (p.stdout + p.stderr).lower()
                if "stale" in out:
                    findings.append(f"generated artifact reported stale: {path}")
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
            findings.append(f"DoD validation exit mismatch: {cmd} expected {exp_exit} got {p.returncode}")
        if must_contain:
            combined = p.stdout + p.stderr
            if must_contain not in combined:
                # For empty must_contain, skip
                if must_contain.strip() != "":
                    findings.append(f"DoD validation missing expected substring '{must_contain}' in {cmd}")
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
    findings.extend(check_allowed_changes(data))
    findings.extend(check_generated_artifacts(data))
    findings.extend(check_mandatory_validations(data))
    if findings:
        print(f"release-truth gate: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        return 1
    else:
        print("release-truth gate: 0 finding(s)")
        return 0

# Self-test with disposable fixtures
def self_test():
    vectors = []

    def make_temp_repo():
        tmp = tempfile.mkdtemp()
        run("git init -q", cwd=tmp, check=True)
        run("git config user.email test@test.com", cwd=tmp, check=True)
        run("git config user.name Test", cwd=tmp, check=True)
        pathlib.Path(tmp, "README.md").write_text("hi\n", encoding="utf-8")
        run("git add README.md && git commit -qm init", cwd=tmp, check=True)
        return tmp

    # Vector 1: wrong base SHA -> reject
    def v_wrong_base():
        tmp = make_temp_repo()
        try:
            # Create expectation with wrong base
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
                "mandatory_validations": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            # Run checker in tmp
            # Copy checker script
            checker_src = ROOT / "scripts" / "release_truth_check.py"
            shutil.copy(str(checker_src), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            # Should fail (non-zero) because base does not exist
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Vector 2: required deleted file still on disk -> reject
    def v_file_still_on_disk():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            # Get current HEAD as base
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Create a file that should be absent
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
                "mandatory_validations": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Vector 3: expected delete missing from git diff -> reject
    def v_delete_missing_from_diff():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            # Create file, commit it, then delete without staging? Actually need base with file present, HEAD without file but not D in diff? Simplest: base has file, HEAD also has file deleted but we don't stage D? We need diff base..HEAD to NOT contain D, but file absent on disk check passes? Let's simulate: base has file, we delete file on disk but don't commit, so diff base..HEAD shows no D (since HEAD still has file), but file absent on disk passes absent check? Actually we want delete missing from diff vector: required deletion says must_be_D_in_diff true, but diff does not contain D.
            stale = pathlib.Path(tmp, "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json")
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_text("{}", encoding="utf-8")
            run("git add . && git commit -qm add-stale", cwd=tmp, check=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Now delete file on disk but NOT commit, and also remove from index? Actually to make diff base..HEAD have no D, we need HEAD to still have file. So we keep HEAD with file, but we delete file on disk and set expectation that file must be D in diff — it won't be D because HEAD still has it, only working tree deletion. So diff base..HEAD will be empty (since base==HEAD), not D.
            # Remove file on disk
            stale.unlink()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [{"path": "catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json", "must_be_D_in_diff": True}],
                "required_generated_artifacts": [],
                "mandatory_validations": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Vector 4: undeclared changed path -> reject
    def v_undeclared_path():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Create undeclared file and commit
            pathlib.Path(tmp, "evil.txt").write_text("evil", encoding="utf-8")
            run("git add evil.txt && git commit -qm evil", cwd=tmp, check=True)
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [{"path": "README.md", "kind": "M"}],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Vector 5: stale generated artifact -> reject
    def v_stale_artifact():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            # Create a freshness check that fails
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [{"path": "catalogs/model_research/INVENTORY.generated.txt", "freshness_check": "false"}],
                "mandatory_validations": []
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Vector 6: missing DoD command/outcome -> reject
    def v_missing_dod():
        tmp = make_temp_repo()
        try:
            exp_dir = pathlib.Path(tmp, "docs/RELEASE_TRUTH_GATE")
            exp_dir.mkdir(parents=True, exist_ok=True)
            p = run("git rev-parse HEAD", cwd=tmp)
            base = p.stdout.strip()
            exp = {
                "base_sha": base,
                "base_must_be_ancestor": True,
                "allowed_changes": [],
                "required_absent_on_disk": [],
                "required_deletions": [],
                "required_generated_artifacts": [],
                "mandatory_validations": [{"command": "false", "expected_exit": 0, "must_contain": ""}]
            }
            (exp_dir / "EXPECTATION.json").write_text(json.dumps(exp), encoding="utf-8")
            pathlib.Path(tmp, "scripts").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "release_truth_check.py"), str(pathlib.Path(tmp, "scripts/release_truth_check.py")))
            p = run("python3 scripts/release_truth_check.py", cwd=tmp)
            return p.returncode != 0
        finally:
            shutil.rmtree(tmp)

    # Positive vector: clean repo should pass
    def v_positive():
        # Use current ROOT which is clean green
        p = run("python3 scripts/release_truth_check.py", cwd=ROOT)
        return p.returncode == 0

    tests = [
        ("wrong base SHA -> reject", v_wrong_base),
        ("required deleted file still on disk -> reject", v_file_still_on_disk),
        ("expected delete missing from git diff -> reject", v_delete_missing_from_diff),
        ("undeclared changed path -> reject", v_undeclared_path),
        ("stale generated artifact -> reject", v_stale_artifact),
        ("missing DoD command/outcome -> reject", v_missing_dod),
        ("positive clean -> pass", v_positive),
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
