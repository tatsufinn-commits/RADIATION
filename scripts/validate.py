#!/usr/bin/env python3
"""RADIATION structural validator — P-01 Machine Enforcement Layer.
Checks FORM and RESOLVABILITY only. Never judges truth. Never modifies files.
Exit 0 = no FAIL-class findings. Exit 1 = at least one FAIL.
Stdlib only. No network (check 13 skipped offline by design).
"""
import hashlib, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []
def rec(check, sev, ok, msg):
    RESULTS.append({"check": check, "severity": sev, "ok": ok, "msg": msg})
# NOTE: _local_backup/ is the Commander-local scratch folder created by
# APPLY.sh (it holds the re-homed vehicles). It is git-ignored and is NOT
# part of the repository, so every walk skips it -- including md_files(),
# check 3 and check 12. Scanning it would fail CI on files that never ship.
def md_files():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {".git", ".github", "node_modules", "_local_backup"}]
        for f in fn:
            if f.endswith(".md") or f == ".readme":
                out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)
def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8", errors="replace") as fh:
        return fh.read()
def archive_exempt():
    """Exempt-path column of docs/ARCHIVE_NOTES.md table rows ONLY (closure fix:
    the old scraper read every backtick incl. the title line, so the file
    exempted ITSELF and phantom rows went unverified). ARCHIVE_NOTES.md itself
    is never exempt. Check 1b asserts every listed path exists."""
    ex = set()
    p = os.path.join(ROOT, "docs/ARCHIVE_NOTES.md")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines():
            if ln.strip().startswith("|"):
                m = re.match(r"\|\s*`([^`]+)`\s*\|", ln.strip())
                if m: ex.add(m.group(1).rstrip("/"))
    ex.discard("docs/ARCHIVE_NOTES.md")
    def is_ex(path):
        return any(path == e or path.startswith(e + "/") for e in ex)
    is_ex.paths = ex
    return is_ex
IS_EX = archive_exempt()
def pend_narrow(path):
    """Files under proposal homes are exempt from checks 8/9 ONLY while listed
    (or their directory is listed) in docs/PENDING_RATIFICATIONS.md."""
    if not ("/proposals/" in path or path.startswith("scaffolding/improved/")): return False
    pr = os.path.join(ROOT, "docs/PENDING_RATIFICATIONS.md")
    if not os.path.exists(pr): return False
    t = open(pr, encoding="utf-8").read()
    return path in t or os.path.dirname(path) + "/" in t

# ---- check 1: internal path resolution -------------------------------------
def c1():
    bad = []
    pat = re.compile(r"`([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-#]+)+\.(?:md|py|json|yml|txt))`")
    for f in md_files():
        if IS_EX(f): continue
        for m in pat.finditer(read(f)):
            p = m.group(1)
            if "*" in p or p.startswith(("http", "/", "~")): continue
            if not os.path.exists(os.path.join(ROOT, p)):
                bad.append(f"{f} -> {p}")
    rec(1, "FAIL", not bad, "internal path resolution" + ("" if not bad else ": " + "; ".join(bad[:6])))
    ghosts = [e for e in sorted(IS_EX.paths) if not os.path.exists(os.path.join(ROOT, e))]
    rec(1.5, "FAIL", not ghosts, "no phantom exemptions (every ARCHIVE_NOTES path exists)" + ("" if not ghosts else ": " + "; ".join(ghosts[:6])))
# ---- check 2: required files present & non-empty ---------------------------
REQUIRED = ["README.md","docs/.readme","BOOT_SEQUENCE.md","docs/AI_RULES.md",
 "docs/SYSTEM_STATE.md","docs/MODES.md","docs/CUE_SYSTEM.md","CHANGELOG.md",
 "docs/PATCH_LEDGER.md","Brain/frontal_lobe/task_ledger.md",
 "07-inspect/DEBT_REGISTER.md","docs/DECAY_REGISTER.md","01-research/REFERENCES.md",
 "06-triangulate/CONFLICT_REGISTER.md","09-nota/CORE_INDEX.md","Brain/BRAIN_INDEX.md",
 "Brain/external_sources/INDEX.md","cue/CUE_INDEX.md"]
