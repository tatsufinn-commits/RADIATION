#!/usr/bin/env python3
"""
deck_rules_check.py — Deck Rules + Outline Schema lint (S-2-PPTX-A stage 1)

Deterministic, house finding style, stdlib-only, no network, no pptx import.

Validates outline JSON vs schema radiation.deck_outline/1 and every declared constraint via DECK_RULES.json (data-driven: rule file is the policy — he who edits the rule file edits the law, ledger rows record it).

Finding text names OUTLINE-id · slide ref · rule id · observed vs threshold.

Rules v0:
 R-001 max_bullets_per_slide ≤6
 R-002 max_chars_per_slide ≤400
 R-003 max_chars_per_bullet ≤80
 R-004 max_slides_per_deck: content decides (no cap) — claim-list slides may each cite ONE receipt (warn, no cap)
 R-005 theme ∈ theme_registry (anchor, slate PROVISIONAL)
 R-006 fixed hex set per theme (theme_lock) — 5 fixed hexes each

Discipline: source_ref admissible only to register lanes (SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-…); bullet without source_ref is claim awaiting one → WARN UNBACKED-BULLET (never fail).

No python-pptx import anywhere (import pptx = policy FAIL-class) — this file must never import pptx.
No renderer, no verify_deck verb (B), no plan/fill verbs (C), no dependency, no committed .pptx binary.

Self-test ≥4 vectors: clean pass, R-001 violation, R-002 violation, schema-invalid outline, plus one WARN-class unbacked-bullet vector.
"""
import argparse
import json
import pathlib
import re
import sys
import tempfile
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "deck_outline.schema.json"
RULES_PATH = ROOT / "decks" / "DECK_RULES.json"

# Policy: import pptx = FAIL-class — ensure this file does not import pptx
# We check at runtime that pptx is not imported
if "pptx" in sys.modules:
    print("FAIL: pptx module imported — policy FAIL-class per S-2-PPTX-A", file=sys.stderr)
    sys.exit(1)

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

def load_json(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), ""
    except Exception as e:
        return None, f"invalid JSON at {path}: {e}"

def load_schema():
    if not SCHEMA_PATH.exists():
        return None, f"schema missing at {SCHEMA_PATH}"
    data, err = load_json(SCHEMA_PATH)
    return data, err

def load_rules():
    if not RULES_PATH.exists():
        return None, f"rules missing at {RULES_PATH}"
    data, err = load_json(RULES_PATH)
    return data, err

