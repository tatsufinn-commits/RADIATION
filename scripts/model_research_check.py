#!/usr/bin/env python3
"""model_research_check — ONE entry point for the Candidate C catalog contract.

5710 "Calibrate" hardening per the Atlas independent review (F1–F3):

  R1 uniqueness     : one record per (identifier, surface, region); the
                      identifier is the VERIFIED exact_model_id, or the
                      candidate label under a distinct "candidate:" namespace
                      (an unverified label can never collide with — or
                      impersonate — a verified token).
  R2 real dates     : datetime.date.fromisoformat — impossible dates like
                      2026-13-40 fail; review window enforced: retrieved_on
                      <= review_after <= retrieved_on + 90 days (the
                      documented re-review policy).
  R3 confirmed      : exact_id_verified is true AND at least one TYPED
                      declaration with tier "O" whose source_id resolves in
                      the typed register (same tier) and whose retrieved_on
                      matches the record's. Substring tier strings ("[O…]")
                      are structurally impossible: tier is an enum and the
                      register is the binding.
  R4 non-boot scan  : the scanned set is DERIVED from BOOT_SEQUENCE.md (the
                      mandatory boot manifest) — path tokens + wildcard
                      directories expanded — plus a guaranteed floor
                      (BOOT_SEQUENCE.md itself, the docs/.readme First-Read
                      Gate, cue/CUE_INDEX.md, README.md). This is a SCAN over
                      the derived boot graph, not a proof over every possible
                      transitive include; the wording everywhere says "scan".
  R5 register       : sources/REGISTER.json is schema-executed, nonempty,
                      every row dated with a real calendar day; every record
                      evidence source_id resolves with a MATCHING tier.
  R6 filename bind  : the filename must equal
                      <provider>__<identifier-slug>__<surface>__<region>.json
                      — a record cannot masquerade under another's name.

RESEARCH LAYER ONLY: an entry grants no tool, effect, identity, privacy
guarantee, or legal conclusion. Record schema: central
`schemas/model_research_record.schema.json` (so check 40's coverage law sees
it); the catalog's schemas/ directory holds a pointer, by declaration.

--self-test runs the 21-vector negative battery against temp catalog copies.
Exit: 0 clean, 1 findings.
"""
import copy
import datetime
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
RECORD_SCHEMA = "model_research_record.schema.json"
REGISTER_SCHEMA = "model_research_register.schema.json"
BOOT_MANIFEST = "BOOT_SEQUENCE.md"
REVIEW_WINDOW_DAYS = 90  # documented in catalogs/model_research/README.md


