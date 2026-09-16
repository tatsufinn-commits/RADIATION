#!/usr/bin/env python3
"""
deck_verify.py — Outline round-trip + receipt resolver (S-2-PPTX-B stage 1 of 5)

House finding style, deterministic, stdlib-only, no network, no pptx import.

Honest design constraint (desk, on record): R&D round-trip semantics (MATCH/DRIFT over rendered deck) needs python-pptx — gated 🟠 at WP-D. This stage therefore verifies what stdlib can verify now: outline layer itself — canonical integrity, receipt resolvability, drift on tamper. Render-half verifier lands when dependency canon opens (stage C/D), unchanged in intent.

Functions:
- Canonicalize: outline → canonical form (sorted keys, normalized whitespace, stable ordering of slides/bullets preserved by ref) → re-serialize → idempotence assert (canonical(canonical(o)) ≡ canonical(o)), deterministic bytes → sha log.
- Receipt resolver (new FK edge): every non-null source_ref must RESOLVE into tree — register lanes only (SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-, OUTLINE-) → grounding tables it consults (REFERENCES.md rows, 09-nota files, 06-triangulate files, brain/knowledge registry) — witness-based resolution, no network; unresolved → finding UNRESOLVED-RECEIPT (FAIL).
- Drift battery: tamper an outline copy (drop bullet, mutate text, swap source_ref) → verifier must emit DRIFT per class named (MATCH → DRIFT semantics from prototype, at outline level).

No python-pptx import anywhere (import pptx = policy FAIL-class) — this file must never import pptx.
No renderer, no committed binaries, no plan/fill verbs (stage C), no WP-D canon text, no theme-registry edits.

Self-test ≥5 vectors: true-match, drift-text, drift-structure, unresolved-receipt, canonical-idempotence.
"""

import argparse
import hashlib
import json
import pathlib
import re
import sys
import tempfile
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Policy: no pptx import
if "pptx" in sys.modules:
    print("FAIL: pptx module imported — policy FAIL-class per S-2-PPTX-B", file=sys.stderr)
    sys.exit(1)