def check_outline_file(path):
    findings = []  # list of (class, message)
    # Load file
    data, err = load_json(path)
    if err:
        findings.append(("error", f"outline file invalid JSON at {path}: {err} · schema-invalid"))
        return findings

    # Minimal schema validation
    # Required fields
    for field in ["schema_name", "id", "title", "theme", "slides", "constraints", "provenance"]:
        if field not in data:
            findings.append(("error", f"{data.get('id','UNKNOWN')} · schema · schema-invalid · missing required field {field}"))

    # schema_name const
    if data.get("schema_name") != "radiation.deck_outline/1":
        findings.append(("error", f"{data.get('id','UNKNOWN')} · schema · schema-invalid · schema_name must be radiation.deck_outline/1 got {data.get('schema_name')!r}"))

    # id pattern OUTLINE-<slug>
    oid = data.get("id", "")
    if not re.fullmatch(r"OUTLINE-[A-Za-z0-9_-]+", oid or ""):
        findings.append(("error", f"{oid or 'UNKNOWN'} · schema · schema-invalid · id must match OUTLINE-<slug> pattern got {oid!r}"))

    # theme
    theme = data.get("theme") or {}
    tname = theme.get("name")
    tlock = theme.get("theme_lock") or []
    # Load rules for theme registry
    rules_data, rerr = load_rules()
    theme_registry = {}
    if rules_data:
        theme_registry = rules_data.get("theme_registry", {})

    # R-005 theme ∈ theme_registry
    if tname not in theme_registry:
        findings.append(("error", f"{oid} · theme · R-005 · observed theme {tname!r} not in registry {list(theme_registry.keys())} vs threshold registry membership"))

    # R-006 fixed hex set per theme
    if tname in theme_registry:
        expected_hexes = theme_registry[tname].get("hexes", [])
        if len(tlock) != 5:
            findings.append(("error", f"{oid} · theme · R-006 · observed {len(tlock)} hexes vs threshold 5 fixed hexes per theme"))
        # Check exact match of hex set (order matters? we check set equality)
        if set(tlock) != set(expected_hexes):
            findings.append(("error", f"{oid} · theme · R-006 · observed theme_lock {tlock} vs threshold {expected_hexes} fixed hex set per theme"))
        # Validate hex pattern
        for hx in tlock:
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}", hx or ""):
                findings.append(("error", f"{oid} · theme · R-006 · observed invalid hex {hx!r} vs threshold #[0-9A-Fa-f]{{6}}"))

    # slides
    slides = data.get("slides") or []
    if not isinstance(slides, list) or len(slides) == 0:
        findings.append(("error", f"{oid} · slides · schema-invalid · slides must be non-empty array"))
    else:
        for slide in slides:
            ref = slide.get("ref", "UNKNOWN-SLIDE")
            stype = slide.get("type")
            bullets = slide.get("bullets") or []
            # type enum
            if stype not in ["title", "section", "content", "compare", "claim-list", "closing"]:
                findings.append(("error", f"{oid} · {ref} · schema-invalid · invalid slide type {stype!r}"))

            # R-001 max_bullets_per_slide ≤6
            # Rule threshold from DECK_RULES
            r001_thresh = 6
            if rules_data:
                for r in rules_data.get("rules", []):
                    if r.get("id") == "R-001":
                        r001_thresh = r.get("threshold", 6)
            if len(bullets) > r001_thresh:
                findings.append(("error", f"{oid} · {ref} · R-001 · observed {len(bullets)} bullets vs threshold {r001_thresh} max_bullets_per_slide"))

            # R-002 max_chars_per_slide ≤400
            total_chars = sum(len(b.get("text", "")) for b in bullets)
            r002_thresh = 400
            if rules_data:
                for r in rules_data.get("rules", []):
                    if r.get("id") == "R-002":
                        r002_thresh = r.get("threshold", 400)
            if total_chars > r002_thresh:
                findings.append(("error", f"{oid} · {ref} · R-002 · observed {total_chars} chars vs threshold {r002_thresh} max_chars_per_slide"))

            # R-003 max_chars_per_bullet ≤80 per bullet
            r003_thresh = 80
            if rules_data:
                for r in rules_data.get("rules", []):
                    if r.get("id") == "R-003":
                        r003_thresh = r.get("threshold", 80)
            for idx, b in enumerate(bullets):
                txt = b.get("text", "")
                if len(txt) > r003_thresh:
                    findings.append(("error", f"{oid} · {ref} · R-003 · observed bullet {idx} {len(txt)} chars vs threshold {r003_thresh} max_chars_per_bullet"))

            # UNBACKED-BULLET WARN: bullet without source_ref
            for idx, b in enumerate(bullets):
                sref = b.get("source_ref")
                if sref is None:
                    findings.append(("warn", f"{oid} · {ref} · UNBACKED-BULLET · observed bullet {idx} without source_ref vs threshold source_ref required for backed claim — claim awaiting source"))

            # source_ref admissible only to register lanes
            for idx, b in enumerate(bullets):
                sref = b.get("source_ref")
                if sref is None:
                    continue
                if not re.fullmatch(r"(SRC-[A-Za-z0-9_-]+|ANNOT_[A-Za-z0-9_-]+|TRI_[A-Za-z0-9_-]+|CARD_[A-Za-z0-9_-]+|GAP-[A-Za-z0-9_-]+|R2-[A-Za-z0-9_-]+)", sref):
                    findings.append(("error", f"{oid} · {ref} · source_ref · observed invalid source_ref {sref!r} vs threshold register lanes SRC-/ANNOT_/TRI_/CARD_/GAP-/R2-"))

    # constraints: rule IDs declared compliance to — must be valid rule IDs
    constraints = data.get("constraints") or []
    valid_rule_ids = set()
    if rules_data:
        valid_rule_ids = {r.get("id") for r in rules_data.get("rules", [])}
    for cid in constraints:
        if cid not in valid_rule_ids:
            findings.append(("error", f"{oid} · constraints · schema-invalid · observed constraint {cid!r} not in rule registry {valid_rule_ids}"))

    # provenance
    prov = data.get("provenance") or {}
    for pf in ["task", "date", "source_refs"]:
        if pf not in prov:
            findings.append(("error", f"{oid} · provenance · schema-invalid · missing {pf}"))

    return findings

