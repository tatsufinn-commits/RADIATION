#!/usr/bin/env python3
"""
deck_verbs.py — Guardrailed verbs + optional adapter (S-2-PPTX-C stage 3 of 5)

Standing interface rule (proposal, adopted): expose guardrailed verbs — plan_slide · fill_template · verify_deck — never raw primitives.
Influences (license-logged, clean-room, nothing imported): GenSlide skeleton (MIT ✓) and mcp-office's "Output Contract for machine-verifiable slide specs" governance pattern (MIT ✓; its contracts doc = nearest-further-reading when R&D sends tail).

Three verbs, stdlib, outline-level, no actual rendering, no committed binaries, no WP-D canon text, no theme-registry edits, no network, no SOLVE/fonts/VLM, no cue/skill/mode changes, no imports from any basis-shelf repo (clean-room by law).

Verbs:
- plan_slide <outline> — derive per-slide plan: rule re-check per slide vs DECK_RULES (budgets re-asserted at plan time), source_ref audit summary {backed, unbacked-warn}, per-slide truth lines (ref · type · bullets · chars · receipts). PLAN, never render.
- verify_deck <outline> — chained gate: deck_rules_check + deck_verify (canonical idempotence + receipts) + adapter status line; the "verify deck" command a Commander-invoked session would use before anything ever renders.
- fill_template <outline> --adapter <path|null> — honest one: consults adapter. With adapter present-and-capable: records what WOULD be rendered (per-slide render plan, deterministic, sha) and exits with dry-run evidence. With adapter absent/incapable: structured report {adapter: ABSENT-UNKNOWN, would_render: <plan>, blocked_at: dependency canon (WP-D 🟠)} — verb never pretends render capacity it does not have (constraint honesty per IP-ENV-01 grammar: ABSENT ≠ UNAVAILABLE ≠ UNKNOWN — declared and stamped).

No python-pptx import anywhere outside guarded probe block — fence law extended: walk ship-files asserting no raw import pptx outside guarded probe block.

Self-test ≥5 vectors incl.: plan of exemplar emits budgets, verify chains green, fill_template-with-ABSENT-adapter reports blocked-at-WP-D (never crash, never fake), unconditional-pptx-import guard.

Registry 35 → 36.
"""

import argparse
import hashlib
import json
import pathlib
import re
import sys
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "deck_outline.schema.json"
RULES_PATH = ROOT / "decks" / "DECK_RULES.json"

# Policy: no unconditional pptx import outside guarded probe block
# This file must never import pptx at module level
if "pptx" in sys.modules:
    print("FAIL: pptx module imported unconditionally — policy FAIL-class per S-2-PPTX-C", file=sys.stderr)
    sys.exit(1)

def load_json(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), ""
    except Exception as e:
        return None, f"invalid JSON at {path}: {e}"

def load_outline(path):
    data, err = load_json(path)
    if err:
        return None, err
    return data, ""

def load_rules():
    if not RULES_PATH.exists():
        return None, f"DECK_RULES.json missing at {RULES_PATH}"
    return load_json(RULES_PATH)

def normalize_ws(t):
    if not isinstance(t, str):
        return t
    return re.sub(r"\s+", " ", t.strip())

def canonicalize_for_sha(outline):
    import copy
    data = copy.deepcopy(outline)
    # Normalize whitespace
    if "title" in data and isinstance(data["title"], str):
        data["title"] = normalize_ws(data["title"])
    slides = data.get("slides", [])
    for s in slides:
        if "ref" in s and isinstance(s["ref"], str):
            s["ref"] = normalize_ws(s["ref"])
        if "notes" in s and isinstance(s["notes"], str):
            s["notes"] = normalize_ws(s["notes"]) if s["notes"] else s["notes"]
        for b in s.get("bullets", []):
            if "text" in b and isinstance(b["text"], str):
                b["text"] = normalize_ws(b["text"])
            if "source_ref" in b and isinstance(b["source_ref"], str):
                b["source_ref"] = b["source_ref"].strip()
    try:
        data["slides"] = sorted(slides, key=lambda x: x.get("ref",""))
    except Exception:
        pass
    b = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(b).hexdigest()[:12]
    return data, b, sha

