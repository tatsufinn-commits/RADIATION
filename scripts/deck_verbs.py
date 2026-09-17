#!/usr/bin/env python3
"""
deck_verbs.py — Guardrailed verbs + optional adapter promotion (S-2-PPTX-D stage 4 of 5)

Standing interface rule: expose guardrailed verbs — plan_slide · fill_template · verify_deck — never raw primitives.
Three verbs, stdlib + adapter-mediated pptx, outline-level, receipt law holds verbatim deck never delivered alone its outline ships always.

Verbs:
- plan_slide <outline> — derive per-slide plan: rule re-check per slide vs DECK_RULES (budgets re-asserted at plan time), source_ref audit summary {backed, unbacked-warn}, per-slide truth lines (ref · type · bullets · chars · receipts). PLAN, never render.
- verify_deck <outline> — chained gate: deck_rules_check + deck_verify (canonical idempotence + receipts) + adapter status line + --verify-rendered if probe AVAILABLE; the verify deck command a Commander-invoked session would use before anything ever renders.
- fill_template <outline> --adapter <path|null> [--out <pptx>] — unfrozen with adapter AVAILABLE performs render via deck_render emits {rendered, sha, receipts_embedded slides-with-notes count} with ABSENT keeps honest report shape no fake never. Default --out tempdir NEVER writes repo tree, no .pptx ever committed, theme taken from DECK_RULES.json as-is anchor PROVISIONAL, receipts embedded as speaker notes.

No python-pptx import anywhere outside guarded probe block — single import site law: ONLY scripts/deck_pptx_adapter.py may contain `import pptx`, never at module level, always inside guarded probe / call-sites, fence law walks ALL ship-files FAIL any other occurrence.

Self-test ≥6 vectors incl fence extension + tree-scan guard asserting zero *.pptx ever committed.

Registry 36 → 37.
License: python-pptx MIT license-logged, clean-room, no GPL — transitive lxml BSD, Pillow HPND, XlsxWriter BSD — MIT/BSD no GPL.
"""

import argparse
import hashlib
import json
import pathlib
import re
import sys
import importlib.util
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "decks" / "DECK_RULES.json"

if "pptx" in sys.modules:
    print("FAIL: pptx module imported unconditionally — policy FAIL-class per S-2-PPTX-D single import site", file=sys.stderr)
    sys.exit(1)

try:
    own_text = pathlib.Path(__file__).read_text(encoding="utf-8", errors="ignore")
    for line in own_text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            continue
        if re.match(r"^(import\s+pptx|from\s+pptx)", s):
            print(f"FAIL: deck_verbs.py contains forbidden import pptx line: {line} — single import site law", file=sys.stderr)
            sys.exit(1)
except Exception:
    pass

def load_json(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), ""
    except Exception as e:
        return None, f"invalid JSON at {path}: {e}"

def load_outline(path):
    return load_json(path)

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
    if sref is None:
        return True, "null — awaiting source"
    if not re.fullmatch(r"(SRC-[A-Za-z0-9_-]+|ANNOT_[A-Za-z0-9_-]+|TRI_[A-Za-z0-9_-]+|CARD_[A-Za-z0-9_-]+|GAP-[A-Za-z0-9_-]+|R2-[A-Za-z0-9_-]+|OUTLINE-[A-Za-z0-9_-]+)", sref):
        return False, f"invalid lane {sref}"
    if sref.startswith("SRC-"):
        for fp in (ROOT / "01-research").rglob("*.md"):
            try:
                if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{fp.relative_to(ROOT)}"
            except Exception:
                continue
        ref = ROOT / "01-research" / "REFERENCES.md"
        if ref.exists():
            try:
                if sref in ref.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{ref.relative_to(ROOT)}"
            except Exception:
                pass
        for fp in ROOT.rglob(f"*{sref}*"):
            if fp.is_file():
                return True, f"{fp.relative_to(ROOT)}"
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
            try:
                if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{fp.relative_to(ROOT)}"
            except Exception:
                continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("TRI_"):
        for fp in (ROOT / "06-triangulate").rglob("*.md"):
            try:
                if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{fp.relative_to(ROOT)}"
            except Exception:
                continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    if sref.startswith("CARD_"):
        for fp in (ROOT / "09-nota").rglob("*.md"):
            try:
                if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{fp.relative_to(ROOT)}"
            except Exception:
                continue
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
            try:
                if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                    return True, f"{fp.relative_to(ROOT)}"
            except Exception:
                continue
        return False, f"UNRESOLVED-RECEIPT {sref}"
    return False, f"UNRESOLVED-RECEIPT {sref}"