def c2():
    bad = [p for p in REQUIRED if not os.path.exists(os.path.join(ROOT,p)) or os.path.getsize(os.path.join(ROOT,p)) == 0]
    for d in sorted(os.listdir(os.path.join(ROOT,"Brain"))):
        dd = os.path.join(ROOT,"Brain",d)
        if os.path.isdir(dd) and not any(os.path.exists(os.path.join(dd,n)) for n in ("README.md","INDEX.md","BRAIN_INDEX.md")):
            if d not in ("long_term","short_term","subsidiary","cerebellum"):  # region docs live in BRAIN_INDEX
                bad.append(f"Brain/{d}/ lacks README/INDEX")
    rec(2, "FAIL", not bad, "required files" + ("" if not bad else ": missing " + "; ".join(bad[:6])))
# ---- check 2.5: Brain/courses/ — records only, no vehicles, no identifiers ----
# P-10 §3.3. Cures the 4a98e59 exposure class: FAILs the exact shapes published
# on 2026-09-13 (binaries, a credential URL, room/section strings).
# NOTE (v2, after self-test): an earlier revision flagged the bare WORD
# "Instructor" and failed the course records that state the exclusion. The rule
# targets VALUES, never vocabulary — a name-bearing label is required to match.
CV_DENY = ["S308","S300","S303","S301","NW408","SW200","SW304","E01","A54","C5",
           "calendarFeed","@mapua.edu"]
CV_PATTERNS = [
    (r"https?://", "URL/credential"),
    (r"\b(?:Instructor|Professors?|Prof\.)\s*[:\-\u2013]?\s*(?:is\s+|was\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", "instructor name"),
    (r"\b(?:Consultation|Email|Contact)\s*(?:Schedule|Hours|Address)?\s*[:\-\u2013]\s*[A-Za-z0-9._%+-]+@", "contact detail"),
    # v3: rooms are S3xx / NW4xx / SW2xx — but S001-S003 are SESSION ids and
    # legitimately appear in this region. The pattern excludes S0xx so the check
    # cannot fail on a session citation.
    (r"\bS[1-9]\d{2}\b", "room code"),
    (r"\b(?:NW|SW|SE|NE)\d{3}\b", "room code"),
    (r"\b(?:E|W)[1-9]\d{2}\b", "room code"),
    (r"\b(?:Section|Sec\.)\s+[A-Z]{1,2}\d{1,3}\b", "section code"),
]
def c25():
    bad = []
    root = os.path.join(ROOT, "Brain/courses")
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            for f in sorted(fn):
                p = os.path.relpath(os.path.join(dp, f), ROOT)
                if not f.endswith(".md"):
                    bad.append(f"{p} (non-markdown vehicle)"); continue
                t = read(p)
                for w in CV_DENY:
                    if w in t: bad.append(f"{p} (published token: {w})")
                for pat, what in CV_PATTERNS:
                    m = re.search(pat, t)
                    if m: bad.append(f"{p} ({what}: {m.group(0)[:24]})")
    rec(2.5, "FAIL", not bad, "Brain/courses/ records-only + no identifiers" + ("" if not bad else ": " + "; ".join(bad[:6])))

# ---- check 3: forbidden transport artifacts (II.8.2) -----------------------
def c3():
    bad = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {".git", "_local_backup"}]
        for d in dn:
            if d in ("append_blocks","append-blocks"): bad.append(os.path.relpath(os.path.join(dp,d),ROOT)+"/")
        for f in fn:
            if "_REPLACEMENT" in f or "_STAGED" in f or "_DIFF" in f or f == "PATCH_NOTES.md":
                bad.append(os.path.relpath(os.path.join(dp,f),ROOT))
    rec(3, "FAIL", not bad, "no transport artifacts or carriers in tree (II.8.2 + closure rule: *_STAGED/*_DIFF/PATCH_NOTES)" + ("" if not bad else ": " + "; ".join(bad)))
# ---- check 3b: scaffolding/core/ closed set — every file named in its INDEX ----
def c3b():
    idx = read("scaffolding/core/INDEX.md")
    files = [f for f in os.listdir(os.path.join(ROOT, "scaffolding/core")) if f.endswith(".md") and f != "INDEX.md"]
    bad = [f for f in files if f"`{f}`" not in idx]
    rec(3.5, "FAIL", not bad, f"core/ closed set ({len(files)} files vs INDEX)" + ("" if not bad else ": unlisted " + "; ".join(bad)))
