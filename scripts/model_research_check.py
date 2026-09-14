#!/usr/bin/env python3
"""model_research_check — ONE entry point for the Candidate C catalog contract (5700).

Executes catalogs/model_research/schemas/model_research_record.schema.json via
the ONE schema executor (radiation_core.relay), then applies the rules JSON
Schema cannot express cleanly. Those are CODE-LEVEL checks, stated as such:

  R1 uniqueness   : one record per (exact_model_id, surface, region)
  R2 date sanity  : review_after >= retrieved_on (ISO strings)
  R3 confirmed    : exact_id_verified is true AND an [O] official declaration exists
  R4 non-boot     : NO boot-tier file may reference catalogs/model_research
                    (the research layer never enters boot context)
  R5 sources      : sources/ carries at least one dated register

RESEARCH LAYER ONLY: an entry grants no tool, effect, identity, privacy
guarantee, or legal conclusion. Non-boot is a checked invariant, not a hope.

--self-test runs the 10-vector negative battery against temp catalog copies.
Exit: 0 clean, 1 findings.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from radiation_core.relay import _schema_check  # ONE schema executor (II.11)

CATALOG = os.path.join("catalogs", "model_research")
SCHEMA = "model_research_record.schema.json"
BOOT_TIERS = [
    "README.md", "docs/SYSTEM_STATE.md", "docs/AI_RULES.md",
    "docs/MODES.md", "docs/CUE_SYSTEM.md", "Brain/frontal_lobe/task_ledger.md",
]


def catalog_findings(root=ROOT):
    bad = []
    cat = os.path.join(root, CATALOG)
    if not os.path.isdir(cat):
        return [f"{CATALOG}/ missing (the research layer is declared law)"]
    rdir = os.path.join(cat, "records")
    keys = set()
    records = []
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            if not f.endswith(".json"):
                continue
            p = os.path.join(rdir, f)
            try:
                rec = json.load(open(p, encoding="utf-8"))
            except Exception as e:
                bad.append(f"records/{f} unparseable: {e}")
                continue
            where = f"records/{f}"
            _schema_check(rec, SCHEMA, where, bad)
            key = (rec.get("exact_model_id"), rec.get("surface"), rec.get("region"))
            if key in keys:
                bad.append(f"{where}: duplicate record key {key} (one record per "
                           "exact model x surface x region)")
            keys.add(key)
            ra, ro = rec.get("review_after", ""), rec.get("retrieved_on", "")
            if re.match(r"^\d{4}-\d{2}-\d{2}$", ra) and re.match(r"^\d{4}-\d{2}-\d{2}$", ro) \
                    and ra < ro:
                bad.append(f"{where}: review_after {ra} precedes retrieved_on {ro}")
            if rec.get("status") == "confirmed":
                if rec.get("exact_id_verified") is not True:
                    bad.append(f"{where}: status confirmed but exact_id_verified is not true")
                if not any("[O" in d for d in rec.get("declarations", [])):
                    bad.append(f"{where}: status confirmed but no [O] official declaration")
            records.append(rec)
    else:
        bad.append(f"{CATALOG}/records/ missing")
    if not records:
        bad.append("no records found (the catalog is declared, it must exist)")
    sdir = os.path.join(cat, "sources")
    if not (os.path.isdir(sdir) and any(f.endswith(".md")
                                        for f in os.listdir(sdir))):
        bad.append(f"{CATALOG}/sources/ carries no dated register")
    # R4 non-boot assertion
    marker = "catalogs/model_research"
    for rel in BOOT_TIERS:
        p = os.path.join(root, rel)
        if os.path.isfile(p) and marker in open(p, encoding="utf-8").read():
            bad.append(f"NON-BOOT VIOLATION: boot-tier {rel} references {marker}")
    return bad


def check(root=ROOT):
    return catalog_findings(root)


def self_test():
    import copy as _c
    ok = 0
    total = 10
    cat_src = os.path.join(ROOT, CATALOG)

    def run(root):
        f = check(root)
        return f

    def temp_catalog(mutate=None, boot_ref=False):
        td = tempfile.mkdtemp(prefix="mrc-check-")
        dst = os.path.join(td, CATALOG)
        shutil.copytree(cat_src, dst)
        if mutate:
            rdir = os.path.join(dst, "records")
            first = sorted(f for f in os.listdir(rdir) if f.endswith(".json"))[0]
            rec = json.load(open(os.path.join(rdir, first), encoding="utf-8"))
            rec = _c.deepcopy(rec)
            mutate(rec)
            json.dump(rec, open(os.path.join(rdir, "z_mutant.json"), "w"))
        if boot_ref:
            os.makedirs(os.path.join(td, "docs"), exist_ok=True)
            open(os.path.join(td, "README.md"), "w").write(
                "# test boot file\nsee catalogs/model_research for details\n")
        return td

    def case(label, make, needle):
        nonlocal ok
        td = make()
        try:
            f = run(td)
            hit = any(needle in x for x in f)
            v = bool(f) and hit
            ok += v
            print(f"  vector {label} -> {'PASS' if v else 'FAIL ' + (f[:1] or ['(clean)'])[0][:80]}")
        finally:
            shutil.rmtree(td, ignore_errors=True)

    # 1: the shipped catalog validates clean (real root)
    f = check(ROOT)
    v1 = not f
    ok += v1
    print(f"  vector 1 shipped catalog validates clean -> "
          f"{'PASS' if v1 else 'FAIL ' + str(f[:2])}")

    def dup(m): m["exact_model_id"] = "grok-4.6"  # collides with the xai record
    def no_review(m): del m["review_after"]
    def unverified_confirmed(m):
        m["status"] = "confirmed"; m["exact_id_verified"] = False
    def bad_surface(m): m["surface"] = "telepathy"
    def rogue(m): m["rogue_field"] = True
    def backwards_dates(m): m["retrieved_on"], m["review_after"] = "2026-12-13", "2026-09-14"
    def path_traversal(m): m["exact_model_id"] = "../not-a-model"
    def bool_as_int(m): m["exact_id_verified"] = 1

    case("2 duplicate (model,surface,region) rejected", lambda: temp_catalog(dup), "duplicate record key")
    case("3 missing review_after rejected (schema)", lambda: temp_catalog(no_review), "schema-required field")
    case("4 confirmed without verified id rejected", lambda: temp_catalog(unverified_confirmed), "exact_id_verified")
    case("5 bad surface enum rejected", lambda: temp_catalog(bad_surface), "outside enum")
    case("6 unknown property rejected", lambda: temp_catalog(rogue), "unknown property")
    case("7 review_after before retrieved_on rejected", lambda: temp_catalog(backwards_dates), "precedes retrieved_on")
    case("8 path traversal as model id rejected", lambda: temp_catalog(path_traversal), "fails pattern")
    case("9 bool-as-integer rejected (strict)", lambda: temp_catalog(bool_as_int), "must be boolean")
    case("10 boot-tier reference rejected (non-boot law)", lambda: temp_catalog(boot_ref=True), "NON-BOOT VIOLATION")
    print(f"model_research_check self-test: {ok}/{total} vectors")
    return 0 if ok == total else 1


def main(argv=None):
    if "--self-test" in (argv or sys.argv[1:]):
        return self_test()
    f = check()
    for x in f:
        print("✗", x)
    print(f"model_research catalog: {len(f)} finding(s) (research layer only — grants nothing)")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
