#!/usr/bin/env python3
"""
skill_check.py — deterministic compile check for skill catalog spine (Dim-7/G4)

Checks (house finding style, exit 0/1):
- catalog valid vs schema (radiation.skill_card/1)
- every entry_path/eval_ref resolves
- unique ids
- status discipline (declared→note; deprecated→superseded_by)
- no eval-free active entries
- description ≤200, id pattern SKILL-NNN, kind/status/activation_note enums, tests[] array
- tests[] entries resolve (strict)

--self-test ≥4 vectors:
- repo passes
- broken eval_ref → FAIL
- eval-free active → FAIL
- unknown status → FAIL
- plus duplicate id, declared missing note, deprecated missing superseded_by, entry_path missing

Stdlib only, deterministic, no network.
"""

import json
import os
import re
import sys
import pathlib
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "skills" / "SKILL_CATALOG.json"
SCHEMA_PATH = ROOT / "schemas" / "skill_card.schema.json"

ID_PATTERN = re.compile(r"^SKILL-[0-9]{3}$")
KIND_ENUM = {"agent", "procedure"}
STATUS_ENUM = {"active", "declared", "deprecated"}
ACTIVATION_ENUM = {"pinned", "asserted"}

def load_catalog(path=CATALOG_PATH):
    if not path.exists():
        return None, [f"catalog missing: {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"catalog unparseable: {e}"]
    if not isinstance(data, list):
        return None, [f"catalog must be JSON array, got {type(data)}"]
    return data, []

def validate_skill_schema(entry, idx):
    errors = []
    required = ["id", "title", "entry_path", "kind", "description", "eval_ref", "status", "activation_note", "tests"]
    for field in required:
        if field not in entry:
            errors.append(f"[{idx}] missing required field '{field}'")
    if errors:
        return errors

    cid = entry.get("id", "")
    if not isinstance(cid, str) or not ID_PATTERN.match(cid):
        errors.append(f"[{cid or idx}] id pattern mismatch '{cid}' must match {ID_PATTERN.pattern}")

    title = entry.get("title", "")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"[{cid}] title must be non-empty string")

    entry_path = entry.get("entry_path", "")
    if not isinstance(entry_path, str) or not entry_path.strip():
        errors.append(f"[{cid}] entry_path must be non-empty string")
    else:
        # Pattern from schema: starts with agents/, scaffolding/, subskills/, docs/, 01-, etc.
        if not re.match(r"^(agents/|scaffolding/|subskills/|docs/|01-|02-|03-|04-|05-|06-|07-|08-|09-).+", entry_path):
            errors.append(f"[{cid}] entry_path pattern mismatch '{entry_path}' must start with agents/|scaffolding/|subskills/|docs/|01-..09-")

    kind = entry.get("kind")
    if kind not in KIND_ENUM:
        errors.append(f"[{cid}] kind enum mismatch '{kind}' not in {KIND_ENUM}")

    desc = entry.get("description", "")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"[{cid}] description must be non-empty")
    elif len(desc) > 200:
        errors.append(f"[{cid}] description length {len(desc)} exceeds 200")

    eval_ref = entry.get("eval_ref", "")
    if not isinstance(eval_ref, str) or not eval_ref.strip():
        errors.append(f"[{cid}] eval_ref must be non-empty string")

    status = entry.get("status")
    if status not in STATUS_ENUM:
        errors.append(f"[{cid}] status enum mismatch '{status}' not in {STATUS_ENUM}")

    activation_note = entry.get("activation_note")
    if activation_note not in ACTIVATION_ENUM:
        errors.append(f"[{cid}] activation_note enum mismatch '{activation_note}' not in {ACTIVATION_ENUM}")

    tests = entry.get("tests")
    if not isinstance(tests, list) or not all(isinstance(t, str) for t in tests):
        errors.append(f"[{cid}] tests must be array of strings")

    # status discipline
    if status == "declared" and "note" not in entry:
        errors.append(f"[{cid}] declared status must carry note")
    if status == "deprecated" and "superseded_by" not in entry:
        errors.append(f"[{cid}] deprecated status must carry superseded_by")
    if status == "deprecated" and "superseded_by" in entry:
        sb = entry["superseded_by"]
        if not isinstance(sb, str) or not ID_PATTERN.match(sb):
            errors.append(f"[{cid}] superseded_by pattern mismatch '{sb}' must match {ID_PATTERN.pattern}")

    # additionalProperties false
    allowed_fields = {"id", "title", "entry_path", "kind", "description", "eval_ref", "status", "activation_note", "tests", "note", "superseded_by"}
    for k in entry.keys():
        if k not in allowed_fields:
            errors.append(f"[{cid}] additional property '{k}' not allowed")

    return errors