# ---- check 4: register table schema ----------------------------------------
SCHEMA_FILES = ["Brain/frontal_lobe/task_ledger.md","docs/PATCH_LEDGER.md",
 "cue/commander-lexicon.md","cue/inference-log.md","Brain/frontal_lobe/learned_cues.md",
 "Brain/frontal_lobe/learned_skills.md","Brain/frontal_lobe/opinions.md",
 "07-inspect/DEBT_REGISTER.md","docs/DECAY_REGISTER.md","01-research/REFERENCES.md"]
def c4():
    bad = []
    for f in SCHEMA_FILES:
        if not os.path.exists(os.path.join(ROOT,f)): continue
        lines = read(f).splitlines(); hdr = None
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s.startswith("|"):
                if hdr is None or (i>0 and not lines[i-1].strip().startswith("|")):
                    hdr = s.count("|")
                elif set(s.replace("|","").replace("-","").replace(":","").strip()) == set():
                    continue
                elif s.count("|") != hdr:
                    bad.append(f"{f}:{i+1} ({s.count('|')} pipes vs header {hdr})")
            else:
                hdr = None
    rec(4, "FAIL", not bad, "register table schema" + ("" if not bad else ": " + "; ".join(bad[:6])))
# ---- check 5: placeholder above live rows -----------------------------------
def c5():
    bad = []
    for f in SCHEMA_FILES + ["Brain/external_sources/law.md","Brain/external_sources/books.md"]:
        if not os.path.exists(os.path.join(ROOT,f)): continue
        t = read(f)
        m = re.search(r"\*\(empty[^)]*\)\*", t)
        if m and re.search(r"^\|[^-\n]+\|", t[m.end():], re.M):
            bad.append(f)
    rec(5, "WARN", not bad, "stale empty-placeholders" + ("" if not bad else ": " + "; ".join(bad)))
# ---- check 6: placeholder identifiers in ledgers ----------------------------
def c6():
    bad = []
    for f in ("Brain/frontal_lobe/task_ledger.md","docs/PATCH_LEDGER.md"):
        for i, ln in enumerate(read(f).splitlines()):
            if re.search(r"\.\.\._|_\.\.\.|…_|_…|\bTBD\b|XXXX", ln):
                bad.append(f"{f}:{i+1}")
    rec(6, "FAIL", not bad, "no placeholder identifiers in ledgers" + ("" if not bad else ": " + "; ".join(bad[:8])))
# ---- check 7: version coherence ---------------------------------------------
def c7():
    def ver(pat, text):
        m = re.search(pat, text); return m.group(1) if m else None
    ss = ver(r"RADIATION (v\d+\.\d+\.\d+)", read("docs/SYSTEM_STATE.md"))
    cl = ver(r"##\s+(v\d+\.\d+\.\d+)", read("CHANGELOG.md"))
    rm = ver(r"\*\*Version:\*\*\s*(v\d+\.\d+\.\d+)", read("README.md"))
    ok = ss == cl == rm and ss is not None
    rec(7, "FAIL", ok, f"version coherence: SYSTEM_STATE={ss} CHANGELOG={cl} README={rm}")
# ---- check 8: derived-count drift (modes) -----------------------------------
def c8():
    canon = len(re.findall(r"^## .*@\w+ —", read("docs/MODES.md"), re.M))
    words = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9}
    bad = []
    for f in md_files():
        if IS_EX(f) or pend_narrow(f) or f == "docs/MODES.md": continue
        for m in re.finditer(r"\b(one|two|three|four|five|six|seven|eight|nine|\d)\s+(?:commander-declared\s+)?modes\b(?!\s+(?:tie|fit))", read(f), re.I):
            n = words.get(m.group(1).lower(), None) or (int(m.group(1)) if m.group(1).isdigit() else None)
            if n is not None and n != canon:
                bad.append(f"{f}: '{m.group(0)}' vs canonical {canon}")
    rec(8, "FAIL", not bad, f"derived-count drift (canonical modes={canon})" + ("" if not bad else ": " + "; ".join(bad[:6])))
