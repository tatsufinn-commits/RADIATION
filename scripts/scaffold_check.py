#!/usr/bin/env python3
"""
scaffold_check.py — deterministic compile check for scaffolding contract spine (Dim-3/G4)

Checks (house finding style, exit 0/1):
- sidecar valid vs schema (radiation.scaffold_contract/1)
- every depends_on id resolves to an existing contract
- every scaffold *.md/*.json has a sidecar (or whitelisted)
- deprecated must carry superseded_by
- draft must carry note
- no cycles in depends_on graph
- file-must-exist: contract file field must exist
- unique ids, id pattern, kind/status enums

--self-test ≥4 vectors: sidecar valid vs schema · broken depends_on → FAIL · uncontracted file → FAIL · cycle → FAIL · deprecated missing superseded_by · draft missing note
Negative fixtures are its own corpus.

Stdlib only, deterministic, no network.
"""

import json
import os
import re
import sys
import pathlib
import tempfile
import shutil
from collections import defaultdict, deque

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAFF_DIR = ROOT / "scaffolding"
SCHEMA_PATH = ROOT / "schemas" / "scaffold_contract.schema.json"

# Whitelist for scaffold files that don't need sidecar — justified: .gitkeep are git placeholders, not scaffold content
WHITELIST = {
    # Example: if new .gitkeep appears without contract, it's whitelisted
    # We whitelist pattern, not specific files: any .gitkeep is whitelisted
}
WHITELIST_SUFFIXES = {".gitkeep"}

# Schema pattern checks (mirror schema)
ID_PATTERN = re.compile(r"^SCAFFOLD-(core|neuron|membrane|other)-[a-z0-9-]+$")
KIND_ENUM = {"core", "neuron", "membrane", "other"}
STATUS_ENUM = {"active", "draft", "deprecated"}
FILE_PATTERN = re.compile(r"^scaffolding/.+")

def load_schema():
    if SCHEMA_PATH.exists():
        try:
            return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def validate_contract_schema(contract, schema=None):
    """Basic schema validation without external lib, returns list of errors."""
    errors = []
    # Required fields
    required = ["id", "file", "kind", "status", "loads_when", "depends_on", "effects", "tests"]
    for field in required:
        if field not in contract:
            errors.append(f"missing required field '{field}'")
    if errors:
        return errors

    # id pattern
    cid = contract.get("id", "")
    if not ID_PATTERN.match(cid):
        errors.append(f"id pattern mismatch '{cid}' must match {ID_PATTERN.pattern}")

    # file pattern
    f = contract.get("file", "")
    if not FILE_PATTERN.match(f):
        errors.append(f"file pattern mismatch '{f}' must match {FILE_PATTERN.pattern}")

    # kind enum
    kind = contract.get("kind")
    if kind not in KIND_ENUM:
        errors.append(f"kind enum mismatch '{kind}' not in {KIND_ENUM}")

    # status enum
    status = contract.get("status")
    if status not in STATUS_ENUM:
        errors.append(f"status enum mismatch '{status}' not in {STATUS_ENUM}")

    # loads_when: string or null
    lw = contract.get("loads_when")
    if not (isinstance(lw, str) or lw is None):
        errors.append(f"loads_when must be string or null, got {type(lw)}")

    # depends_on: array of ids matching pattern
    depends = contract.get("depends_on")
    if not isinstance(depends, list):
        errors.append(f"depends_on must be array")
    else:
        for dep in depends:
            if not isinstance(dep, str) or not ID_PATTERN.match(dep):
                errors.append(f"depends_on entry pattern mismatch '{dep}'")

    # effects: array of strings
    effects = contract.get("effects")
    if not isinstance(effects, list) or not all(isinstance(e, str) for e in effects):
        errors.append(f"effects must be array of strings")

    # tests: array of strings
    tests = contract.get("tests")
    if not isinstance(tests, list) or not all(isinstance(t, str) for t in tests):
        errors.append(f"tests must be array of strings")

    # draft must carry note
    if status == "draft" and "note" not in contract:
        errors.append(f"draft status must carry note")

    # deprecated must carry superseded_by
    if status == "deprecated" and "superseded_by" not in contract:
        errors.append(f"deprecated status must carry superseded_by")
    if status == "deprecated" and "superseded_by" in contract:
        sb = contract["superseded_by"]
        if not isinstance(sb, str) or not ID_PATTERN.match(sb):
            errors.append(f"superseded_by pattern mismatch '{sb}'")

    # additionalProperties false: check no extra fields beyond allowed
    allowed_fields = {"id", "file", "kind", "status", "loads_when", "depends_on", "effects", "tests", "note", "superseded_by"}
    for k in contract.keys():
        if k not in allowed_fields:
            errors.append(f"additional property '{k}' not allowed")

    return errors