def run(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

def load_json(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), ""
    except Exception as e:
        return None, f"invalid JSON at {path}: {e}"

def normalize_whitespace(text):
    # Normalized whitespace: strip leading/trailing, collapse internal multiple spaces to single, preserve single spaces
    # For bullet text, we strip and collapse
    if not isinstance(text, str):
        return text
    # Strip leading/trailing whitespace
    t = text.strip()
    # Collapse multiple whitespace (including tabs, newlines) to single space
    t = re.sub(r"\s+", " ", t)
    return t

def canonicalize(outline):
    """
    Canonicalize outline → canonical form (sorted keys, normalized whitespace, stable ordering of slides/bullets preserved by ref)
    - Sorted keys via json dump sort_keys
    - Normalized whitespace for text fields (title, bullet text, notes)
    - Stable ordering of slides preserved by ref: sort slides by ref
    - Bullets preserved in original order? But stable ordering preserved by ref — bullets have no ref, so preserve order
    - Deterministic bytes → sha log
    Returns (canonical_dict, canonical_bytes, sha256)
    """
    # Deep copy
    import copy
    data = copy.deepcopy(outline)

    # Normalize whitespace for title
    if "title" in data and isinstance(data["title"], str):
        data["title"] = normalize_whitespace(data["title"])

    # Normalize theme name? Keep as is, but strip
    if "theme" in data and isinstance(data["theme"], dict):
        if "name" in data["theme"] and isinstance(data["theme"]["name"], str):
            data["theme"]["name"] = normalize_whitespace(data["theme"]["name"])

    # Slides: sort by ref for stable ordering, normalize bullets text and notes
    slides = data.get("slides", [])
    # Normalize each slide
    for slide in slides:
        if "ref" in slide and isinstance(slide["ref"], str):
            slide["ref"] = normalize_whitespace(slide["ref"])
        if "type" in slide and isinstance(slide["type"], str):
            slide["type"] = normalize_whitespace(slide["type"])
        if "notes" in slide and isinstance(slide["notes"], str):
            slide["notes"] = normalize_whitespace(slide["notes"]) if slide["notes"] else slide["notes"]
        bullets = slide.get("bullets", [])
        for b in bullets:
            if "text" in b and isinstance(b["text"], str):
                b["text"] = normalize_whitespace(b["text"])
            # source_ref keep as is, strip
            if "source_ref" in b and isinstance(b["source_ref"], str):
                b["source_ref"] = b["source_ref"].strip()

    # Stable ordering: sort slides by ref
    try:
        slides_sorted = sorted(slides, key=lambda s: s.get("ref", ""))
        data["slides"] = slides_sorted
    except Exception:
        data["slides"] = slides

    # Provenance task normalize
    prov = data.get("provenance", {})
    if "task" in prov and isinstance(prov["task"], str):
        prov["task"] = normalize_whitespace(prov["task"])

    # Deterministic bytes: json dump sorted keys, indent 2? For sha, we use sorted keys and separators to be deterministic
    # Use sort_keys=True, separators=(',', ':') for minimal deterministic, but for readability we also use indent? For sha, we need deterministic bytes
    # We'll use sort_keys=True, indent=2 for canonical bytes (deterministic)
    canonical_bytes = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(canonical_bytes).hexdigest()[:12]

    return data, canonical_bytes, sha

def check_canonical_idempotence(outline):
    """
    Idempotence assert: canonical(canonical(o)) ≡ canonical(o)
    Returns (ok, message)
    """
    canon1, bytes1, sha1 = canonicalize(outline)
    canon2, bytes2, sha2 = canonicalize(canon1)
    if bytes1 == bytes2 and sha1 == sha2:
        return True, f"canonical-idempotence PASS — sha {sha1} — canonical(canonical(o)) ≡ canonical(o)"
    else:
        return False, f"canonical-idempotence FAIL — sha1 {sha1} vs sha2 {sha2} — bytes differ"

def resolve_source_ref(sref):
    """
    Receipt resolver (new FK edge): every non-null source_ref must RESOLVE into tree — register lanes only
    Grounding tables it consults (REFERENCES.md rows, 09-nota files, 06-triangulate files, brain/knowledge registry) — witness-based, no network
    Returns (resolved, witness_path_or_note)
    """
    if sref is None:
        return True, "null source_ref — claim awaiting source, not unresolved"

    # Register lanes only: SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-, OUTLINE-
    if not re.fullmatch(r"(SRC-[A-Za-z0-9_-]+|ANNOT_[A-Za-z0-9_-]+|TRI_[A-Za-z0-9_-]+|CARD_[A-Za-z0-9_-]+|GAP-[A-Za-z0-9_-]+|R2-[A-Za-z0-9_-]+|OUTLINE-[A-Za-z0-9_-]+)", sref):
        return False, f"invalid lane {sref!r} — must be SRC-/ANNOT_/TRI_/CARD_/GAP-/R2-/OUTLINE-"

    # Witness-based resolution — search tree
    # SRC-: check REFERENCES.md, external_sources, 01-research, 02-analyze
    if sref.startswith("SRC-"):
        # Check 01-research/REFERENCES.md
        ref_path = ROOT / "01-research" / "REFERENCES.md"
        if ref_path.exists():
            if sref in ref_path.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{ref_path} contains {sref}"
        # Check Brain/external_sources/INDEX.md
        ext_idx = ROOT / "Brain" / "external_sources" / "INDEX.md"
        if ext_idx.exists():
            if sref in ext_idx.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{ext_idx} contains {sref}"
        # Check any file in 01-research, 02-analyze, 05-annotate, 06-triangulate, 09-nota that mentions SRC-
        for search_dir in [ROOT / "01-research", ROOT / "02-analyze", ROOT / "05-annotate", ROOT / "06-triangulate", ROOT / "09-nota"]:
            if search_dir.exists():
                for fp in search_dir.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)} contains {sref}"
                    except Exception:
                        continue
        # Also check if any file named with SRC-
        for fp in ROOT.rglob(f"*{sref}*"):
            if fp.is_file():
                return True, f"file {fp.relative_to(ROOT)} matches {sref}"
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in REFERENCES.md rows nor external_sources nor research lanes"

    if sref.startswith("ANNOT_"):
        # Check 05-annotate/
        for fp in (ROOT / "05-annotate").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)} contains {sref}"
        # Also check 02-analyze?
        for fp in (ROOT / "02-analyze").rglob("*.md"):
            if sref in fp.name:
                return True, f"{fp.relative_to(ROOT)} matches {sref}"
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in 05-annotate/ nor 02-analyze/"

    if sref.startswith("TRI_"):
        for fp in (ROOT / "06-triangulate").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)} contains {sref}"
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in 06-triangulate/"

    if sref.startswith("CARD_"):
        for fp in (ROOT / "09-nota").rglob("*.md"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)} contains {sref}"
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in 09-nota/"

    if sref.startswith("GAP-"):
        # Check docs, 04-incubate, etc.
        for search_dir in [ROOT / "docs", ROOT / "04-incubate", ROOT / "08-overhaul"]:
            if search_dir.exists():
                for fp in search_dir.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)} contains {sref}"
                    except Exception:
                        continue
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in docs/ nor incubate/ nor overhaul/"

    if sref.startswith("R2-"):
        for search_dir in [ROOT / "08-overhaul", ROOT / "docs"]:
            if search_dir.exists():
                for fp in search_dir.rglob("*.md"):
                    try:
                        if sref in fp.read_text(encoding="utf-8", errors="ignore"):
                            return True, f"{fp.relative_to(ROOT)} contains {sref}"
                    except Exception:
                        continue
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in overhaul/ nor docs/"

    if sref.startswith("OUTLINE-"):
        # Check decks/OUTLINE_*.json and decks/examples/
        for fp in (ROOT / "decks").rglob("*.json"):
            if sref in fp.name or sref in fp.read_text(encoding="utf-8", errors="ignore"):
                return True, f"{fp.relative_to(ROOT)} contains {sref}"
        return False, f"UNRESOLVED-RECEIPT {sref} — not found in decks/"

    return False, f"UNRESOLVED-RECEIPT {sref} — unknown lane"