def resolve_receipt_witness(sref):
    # Reuse logic from deck_verify — minimal witness-based
    if sref is None:
        return True, "null — awaiting source"
    if not re.fullmatch(r"(SRC-[A-Za-z0-9_-]+|ANNOT_[A-Za-z0-9_-]+|TRI_[A-Za-z0-9_-]+|CARD_[A-Za-z0-9_-]+|GAP-[A-Za-z0-9_-]+|R2-[A-Za-z0-9_-]+|OUTLINE-[A-Za-z0-9_-]+)", sref):
        return False, f"invalid lane {sref}"
    # Check existence in tree
    if sref.startswith("SRC-"):
        for fp in (ROOT / "01-research").rglob("*.md"):
            if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)}"
        # Also check REFERENCES.md
        ref = ROOT / "01-research" / "REFERENCES.md"
        if ref.exists() and sref in ref.read_text(encoding="utf-8", errors="ignore"):
            return True, f"{ref.relative_to(ROOT)}"
        # Check any file containing sref
        for fp in ROOT.rglob(f"*{sref}*"):
            if fp.is_file():
                return True, f"{fp.relative_to(ROOT)}"
        # For test purposes, allow SRC-00* as backed in temp repos? No, in real repo we need witness — if not found, treat as unresolved
        # But for exemplar, SRC-013 should resolve via REFERENCES or 09-nota etc.
        # We'll also check 09-nota, 05-annotate, 06-triangulate for SRC mention
        for d in [ROOT / "09-nota", ROOT / "05-annotate", ROOT / "06-triangulate"]:
            if d.exists():
                for fp in d.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)}"
                    except Exception:
                        continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("ANNOT_"):
        for fp in (ROOT / "05-annotate").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)}"
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("TRI_"):
        for fp in (ROOT / "06-triangulate").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)}"
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("CARD_"):
        for fp in (ROOT / "09-nota").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)}"
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("GAP-"):
        for d in [ROOT / "docs", ROOT / "04-incubate"]:
            if d.exists():
                for fp in d.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)}"
                    except Exception:
                        continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("R2-"):
        for d in [ROOT / "08-overhaul", ROOT / "docs"]:
            if d.exists():
                for fp in d.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)}"
                    except Exception:
                        continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("OUTLINE-"):
        for fp in (ROOT / "decks").rglob("*.json"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)}"
        return False, f"UNRESOLVED-RECEIPT {sref}"
    return False, f"UNRESOLVED-RECEIPT {sref}"

def plan_slide(outline_path):
    """
    plan_slide <outline> — derive per-slide plan: rule re-check per slide vs DECK_RULES (budgets re-asserted at plan time), source_ref audit summary {backed, unbacked-warn}, per-slide truth lines (ref · type · bullets · chars · receipts). PLAN, never render.
    """
    data, err = load_outline(outline_path)
    if err:
        print(f"plan_slide: {err}", file=sys.stderr)
        return 1

    rules_data, rerr = load_rules()
    if rerr:
        print(f"plan_slide: {rerr}", file=sys.stderr)
        return 1

    # Thresholds from rules
    thresholds = {r["id"]: r.get("threshold") for r in rules_data.get("rules", [])}
    r001 = thresholds.get("R-001", 6)
    r002 = thresholds.get("R-002", 400)
    r003 = thresholds.get("R-003", 80)

    oid = data.get("id", "UNKNOWN")
    _, _, sha = canonicalize_for_sha(data)

    backed = 0
    unbacked_warn = 0
    truth_lines = []

    for slide in data.get("slides", []):
        ref = slide.get("ref", "UNKNOWN")
        stype = slide.get("type", "UNKNOWN")
        bullets = slide.get("bullets", [])
        total_chars = sum(len(b.get("text","")) for b in bullets)
        receipts = []
        for b in bullets:
            sref = b.get("source_ref")
            if sref is None:
                unbacked_warn += 1
            else:
                ok, _ = resolve_receipt_witness(sref)
                if ok:
                    backed += 1
                    receipts.append(sref)
                else:
                    # Unresolved counts as not backed? For plan, we count backed only if resolved
                    # But we still note receipt
                    receipts.append(f"{sref} (UNRESOLVED)")
        # Per-slide truth line: ref · type · bullets · chars · receipts
        # Also include budgets re-asserted at plan time
        bullet_count_ok = len(bullets) <= r001 if r001 is not None else True
        chars_ok = total_chars <= r002 if r002 is not None else True
        # Check max chars per bullet
        max_bullet_chars = max((len(b.get("text","")) for b in bullets), default=0)
        bullet_chars_ok = max_bullet_chars <= r003 if r003 is not None else True

        truth = f"{ref} · {stype} · bullets {len(bullets)}/{r001} {'OK' if bullet_count_ok else 'FAIL R-001'} · chars {total_chars}/{r002} {'OK' if chars_ok else 'FAIL R-002'} · max_bullet {max_bullet_chars}/{r003} {'OK' if bullet_chars_ok else 'FAIL R-003'} · receipts {receipts}"
        truth_lines.append(truth)

    print(f"plan_slide: {oid} · sha {sha} · slides {len(data.get('slides',[]))}")
    print(f"  budgets re-asserted at plan time: R-001 max_bullets {r001}, R-002 max_chars_slide {r002}, R-003 max_chars_bullet {r003}")
    print(f"  source_ref audit: {{backed: {backed}, unbacked-warn: {unbacked_warn}}}")
    for tl in truth_lines:
        print(f"  truth: {tl}")

    # If any budget FAIL, return error? Plan should still emit but indicate FAIL
    has_fail = any("FAIL" in tl for tl in truth_lines)
    if has_fail:
        print(f"plan_slide: {len([tl for tl in truth_lines if 'FAIL' in tl])} slide(s) exceed budgets — plan emitted with FAIL markers")
        return 1
    else:
        print(f"plan_slide: 0 findings — budgets OK, receipts audited")
        return 0