# ---- check 9: retired-phrase detector (WARN) ---------------------------------
RETIRED = ["APPEND BLOCK", "append block", "_REPLACEMENT", "Eight Skills"]
def c9():
    bad = []
    for f in md_files():
        if IS_EX(f) or pend_narrow(f): continue
        for i, ln in enumerate(read(f).splitlines()):
            if "~~" in ln: continue
            for ph in RETIRED:
                if ph in ln: bad.append(f"{f}:{i+1} '{ph}'")
    rec(9, "WARN", not bad, "retired phrases" + ("" if not bad else " (ratification decisions pending): " + "; ".join(bad[:8])))
# ---- check 10: register liveness ---------------------------------------------
def c10():
    bad = []
    audits = [f for f in os.listdir(os.path.join(ROOT,"Brain/long_term/audits")) if f.endswith(".md")] if os.path.isdir(os.path.join(ROOT,"Brain/long_term/audits")) else []
    debt_rows = len([l for l in read("07-inspect/DEBT_REGISTER.md").splitlines() if l.strip().startswith("|") and "---" not in l]) - 1
    if audits and debt_rows < 1: bad.append(f"{len(audits)} audit(s) but DEBT_REGISTER has no rows")
    decay_rows = len([l for l in read("docs/DECAY_REGISTER.md").splitlines() if l.strip().startswith("|") and "---" not in l]) - 1
    if decay_rows < 1: bad.append("DECAY_REGISTER empty (PD 1096 stable-domain window expired)")
    rec(10, "FAIL", not bad, "register liveness" + ("" if not bad else ": " + "; ".join(bad)))
# ---- check 11: duplicate detection --------------------------------------------
def c11():
    hashes, bad, warn = {}, [], []
    files = md_files()
    sets = {}
    for f in files:
        t = read(f)
        h = hashlib.md5(t.encode()).hexdigest()
        if h in hashes: bad.append(f"{f} == {hashes[h]}")
        else: hashes[h] = f
        sets[f] = set(l for l in t.splitlines() if l.strip())
    fl = list(sets)
    for i in range(len(fl)):
        for j in range(i+1, len(fl)):
            a, b = sets[fl[i]], sets[fl[j]]
            if not a or not b: continue
            jac = len(a & b) / len(a | b)
            if 0.9 <= jac < 1.0: warn.append(f"{fl[i]} ~ {fl[j]} ({jac:.2f})")
    rec(11, "FAIL", not bad, "duplicate files" + ("" if not bad else ": " + "; ".join(bad[:4])))
    rec(11.5, "WARN", not warn, "near-duplicates" + ("" if not warn else ": " + "; ".join(warn[:4])))
# ---- check 12: filename hygiene -----------------------------------------------
def c12():
    bad = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {".git", "_local_backup"}]
        for f in fn:
            if any(ord(ch) > 127 for ch in f) or f.startswith("#") or "ΓÇ" in f or "╬" in f:
                bad.append(os.path.relpath(os.path.join(dp,f),ROOT))
    rec(12, "FAIL", not bad, "filename hygiene" + ("" if not bad else ": " + "; ".join(bad[:6])))
# ---- check 13: external URLs (offline skip) ------------------------------------
def c13():
    rec(13, "WARN", True, "external URL check SKIPPED (offline by design; run manually if needed)")
# ---- check 14: session-local paths in artifacts --------------------------------
def c14():
    bad = []
    for f in md_files():
        if IS_EX(f) or f.startswith("scripts/"): continue
        for i, ln in enumerate(read(f).splitlines()):
            if re.search(r"audit_fetch/|(?<![`/\w])/tmp/|(?<![`\w])/home/user/", ln):
                bad.append(f"{f}:{i+1}")
    rec(14, "FAIL", not bad, "no session-local paths" + ("" if not bad else ": " + "; ".join(bad[:8])))