def check_skills(catalog_path=CATALOG_PATH, root=ROOT):
    findings = []

    data, load_errs = load_catalog(catalog_path)
    if load_errs:
        findings.extend(load_errs)
        return findings
    # Validate each entry vs schema
    seen_ids = set()
    for idx, entry in enumerate(data):
        cid = entry.get("id", f"idx-{idx}")
        errs = validate_skill_schema(entry, idx)
        for e in errs:
            findings.append(f"{catalog_path.relative_to(root).as_posix() if catalog_path.is_relative_to(root) else str(catalog_path)}: schema violation: {e}")

        # unique ids
        if cid in seen_ids:
            findings.append(f"duplicate id '{cid}'")
        seen_ids.add(cid)

        # every entry_path/eval_ref resolves
        ep = entry.get("entry_path")
        if isinstance(ep, str) and ep.strip():
            ep_path = root / ep
            if not ep_path.exists():
                findings.append(f"{cid}: entry_path does not resolve: '{ep}'")

        er = entry.get("eval_ref")
        if isinstance(er, str) and er.strip():
            er_path = root / er
            if not er_path.exists():
                findings.append(f"{cid}: eval_ref does not resolve: '{er}'")

        # tests[] entries resolve (strict for P-17)
        tests = entry.get("tests", [])
        if isinstance(tests, list):
            for t in tests:
                if isinstance(t, str) and t.strip():
                    tp = root / t
                    if not tp.exists():
                        findings.append(f"{cid}: tests entry does not resolve: '{t}'")

        # no eval-free active entries
        status = entry.get("status")
        if status == "active":
            if not er or not isinstance(er, str) or not er.strip():
                findings.append(f"{cid}: active entry must have eval_ref (eval-free active)")
            else:
                # already checked existence above, but if empty string it's eval-free
                er_path = root / er
                if not er_path.exists():
                    # already reported as eval_ref does not resolve, but also counts as eval-free for discipline
                    pass

    # Seeds ≥8 entries or all found whichever greater — we enforce ≥8
    if len(data) < 8:
        findings.append(f"catalog must have ≥8 entries or all found, got {len(data)}")

    return findings

# ---------------- self-test vectors ----------------