def _iso(s):
    """Strict calendar date: pattern AND a real day."""
    if not isinstance(s, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return None
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _boot_scan_set(root):
    """Derive the boot-sensitive file set from the canonical manifest
    (BOOT_SEQUENCE.md): path tokens, wildcard dirs expanded, plus a floor."""
    files = {BOOT_MANIFEST, "docs/.readme", os.path.join("cue", "CUE_INDEX.md"),
             "README.md"}
    mp = os.path.join(root, BOOT_MANIFEST)
    if os.path.isfile(mp):
        text = open(mp, encoding="utf-8", errors="replace").read()
        for tok in re.findall(
                r"(?:docs|Brain|subskills|scaffolding|styles|cue|09-nota|agents|"
                r"catalogs|evidence|schemas|tools|scripts|radiation_core)"
                r"/[A-Za-z0-9_./-]+", text):
            tok = tok.rstrip(".,;)")
            if tok.endswith("/*") or tok.endswith("/"):
                d = os.path.join(root, tok.rstrip("*"))
                if os.path.isdir(d):
                    for dp, dn, fn in os.walk(d):
                        dn[:] = [x for x in dn if x not in (".git", "__pycache__")]
                        for f in fn:
                            files.add(os.path.relpath(os.path.join(dp, f), root))
            else:
                files.add(tok)
    return files


def catalog_findings(root=ROOT):
    bad = []
    cat = os.path.join(root, CATALOG)
    if not os.path.isdir(cat):
        return [f"{CATALOG}/ missing (the research layer is declared law)"]
    # ---- R5 register first (records bind to it)
    reg_ids = {}
    reg_p = os.path.join(cat, "sources", "REGISTER.json")
    if not os.path.isfile(reg_p):
        bad.append("sources/REGISTER.json missing (the typed source register is law)")
    else:
        try:
            reg = json.load(open(reg_p, encoding="utf-8"))
        except Exception as e:
            reg = None
            bad.append(f"REGISTER.json unparseable: {e}")
        if isinstance(reg, dict):
            out = []
            _schema_check(reg, REGISTER_SCHEMA, "register", out)
            bad.extend(out[:4])
            for row in reg.get("sources", []):
                if _iso(row.get("retrieved_on")) is None:
                    bad.append(f"register row {row.get('id')}: retrieved_on is not a "
                               f"real calendar day: {row.get('retrieved_on')!r}")
                if row.get("id") in reg_ids:
                    bad.append(f"register: duplicate source id {row.get('id')!r}")
                reg_ids[row.get("id")] = row
    # ---- records
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
            _schema_check(rec, RECORD_SCHEMA, where, bad)
            # R1 uniqueness — verified tokens and candidate labels live in
            # disjoint namespaces
            if rec.get("exact_id_verified") is True:
                ident = rec.get("exact_model_id")
            else:
                ident = "candidate:" + str(rec.get("candidate_model_label"))
            key = (ident, rec.get("surface"), rec.get("region"))
            if key in keys:
                bad.append(f"{where}: duplicate record key {key} (one record per "
                           "exact model x surface x region)")
            keys.add(key)
            # R2 real dates + review window
            ro, ra = _iso(rec.get("retrieved_on")), _iso(rec.get("review_after"))
            if rec.get("retrieved_on") not in (None,) and ro is None:
                bad.append(f"{where}: retrieved_on is not a real calendar day: "
                           f"{rec.get('retrieved_on')!r}")
            if rec.get("review_after") not in (None,) and ra is None:
                bad.append(f"{where}: review_after is not a real calendar day: "
                           f"{rec.get('review_after')!r}")
            if ro and ra:
                if ra < ro:
                    bad.append(f"{where}: review_after {ra} precedes retrieved_on {ro}")
                elif (ra - ro).days > REVIEW_WINDOW_DAYS:
                    bad.append(f"{where}: review window {(ra - ro).days}d exceeds the "
                               f"documented {REVIEW_WINDOW_DAYS}d policy")
            # typed evidence: source binding + date sanity
            for field in ("declarations", "safety_evidence", "independent_evidence"):
                for ev in rec.get(field) or []:
                    if not isinstance(ev, dict):
                        continue
                    sid = ev.get("source_id")
                    if sid not in reg_ids:
                        bad.append(f"{where}: {field} source_id {sid!r} not in the "
                                   "register")
                    elif ev.get("tier") != reg_ids[sid].get("tier"):
                        bad.append(f"{where}: {field} source_id {sid!r} tier "
                                   f"{ev.get('tier')!r} != register tier "
                                   f"{reg_ids[sid].get('tier')!r}")
                    if ev.get("retrieved_on") and _iso(ev.get("retrieved_on")) is None:
                        bad.append(f"{where}: {field} retrieved_on is not a real "
                                   f"calendar day: {ev.get('retrieved_on')!r}")
            # R3 confirmed discipline
            if rec.get("status") == "confirmed":
                if rec.get("exact_id_verified") is not True:
                    bad.append(f"{where}: status confirmed but exact_id_verified "
                               "is not true")
                official = [d for d in rec.get("declarations", [])
                            if isinstance(d, dict) and d.get("tier") == "O"
                            and d.get("source_id") in reg_ids
                            and reg_ids[d["source_id"]].get("tier") == "O"
                            and d.get("retrieved_on") == rec.get("retrieved_on")]
                if not official:
                    bad.append(f"{where}: status confirmed without an official "
                               "declaration bound to the register at the record's "
                               "retrieved_on")
            # R6 filename binding
            want = (f"{_slug(rec.get('provider'))}__"
                    f"{_slug(ident.split('candidate:', 1)[-1])}__"
                    f"{_slug(rec.get('surface'))}__{_slug(rec.get('region'))}.json")
            if f != want:
                bad.append(f"{where}: filename does not bind to the declared "
                           f"identifier/status (want {want})")
            records.append(rec)
    else:
        bad.append(f"{CATALOG}/records/ missing")
    if not records:
        bad.append("no records found (the catalog is declared, it must exist)")
    # ---- R4 non-boot scan over the DERIVED boot graph
    marker = "catalogs/model_research"
    for rel in sorted(_boot_scan_set(root)):
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            try:
                if marker in open(p, encoding="utf-8", errors="replace").read():
                    bad.append(f"NON-BOOT SCAN HIT: boot-graph file {rel} references "
                               f"{marker}")
            except (OSError, UnicodeDecodeError):
                pass
    return bad


def check(root=ROOT):
    return catalog_findings(root)


def self_test():
    ok = 0
    total = 21
    cat_src = os.path.join(ROOT, CATALOG)

    def temp_catalog(mutate_record=None, mutate_register=None, boot_file=None,
                     rename_record=None, base="verified"):
        td = tempfile.mkdtemp(prefix="mrc-check-")
        shutil.copytree(cat_src, os.path.join(td, CATALOG))
        # the boot-graph scan derives from the manifest — temp roots need it
        shutil.copy(os.path.join(ROOT, BOOT_MANIFEST),
                    os.path.join(td, BOOT_MANIFEST))
        rdir = os.path.join(td, CATALOG, "records")
        files = sorted(f for f in os.listdir(rdir) if f.endswith(".json"))
        first = files[0]
        if base == "verified":
            # mutate a VERIFIED record so exact_model_id edits stay coherent
            first = next((f for f in files if json.load(
                open(os.path.join(rdir, f)))["exact_id_verified"] is True), files[0])
        # "candidate": derive an UNVERIFIED record from a verified one (the
        # shipped catalog may legitimately contain none)
        if mutate_record:
            rec = copy.deepcopy(json.load(open(os.path.join(rdir, first))))
            if base == "candidate":
                rec["exact_id_verified"] = False
                rec["exact_model_id"] = None
                rec["candidate_model_label"] = "derived-candidate"
            mutate_record(rec)
            json.dump(rec, open(os.path.join(rdir, "z_mutant.json"), "w"))
        if mutate_register:
            rp = os.path.join(td, CATALOG, "sources", "REGISTER.json")
            reg = copy.deepcopy(json.load(open(rp)))
            mutate_register(reg)
            json.dump(reg, open(rp, "w"))
        if boot_file:
            path = os.path.join(td, boot_file)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").write(f"see {CATALOG} for details\n")
        if rename_record:
            os.rename(os.path.join(rdir, first), os.path.join(rdir, rename_record))
        return td

    def case(label, make, needle):
        nonlocal ok
        td = make()
        try:
            f = check(td)
            hit = any(needle in x for x in f)
            v = bool(f) and hit
            ok += v
            print(f"  vector {label} -> {'PASS' if v else 'FAIL ' + (str(f[:1]) if f else '(clean)')[:80]}")
        finally:
            shutil.rmtree(td, ignore_errors=True)

    f = check(ROOT)
    v1 = not f
    ok += v1
    print(f"  vector 1 shipped catalog validates clean -> "
          f"{'PASS' if v1 else 'FAIL ' + str(f[:2])}")

    def dup(m): m["exact_model_id"] = "grok-4.6"; m["exact_id_verified"] = True
    def no_review(m): del m["review_after"]
    def unverified_confirmed(m): m["status"] = "confirmed"; m["exact_id_verified"] = False
    def bad_surface(m): m["surface"] = "telepathy"
    def rogue(m): m["rogue_field"] = True
    def backwards(m): m["retrieved_on"], m["review_after"] = "2026-12-13", "2026-09-14"
    def impossible(m): m["retrieved_on"], m["review_after"] = "2026-13-40", "2026-14-41"
    def traversal(m): m["exact_model_id"] = "../not-a-model"
    def bool_int(m): m["exact_id_verified"] = 1
    def spoof_tier(m): m["declarations"] = [
        {"tier": "OOPS", "source_id": "O1", "url": "https://x", "retrieved_on": "2026-09-14",
         "claim": "invented"}]
    def unbound_source(m): m["declarations"] = [
        {"tier": "O", "source_id": "O99", "url": "https://x", "retrieved_on": "2026-09-14",
         "claim": "unbound"}]
    def wrong_source_date(m): m["declarations"] = [
        {"tier": "O", "source_id": "O1", "url": "https://x", "retrieved_on": "2026-01-01",
         "claim": "right source, wrong day"}]
    def unverified_in_exact(m):
        m["exact_id_verified"] = False; m["exact_model_id"] = "not-captured"
        m["candidate_model_label"] = "not-captured-candidate"
    def missing_label(m):
        m["exact_id_verified"] = False; m["exact_model_id"] = None
        m.pop("candidate_model_label", None)  # the defect under test
    def overdue(m):
        m["review_after"] = (datetime.date(2026, 9, 14)
                             + datetime.timedelta(days=200)).isoformat()

    case("2 duplicate (identifier,surface,region) rejected", lambda: temp_catalog(mutate_record=dup), "duplicate record key")
    case("3 missing review_after rejected (schema)", lambda: temp_catalog(mutate_record=no_review), "schema-required field")
    case("4 confirmed without verified id rejected", lambda: temp_catalog(mutate_record=unverified_confirmed), "exact_id_verified")
    case("5 bad surface enum rejected", lambda: temp_catalog(mutate_record=bad_surface), "outside enum")
    case("6 unknown property rejected", lambda: temp_catalog(mutate_record=rogue), "unknown property")
    case("7 review_after before retrieved_on rejected", lambda: temp_catalog(mutate_record=backwards), "precedes retrieved_on")
    case("8 impossible calendar dates rejected (2026-13-40)", lambda: temp_catalog(mutate_record=impossible), "not a real calendar day")
    case("9 path traversal as id rejected (schema)", lambda: temp_catalog(mutate_record=traversal), "anyOf violated")
    case("10 bool-as-integer rejected (strict)", lambda: temp_catalog(mutate_record=bool_int), "must be boolean")
    case("11 spoofed tier '[OOPS]' rejected (enum)", lambda: temp_catalog(mutate_record=spoof_tier), "outside enum")
    case("12 source_id not in register rejected", lambda: temp_catalog(mutate_record=unbound_source), "not in the register")
    case("13 confirmed with wrong source date rejected", lambda: temp_catalog(mutate_record=wrong_source_date), "at the record's")
    case("14 unverified id stored in exact field rejected (if/then)", lambda: temp_catalog(mutate_record=unverified_in_exact, base="candidate"), "must be null")
    case("15 missing candidate label when unverified rejected", lambda: temp_catalog(mutate_record=missing_label, base="candidate"), "candidate_model_label")
    case("16 overdue review window rejected (>90d)", lambda: temp_catalog(mutate_record=overdue), "review window")
    def empty_reg(r): r["sources"] = []
    def undated_row(r): r["sources"][0]["retrieved_on"] = "2026-13-40"
    case("17 empty register rejected", lambda: temp_catalog(mutate_register=empty_reg), "fewer than minItems")
    case("18 undated register row rejected", lambda: temp_catalog(mutate_register=undated_row), "not a real calendar day")
    case("19 filename not bound to identifier rejected", lambda: temp_catalog(rename_record="zzz__wrong__api__undeclared.json"), "filename does not bind")
    case("20 docs/.readme boot reference rejected (First-Read Gate)", lambda: temp_catalog(boot_file="docs/.readme"), "NON-BOOT SCAN HIT")
    case("21 transitive boot-graph reference rejected (passive spec)", lambda: temp_catalog(boot_file="subskills/passive/compass.md"), "NON-BOOT SCAN HIT")
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