# ---- check 15: boot-byte budget (P-09; WARN until EVAL-FIRST ratified into AI_RULES) ----
def c15():
    def sz(rel):
        fp = os.path.join(ROOT, rel)
        return os.path.getsize(fp) if os.path.exists(fp) else 0
    # boot-effective task_ledger: BOOT_SEQUENCE Tier 0 reads only the LAST 3 entries
    tl_lines = read("Brain/frontal_lobe/task_ledger.md").splitlines()
    rows = [l for l in tl_lines if l.strip().startswith("|") and "---" not in l.replace("|","")]
    non_table = [l for l in tl_lines if not l.strip().startswith("|")]
    eff_lines = non_table + rows[:1] + rows[-3:] if len(rows) > 4 else tl_lines
    tl_eff = len(("\n".join(eff_lines)).encode("utf-8"))
    t01 = sz("docs/.readme") + sz("docs/SYSTEM_STATE.md") + sz("docs/AI_RULES.md") + tl_eff
    t2  = sum(sz(x) for x in ("docs/MODES.md","docs/CUE_SYSTEM.md",
          "subskills/passive/compass.md","subskills/passive/curator.md",
          "subskills/passive/sentinel.md","subskills/passive/surgeon.md"))
    t02 = t01 + t2
    ratified = "EVAL-FIRST" in read("docs/AI_RULES.md")
    wpath = os.path.join(ROOT, "docs/BOOT_BUDGET_WAIVERS.md")
    waived = os.path.exists(wpath) and "ACTIVE" in open(wpath, encoding="utf-8").read()
    ok = t01 <= 40960 and t02 <= 81920
    sev = "FAIL" if (ratified and not waived) else "WARN"
    rec(15, sev, ok,
        f"boot-byte budget: Tier0+1={t01} B ({t01/1024:.1f} KB / cap 40) · "
        f"Tier0-2={t02} B ({t02/1024:.1f} KB / cap 80) · ~{t02//4} tokens · "
        f"task_ledger boot-effective (last 3 rows)={tl_eff} B · "
        f"enforcement={'FAIL-class (EVAL-FIRST ratified)' if ratified else 'WARN-class (P-09 pending ratification)'}"
        + (" · WAIVER ACTIVE" if waived else ""))
# ---- check 16: canon-vs-content meta-budget ratio (P-09; reporting) -------------
def c16():
    rows = [l for l in read("docs/PATCH_LEDGER.md").splitlines() if l.strip().startswith("|")]
    canon = len([l for l in rows if "\U0001F7E0" in l])
    tdir = os.path.join(ROOT, "Brain/temporal_lobe")
    sessions = len([d for d in os.listdir(tdir) if re.match(r"S\d{3}_", d)]) if os.path.isdir(tdir) else 0
    ok = canon * 3 <= sessions
    rec(16, "WARN", ok,
        f"meta-budget: {canon} canon(orange) patches vs {sessions} content sessions "
        f"(law allows 1 per 3 => {'WITHIN' if ok else 'OVER'} budget by {canon*3 - sessions if not ok else 0} session-equivalents)")


# ---- check 17: knowledge-registry integrity (P-03) ------------------------------
def c17():
    bad = []
    regtxt = read("docs/KNOWLEDGE_REGISTRY.md") if os.path.exists(os.path.join(ROOT,"docs/KNOWLEDGE_REGISTRY.md")) else ""
    kpat = re.compile(r"\bK-(?:LAW|STD|CUR|BK|MOD|MTH|REF|EXT)(?:-[A-Z0-9]+)*-\d{3}\b")
    defined = []
    for ln in regtxt.splitlines():
        if ln.startswith("## "):
            m = kpat.search(ln)
            if m: defined.append(m.group(0))
    dupes = {k for k in defined if defined.count(k) > 1}
    if dupes: bad.append("duplicate K-IDs: " + ", ".join(sorted(dupes)))
    dset = set(defined)
    for f in md_files():
        if IS_EX(f): continue
        for i, ln in enumerate(read(f).splitlines()):
            for m in kpat.finditer(ln):
                if m.group(0) not in dset:
                    bad.append(f"{f}:{i+1} dangling ref {m.group(0)}")
    paths = []
    for b in re.split(r"\n## (?=K-)", regtxt)[1:]:
        kid = b.split(" ")[0].strip()
        pm = re.search(r"Canonical path:\s*`([^`]+)`", b)
        if pm:
            paths.append(pm.group(1))
            if not os.path.exists(os.path.join(ROOT, pm.group(1))):
                bad.append(f"{kid} canonical path missing: {pm.group(1)}")
        st = re.search(r"Status:\s*(CURRENT|VERIFIED)", b)
        lv = re.search(r"Last verified:\s*\d{4}-\d{2}-\d{2}", b)
        if st and not lv: bad.append(f"{kid} status {st.group(1)} but Last verified blank")
        sb = re.search(r"Supersedes/by:\s*\S+\s*/\s*(K-\S+)", b)
        if sb and sb.group(1).rstrip(",") not in dset: bad.append(f"{kid} superseded_by unresolvable: {sb.group(1)}")
    dp = {x for x in paths if paths.count(x) > 1}
    if dp: bad.append("two rows share a canonical path: " + ", ".join(sorted(dp)))
    rec(17, "FAIL", not bad, f"knowledge registry ({len(dset)} K-IDs)" + ("" if not bad else ": " + "; ".join(bad[:6])))