def find_scaffold_files():
    """Find all scaffold files under scaffolding/** excluding contract.json sidecars."""
    files = []
    if not SCAFF_DIR.exists():
        return files
    for p in SCAFF_DIR.rglob("*"):
        if p.is_file():
            # Exclude contract sidecars themselves
            if p.name.endswith(".contract.json"):
                continue
            files.append(p)
    return sorted(files)

def find_contract_files():
    """Find all sidecar contracts."""
    files = []
    if not SCAFF_DIR.exists():
        return files
    for p in SCAFF_DIR.rglob("*.contract.json"):
        if p.is_file():
            files.append(p)
    return sorted(files)

def is_whitelisted(scaffold_path: pathlib.Path):
    """Check if scaffold file is whitelisted (no sidecar needed)."""
    # Whitelist by suffix
    if scaffold_path.name in WHITELIST_SUFFIXES or scaffold_path.suffix in WHITELIST_SUFFIXES:
        return True
    # Whitelist by exact relative path
    rel = scaffold_path.relative_to(ROOT).as_posix()
    if rel in WHITELIST:
        return True
    # Whitelist pattern: any .gitkeep
    if scaffold_path.name == ".gitkeep":
        return True
    return False

def check_scaffolding():
    findings = []

    scaffold_files = find_scaffold_files()
    contract_files = find_contract_files()

    # Map file -> contract path expected: sibling X.contract.json
    expected_contracts = {}
    for sf in scaffold_files:
        expected = sf.with_name(sf.name + ".contract.json")
        expected_contracts[sf] = expected

    # Check every scaffold *.md/*.json has sidecar (or whitelisted)
    # Per directive: every scaffold *.md/*.json has a sidecar (or whitelisted)
    # We'll check all files, but focus on md/json as primary, others via whitelist
    for sf in scaffold_files:
        rel = sf.relative_to(ROOT).as_posix()
        # Only enforce for *.md and *.json (and maybe others? but spec says *.md/*.json)
        if sf.suffix not in {".md", ".json"}:
            # For non-md/json, allow whitelist
            if is_whitelisted(sf):
                continue
            # If not whitelisted and no contract, it's still a finding? The spec says every scaffold *.md/*.json has sidecar (or whitelisted)
            # So for non-md/json, we skip unless whitelisted check fails? We'll still check if contract exists, but not require? Safer to require for all files except whitelisted
            # For .gitkeep we already whitelisted, so skip
            if not expected_contracts[sf].exists():
                # For non-md/json not whitelisted, report as uncontracted only if it's not .gitkeep
                # We have .gitkeep whitelisted, so this won't trigger
                # For other non-md/json like maybe other extensions, we still want contract? But we have contracts for all, so skip
                pass
            continue
        # For md/json, check sidecar exists or whitelisted
        if is_whitelisted(sf):
            continue
        exp = expected_contracts[sf]
        if not exp.exists():
            findings.append(f"uncontracted scaffold file: {rel} missing sidecar {exp.relative_to(ROOT).as_posix()}")

    # Load contracts and validate
    contracts_by_id = {}
    contracts_by_file = {}
    all_ids = set()
    for cf in contract_files:
        try:
            data = json.loads(cf.read_text(encoding="utf-8"))
        except Exception as e:
            findings.append(f"{cf.relative_to(ROOT).as_posix()}: unparseable JSON: {e}")
            continue

        # Schema validation
        errs = validate_contract_schema(data)
        if errs:
            for err in errs:
                findings.append(f"{cf.relative_to(ROOT).as_posix()}: schema violation: {err}")
            # Continue still to check other rules if possible, but skip if id missing
            if "id" not in data:
                continue

        cid = data.get("id")
        if cid in all_ids:
            findings.append(f"duplicate id '{cid}' in {cf.relative_to(ROOT).as_posix()}")
        all_ids.add(cid)

        # file-must-exist
        file_field = data.get("file")
        if file_field:
            file_path = ROOT / file_field
            if not file_path.exists():
                findings.append(f"{cf.relative_to(ROOT).as_posix()}: file-must-exist FAIL: '{file_field}' does not exist")
            else:
                # Also check that contract is sibling of file? Not strictly required but good
                expected_sibling = file_path.with_name(file_path.name + ".contract.json")
                if expected_sibling.resolve() != cf.resolve():
                    # Allow if file field points to existing file but contract not sibling? That would be weird, but we flag as warning? For now, not a FAIL, just info
                    # We'll not flag as finding to keep lenient, but could
                    pass

        # Track
        if cid:
            if cid in contracts_by_id:
                # duplicate already reported
                pass
            else:
                contracts_by_id[cid] = data
        if file_field:
            contracts_by_file[file_field] = data

    # Check every depends_on id resolves
    for cid, data in contracts_by_id.items():
        depends = data.get("depends_on", [])
        for dep in depends:
            if dep not in contracts_by_id:
                findings.append(f"{cid}: depends_on id '{dep}' does not resolve to existing contract")

    # Check no cycles in depends_on graph
    # Build graph
    graph = {cid: set(data.get("depends_on", [])) for cid, data in contracts_by_id.items()}
    # Detect cycles via DFS
    visiting = set()
    visited = set()
    stack = []

    def dfs(node):
        if node in visited:
            return False
        if node in visiting:
            # Cycle found
            # Find cycle path
            try:
                idx = stack.index(node)
                cycle = stack[idx:] + [node]
                findings.append(f"cycle detected in depends_on graph: {' -> '.join(cycle)}")
            except ValueError:
                findings.append(f"cycle detected involving {node}")
            return True
        visiting.add(node)
        stack.append(node)
        has_cycle = False
        for neighbor in graph.get(node, []):
            if neighbor in contracts_by_id:  # only check existing nodes
                if dfs(neighbor):
                    has_cycle = True
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return has_cycle

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)

    return findings