def self_test():
    """
    ≥4 vectors:
    - repo passes
    - broken eval_ref → FAIL
    - eval-free active → FAIL
    - unknown status → FAIL
    Plus: duplicate id, declared missing note, deprecated missing superseded_by, entry_path missing
    """
    vectors = []

    def run_in_temp(temp_root: pathlib.Path, catalog_data):
        # Write catalog to temp_root/skills/SKILL_CATALOG.json
        (temp_root / "skills").mkdir(parents=True, exist_ok=True)
        cat_path = temp_root / "skills" / "SKILL_CATALOG.json"
        cat_path.write_text(json.dumps(catalog_data), encoding="utf-8")
        # Also need at least empty schemas dir for path resolution not needed but keep
        (temp_root / "schemas").mkdir(parents=True, exist_ok=True)
        # Copy schema if exists
        src_schema = ROOT / "schemas" / "skill_card.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, temp_root / "schemas" / "skill_card.schema.json")
        findings = check_skills(catalog_path=cat_path, root=temp_root)
        return findings

    def make_valid_entry(suffix="001", status="active", eval_ref="evals/skills/SKILL-001.eval.md", entry_path="agents/Arena_AI/BOOT.md", extra=None):
        base = {
            "id": f"SKILL-{suffix}",
            "title": f"Test skill {suffix}",
            "entry_path": entry_path,
            "kind": "agent",
            "description": f"Test description for skill {suffix} valid ≤200.",
            "eval_ref": eval_ref,
            "status": status,
            "activation_note": "asserted",
            "tests": [eval_ref] if eval_ref else []
        }
        if extra:
            base.update(extra)
        return base

    def vector_repo_passes():
        # Use real repo catalog
        findings = check_skills()
        ok = len(findings) == 0
        return ok, findings

    def vector_broken_eval_ref():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            # Create entry_path file
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            # Do NOT create eval file
            entry = make_valid_entry("001", status="active", eval_ref="evals/skills/missing.eval.md", entry_path="agents/Arena_AI/BOOT.md")
            findings = run_in_temp(tr, [entry])
            ok = any("eval_ref does not resolve" in f for f in findings)
            return ok, findings

    def vector_eval_free_active():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            entry = make_valid_entry("001", status="active", eval_ref="", entry_path="agents/Arena_AI/BOOT.md")
            # Manually set eval_ref empty and tests empty to trigger eval-free
            entry["eval_ref"] = ""
            entry["tests"] = []
            findings = run_in_temp(tr, [entry])
            # Should have schema violation for eval_ref empty + eval-free active or schema violation
            ok = any("eval_ref" in f for f in findings)
            return ok, findings

    def vector_unknown_status():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            entry = make_valid_entry("001", status="active", eval_ref="evals/skills/SKILL-001.eval.md", entry_path="agents/Arena_AI/BOOT.md")
            entry["status"] = "unknown_status"
            findings = run_in_temp(tr, [entry])
            ok = any("status enum" in f for f in findings)
            return ok, findings

    def vector_duplicate_id():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            e1 = make_valid_entry("001", eval_ref="evals/skills/SKILL-001.eval.md")
            e2 = make_valid_entry("001", eval_ref="evals/skills/SKILL-001.eval.md")
            findings = run_in_temp(tr, [e1, e2])
            ok = any("duplicate id" in f for f in findings)
            return ok, findings

    def vector_declared_missing_note():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            entry = make_valid_entry("001", status="declared", eval_ref="evals/skills/SKILL-001.eval.md")
            # no note
            findings = run_in_temp(tr, [entry])
            ok = any("declared" in f and "note" in f for f in findings)
            return ok, findings

    def vector_deprecated_missing_superseded():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "agents" / "Arena_AI").mkdir(parents=True, exist_ok=True)
            (tr / "agents" / "Arena_AI" / "BOOT.md").write_text("# boot\n", encoding="utf-8")
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            entry = make_valid_entry("001", status="deprecated", eval_ref="evals/skills/SKILL-001.eval.md")
            findings = run_in_temp(tr, [entry])
            ok = any("deprecated" in f and "superseded_by" in f for f in findings)
            return ok, findings

    def vector_entry_path_missing():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "evals" / "skills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "skills" / "SKILL-001.eval.md").write_text("# eval\n", encoding="utf-8")
            entry = make_valid_entry("001", entry_path="agents/Arena_AI/MISSING.md", eval_ref="evals/skills/SKILL-001.eval.md")
            findings = run_in_temp(tr, [entry])
            ok = any("entry_path does not resolve" in f for f in findings)
            return ok, findings

    tests = [
        ("repo passes (positive)", vector_repo_passes),
        ("broken eval_ref → FAIL", vector_broken_eval_ref),
        ("eval-free active → FAIL", vector_eval_free_active),
        ("unknown status → FAIL", vector_unknown_status),
        ("duplicate id → FAIL", vector_duplicate_id),
        ("declared missing note → FAIL", vector_declared_missing_note),
        ("deprecated missing superseded_by → FAIL", vector_deprecated_missing_superseded),
        ("entry_path missing → FAIL", vector_entry_path_missing),
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

    print(f"\nskill_check self-test: {passed} passed, {failed} failed — {len(tests)} vectors")
    return failed == 0

def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    findings = check_skills()
    if findings:
        print(f"skill_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("skill_check: 0 finding(s) — catalog valid, entry_path/eval_ref resolve, unique ids, status discipline ok, no eval-free active")
        sys.exit(0)

if __name__ == "__main__":
    main()