# ---- check 18: canonical-module depth integrity (P-06) --------------------------
def c18():
    bad, warn = [], []
    mods = []
    for f in md_files():
        t = read(f)
        m = re.search(r"depth_level:\s*(\d)", t)
        if m: mods.append((f, int(m.group(1)), t))
    for f, lvl, t in mods:
        if not re.search(r"yield_rank:\s*(?!\|)[0-9]", t): warn.append(f"{f}: yield_rank empty/non-numeric")
        if not re.search(r"K-(?:MOD|LAW|STD|CUR|BK|REF|MTH|EXT)\S*", t): bad.append(f"{f}: no K-ID")
        if "LIMITS" not in t: bad.append(f"{f}: L{lvl} missing LIMITS line")
        if lvl >= 2:
            for h in ("WHY THIS MATTERS","CORE CONTENT","AUTHORITY TABLE","NUMBERS TO KNOW","WORKED EXAMPLE","EXAM TRAPS","LINEAGE"):
                if h not in t: bad.append(f"{f}: L{lvl} missing section {h}")
        traps = len(re.findall(r"\*\*TRAP \d", t))
        worked = len(re.findall(r"### Worked Example", t))
        gloss = len(re.findall(r"- \*\*[A-Za-z]", t.split("GLOSSARY",1)[1])) if "GLOSSARY" in t else 0
        if lvl >= 3 and (traps < 4 or gloss < 10 or worked < 1):
            bad.append(f"{f}: L{lvl} needs >=4 traps/>=10 glossary/>=1 worked (has {traps}/{gloss}/{worked})")
        if lvl >= 4 and (traps < 8 or worked < 2): bad.append(f"{f}: L{lvl} needs >=8 traps & >=2 worked (has {traps}/{worked})")
        if lvl == 5:
            drill = len(re.findall(r"^\s*Q\d+", t, re.M))
            if "DRILL" not in t or drill < 10: bad.append(f"{f}: L5 claims but drill absent/short ({drill} items)")
            if "CASE STUD" not in t.upper(): bad.append(f"{f}: L5 without case studies")
    mdir = os.path.join(ROOT, "Brain/long_term/modules")
    if os.path.isdir(mdir):
        files = [x for x in os.listdir(mdir) if x.endswith(".md") and x != "MODULES_INDEX.md"]
        idx = os.path.join(mdir, "MODULES_INDEX.md")
        rows = len([l for l in open(idx, encoding="utf-8").read().splitlines() if l.strip().startswith("|") and "---" not in l.replace("|","")]) - 1 if os.path.exists(idx) else -1
        if rows != len(files): bad.append(f"modules/: {len(files)} module file(s) vs {rows} index row(s)")
    rec(18, "FAIL", not bad, f"module depth integrity ({len(mods)} module(s))" + ("" if not bad else ": " + "; ".join(bad[:5])))
    if warn: rec(18.5, "WARN", False, "module yield_rank: " + "; ".join(warn[:4]))