def main_check():
    # If no outline file specified, lint all outlines in decks/ and decks/examples/
    # RIDER S-2-PPTX-B: zero-findings witness line becomes "checked N outline file(s) — 0 findings" (N real)
    # Truth-bearing coverage: N real; with 0 present, "no outlines present" is allowed to name itself then, and only then
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=None, help="outline JSON path")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    findings = []
    checked_count = 0
    if args.path:
        p = pathlib.Path(args.path)
        if not p.exists():
            print(f"deck_rules_check: outline not found at {p}")
            return 1
        findings = check_outline_file(p)
        checked_count = 1
    else:
        # Lint all outlines in decks/
        decks_dir = ROOT / "decks"
        outline_files = []
        if decks_dir.exists():
            outline_files = list(decks_dir.rglob("OUTLINE_*.json"))
            checked_count = len(outline_files)
            for fp in outline_files:
                f = check_outline_file(fp)
                findings.extend(f)
        # If no outline files found, check DECK_RULES itself is valid
        if checked_count == 0:
            rules_data, rerr = load_rules()
            if rerr:
                findings.append(("error", rerr))
            else:
                for r in rules_data.get("rules", []):
                    if len(r.get("text", "")) > 200:
                        findings.append(("error", f"DECK_RULES · {r.get('id')} · text length {len(r.get('text',''))} vs threshold 200"))
            if not findings:
                print("deck_rules_check: no outlines present — checked DECK_RULES.json only — 0 findings (truth-bearing: checked 0 outline file(s))" )
                return 0

    errors = [m for cls, m in findings if cls == "error"]
    warns = [m for cls, m in findings if cls == "warn"]

    if errors:
        print(f"deck_rules_check: {len(errors)} error(s), {len(warns)} warn(s) — checked {checked_count} outline file(s)")
        for msg in errors[:20]:
            print(f"  ERROR {msg}")
        for msg in warns[:20]:
            print(f"  WARN {msg}")
        return 1
    else:
        if warns:
            print(f"deck_rules_check: 0 error(s), {len(warns)} warn(s) — checked {checked_count} outline file(s)")
            for msg in warns[:20]:
                print(f"  WARN {msg}")
            return 0
        else:
            # RIDER: zero-findings witness line must be truth-bearing with N real
            print(f"deck_rules_check: checked {checked_count} outline file(s) — 0 findings — outline schema-valid, constraints via DECK_RULES OK")
            return 0