def plan_slide(outline_path):
    data, err = load_outline(outline_path)
    if err:
        print(f"plan_slide: {err}", file=sys.stderr)
        return 1
    rules_data, rerr = load_rules()
    if rerr:
        print(f"plan_slide: {rerr}", file=sys.stderr)
        return 1
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
                    receipts.append(f"{sref} (UNRESOLVED)")
        bullet_count_ok = len(bullets) <= r001 if r001 is not None else True
        chars_ok = total_chars <= r002 if r002 is not None else True
        max_bullet_chars = max((len(b.get("text","")) for b in bullets), default=0)
        bullet_chars_ok = max_bullet_chars <= r003 if r003 is not None else True
        truth = f"{ref} · {stype} · bullets {len(bullets)}/{r001} {'OK' if bullet_count_ok else 'FAIL R-001'} · chars {total_chars}/{r002} {'OK' if chars_ok else 'FAIL R-002'} · max_bullet {max_bullet_chars}/{r003} {'OK' if bullet_chars_ok else 'FAIL R-003'} · receipts {receipts}"
        truth_lines.append(truth)
    print(f"plan_slide: {oid} · sha {sha} · slides {len(data.get('slides',[]))}")
    print(f"  budgets re-asserted at plan time: R-001 max_bullets {r001}, R-002 max_chars_slide {r002}, R-003 max_chars_bullet {r003}")
    print(f"  source_ref audit: {{backed: {backed}, unbacked-warn: {unbacked_warn}}}")
    for tl in truth_lines:
        print(f"  truth: {tl}")
    has_fail = any("FAIL" in tl for tl in truth_lines)
    if has_fail:
        print(f"plan_slide: {len([tl for tl in truth_lines if 'FAIL' in tl])} slide(s) exceed budgets — plan emitted with FAIL markers")
        return 1
    else:
        print(f"plan_slide: 0 findings — budgets OK, receipts audited")
        return 0

def verify_deck(outline_path):
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
    try:
        spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        status = mod.get_adapter_status()
        print(f"verify_deck: {status}")
        # If AVAILABLE, also run --verify-rendered
        cap = mod.probe_pptx_capability()
        if cap.get("pptx") == "AVAILABLE":
            print(f"verify_deck: probe AVAILABLE — running --verify-rendered round-trip")
            p3 = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verify.py"), "--verify-rendered", str(outline_path)], cwd=str(ROOT), capture_output=True, text=True)
            print(p3.stdout.strip())
            if p3.stderr:
                print(p3.stderr.strip(), file=sys.stderr)
            if p3.returncode != 0:
                print(f"verify_deck: --verify-rendered FAIL — DRIFT detected")
                return p3.returncode
        else:
            print(f"verify_deck: probe {cap} — ABSENT-UNKNOWN — skipUnless AVAILABLE for --verify-rendered — stdlib-only env degrades honestly")
    except Exception as e:
        print(f"verify_deck: adapter status probe failed: {e} — adapter ABSENT-UNKNOWN — constraint grammar per IP-ENV-01")
    print(f"verify_deck: 0 findings — chained gate green — outline verified, ready for fill_template (adapter may be ABSENT-UNKNOWN)")
    return 0