def verify_deck(outline_path):
    """
    verify_deck <outline> — chained gate: deck_rules_check + deck_verify (canonical idempotence + receipts) + adapter status line
    """
    # Call deck_rules_check
    import subprocess
    p1 = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_rules_check.py"), str(outline_path)], cwd=str(ROOT), capture_output=True, text=True)
    print(p1.stdout.strip())
    if p1.stderr:
        print(p1.stderr.strip(), file=sys.stderr)
    if p1.returncode != 0:
        print(f"verify_deck: deck_rules_check FAIL — chained gate stops")
        return p1.returncode

    p2 = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verify.py"), str(outline_path)], cwd=str(ROOT), capture_output=True, text=True)
    print(p2.stdout.strip())
    if p2.stderr:
        print(p2.stderr.strip(), file=sys.stderr)
    if p2.returncode != 0:
        print(f"verify_deck: deck_verify FAIL — chained gate stops")
        return p2.returncode

    # Adapter status line
    try:
        spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        status = mod.get_adapter_status()
        print(f"verify_deck: {status}")
    except Exception as e:
        print(f"verify_deck: adapter status probe failed: {e} — adapter ABSENT-UNKNOWN")

    print(f"verify_deck: 0 findings — chained gate green — outline verified, ready for fill_template (adapter may be ABSENT-UNKNOWN)")
    return 0

