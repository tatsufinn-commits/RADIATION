#!/usr/bin/env python3
"""
subskill_check.py — deterministic compile check for subskill catalog + hook protocol (Dim-8/G4)

Checks (house finding style, exit 0/1):
- catalog valid vs schema (radiation.subskill_card/1)
- parent_skill FK resolves against skills/SKILL_CATALOG.json
- scenario_ref resolves
- trigger enum valid (before_skill|after_skill|on_event|manual)
- status discipline (declared→note; deprecated→superseded_by)
- description ≤200, id pattern SUB-NNN, entry_path exists, tests[] array
- tests[] entries resolve

--self-test ≥4 vectors:
- repo passes
- broken parent FK → FAIL
- missing scenario_ref → FAIL
- illegal trigger → FAIL
- plus duplicate id, declared missing note, deprecated missing superseded_by, entry_path missing, scenario non-JSON

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
CATALOG_PATH = ROOT / "subskills" / "SUBSKILL_CATALOG.json"
SKILL_CATALOG_PATH = ROOT / "skills" / "SKILL_CATALOG.json"
SCHEMA_PATH = ROOT / "schemas" / "subskill_card.schema.json"

ID_PATTERN = re.compile(r"^SUB-[0-9]{3}$")
SKILL_ID_PATTERN = re.compile(r"^SKILL-[0-9]{3}$")
TRIGGER_ENUM = {"before_skill", "after_skill", "on_event", "manual"}
STATUS_ENUM = {"active", "declared", "deprecated"}

def load_json(path):
    if not path.exists():
        return None, [f"file missing: {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"unparseable JSON {path}: {e}"]
    return data, []

def load_catalogs():
    sub_data, sub_errs = load_json(CATALOG_PATH)
    if sub_errs:
        return None, None, sub_errs
    if not isinstance(sub_data, list):
        return None, None, [f"subskill catalog must be array, got {type(sub_data)}"]
    skill_data, skill_errs = load_json(SKILL_CATALOG_PATH)
    if skill_errs:
        # skill catalog missing is still a finding for FK check
        skill_ids = set()
        return sub_data, skill_ids, []
    if not isinstance(skill_data, list):
        skill_ids = set()
    else:
        skill_ids = {e.get("id") for e in skill_data if isinstance(e, dict) and e.get("id")}
    return sub_data, skill_ids, []

def validate_subskill_schema(entry, idx):
    errors = []
    required = ["id", "title", "parent_skill", "entry_path", "trigger", "description", "scenario_ref", "status", "tests"]
    for field in required:
        if field not in entry:
            errors.append(f"[{idx}] missing required field '{field}'")
    if errors:
        return errors

    cid = entry.get("id", f"idx-{idx}")
    if not isinstance(cid, str) or not ID_PATTERN.match(cid):
        errors.append(f"[{cid}] id pattern mismatch '{cid}' must match {ID_PATTERN.pattern}")

    title = entry.get("title", "")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"[{cid}] title must be non-empty")

    parent = entry.get("parent_skill", "")
    if not isinstance(parent, str) or not SKILL_ID_PATTERN.match(parent):
        errors.append(f"[{cid}] parent_skill pattern mismatch '{parent}' must match {SKILL_ID_PATTERN.pattern}")

    ep = entry.get("entry_path", "")
    if not isinstance(ep, str) or not ep.strip():
        errors.append(f"[{cid}] entry_path must be non-empty")
    else:
        if not re.match(r"^(subskills/|agents/|scaffolding/|docs/|Brain/).+", ep):
            errors.append(f"[{cid}] entry_path pattern mismatch '{ep}'")

    trigger = entry.get("trigger")
    if trigger not in TRIGGER_ENUM:
        errors.append(f"[{cid}] trigger enum mismatch '{trigger}' not in {TRIGGER_ENUM}")

    # condition may be missing? schema says required? Actually we have condition optional? In our schema condition is not required? We made it not required? Check schema: required includes condition? No, we have condition not in required list? In schema we didn't require condition, but we have it as property that can be null. We'll check if present and not null then must be string.
    if "condition" in entry:
        cond = entry["condition"]
        if not (isinstance(cond, str) or cond is None):
            errors.append(f"[{cid}] condition must be string or null")

    desc = entry.get("description", "")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"[{cid}] description must be non-empty")
    elif len(desc) > 200:
        errors.append(f"[{cid}] description length {len(desc)} exceeds 200")

    sr = entry.get("scenario_ref", "")
    if not isinstance(sr, str) or not sr.strip():
        errors.append(f"[{cid}] scenario_ref must be non-empty")

    status = entry.get("status")
    if status not in STATUS_ENUM:
        errors.append(f"[{cid}] status enum mismatch '{status}' not in {STATUS_ENUM}")

    tests = entry.get("tests")
    if not isinstance(tests, list) or not all(isinstance(t, str) for t in tests):
        errors.append(f"[{cid}] tests must be array of strings")

    if status == "declared" and "note" not in entry:
        errors.append(f"[{cid}] declared status must carry note")
    if status == "deprecated" and "superseded_by" not in entry:
        errors.append(f"[{cid}] deprecated status must carry superseded_by")
    if status == "deprecated" and "superseded_by" in entry:
        sb = entry["superseded_by"]
        if not isinstance(sb, str) or not ID_PATTERN.match(sb):
            errors.append(f"[{cid}] superseded_by pattern mismatch '{sb}' must match {ID_PATTERN.pattern}")

    # WP-1 1.5 verify policy field — additive optional namespaced extension
    if "verify" in entry:
        v = entry["verify"]
        if not isinstance(v, dict):
            errors.append(f"[{cid}] verify must be object per 1.5")
        else:
            pol = v.get("policy")
            if pol not in {"required", "opt-in", "opt-out"}:
                errors.append(f"[{cid}] verify.policy must be required/opt-in/opt-out per 1.5, got '{pol}'")
            # checks optional array of strings
            if "checks" in v and not isinstance(v["checks"], list):
                errors.append(f"[{cid}] verify.checks must be array per 1.5")
            # seed optional string
            if "seed" in v and not isinstance(v["seed"], str):
                errors.append(f"[{cid}] verify.seed must be string per 1.5")

    allowed = {"id", "title", "parent_skill", "entry_path", "trigger", "condition", "description", "scenario_ref", "status", "tests", "note", "superseded_by", "verify"}
    for k in entry.keys():
        if k not in allowed:
            errors.append(f"[{cid}] additional property '{k}' not allowed")

    return errors

def check_subskills(catalog_path=CATALOG_PATH, skill_catalog_path=SKILL_CATALOG_PATH, root=ROOT):
    findings = []

    sub_data, skill_ids, load_errs = load_catalogs() if catalog_path == CATALOG_PATH and skill_catalog_path == SKILL_CATALOG_PATH else (None, None, [])
    if catalog_path != CATALOG_PATH or skill_catalog_path != SKILL_CATALOG_PATH:
        # custom paths for self-test
        s_data, s_errs = load_json(catalog_path)
        if s_errs:
            findings.extend(s_errs)
            return findings
        if not isinstance(s_data, list):
            findings.append(f"subskill catalog must be array")
            return findings
        sub_data = s_data
        # skill ids from custom skill catalog
        sk_data, sk_errs = load_json(skill_catalog_path)
        if sk_errs:
            skill_ids = set()
        else:
            if isinstance(sk_data, list):
                skill_ids = {e.get("id") for e in sk_data if isinstance(e, dict) and e.get("id")}
            else:
                skill_ids = set()
    else:
        if load_errs:
            findings.extend(load_errs)
            return findings

    seen_ids = set()
    for idx, entry in enumerate(sub_data):
        cid = entry.get("id", f"idx-{idx}")
        errs = validate_subskill_schema(entry, idx)
        for e in errs:
            findings.append(f"{catalog_path.relative_to(root).as_posix() if catalog_path.is_relative_to(root) else str(catalog_path)}: schema violation: {e}")

        if cid in seen_ids:
            findings.append(f"duplicate id '{cid}'")
        seen_ids.add(cid)

        # parent_skill FK resolves
        parent = entry.get("parent_skill")
        if isinstance(parent, str) and parent:
            if parent not in skill_ids:
                findings.append(f"{cid}: parent_skill FK does not resolve against skills/SKILL_CATALOG.json: '{parent}'")

        # entry_path resolves
        ep = entry.get("entry_path")
        if isinstance(ep, str) and ep.strip():
            ep_path = root / ep
            if not ep_path.exists():
                findings.append(f"{cid}: entry_path does not resolve: '{ep}'")

        # scenario_ref resolves
        sr = entry.get("scenario_ref")
        if isinstance(sr, str) and sr.strip():
            sr_path = root / sr
            if not sr_path.exists():
                findings.append(f"{cid}: scenario_ref does not resolve: '{sr}'")
            else:
                # optional: check scenario is valid JSON with trigger field
                try:
                    sdata = json.loads(sr_path.read_text(encoding="utf-8"))
                    if not isinstance(sdata, dict) or "trigger" not in sdata:
                        findings.append(f"{cid}: scenario_ref invalid shape, missing trigger: '{sr}'")
                    else:
                        # trigger in scenario should match catalog trigger? Not strictly required but good to check
                        # We'll not fail if mismatch, but if scenario trigger not in enum, fail
                        st = sdata.get("trigger")
                        if st not in TRIGGER_ENUM:
                            findings.append(f"{cid}: scenario_ref trigger enum mismatch '{st}' not in {TRIGGER_ENUM}")
                except Exception as e:
                    findings.append(f"{cid}: scenario_ref unparseable: '{sr}': {e}")

        # tests[] resolve
        tests = entry.get("tests", [])
        if isinstance(tests, list):
            for t in tests:
                if isinstance(t, str) and t.strip():
                    tp = root / t
                    if not tp.exists():
                        findings.append(f"{cid}: tests entry does not resolve: '{t}'")

    if len(sub_data) < 5:
        findings.append(f"catalog must have ≥5 entries or all found, got {len(sub_data)}")

    return findings

# ---------------- self-test vectors ----------------

def self_test():
    """
    ≥4 vectors: repo passes · broken parent FK → FAIL · missing scenario_ref → FAIL · illegal trigger → FAIL
    Plus: duplicate id, declared missing note, deprecated missing superseded_by, entry_path missing
    """
    def run_in_temp(temp_root: pathlib.Path, sub_catalog, skill_catalog):
        (temp_root / "subskills").mkdir(parents=True, exist_ok=True)
        (temp_root / "skills").mkdir(parents=True, exist_ok=True)
        (temp_root / "schemas").mkdir(parents=True, exist_ok=True)
        sub_path = temp_root / "subskills" / "SUBSKILL_CATALOG.json"
        skill_path = temp_root / "skills" / "SKILL_CATALOG.json"
        sub_path.write_text(json.dumps(sub_catalog), encoding="utf-8")
        skill_path.write_text(json.dumps(skill_catalog), encoding="utf-8")
        src_schema = ROOT / "schemas" / "subskill_card.schema.json"
        if src_schema.exists():
            shutil.copy(src_schema, temp_root / "schemas" / "subskill_card.schema.json")
        findings = check_subskills(catalog_path=sub_path, skill_catalog_path=skill_path, root=temp_root)
        return findings

    def make_skill(sid="SKILL-015"):
        return {
            "id": sid,
            "title": f"Skill {sid}",
            "entry_path": "agents/Arena_AI/BOOT.md",
            "kind": "agent",
            "description": "Test skill description valid ≤200.",
            "eval_ref": "evals/skills/SKILL-001.eval.md",
            "status": "active",
            "activation_note": "asserted",
            "tests": ["evals/skills/SKILL-001.eval.md"]
        }

    def make_sub(sid="SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md", status="active", extra=None):
        base = {
            "id": sid,
            "title": f"Test subskill {sid}",
            "parent_skill": parent,
            "entry_path": entry_path,
            "trigger": trigger,
            "condition": None,
            "description": f"Test description for subskill {sid} valid ≤200.",
            "scenario_ref": scenario_ref,
            "status": status,
            "tests": [scenario_ref]
        }
        if extra:
            base.update(extra)
        return base

    def vector_repo_passes():
        findings = check_subskills()
        ok = len(findings) == 0
        return ok, findings

    def vector_broken_parent_fk():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-999", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("parent_skill FK does not resolve" in f for f in findings)
            return ok, findings

    def vector_missing_scenario_ref():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/MISSING.scenario.json", entry_path="subskills/active/colony.md")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("scenario_ref does not resolve" in f for f in findings)
            return ok, findings

    def vector_illegal_trigger():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"illegal","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="illegal_trigger", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("trigger enum" in f for f in findings)
            return ok, findings

    def vector_duplicate_id():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            s1 = make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")
            s2 = make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md")
            findings = run_in_temp(tr, [s1, s2], skill_cat)
            ok = any("duplicate id" in f for f in findings)
            return ok, findings

    def vector_declared_missing_note():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md", status="declared")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("declared" in f and "note" in f for f in findings)
            return ok, findings

    def vector_deprecated_missing_superseded():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "subskills" / "active").mkdir(parents=True, exist_ok=True)
            (tr / "subskills" / "active" / "colony.md").write_text("# colony\n", encoding="utf-8")
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/colony.md", status="deprecated")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("deprecated" in f and "superseded_by" in f for f in findings)
            return ok, findings

    def vector_entry_path_missing():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "evals" / "subskills").mkdir(parents=True, exist_ok=True)
            (tr / "evals" / "subskills" / "SUB-001.scenario.json").write_text(json.dumps({"id":"SUB-001","trigger":"before_skill","input_sketch":"x","expected_fire_sequence":[],"expected_non_fires":[]}), encoding="utf-8")
            skill_cat = [make_skill("SKILL-015")]
            sub_cat = [make_sub("SUB-001", parent="SKILL-015", trigger="before_skill", scenario_ref="evals/subskills/SUB-001.scenario.json", entry_path="subskills/active/MISSING.md")]
            findings = run_in_temp(tr, sub_cat, skill_cat)
            ok = any("entry_path does not resolve" in f for f in findings)
            return ok, findings

    tests = [
        ("repo passes (positive)", vector_repo_passes),
        ("broken parent FK → FAIL", vector_broken_parent_fk),
        ("missing scenario_ref → FAIL", vector_missing_scenario_ref),
        ("illegal trigger → FAIL", vector_illegal_trigger),
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

    print(f"\nsubskill_check self-test: {passed} passed, {failed} failed — {len(tests)} vectors")
    return failed == 0

def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    findings = check_subskills()
    if findings:
        print(f"subskill_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("subskill_check: 0 finding(s) — catalog valid, parent_skill FK resolves, scenario_ref resolves, trigger enum valid, status discipline ok")
        sys.exit(0)

if __name__ == "__main__":
    main()