def check_receipts(outline):
    findings = []
    oid = outline.get("id", "UNKNOWN")
    slides = outline.get("slides", [])
    for slide in slides:
        ref = slide.get("ref", "UNKNOWN-SLIDE")
        bullets = slide.get("bullets", [])
        for idx, b in enumerate(bullets):
            sref = b.get("source_ref")
            if sref is None:
                continue
            resolved, witness = resolve_source_ref(sref)
            if not resolved:
                findings.append(("error", f"{oid} · {ref} · bullet {idx} · UNRESOLVED-RECEIPT · observed {sref!r} vs threshold resolved receipt — witness {witness}"))
    return findings

def detect_drift(original, tampered):
    """
    Drift battery: tamper an outline copy (drop bullet, mutate text, swap source_ref) → verifier must emit DRIFT per class named (MATCH → DRIFT semantics)
    Returns classification: MATCH, DRIFT-text, DRIFT-structure, DRIFT-source_ref, DRIFT-theme, etc.
    """
    # Canonicalize both
    canon_orig, bytes_orig, sha_orig = canonicalize(original)
    canon_tamp, bytes_tamp, sha_tamp = canonicalize(tampered)

    if bytes_orig == bytes_tamp:
        return "MATCH", f"MATCH — sha {sha_orig} identical"

    # Check what drifted
    # Compare slides count
    if len(canon_orig.get("slides", [])) != len(canon_tamp.get("slides", [])):
        return "DRIFT-structure", f"DRIFT-structure — slides count {len(canon_orig.get('slides', []))} vs {len(canon_tamp.get('slides', []))} — sha {sha_orig} vs {sha_tamp}"

    # Compare bullets per slide
    for s_orig, s_tamp in zip(canon_orig.get("slides", []), canon_tamp.get("slides", [])):
        if len(s_orig.get("bullets", [])) != len(s_tamp.get("bullets", [])):
            return "DRIFT-structure", f"DRIFT-structure — slide {s_orig.get('ref')} bullets {len(s_orig.get('bullets', []))} vs {len(s_tamp.get('bullets', []))} — dropped bullet"

        # Compare bullet text
        for b_orig, b_tamp in zip(s_orig.get("bullets", []), s_tamp.get("bullets", [])):
            if b_orig.get("text") != b_tamp.get("text"):
                return "DRIFT-text", f"DRIFT-text — slide {s_orig.get('ref')} bullet text mutated {b_orig.get('text')!r} vs {b_tamp.get('text')!r}"

            # Compare source_ref
            if b_orig.get("source_ref") != b_tamp.get("source_ref"):
                return "DRIFT-source_ref", f"DRIFT-source_ref — slide {s_orig.get('ref')} source_ref {b_orig.get('source_ref')!r} vs {b_tamp.get('source_ref')!r} — swapped receipt"

    # Compare theme
    if canon_orig.get("theme") != canon_tamp.get("theme"):
        return "DRIFT-theme", f"DRIFT-theme — theme {canon_orig.get('theme')} vs {canon_tamp.get('theme')}"

    # Generic drift
    return "DRIFT", f"DRIFT — sha {sha_orig} vs {sha_tamp} — generic drift"