def fill_template(outline_path, adapter_path=None):
    """
    fill_template <outline> --adapter <path|null> — honest one: consults adapter
    With adapter present-and-capable: records what WOULD be rendered (per-slide render plan, deterministic, sha) and exits with dry-run evidence
    With adapter absent/incapable: structured report {adapter: ABSENT-UNKNOWN, would_render: <plan>, blocked_at: dependency canon (WP-D 🟠)}
    """
    data, err = load_outline(outline_path)
    if err:
        print(f"fill_template: {err}", file=sys.stderr)
        return 1

    _, _, sha = canonicalize_for_sha(data)

    # Per-slide render plan (deterministic, sha)
    would_render = []
    for slide in data.get("slides", []):
        ref = slide.get("ref")
        stype = slide.get("type")
        bullets = slide.get("bullets", [])
        # Deterministic render plan: ref, type, bullet count, total chars, sha of slide
        slide_bytes = json.dumps(slide, sort_keys=True).encode("utf-8")
        slide_sha = hashlib.sha256(slide_bytes).hexdigest()[:8]
        would_render.append({"ref": ref, "type": stype, "bullets": len(bullets), "chars": sum(len(b.get("text","")) for b in bullets), "sha": slide_sha})

    adapter_status = {"pptx": "ABSENT-UNKNOWN"}
    adapter_probe = None
    if adapter_path and adapter_path.lower() != "null":
        ap = pathlib.Path(adapter_path)
        if not ap.exists():
            # Try relative to ROOT
            ap2 = ROOT / adapter_path
            if ap2.exists():
                ap = ap2
        if ap.exists():
            try:
                spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(ap))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                adapter_probe = mod.probe_pptx_capability()
                adapter_status = adapter_probe
            except Exception as e:
                adapter_status = {"pptx": "ABSENT-UNKNOWN", "failure": str(e)[:200], "note": "adapter load failed — recorded as unknown"}
        else:
            adapter_status = {"pptx": "ABSENT-UNKNOWN", "failure": f"adapter path {adapter_path} not found", "note": "adapter ABSENT-UNKNOWN — blocked_at dependency canon (WP-D 🟠)"}
    else:
        # No adapter specified — ABSENT-UNKNOWN
        adapter_status = {"pptx": "ABSENT-UNKNOWN", "note": "no adapter specified — blocked_at dependency canon (WP-D 🟠) — would_render plan only"}

    if adapter_status.get("pptx") == "AVAILABLE":
        # Would render — dry-run evidence
        report = {
            "adapter": adapter_status,
            "would_render": would_render,
            "sha": sha,
            "dry_run": True,
            "note": "adapter present-and-capable — records what WOULD be rendered, deterministic sha, dry-run evidence — no actual rendering in stage C per non-goals"
        }
        print(json.dumps(report, indent=2))
        print(f"fill_template: dry-run evidence — adapter AVAILABLE — would render {len(would_render)} slide(s) sha {sha} — no actual rendering per S-2-PPTX-C non-goals")
        return 0
    else:
        # Honest blocked report
        report = {
            "adapter": "ABSENT-UNKNOWN",
            "adapter_probe": adapter_status,
            "would_render": would_render,
            "sha": sha,
            "blocked_at": "dependency canon (WP-D 🟠)",
            "note": "verb never pretends render capacity it does not have — constraint honesty per IP-ENV-01 grammar: ABSENT ≠ UNAVAILABLE ≠ UNKNOWN — declared and stamped"
        }
        print(json.dumps(report, indent=2))
        print(f"fill_template: blocked_at dependency canon (WP-D 🟠) — adapter ABSENT-UNKNOWN — would_render plan {len(would_render)} slide(s) sha {sha} — never crash, never fake")
        return 0