# ---- check 20: term plan integrity (P-10; and the register's own privacy rule) ----
def c20():
    bad = []
    reg = os.path.join(ROOT, "Brain/short_term/plan/TERM1_DEADLINES.json")
    if os.path.exists(reg):
        try:
            d = json.load(open(reg, encoding="utf-8"))
        except Exception as e:
            bad.append(f"TERM1_DEADLINES.json unparseable: {e}"); d = None
        if isinstance(d, dict):
            if d.get("schema") != "rad.term_deadlines/v1":
                bad.append("schema key missing/wrong")
            codes = {c.get("code") for c in d.get("courses", [])}
            kids  = {c.get("k_id") for c in d.get("courses", [])}
            weeks = (d.get("term") or {}).get("weeks") or 11
            for it in d.get("items", []):
                if it.get("course") not in codes: bad.append(f"unknown course {it.get('course')}")
                if it.get("k_id") not in kids:    bad.append(f"unknown k_id {it.get('k_id')}")
                w = it.get("week")
                if w is not None and not (isinstance(w, int) and 1 <= w <= weeks):
                    bad.append(f"week out of range {it.get('course')} W{w}")
            blob = json.dumps(d)
            if "http" in blob: bad.append("URL in term register")
            for pat, what in CV_PATTERNS:
                if re.search(pat, blob): bad.append(f"{what} in term register")
            for tok in CV_DENY:
                if tok in blob: bad.append(f"published token in term register: {tok}")
        # the register's k_ids must exist in the knowledge registry
        regtxt = read("docs/KNOWLEDGE_REGISTRY.md") if os.path.exists(os.path.join(ROOT,"docs/KNOWLEDGE_REGISTRY.md")) else ""
        if isinstance(d, dict):
            for c in d.get("courses", []):
                if c.get("k_id") and f"## {c['k_id']}" not in regtxt:
                    bad.append(f"course K-ID not registered: {c.get('k_id')}")
    # any generated window must stay local + short-horizoned
    pdir = os.path.join(ROOT, "Brain/short_term/plan")
    if os.path.isdir(pdir):
        for f in os.listdir(pdir):
            if f.endswith(".local.md"):
                t = read(os.path.relpath(os.path.join(pdir, f), ROOT))
                if "http" in t: bad.append(f"{f}: URL in window")
                m = re.search(r"horizon[:\s]+(\d+)\s*day", t, re.I)
                if m and int(m.group(1)) > 14: bad.append(f"{f}: horizon {m.group(1)}d > 14")
    rec(20, "FAIL", not bad, "term plan integrity" + ("" if not bad else ": " + "; ".join(bad[:6])))

# ---- check 20.5: plans vs attempts — the AP-08 guard (WARN) ------------------
def c205():
    reg = os.path.join(ROOT, "Brain/short_term/plan/TERM1_DEADLINES.json")
    if not os.path.exists(reg):
        rec(20.5, "WARN", True, "planner theater: no plan register — nothing to guard"); return
    led = read("Brain/frontal_lobe/task_ledger.md").splitlines()
    tail = [l for l in led if l.strip().startswith("|")][-3:]
    has_attempt = any("mastery" in l.lower() or "drill" in l.lower() or "@Review" in l for l in tail)
    rec(20.5, "WARN", has_attempt,
        "planner theater guard: plan exists" + ("" if has_attempt else
        " and the last 3 task_ledger rows record no attempt — plans are not progress (AP-08)"))

# ---- check 19: [R] publisher rule — blocklist (P-07; enforces I.2's existing "peer-reviewed or formally studied") ----
BLOCKLIST = ["grokipedia.com","scribd.com","fiveable.me","coursehero.com","studocu.com","flickr.com","planningtank.com","blogspot.","medium.com"]
def c19():
    bad = []
    for f in md_files():
        if IS_EX(f): continue
        for i, ln in enumerate(read(f).splitlines()):
            hits = sum(d in ln for d in BLOCKLIST)
            if "[R]" in ln and hits == 1:  # >=2 domains on one line = the rule/blocklist text itself, not a citation
                bad.append(f"{f}:{i+1}")
    rec(19, "FAIL", not bad, "publisher rule: no [R] carried by blocklisted aggregator" + ("" if not bad else ": " + "; ".join(bad[:6])))

for fn in (c1,c2,c25,c3,c3b,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c205): fn()
fails = [r for r in RESULTS if r["severity"] == "FAIL" and not r["ok"]]
warns = [r for r in RESULTS if r["severity"] == "WARN" and not r["ok"]]
for r in RESULTS:
    icon = "✅ PASS" if r["ok"] else ("❌ FAIL" if r["severity"]=="FAIL" else "⚠️ WARN")
    print(f"{icon}  [check {r['check']}] {r['msg']}")
print(f"\n{len(RESULTS)} checks run · {len(RESULTS)-len(fails)-len(warns)} pass · {len(warns)} warn · {len(fails)} fail")
with open(os.path.join(ROOT,"validation_report.json"),"w") as fh:
    json.dump(RESULTS, fh, indent=1)
sys.exit(1 if fails else 0)