# ---------------- self-test vectors ----------------

def self_test():
    """
    ≥4 vectors:
    - sidecar valid vs schema
    - broken depends_on → FAIL
    - uncontracted file → FAIL
    - cycle → FAIL
    - deprecated missing superseded_by
    - draft missing note
    """
    vectors = []

    def run_in_temp(temp_root: pathlib.Path):
        # Override ROOT, SCAFF_DIR, SCHEMA_PATH temporarily
        global ROOT, SCAFF_DIR, SCHEMA_PATH
        old_root = ROOT
        old_scaff = SCAFF_DIR
        old_schema = SCHEMA_PATH
        try:
            ROOT = temp_root
            SCAFF_DIR = temp_root / "scaffolding"
            SCHEMA_PATH = temp_root / "schemas" / "scaffold_contract.schema.json"
            findings = check_scaffolding()
            return findings
        finally:
            ROOT = old_root
            SCAFF_DIR = old_scaff
            SCHEMA_PATH = old_schema

    def vector_valid():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            # Copy schema
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            else:
                (tr / "schemas" / "scaffold_contract.schema.json").write_text("{}", encoding="utf-8")
            # Create scaffold file and valid contract
            sf = tr / "scaffolding" / "core" / "test.md"
            sf.write_text("# test\n", encoding="utf-8")
            contract = {
                "id": "SCAFFOLD-core-test-md",
                "file": "scaffolding/core/test.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": [],
                "effects": ["read"],
                "tests": []
            }
            (tr / "scaffolding" / "core" / "test.md.contract.json").write_text(json.dumps(contract), encoding="utf-8")
            findings = run_in_temp(tr)
            ok = len(findings) == 0
            return ok, findings

    def vector_broken_depends():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "test.md"
            sf.write_text("# test\n", encoding="utf-8")
            contract = {
                "id": "SCAFFOLD-core-test-md",
                "file": "scaffolding/core/test.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-nonexistent"],
                "effects": ["read"],
                "tests": []
            }
            (tr / "scaffolding" / "core" / "test.md.contract.json").write_text(json.dumps(contract), encoding="utf-8")
            findings = run_in_temp(tr)
            ok = any("depends_on" in f and "does not resolve" in f for f in findings)
            return ok, findings

    def vector_uncontracted():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "orphan.md"
            sf.write_text("# orphan\n", encoding="utf-8")
            # No contract
            findings = run_in_temp(tr)
            ok = any("uncontracted" in f for f in findings)
            return ok, findings

    def vector_cycle():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            # Two files that depend on each other
            sf1 = tr / "scaffolding" / "core" / "a.md"
            sf1.write_text("# a\n", encoding="utf-8")
            sf2 = tr / "scaffolding" / "core" / "b.md"
            sf2.write_text("# b\n", encoding="utf-8")
            c1 = {
                "id": "SCAFFOLD-core-a-md",
                "file": "scaffolding/core/a.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-b-md"],
                "effects": ["read"],
                "tests": []
            }
            c2 = {
                "id": "SCAFFOLD-core-b-md",
                "file": "scaffolding/core/b.md",
                "kind": "core",
                "status": "active",
                "loads_when": None,
                "depends_on": ["SCAFFOLD-core-a-md"],
                "effects": ["read"],
                "tests": []
            }
            (tr / "scaffolding" / "core" / "a.md.contract.json").write_text(json.dumps(c1), encoding="utf-8")
            (tr / "scaffolding" / "core" / "b.md.contract.json").write_text(json.dumps(c2), encoding="utf-8")
            findings = run_in_temp(tr)
            ok = any("cycle" in f.lower() for f in findings)
            return ok, findings

    def vector_deprecated_missing():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "old.md"
            sf.write_text("# old\n", encoding="utf-8")
            contract = {
                "id": "SCAFFOLD-core-old-md",
                "file": "scaffolding/core/old.md",
                "kind": "core",
                "status": "deprecated",
                "loads_when": None,
                "depends_on": [],
                "effects": ["read"],
                "tests": []
                # missing superseded_by
            }
            (tr / "scaffolding" / "core" / "old.md.contract.json").write_text(json.dumps(contract), encoding="utf-8")
            findings = run_in_temp(tr)
            ok = any("deprecated" in f and "superseded_by" in f for f in findings)
            return ok, findings

    def vector_draft_missing():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "scaffolding" / "core").mkdir(parents=True)
            (tr / "schemas").mkdir(parents=True)
            schema_src = pathlib.Path(__file__).resolve().parent.parent / "schemas" / "scaffold_contract.schema.json"
            if schema_src.exists():
                shutil.copy(schema_src, tr / "schemas" / "scaffold_contract.schema.json")
            sf = tr / "scaffolding" / "core" / "draft.md"
            sf.write_text("# draft\n", encoding="utf-8")
            contract = {
                "id": "SCAFFOLD-core-draft-md",
                "file": "scaffolding/core/draft.md",
                "kind": "core",
                "status": "draft",
                "loads_when": None,
                "depends_on": [],
                "effects": ["read"],
                "tests": []
                # missing note
            }
            (tr / "scaffolding" / "core" / "draft.md.contract.json").write_text(json.dumps(contract), encoding="utf-8")
            findings = run_in_temp(tr)
            ok = any("draft" in f and "note" in f for f in findings)
            return ok, findings

    tests = [
        ("sidecar valid vs schema (positive)", vector_valid),
        ("broken depends_on → FAIL", vector_broken_depends),
        ("uncontracted file → FAIL", vector_uncontracted),
        ("cycle → FAIL", vector_cycle),
        ("deprecated missing superseded_by → FAIL", vector_deprecated_missing),
        ("draft missing note → FAIL", vector_draft_missing),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        ok, findings = fn()
        if ok:
            print(f"  ✅ self-test vector PASS: {name}")
            passed += 1
        else:
            print(f"  ❌ self-test vector FAIL: {name} — findings: {findings}")
            failed += 1

    print(f"\nscaffold_check self-test: {passed} passed, {failed} failed — {len(tests)} vectors")
    return failed == 0

def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    findings = check_scaffolding()
    if findings:
        print(f"scaffold_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("scaffold_check: 0 finding(s) — all sidecars valid, depends_on resolves, no cycles, coverage ok")
        sys.exit(0)

if __name__ == "__main__":
    main()