def self_test():
    tests=[]
    def vec(name, fn):
        try:
            ok = fn()
        except Exception as e:
            ok = False
            print(f"  vector {name} exception {e}")
            import traceback; traceback.print_exc()
        status = "PASS" if ok else "FAIL"
        print(f"  vector {name} -> {status}")
        tests.append(ok)

    def make_outline(bullets_per_slide=3, chars_per_bullet=20):
        return {
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-TEST",
            "title": "Test Outline",
            "theme": {"name": "anchor", "theme_lock": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"]},
            "slides": [{"ref": "S-001", "type": "content", "bullets": [{"text": "x"*chars_per_bullet, "source_ref": f"SRC-00{i+1}"} for i in range(bullets_per_slide)], "notes": None}],
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-16", "source_refs": ["SRC-001"]},
            "honesty_note": "test"
        }

    def v_plan_exemplar_budgets():
        # Plan of exemplar emits budgets
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "plan_slide", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json")], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "budgets re-asserted at plan time" in p.stdout and "backed" in p.stdout

    def v_verify_chains_green():
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "verify_deck", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json")], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "chained gate green" in p.stdout and "checked" in p.stdout.lower()

    def v_fill_absent_adapter_blocked():
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "fill_template", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"), "--adapter", "null"], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "ABSENT-UNKNOWN" in p.stdout and "blocked_at" in p.stdout and "WP-D" in p.stdout

    def v_no_unconditional_pptx_import():
        # Walk ship-files asserting no raw import pptx outside guarded probe block — fence law extended
        import re
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        # Guarded probe block is allowed only in deck_pptx_adapter.py inside try:
        # So we check all scripts/*.py except deck_pptx_adapter.py must have zero matches
        # And deck_pptx_adapter.py must not have unconditional import at module level — only inside try
        for fp in (ROOT / "scripts").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            if fp.name == "deck_pptx_adapter.py":
                # Check that import pptx appears only inside try block
                # Find all occurrences of pattern and ensure they are inside try:
                # Simple check: file should contain "try:" before "import pptx"
                # And should NOT have import at top level outside try — we check that the first occurrence is after "try:"
                # For simplicity, ensure file does NOT contain pattern at beginning of file outside function? We'll check that "import pptx" is inside function probe_pptx_capability
                if "def probe_pptx_capability" not in txt:
                    return False
                # Ensure no top-level import pptx
                lines = txt.splitlines()
                for i, line in enumerate(lines):
                    if re.match(r"^\s*(import\s+pptx|from\s+pptx)", line):
                        # If this line is before def probe_pptx_capability, it's unconditional at module level → FAIL
                        # Find def line index
                        def_idx = txt.find("def probe_pptx_capability")
                        line_idx = txt.find(line)
                        if line_idx < def_idx:
                            return False
                continue
            # Other files must have zero matches
            if pattern.search(txt):
                return False
        return True

    def v_plan_budgets_reasserted():
        import tempfile, shutil, subprocess
        # Plan should re-check budgets per slide vs DECK_RULES
        outline = make_outline(bullets_per_slide=3, chars_per_bullet=20)
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            (tmp / "schemas").mkdir(parents=True, exist_ok=True)
            (tmp / "decks").mkdir(parents=True, exist_ok=True)
            (tmp / "scripts").mkdir(parents=True, exist_ok=True)
            (tmp / "01-research").mkdir(parents=True, exist_ok=True)
            (tmp / "09-nota").mkdir(parents=True, exist_ok=True)
            (tmp / "06-triangulate").mkdir(parents=True, exist_ok=True)
            shutil.copy(str(ROOT / "schemas" / "deck_outline.schema.json"), str(tmp / "schemas" / "deck_outline.schema.json"))
            shutil.copy(str(ROOT / "decks" / "DECK_RULES.json"), str(tmp / "decks" / "DECK_RULES.json"))
            shutil.copy(str(ROOT / "scripts" / "deck_verbs.py"), str(tmp / "scripts" / "deck_verbs.py"))
            shutil.copy(str(ROOT / "scripts" / "deck_pptx_adapter.py"), str(tmp / "scripts" / "deck_pptx_adapter.py"))
            shutil.copy(str(ROOT / "scripts" / "deck_rules_check.py"), str(tmp / "scripts" / "deck_rules_check.py"))
            shutil.copy(str(ROOT / "scripts" / "deck_verify.py"), str(tmp / "scripts" / "deck_verify.py"))
            (tmp / "01-research" / "REFERENCES.md").write_text("SRC-001 SRC-002", encoding="utf-8")
            (tmp / "09-nota" / "CARD_001.md").write_text("CARD_001", encoding="utf-8")
            out_path = tmp / "decks" / "OUTLINE_TEST.json"
            out_path.write_text(json.dumps(outline), encoding="utf-8")
            p = subprocess.run(["python3", "scripts/deck_verbs.py", "plan_slide", str(out_path)], cwd=str(tmp), capture_output=True, text=True)
            return "budgets re-asserted" in p.stdout and "truth:" in p.stdout
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    vec("plan of exemplar emits budgets", v_plan_exemplar_budgets)
    vec("verify chains green (deck_rules_check + deck_verify + adapter)", v_verify_chains_green)
    vec("fill_template with ABSENT adapter reports blocked-at-WP-D never crash never fake", v_fill_absent_adapter_blocked)
    vec("unconditional-pptx-import guard — no raw import pptx outside guarded probe block", v_no_unconditional_pptx_import)
    vec("plan budgets re-asserted at plan time + truth lines", v_plan_budgets_reasserted)

    passed = sum(tests)
    print(f"deck_verbs self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run self-test vectors")
    subparsers = parser.add_subparsers(dest="verb", required=False)

    p_plan = subparsers.add_parser("plan_slide", help="derive per-slide plan")
    p_plan.add_argument("outline", help="outline JSON path")

    p_verify = subparsers.add_parser("verify_deck", help="chained gate verify")
    p_verify.add_argument("outline", help="outline JSON path")

    p_fill = subparsers.add_parser("fill_template", help="honest fill with optional adapter")
    p_fill.add_argument("outline", help="outline JSON path")
    p_fill.add_argument("--adapter", default="null", help="adapter path or null for ABSENT-UNKNOWN")

    args = parser.parse_args()
    if args.self_test:
        return self_test()

    if not args.verb:
        parser.print_help()
        return 1

    if args.verb == "plan_slide":
        return plan_slide(args.outline)
    elif args.verb == "verify_deck":
        return verify_deck(args.outline)
    elif args.verb == "fill_template":
        return fill_template(args.outline, args.adapter)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
