#!/usr/bin/env python3
"""RADIATION structural validator — P-01 Machine Enforcement Layer.
Checks FORM and RESOLVABILITY only. Never judges truth. Never modifies files.
Exit 0 = no FAIL-class findings. Exit 1 = at least one FAIL.
Stdlib only. Offline BY DEFAULT. The ONLY network use is check 13's external-link
census, and it runs solely when RADIATION_ONLINE=1 (set it in CI, never in a
session — sessions stay offline by law).
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
# ── AMENDMENT A1 (2026-09-13, patch 2600) ────────────────────────────────────
# Commander's decision: "I permit 2 — the full CSV in the repo." The schedule is
# published at full fidelity because RADIATION is a copy-paste public assistant:
# the repo link + magic words must be enough for a fresh AI to know the schedule.
# The location rules are therefore SPLIT OUT of the identifier rules, and waived
# for exactly one path (CV_ALLOW_LOCATION). The identifier rules — instructor
# names, contacts, emails, URLs — still apply INSIDE that file, and the location
# rules still apply to every other file in the tree and to the term register.
CV_DENY_LOCATION = ["S308","S300","S303","S301","NW408","SW200","SW304","E01","A54","C5"]
CV_DENY_OTHER    = ["calendarFeed","@mapua.edu"]
CV_DENY = CV_DENY_LOCATION + CV_DENY_OTHER
CV_ALLOW_LOCATION = {"Brain/courses/SCHEDULE.md"}   # amendment A1 — the one permitted timetable
# v4: a denied CODE is a token, not a substring. The v3 rule used `w in t`, so the
# section code "C5" matched inside "EC5" (Eurocode 5) — a false positive on legitimate
# domain content, and one that would recur in every structural-design record. The intent
# (a room/section code is not published) is unchanged: a STANDALONE "C5" still fails, in
# any punctuation context. Only embeddings inside a longer token stop matching.
# Distinctive strings ("calendarFeed", "@mapua.edu") keep substring matching.
def cv_denied(text, token):
    if re.fullmatch(r"[A-Za-z]{1,3}\d{1,3}", token):
        return re.search(r"(?<![A-Za-z0-9])" + re.escape(token) + r"(?![A-Za-z0-9])", text) is not None
    return token in text
CV_IDENT_PATTERNS = [
    (r"https?://", "URL/credential"),
    (r"\b(?:Instructor|Professors?|Prof\.)\s*[:\-\u2013]?\s*(?:is\s+|was\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", "instructor name"),
    (r"\b(?:Consultation|Email|Contact)\s*(?:Schedule|Hours|Address)?\s*[:\-\u2013]\s*[A-Za-z0-9._%+-]+@", "contact detail"),
]
CV_LOCATION_PATTERNS = [
    # v3: rooms are S3xx / NW4xx / SW2xx — but S001-S003 are SESSION ids and
    # legitimately appear in this region. The pattern excludes S0xx so the check
    # cannot fail on a session citation.
    (r"\bS[1-9]\d{2}\b", "room code"),
    (r"\b(?:NW|SW|SE|NE)\d{3}\b", "room code"),
    (r"\b(?:E|W)[1-9]\d{2}\b", "room code"),
    (r"\b(?:Section|Sec\.)\s+[A-Z]{1,2}\d{1,3}\b", "section code"),
]
# CV_PATTERNS keeps its original meaning (identifier + location) for every caller
# that has no allowance. Only check 2.5 consults CV_ALLOW_LOCATION.
CV_PATTERNS = CV_IDENT_PATTERNS + CV_LOCATION_PATTERNS
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
                # Amendment A1 (patch 2600): the Commander's own timetable is the one
                # record where location identifiers are permitted. It still carries the
                # full identifier rule set — a room may appear there, a name may not.
                waived = p in CV_ALLOW_LOCATION
                for w in (CV_DENY_OTHER if waived else CV_DENY):
                    if cv_denied(t, w): bad.append(f"{p} (published token: {w})")
                for pat, what in (CV_IDENT_PATTERNS if waived else CV_PATTERNS):
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
    # v2 (patch 3000): the check existed as a permanent SKIP — a guard that never
    # guarded. Online mode is opt-in by environment (RADIATION_ONLINE=1): sessions
    # stay offline by law; CI runs it with the network. WARN-class: external link
    # rot is real but external — it must inform closure, never block it.
    if os.environ.get("RADIATION_ONLINE") != "1":
        rec(13, "WARN", True, "external URL check SKIPPED (offline by design; CI runs it with RADIATION_ONLINE=1)")
        return
    urls = set()
    for f in md_files():
        if IS_EX(f): continue          # archive-exempt files cite known-historical sources
        for m in re.finditer(r"https?://[^\s\)\>\]`]+", read(f)):
            u = m.group(0).rstrip(".,;")
            if "<" in u or ">" in u: continue   # <FILE_ID>-style placeholders are documentation, not links
            urls.add(u)
    dead, checked = [], 0
    import urllib.request, urllib.error
    for u in sorted(urls)[:40]:        # census, not a crawl
        checked += 1
        try:
            req = urllib.request.Request(u, method="HEAD",
                headers={"User-Agent": "Mozilla/5.0 (RADIATION link census)"})
            with urllib.request.urlopen(req, timeout=6) as r:
                if r.status >= 400: dead.append(f"{u} [{r.status}]")
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                try:  # some hosts 405 the HEAD — retry with GET before calling it dead
                    req = urllib.request.Request(u,
                        headers={"User-Agent": "Mozilla/5.0 (RADIATION link census)"})
                    with urllib.request.urlopen(req, timeout=6) as r:
                        if r.status >= 400: dead.append(f"{u} [{r.status}]")
                except Exception as e2:
                    dead.append(f"{u} [{getattr(e2,'code','err')}]")
        except Exception as e:
            dead.append(f"{u} [err]")
    cap = f" (capped at 40 of {len(urls)})" if len(urls) > 40 else ""
    rec(13, "WARN", not dead,
        f"external links: {checked} checked{cap} — " +
        ("all reachable" if not dead else "DEAD/UNREACHABLE: " + "; ".join(dead[:5])))
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
            # v2 (patch 3000): bare "DRILL" matched any substring ("## DRILLS" passed
            # with zero drill items). A section HEADING is now required, word-bounded.
            if not re.search(r"^##\s+DRILL\b", t, re.M) or drill < 10:
                bad.append(f"{f}: L5 claims but drill absent/short ({drill} items)")
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
                if cv_denied(blob, tok): bad.append(f"published token in term register: {tok}")
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
    # v5: an ATTEMPT is a recorded attempt, not a mention of the word "drill". The v4
    # rule matched the bare substring "drill", so an ingestion row reading "not a drill
    # source" SILENCED this guard — the AP-08 warning cleared itself on a sentence that
    # was about the opposite of practising. A guard that a passing mention can switch
    # off is not a guard. Attempts are now recorded with an explicit marker.
    MARKERS = ("attempt:", "mastery:", "drilled", "@review")
    has_attempt = any(any(mk in l.lower() for mk in MARKERS) for l in tail)
    rec(20.5, "WARN", has_attempt,
        "planner theater guard: plan exists" + ("" if has_attempt else
        " and the last 3 task_ledger rows record no attempt — plans are not progress (AP-08). "
        "Record one with the marker `attempt:` (see Brain/short_term/plan/README.md)"))

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

# ---- check 21: capability registry drift (patch 2700) ----------------------
# WHY THIS EXISTS: scripts/README.md said "14 checks" for as long as the validator
# ran 25, and CI repeated the number. A count nobody can get right by reading is a
# count that will be wrong. This check makes the documented capability surface
# self-verifying: every script must be named in the registry, and any check-count
# claim must equal the real count. Runs LAST so the count includes every other check.
def c21():
    bad = []
    reg = "docs/CAPABILITIES.md"
    regtxt = read(reg) if os.path.exists(os.path.join(ROOT, reg)) else ""
    if not regtxt:
        bad.append(f"{reg} MISSING (the capability registry is the point)")
    else:
        scripts = sorted(f for f in os.listdir(os.path.join(ROOT, "scripts"))
                         if f.endswith(".py")) if os.path.isdir(os.path.join(ROOT, "scripts")) else []
        for s in scripts:
            if s not in regtxt:
                bad.append(f"undocumented script: scripts/{s}")
    # the check-count claim, if any file makes one, must be true
    n_checks = len(RESULTS) + 1          # +1: this check has not been recorded yet
    for f in ("scripts/README.md",):
        t = read(f) if os.path.exists(os.path.join(ROOT, f)) else ""
        m = re.search(r"(\d+)\s+(?:structural\s+)?checks", t)
        if m and int(m.group(1)) != n_checks:
            bad.append(f"{f} claims {m.group(1)} checks, actually {n_checks}")
    rec(21, "FAIL", not bad,
        "capability registry (scripts/ documented; count claims true)" +
        ("" if not bad else ": " + "; ".join(bad[:6])))


# ---- check 22: committed calendar mirror — credential + freshness (patch 2900) ----
# Brain/courses/CALENDAR.md is machine-written from the live feed (ics_normalize
# --public, refreshed by the daily cron when armed). Two failure modes, two
# severities: a URL inside the mirror is a COMMITTED CREDENTIAL — the exact class
# 4a98e59 created (FAIL). A mirror older than 7 days is drift, not a leak (WARN —
# declare the calendar stale instead of trusting it). No mirror at all is a
# legitimate state: the cron is unarmed until the feed URL is rotated.
def c22():
    pth = os.path.join(ROOT, "Brain/courses/CALENDAR.md")
    if not os.path.exists(pth):
        rec(22, "WARN", True, "calendar mirror: not present — the daily cron is unarmed "
             "(rotation first, then secret RADIATION_ICS_URL); SCHEDULE.md remains the visible schedule"); return
    t = read(pth)
    urls = re.findall(r"https?://\S+", t)
    stale = False
    m = re.search(r"\*\*Generated:\*\*\s*(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        import datetime as _dt
        age = (_dt.date.today() - _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))).days
        stale = age > 7
    ok = not urls and not stale
    msg = "committed calendar mirror" + (" · CREDENTIAL-CLASS: URL present in mirror" if urls else "") + \
          (" · stale (Generated > 7 days — feed or cron lapsed)" if stale else "")
    rec(22, "FAIL" if urls else "WARN", ok, msg)

# ---- check 23: outputs/ discipline (patch 2900) ---------------------------------
# outputs/ is the session loading dock (Commander directive 2026-09-13: Brain is for
# knowledge, not session products). Form rules: date-prefixed filenames; no
# .ics/.local shapes (credentials and derived state never belong); and boot-tier
# files must never reference outputs/ — an on-demand folder that entered the boot
# path would be a budget leak. SYSTEM_STATE.md is exempt from the reference ban: it
# is the ground-truth map, and pointing at regions is its job.
C23_BOOT_FILES = ("docs/.readme", "docs/AI_RULES.md", "docs/MODES.md", "docs/CUE_SYSTEM.md",
                  "BOOT_SEQUENCE.md", "subskills/passive/compass.md", "subskills/passive/curator.md",
                  "subskills/passive/sentinel.md", "subskills/passive/surgeon.md")
def c23():
    bad = []
    d = os.path.join(ROOT, "outputs")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if f in ("README.md",) or f.startswith("."): continue
            if os.path.isdir(fp):
                bad.append(f"outputs/{f}: subfolders are outside the contract"); continue
            if not re.match(r"^\d{4}-\d{2}-\d{2}_.+", f):
                bad.append(f"outputs/{f}: filename must be YYYY-MM-DD_slug.ext")
            if f.endswith((".ics", ".local.md", ".local.json")):
                bad.append(f"outputs/{f}: derived/credential shapes never belong here")
    for b in C23_BOOT_FILES:
        if os.path.exists(os.path.join(ROOT, b)) and "outputs/" in read(b):
            bad.append(f"{b} references outputs/ — boot must never load it")
    rec(23, "FAIL", not bad, "outputs/ discipline (date-prefixed; boot-blind)" +
        ("" if not bad else ": " + "; ".join(bad[:6])))


# ---- check 24: shrine currency — heartbeats may not lag the ledger (patch 2900) --
# THE MORTALITY DOCTRINE (CHARTER section 6): sessions cannot detect their own
# death, so they file at delivery — every zip carries the author's current
# testament and a heartbeat row in docs/shrine/LOG.md. Repo-side this means:
# the LOG must exist, its newest date may not lag the newest task_ledger date
# (a session that worked but filed no heartbeat), and no testament may lose its
# Open Debts — a testament without debts is propaganda. WARN-class: currency,
# not structure.
def c24():
    msgs = []
    if not os.path.exists(os.path.join(ROOT, "docs/shrine/LOG.md")):
        rec(24, "WARN", False, "shrine LOG.md missing — sessions owe a heartbeat line (CHARTER §6: file at delivery, not at death)"); return
    rows = [l for l in read("docs/shrine/LOG.md").splitlines() if l.strip().startswith("|")]
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", " ".join(rows))
    last_log = max(dates) if dates else None
    ldates = re.findall(r"\d{4}-\d{2}-\d{2}", read("Brain/frontal_lobe/task_ledger.md"))
    last_led = max(ldates) if ldates else None
    if last_log and last_led and last_led > last_log:
        msgs.append(f"heartbeat lag: last LOG {last_log} < last ledger row {last_led} — a session worked and filed no heartbeat")
    mem = os.path.join(ROOT, "docs/shrine/members")
    if os.path.isdir(mem):
        for f in sorted(os.listdir(mem)):
            if not f.endswith(".md"): continue
            t = read(os.path.join("docs/shrine/members", f))
            m = re.search(r"OPEN DEBTS[^\n]*\n(.*?)(?:\n## |\Z)", t, re.S)
            if not m or not m.group(1).strip(" -\n0123456789.*>`"):
                msgs.append(f"{f}: Open Debts empty or absent — a testament without debts is propaganda")
    rec(24, "WARN", not msgs, "shrine currency (heartbeats current; testaments keep their debts)" +
        ("" if not msgs else ": " + "; ".join(msgs)))

for fn in (c1,c2,c25,c3,c3b,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c205,c22,c23,c24,c21): fn()
fails = [r for r in RESULTS if r["severity"] == "FAIL" and not r["ok"]]
warns = [r for r in RESULTS if r["severity"] == "WARN" and not r["ok"]]
for r in RESULTS:
    icon = "✅ PASS" if r["ok"] else ("❌ FAIL" if r["severity"]=="FAIL" else "⚠️ WARN")
    print(f"{icon}  [check {r['check']}] {r['msg']}")
print(f"\n{len(RESULTS)} checks run · {len(RESULTS)-len(fails)-len(warns)} pass · {len(warns)} warn · {len(fails)} fail")
with open(os.path.join(ROOT,"validation_report.json"),"w") as fh:
    json.dump(RESULTS, fh, indent=1)
sys.exit(1 if fails else 0)