def self_test():
    def make_outline(bullets_per_slide=3, chars_per_bullet=20, chars_per_slide=100, theme_name="anchor", unbacked=False, invalid_schema=False, theme_lock_override=None):
        # Build minimal valid outline
        registry_hexes = {
            "anchor": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"],
            "slate": ["#1E293B", "#E2E8F0", "#818CF8", "#F472B6", "#22D3EE"]
        }
        tlock = theme_lock_override if theme_lock_override is not None else registry_hexes.get(theme_name, registry_hexes["anchor"])
        slides=[]
        # Create one slide
        bullets=[]
        for i in range(bullets_per_slide):
            txt = "x" * chars_per_bullet
            if len(txt) == 0:
                txt = f"Bullet {i+1}"
            sref = None if unbacked and i==0 else f"SRC-00{i+1}"
            # Adjust to fit chars_per_slide if needed
            bullets.append({"text": txt, "source_ref": sref})
        # If chars_per_slide is small, we may need to adjust total chars
        # For R-002 violation test, we want total chars >400
        # Our total is bullets_per_slide * chars_per_bullet
        # So caller should set accordingly
        slides.append({"ref": "S-001", "type": "content", "bullets": bullets, "notes": None})
        outline={
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-TEST",
            "title": "Test Outline",
            "theme": {"name": theme_name, "theme_lock": tlock},
            "slides": slides,
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-16", "source_refs": ["SRC-001"]},
            "honesty_note": "test outline"
        }
        if invalid_schema:
            outline.pop("title", None)
        return outline

    def run_check_on_outline(outline_dict):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            (tmp / "schemas").mkdir(parents=True, exist_ok=True)
            (tmp / "decks").mkdir(parents=True, exist_ok=True)
            # Copy schema and rules
            shutil.copy(str(SCHEMA_PATH), str(tmp / "schemas" / "deck_outline.schema.json"))
            shutil.copy(str(RULES_PATH), str(tmp / "decks" / "DECK_RULES.json"))
            (tmp / "scripts").mkdir(exist_ok=True)
            shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp / "scripts" / "deck_rules_check.py"))
            # Write outline
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline_dict), encoding="utf-8")
            p = run(f"python3 scripts/deck_rules_check.py {out_path}", cwd=tmp)
            return p.returncode, p.stdout + p.stderr
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    tests=[]
    def vec(name, fn):
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"  vector {name} exception {e}")
        status = "PASS" if ok else "FAIL"
        print(f"  vector {name} -> {status}")
        tests.append(ok)

    # Clean pass
    def v_clean():
        outline = make_outline(bullets_per_slide=3, chars_per_bullet=20, theme_name="anchor")
        code, out = run_check_on_outline(outline)
        return code == 0 and "0 finding" in out

    # R-001 violation: max bullets per slide ≤6, set 7 bullets
    def v_r001():
        outline = make_outline(bullets_per_slide=7, chars_per_bullet=10)
        code, out = run_check_on_outline(outline)
        return code != 0 and "R-001" in out and "7 bullets vs threshold 6" in out

    # R-002 violation: max chars per slide ≤400, set 5 bullets * 100 chars = 500 >400
    def v_r002():
        outline = make_outline(bullets_per_slide=5, chars_per_bullet=100)
        code, out = run_check_on_outline(outline)
        return code != 0 and "R-002" in out and "chars vs threshold 400" in out

    # R-003 violation: max chars per bullet ≤80, set 1 bullet 100 chars
    def v_r003():
        outline = make_outline(bullets_per_slide=1, chars_per_bullet=100)
        code, out = run_check_on_outline(outline)
        return code != 0 and "R-003" in out

    # Schema-invalid outline: missing title
    def v_schema_invalid():
        outline = make_outline(invalid_schema=True)
        code, out = run_check_on_outline(outline)
        return code != 0 and "schema-invalid" in out.lower()

    # WARN-class unbacked-bullet
    def v_unbacked():
        outline = make_outline(bullets_per_slide=2, chars_per_bullet=20, unbacked=True)
        code, out = run_check_on_outline(outline)
        # Should be 0 error, 1 warn, exit 0
        return code == 0 and "UNBACKED-BULLET" in out and "warn" in out.lower()

    vec("clean pass", v_clean)
    vec("R-001 violation max_bullets_per_slide", v_r001)
    vec("R-002 violation max_chars_per_slide", v_r002)
    vec("R-003 violation max_chars_per_bullet", v_r003)
    vec("schema-invalid outline", v_schema_invalid)
    vec("WARN-class UNBACKED-BULLET", v_unbacked)

    # RIDER S-2-PPTX-B: truth-bearing coverage witness line
    def v_rider_truth_bearing():
        # ≥1 outline present → line must say checked N outline file(s) with N real
        outline = make_outline(bullets_per_slide=2, chars_per_bullet=20)
        code, out = run_check_on_outline(outline)
        has_checked = "checked" in out.lower() and "outline file(s)" in out.lower() and "0 findings" in out.lower()
        # With 0 outlines present, allowed to say "no outlines present" then, and only then
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            (tmp / "schemas").mkdir(parents=True, exist_ok=True)
            (tmp / "decks").mkdir(parents=True, exist_ok=True)
            (tmp / "scripts").mkdir(exist_ok=True)
            import shutil
            shutil.copy(str(SCHEMA_PATH), str(tmp / "schemas" / "deck_outline.schema.json"))
            shutil.copy(str(RULES_PATH), str(tmp / "decks" / "DECK_RULES.json"))
            shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp / "scripts" / "deck_rules_check.py"))
            # No OUTLINE_*.json files in tmp/decks
            p = run(f"python3 scripts/deck_rules_check.py", cwd=tmp)
            has_no_outlines = "no outlines present" in p.stdout.lower() and "checked 0 outline file(s)" in p.stdout.lower()
            return has_checked and has_no_outlines and p.returncode == 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    vec("RIDER truth-bearing coverage witness line (checked N + no outlines present)", v_rider_truth_bearing)

    passed = sum(tests)
    print(f"deck_rules_check self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main_check())
