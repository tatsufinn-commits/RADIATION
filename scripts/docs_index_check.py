#!/usr/bin/env python3
"""
docs_index_check.py — deterministic stdlib checker, house finding style (G6)

Checks:
(i) every relative markdown link in START_HERE.md, README.md, AGENTS.md, PROTOCOL.md, docs/INDEX.md, docs/*.md resolves (skip http(s), tolerate anchors)
(ii) every docs/*.md is listed in INDEX.md or in declared whitelist
(iii) INDEX.md lists only existing files

--self-test ≥4 vectors (broken link caught · orphan caught · whitelist honored · URL skip)
Live run must exit 0.

Stdlib only, deterministic, no network.
"""
import os
import re
import sys
import pathlib
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Files to check for broken links (G6 spec)
LINK_CHECK_FILES = [
    ROOT / "START_HERE.md",
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "PROTOCOL.md",
    ROOT / "docs" / "INDEX.md",
]
# plus docs/*.md will be added dynamically

# Whitelist for INDEX coverage — files that may exist in docs/ but not listed in INDEX.md
# INDEX.md itself is whitelisted to avoid self-reference requirement
WHITELIST = {
    "docs/INDEX.md",  # the index itself
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

def extract_links(text):
    """Extract raw link targets from markdown."""
    return LINK_RE.findall(text)

def is_external(url):
    u = url.strip()
    if not u:
        return True  # empty treated as external/skip to avoid false positive
    # Skip http(s), //, mailto, data:, etc.
    if u.startswith("http://") or u.startswith("https://") or u.startswith("//"):
        return True
    if "://" in u:  # any scheme
        return True
    if u.startswith("mailto:") or u.startswith("data:"):
        return True
    # Anchor-only link like #section
    if u.startswith("#"):
        return True
    return False

def resolve_link(source_path: pathlib.Path, raw_target: str):
    """
    Resolve relative markdown link target to absolute Path, or None if skipped.
    Tolerates anchors: strips #anchor part.
    Returns None if external or empty after anchor strip.
    """
    raw = raw_target.strip()
    if not raw:
        return None
    if is_external(raw):
        return None
    # Strip anchor
    # Split on # first, keep path part
    path_part = raw.split("#", 1)[0].strip()
    if not path_part:
        return None  # anchor-only after strip
    # Remove optional title after space: [text](path "title") — markdown allows title
    # The regex may capture title too; split on whitespace and take first token if it looks like path?
    # Simplistic: if contains space, take first token that doesn't start with " or '
    # Actually markdown link can be: (path "title") — our regex captures inside parens including title.
    # We should handle: path may be followed by space + quoted title.
    # So extract first whitespace-separated token, strip quotes.
    # Example: 'docs/foo.md "title"' -> 'docs/foo.md'
    # Example: "docs/foo.md" -> docs/foo.md
    # We'll split respecting quotes roughly: take first token, strip surrounding quotes.
    # Better: use regex to split.
    m = re.match(r"""^\s*<?([^ \t"'<>]+)>?(?:\s+.*)?$""", path_part)
    if m:
        path_part = m.group(1)
    # Strip surrounding < > and quotes
    path_part = path_part.strip().strip("<>").strip().strip('"').strip("'")
    if not path_part:
        return None
    if is_external(path_part):
        return None
    # Now resolve relative to source_path's directory
    # source_path is absolute Path to file containing link
    source_dir = source_path.parent
    # If path_part is absolute (starts with /), treat as repo-root relative? But spec says relative markdown links, so skip absolute?
    # For safety, if starts with /, resolve from ROOT
    if path_part.startswith("/"):
        # Absolute from repo root? Skip? We'll treat as ROOT / stripped leading /
        resolved = (ROOT / path_part.lstrip("/")).resolve()
    else:
        resolved = (source_dir / path_part).resolve()
    # Ensure resolved is inside ROOT or at least exists? We'll check existence later, but return resolved
    # For security, we still return even if outside ROOT, but check existence will fail if outside and not exist — that's okay, but we should not flag outside ROOT as broken if it doesn't exist? Actually we should flag if it doesn't exist.
    # However, to avoid false positives for paths outside repo (like /tmp), we will only check if resolved is inside ROOT or exists.
    # We'll return resolved regardless; caller will check existence.
    return resolved

def check_broken_links(files):
    findings = []
    for f in files:
        if not f.exists():
            findings.append(f"{f.relative_to(ROOT)} missing (expected file for link check)")
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            findings.append(f"{f.relative_to(ROOT)} unreadable: {e}")
            continue
        links = extract_links(text)
        for raw in links:
            # Skip external already handled in resolve, but also skip here quickly
            if is_external(raw):
                continue
            resolved = resolve_link(f, raw)
            if resolved is None:
                continue
            # Check existence
            # Only flag if resolved does not exist AND resolved is inside ROOT or is a relative-looking path
            # We consider any resolved path that does not exist as broken, unless it's outside ROOT and we want to ignore?
            # For G6, we only care about repo-internal markdown links. So if resolved is outside ROOT, we skip (tolerate)
            try:
                # Check if resolved is inside ROOT
                resolved.relative_to(ROOT)
                inside = True
            except ValueError:
                # Outside ROOT — skip unless it exists? We'll skip to avoid false positives
                inside = False
                # If outside ROOT and doesn't exist, we skip (not part of repo)
                # If outside ROOT but exists (unlikely), we also skip
                continue
            if not resolved.exists():
                # Report relative to ROOT for readability
                rel_source = f.relative_to(ROOT)
                # Show raw target and resolved relative
                try:
                    rel_target = resolved.relative_to(ROOT)
                except ValueError:
                    rel_target = resolved
                findings.append(f"{rel_source}: broken link '{raw}' -> '{rel_target}' not found")
    return findings

def check_index_coverage():
    findings = []
    index_path = ROOT / "docs" / "INDEX.md"
    if not index_path.exists():
        findings.append("docs/INDEX.md missing — cannot check coverage")
        return findings
    try:
        index_text = index_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        findings.append(f"docs/INDEX.md unreadable: {e}")
        return findings

    # Collect all docs/*.md files on disk
    docs_dir = ROOT / "docs"
    docs_files = sorted([p for p in docs_dir.glob("*.md")])
    docs_rel = [p.relative_to(ROOT).as_posix() for p in docs_files]

    # (iii) INDEX.md lists only existing files — check every markdown link in INDEX.md that looks like docs/*.md or *.md
    links_in_index = extract_links(index_text)
    for raw in links_in_index:
        if is_external(raw):
            continue
        resolved = resolve_link(index_path, raw)
        if resolved is None:
            continue
        # Only care about .md files
        if resolved.suffix != ".md":
            continue
        # If resolved is inside ROOT/docs or ROOT, check existence
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            continue
        if not resolved.exists():
            findings.append(f"docs/INDEX.md: lists non-existing file '{raw}' -> '{resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else resolved}'")

    # (ii) every docs/*.md is listed in INDEX.md or whitelist
    # For listing check, we consider a docs file listed if its basename or relative path appears in INDEX.md text
    # Simple heuristic: if "FILENAME.md" appears in INDEX.md, it's listed
    for rel in docs_rel:
        basename = pathlib.Path(rel).name
        # If whitelisted, skip
        if rel in WHITELIST:
            continue
        # Check if basename or rel appears in INDEX text
        # We look for exact basename substring
        if basename not in index_text and rel not in index_text:
            findings.append(f"orphan docs file not listed in INDEX.md nor whitelisted: {rel}")

    return findings

def run_checks():
    # Build file list for link checks
    files = []
    for p in LINK_CHECK_FILES:
        if p.exists():
            files.append(p)
    # Add docs/*.md
    docs_dir = ROOT / "docs"
    if docs_dir.exists():
        for p in sorted(docs_dir.glob("*.md")):
            if p not in files:
                files.append(p)

    findings = []
    findings.extend(check_broken_links(files))
    findings.extend(check_index_coverage())
    return findings

# ---------------- self-test vectors ----------------

def self_test():
    """
    ≥4 vectors:
    - broken link caught
    - orphan caught
    - whitelist honored
    - URL skip
    """
    vectors = []

    # Helper to run checks in temp root
    def run_in_temp(temp_root: pathlib.Path, extra_whitelist=None):
        # Temporarily override ROOT and WHITELIST
        global ROOT, WHITELIST
        old_root = ROOT
        old_whitelist = WHITELIST.copy()
        try:
            ROOT = temp_root
            if extra_whitelist:
                WHITELIST = old_whitelist | set(extra_whitelist)
            # Build file list manually for temp
            files = []
            for rel in ["START_HERE.md", "README.md", "AGENTS.md", "PROTOCOL.md", "docs/INDEX.md"]:
                p = temp_root / rel
                if p.exists():
                    files.append(p)
            docs_dir = temp_root / "docs"
            if docs_dir.exists():
                for p in sorted(docs_dir.glob("*.md")):
                    if p not in files:
                        files.append(p)
            findings = []
            findings.extend(check_broken_links(files))
            findings.extend(check_index_coverage())
            return findings
        finally:
            ROOT = old_root
            WHITELIST = old_whitelist

    # Vector 1: broken link caught
    def vector_broken_link():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "docs").mkdir(parents=True)
            # Minimal INDEX that lists itself and one file to avoid orphan noise
            (tr / "docs" / "INDEX.md").write_text("# INDEX\n- [EXISTS.md](EXISTS.md)\n", encoding="utf-8")
            (tr / "docs" / "EXISTS.md").write_text("# exists\n", encoding="utf-8")
            (tr / "START_HERE.md").write_text("[broken](nonexistent.md)\n", encoding="utf-8")
            (tr / "README.md").write_text("", encoding="utf-8")
            (tr / "AGENTS.md").write_text("", encoding="utf-8")
            (tr / "PROTOCOL.md").write_text("", encoding="utf-8")
            findings = run_in_temp(tr, extra_whitelist={"docs/INDEX.md"})
            # Should have broken link finding
            ok = any("broken link" in f and "nonexistent.md" in f for f in findings)
            return ok, findings

    # Vector 2: orphan caught
    def vector_orphan():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "docs").mkdir(parents=True)
            (tr / "docs" / "INDEX.md").write_text("# INDEX\n- [LISTED.md](LISTED.md)\n", encoding="utf-8")
            (tr / "docs" / "LISTED.md").write_text("# listed\n", encoding="utf-8")
            (tr / "docs" / "ORPHAN.md").write_text("# orphan\n", encoding="utf-8")
            (tr / "START_HERE.md").write_text("", encoding="utf-8")
            (tr / "README.md").write_text("", encoding="utf-8")
            (tr / "AGENTS.md").write_text("", encoding="utf-8")
            (tr / "PROTOCOL.md").write_text("", encoding="utf-8")
            findings = run_in_temp(tr, extra_whitelist={"docs/INDEX.md"})
            ok = any("orphan" in f and "ORPHAN.md" in f for f in findings)
            return ok, findings

    # Vector 3: whitelist honored
    def vector_whitelist():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "docs").mkdir(parents=True)
            (tr / "docs" / "INDEX.md").write_text("# INDEX\n- [LISTED.md](LISTED.md)\n", encoding="utf-8")
            (tr / "docs" / "LISTED.md").write_text("# listed\n", encoding="utf-8")
            (tr / "docs" / "WHITELISTED.md").write_text("# whitelisted\n", encoding="utf-8")
            (tr / "START_HERE.md").write_text("", encoding="utf-8")
            (tr / "README.md").write_text("", encoding="utf-8")
            (tr / "AGENTS.md").write_text("", encoding="utf-8")
            (tr / "PROTOCOL.md").write_text("", encoding="utf-8")
            findings = run_in_temp(tr, extra_whitelist={"docs/INDEX.md", "docs/WHITELISTED.md"})
            # Should NOT have orphan finding for WHITELISTED.md
            has_whitelisted_orphan = any("WHITELISTED.md" in f and "orphan" in f for f in findings)
            ok = not has_whitelisted_orphan
            return ok, findings

    # Vector 4: URL skip
    def vector_url_skip():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "docs").mkdir(parents=True)
            (tr / "docs" / "INDEX.md").write_text("# INDEX\n- [EXISTS.md](EXISTS.md)\n", encoding="utf-8")
            (tr / "docs" / "EXISTS.md").write_text("# exists\n", encoding="utf-8")
            (tr / "START_HERE.md").write_text("[url](https://example.com)\n[url2](http://example.com)\n", encoding="utf-8")
            (tr / "README.md").write_text("", encoding="utf-8")
            (tr / "AGENTS.md").write_text("", encoding="utf-8")
            (tr / "PROTOCOL.md").write_text("", encoding="utf-8")
            findings = run_in_temp(tr, extra_whitelist={"docs/INDEX.md"})
            # Should have NO broken link findings for https
            has_broken = any("broken link" in f for f in findings)
            ok = not has_broken
            return ok, findings

    # Vector 5 (extra): INDEX lists only existing files
    def vector_index_nonexist():
        with tempfile.TemporaryDirectory() as td:
            tr = pathlib.Path(td)
            (tr / "docs").mkdir(parents=True)
            (tr / "docs" / "INDEX.md").write_text("# INDEX\n- [MISSING.md](MISSING.md)\n", encoding="utf-8")
            (tr / "START_HERE.md").write_text("", encoding="utf-8")
            (tr / "README.md").write_text("", encoding="utf-8")
            (tr / "AGENTS.md").write_text("", encoding="utf-8")
            (tr / "PROTOCOL.md").write_text("", encoding="utf-8")
            findings = run_in_temp(tr, extra_whitelist={"docs/INDEX.md"})
            ok = any("lists non-existing" in f and "MISSING.md" in f for f in findings)
            return ok, findings

    tests = [
        ("broken link caught", vector_broken_link),
        ("orphan caught", vector_orphan),
        ("whitelist honored", vector_whitelist),
        ("URL skip", vector_url_skip),
        ("INDEX lists only existing", vector_index_nonexist),
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

    print(f"\ndocs_index_check self-test: {passed} passed, {failed} failed — {len(tests)} vectors")
    return failed == 0

def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    findings = run_checks()
    if findings:
        print(f"docs_index_check: {len(findings)} finding(s)")
        for f in findings:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("docs_index_check: 0 finding(s) — all links resolve, INDEX coverage ok, whitelist honored")
        sys.exit(0)

if __name__ == "__main__":
    main()