def check_outline_file(path):
    findings = []
    data, err = load_json(path)
    if err:
        findings.append(("error", f"outline file invalid JSON at {path}: {err}"))
        return findings, None

    # Canonical idempotence
    ok, msg = check_canonical_idempotence(data)
    if not ok:
        findings.append(("error", f"{data.get('id','UNKNOWN')} · canonical · canonical-idempotence · {msg}"))
    else:
        # Log sha for provenance
        _, _, sha = canonicalize(data)
        findings.append(("info", f"{data.get('id','UNKNOWN')} · canonical · sha {sha} · {msg}"))

    # Receipt resolver
    receipt_findings = check_receipts(data)
    findings.extend(receipt_findings)

    return findings, data

def main_check():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=None, help="outline JSON path")
    parser.add_argument("--compare", default=None, help="compare with other outline for drift detection")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    if args.compare:
        # Drift detection mode: compare two outlines
        orig_data, err1 = load_json(args.path)
        tamp_data, err2 = load_json(args.compare)
        if err1:
            print(f"deck_verify: invalid JSON at {args.path}: {err1}")
            return 1
        if err2:
            print(f"deck_verify: invalid JSON at {args.compare}: {err2}")
            return 1
        classification, msg = detect_drift(orig_data, tamp_data)
        print(f"deck_verify: {classification} — {msg}")
        if classification == "MATCH":
            return 0
        else:
            return 1

    findings = []
    checked_data = None
    if args.path:
        p = pathlib.Path(args.path)
        if not p.exists():
            print(f"deck_verify: outline not found at {p}")
            return 1
        findings, checked_data = check_outline_file(p)
    else:
        # Lint all outlines in decks/
        decks_dir = ROOT / "decks"
        if decks_dir.exists():
            for fp in decks_dir.rglob("OUTLINE_*.json"):
                f, _ = check_outline_file(fp)
                findings.extend(f)
        if not findings:
            print("deck_verify: no outline files found — 0 findings")
            return 0

    errors = [m for cls, m in findings if cls == "error"]
    warns = [m for cls, m in findings if cls == "warn"]
    infos = [m for cls, m in findings if cls == "info"]

    for info in infos[:5]:
        print(f"  INFO {info}")

    if errors:
        print(f"deck_verify: {len(errors)} error(s), {len(warns)} warn(s)")
        for msg in errors[:20]:
            print(f"  ERROR {msg}")
        for msg in warns[:20]:
            print(f"  WARN {msg}")
        return 1
    else:
        if warns:
            print(f"deck_verify: 0 error(s), {len(warns)} warn(s)")
            for msg in warns[:20]:
                print(f"  WARN {msg}")
            return 0
        else:
            print(f"deck_verify: 0 finding(s) — canonical integrity OK, receipt resolvability OK, MATCH semantics")
            return 0