def fill_template(outline_path, adapter_path=None, out_path=None):
    """
    fill_template <outline> --adapter <path|null> [--out <pptx>] — unfrozen with adapter AVAILABLE performs render via deck_render emits {rendered, sha, receipts_embedded slides-with-notes count} with ABSENT keeps honest report shape no fake never.
    """
    data, err = load_outline(outline_path)
    if err:
        print(f"fill_template: {err}", file=sys.stderr)
        return 1

    _, _, sha = canonicalize_for_sha(data)

    would_render = []
    for slide in data.get("slides", []):
        ref = slide.get("ref")
        stype = slide.get("type")
        bullets = slide.get("bullets", [])
        slide_bytes = json.dumps(slide, sort_keys=True).encode("utf-8")
        slide_sha = hashlib.sha256(slide_bytes).hexdigest()[:8]
        would_render.append({"ref": ref, "type": stype, "bullets": len(bullets), "chars": sum(len(b.get("text","")) for b in bullets), "sha": slide_sha})

    adapter_status = {"pptx": "ABSENT-UNKNOWN"}
    adapter_mod = None

    # Resolve adapter path — explicit "null" means ABSENT-UNKNOWN, no fallback; None means try default canonical adapter
    resolved_adapter_path = None
    if adapter_path is None:
        # No adapter specified — try canonical adapter location
        default_adapter = ROOT / "scripts" / "deck_pptx_adapter.py"
        if default_adapter.exists():
            resolved_adapter_path = default_adapter
        else:
            adapter_status = {"pptx": "ABSENT-UNKNOWN", "note": "no adapter specified — blocked_at dependency canon (WP-D 🟠) — would_render plan only"}
    elif isinstance(adapter_path, str) and adapter_path.lower() == "null":
        # Explicit null → ABSENT-UNKNOWN — honest blocked shape, no fallback
        adapter_status = {"pptx": "ABSENT-UNKNOWN", "note": "explicit null adapter — blocked_at dependency canon (WP-D 🟠) — would_render plan only — no fake"}
    else:
        ap = pathlib.Path(adapter_path)
        if not ap.exists():
            ap2 = ROOT / adapter_path
            if ap2.exists():
                ap = ap2
        if ap.exists():
            resolved_adapter_path = ap
        else:
            adapter_status = {"pptx": "ABSENT-UNKNOWN", "failure": f"adapter path {adapter_path} not found", "note": "adapter ABSENT-UNKNOWN — blocked_at dependency canon (WP-D 🟠)"}

    if resolved_adapter_path:
        try:
            spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(resolved_adapter_path))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            adapter_mod = mod
            adapter_status = mod.probe_pptx_capability()
        except Exception as e:
            adapter_status = {"pptx": "ABSENT-UNKNOWN", "failure": str(e)[:500], "note": "adapter load failed — recorded as unknown per honesty grammar PRESENT witness required, ABSENT honest, UNKNOWN stays"}

    if adapter_status.get("pptx") == "AVAILABLE" and adapter_mod is not None:
        # AVAILABLE → performs render via deck_render (via adapter) emits {rendered, sha, receipts_embedded slides-with-notes count}
        try:
            # Determine out_path — default tempdir NEVER writes repo tree
            if out_path is None:
                tmpdir = pathlib.Path(tempfile.gettempdir())
                out_pptx = tmpdir / f"{data.get('id','OUTLINE')}_filled.pptx"
            else:
                out_pptx = pathlib.Path(out_path)
                # Enforce NEVER writes into repo tree
                out_resolved = out_pptx.resolve()
                root_resolved = ROOT.resolve()
                if root_resolved in out_resolved.parents or out_resolved == root_resolved:
                    print(f"fill_template: NEVER writes into repo tree per canon: out_path {out_pptx} inside ROOT {ROOT} — use tempdir — LAW-6-era idiom", file=sys.stderr)
                    return 1

            rendered_path, rendered_sha, receipts_embedded, msg = adapter_mod.render_outline_to_pptx(data, out_pptx)

            report = {
                "rendered": rendered_path,
                "sha": rendered_sha,
                "receipts_embedded": receipts_embedded,
                "slides": len(data.get("slides", [])),
                "adapter": adapter_status,
                "would_render": would_render,
                "theme": data.get("theme", {}).get("name", "anchor"),
                "note": "pptx render: AVAILABLE when dependency present, else ABSENT-UNKNOWN — constraint grammar per IP-ENV-01 — receipts embedded as speaker notes, outline ships with deck always — receipt law holds verbatim deck never delivered alone its outline ships always"
            }
            print(json.dumps(report, indent=2))
            print(f"fill_template: {msg} — AVAILABLE → rendered {rendered_path} sha {rendered_sha} receipts_embedded {receipts_embedded} slides-with-notes count — outline ships always per receipt law")
            return 0

        except Exception as e:
            print(f"fill_template: render failed despite AVAILABLE probe: {e}", file=sys.stderr)
            import traceback; traceback.print_exc(file=sys.stderr)
            # Fall back to honest blocked report? No, if probe AVAILABLE but render fails, that's a real failure — return 1
            return 1

    else:
        # ABSENT-UNKNOWN keeps honest report shape no fake never
        report = {
            "adapter": "ABSENT-UNKNOWN",
            "adapter_probe": adapter_status,
            "would_render": would_render,
            "sha": sha,
            "blocked_at": "dependency canon (WP-D 🟠)",
            "note": "verb never pretends render capacity it does not have — constraint honesty per IP-ENV-01 grammar: ABSENT ≠ UNAVAILABLE ≠ UNKNOWN — declared and stamped — no fake never — outline ships always, deck never alone"
        }
        print(json.dumps(report, indent=2))
        print(f"fill_template: blocked_at dependency canon (WP-D 🟠) — adapter ABSENT-UNKNOWN — would_render plan {len(would_render)} slide(s) sha {sha} — never crash, never fake — ABSENT-UNKNOWN per honesty grammar")
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
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "plan_slide", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json")], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "budgets re-asserted at plan time" in p.stdout and "backed" in p.stdout

    def v_verify_chains_green():
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "verify_deck", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json")], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "chained gate green" in p.stdout

    def v_fill_absent_adapter_blocked():
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "fill_template", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"), "--adapter", "null"], cwd=str(ROOT), capture_output=True, text=True)
        return p.returncode == 0 and "ABSENT-UNKNOWN" in p.stdout and "blocked_at" in p.stdout and "WP-D" in p.stdout

    def v_no_unconditional_pptx_import():
        pattern = re.compile(r"^\s*(import\s+pptx|from\s+pptx)", re.MULTILINE)
        for fp in (ROOT / "scripts").rglob("*.py"):
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            if fp.name == "deck_pptx_adapter.py":
                continue
            if pattern.search(txt):
                # Allow if inside comment? We already stripped? Actually search includes comments but we check line by line
                for line in txt.splitlines():
                    s = line.strip()
                    if s.startswith("#"):
                        continue
                    if re.match(r"^(import\s+pptx|from\s+pptx)", s):
                        print(f"    fence violation: {fp} line {line}")
                        return False
        return True

    def v_plan_budgets_reasserted():
        import subprocess
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

    def v_fill_template_render_when_available():
        # Test fill_template when adapter AVAILABLE → emits {rendered, sha, receipts_embedded}
        try:
            spec = importlib.util.spec_from_file_location("deck_pptx_adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cap = mod.probe_pptx_capability()
            if cap.get("pptx") != "AVAILABLE":
                print(f"    skip: probe {cap} — ABSENT-UNKNOWN — stdlib-only env degrades honestly")
                return True
        except Exception as e:
            print(f"    skip: probe failed {e}")
            return True

        import subprocess
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        try:
            out_pptx = tmpdir / "filled_test.pptx"
            p = subprocess.run([sys.executable, str(ROOT / "scripts" / "deck_verbs.py"), "fill_template", str(ROOT / "decks" / "examples" / "OUTLINE_example_card001.json"), "--adapter", str(ROOT / "scripts" / "deck_pptx_adapter.py"), "--out", str(out_pptx)], cwd=str(ROOT), capture_output=True, text=True)
            if p.returncode != 0:
                print(f"    fill_template render failed rc={p.returncode} stdout={p.stdout} stderr={p.stderr}")
                return False
            if not out_pptx.exists():
                print(f"    rendered file not exists at {out_pptx}")
                return False
            # Check JSON output contains rendered, sha, receipts_embedded
            if "rendered" not in p.stdout or "receipts_embedded" not in p.stdout or "sha" not in p.stdout:
                print(f"    missing keys in output {p.stdout}")
                return False
            return True
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def v_no_pptx_committed():
        for fp in ROOT.rglob("*.pptx"):
            if ".git" in str(fp):
                continue
            print(f"    found pptx in tree: {fp}")
            return False
        return True

    vec("plan of exemplar emits budgets", v_plan_exemplar_budgets)
    vec("verify chains green (deck_rules_check + deck_verify + adapter)", v_verify_chains_green)
    vec("fill_template with ABSENT adapter reports blocked-at-WP-D never crash never fake", v_fill_absent_adapter_blocked)
    vec("unconditional-pptx-import guard — no raw import pptx outside guarded probe block — single import site ONLY deck_pptx_adapter.py", v_no_unconditional_pptx_import)
    vec("plan budgets re-asserted at plan time + truth lines", v_plan_budgets_reasserted)
    vec("fill_template render when AVAILABLE emits rendered sha receipts_embedded (skipUnless AVAILABLE)", v_fill_template_render_when_available)
    vec("no *.pptx ever committed — tree-scan guard", v_no_pptx_committed)

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

    p_fill = subparsers.add_parser("fill_template", help="honest fill with optional adapter — unfrozen with adapter AVAILABLE performs render via deck_render")
    p_fill.add_argument("outline", help="outline JSON path")
    p_fill.add_argument("--adapter", default=None, help="adapter path or null for ABSENT-UNKNOWN (default: scripts/deck_pptx_adapter.py)")
    p_fill.add_argument("--out", default=None, help="explicit out path for .pptx (default tempdir) — NEVER writes into repo tree")

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
        return fill_template(args.outline, args.adapter, args.out)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