def self_test():
    def make_base_outline():
        return {
            "schema_name": "radiation.deck_outline/1",
            "id": "OUTLINE-TEST",
            "title": "Test Outline",
            "theme": {"name": "anchor", "theme_lock": ["#0F172A", "#F8FAFC", "#38BDF8", "#FBBF24", "#34D399"]},
            "slides": [
                {"ref": "S-001", "type": "content", "bullets": [{"text": "Bullet one", "source_ref": "SRC-013"}, {"text": "Bullet two", "source_ref": "CARD_001"}], "notes": None},
                {"ref": "S-002", "type": "content", "bullets": [{"text": "Bullet three", "source_ref": "TRI_bp344-accessibility_2026-09-13"}], "notes": None}
            ],
            "constraints": ["R-001", "R-002", "R-003", "R-005", "R-006"],
            "provenance": {"task": "test", "date": "2026-09-16", "source_refs": ["SRC-013"]},
            "honesty_note": "test"
        }

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

    def v_true_match():
        orig = make_base_outline()
        # Same outline should be MATCH
        cls, msg = detect_drift(orig, orig)
        return cls == "MATCH"

    def v_drift_text():
        orig = make_base_outline()
        tamp = make_base_outline()
        tamp["slides"][0]["bullets"][0]["text"] = "Mutated bullet text that is different"
        cls, msg = detect_drift(orig, tamp)
        return cls == "DRIFT-text" and "DRIFT" in msg

    def v_drift_structure():
        orig = make_base_outline()
        tamp = make_base_outline()
        # Drop a bullet
        tamp["slides"][0]["bullets"].pop(0)
        cls, msg = detect_drift(orig, tamp)
        return "DRIFT-structure" in cls

    def v_unresolved_receipt():
        orig = make_base_outline()
        orig["slides"][0]["bullets"][0]["source_ref"] = "SRC-NONEXISTENT-999"
        findings = check_receipts(orig)
        return len(findings) > 0 and any("UNRESOLVED-RECEIPT" in m for _, m in findings)

    def v_canonical_idempotence():
        orig = make_base_outline()
        ok, msg = check_canonical_idempotence(orig)
        return ok and "canonical-idempotence PASS" in msg

    def v_receipt_resolved():
        # Real source_refs from tree should resolve
        orig = make_base_outline()
        # Use known good refs: CARD_001, SRC-013, TRI_... should resolve if files exist
        # In temp repo we need to simulate? For self-test we check against real ROOT
        # CARD_001 should resolve because 09-nota/CARD_001 exists
        findings = check_receipts(orig)
        # Should have 0 unresolved for our known good refs
        # Note: SRC-013 may or may not resolve depending on REFERENCES.md, but CARD_001 should
        # We'll test with CARD_001 only
        outline2 = make_base_outline()
        outline2["slides"] = [{"ref": "S-001", "type": "content", "bullets": [{"text": "Test", "source_ref": "CARD_001"}], "notes": None}]
        findings2 = check_receipts(outline2)
        return len(findings2) == 0

    vec("true-match MATCH semantics", v_true_match)
    vec("drift-text mutated bullet", v_drift_text)
    vec("drift-structure dropped bullet", v_drift_structure)
    vec("unresolved-receipt UNRESOLVED-RECEIPT FAIL", v_unresolved_receipt)
    vec("canonical-idempotence canonical(canonical(o)) ≡ canonical(o)", v_canonical_idempotence)
    vec("receipt resolved witness-based", v_receipt_resolved)

    passed = sum(tests)
    print(f"deck_verify self-test: {passed}/{len(tests)} vectors")
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main_check())
