#!/usr/bin/env python3
"""RADIATION structural validator — P-01 Machine Enforcement Layer.
Checks FORM and RESOLVABILITY only. Never judges truth. Never modifies files.
Exit 0 = no FAIL-class findings. Exit 1 = at least one FAIL.
Stdlib only. Offline BY DEFAULT. The ONLY network use is check 13's external-link
census, and it runs solely when RADIATION_ONLINE=1 (set it in CI, never in a
session — sessions stay offline by law).
"""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from radiation_core.relay import _schema_check, unsupported_keywords  # ONE schema executor (II.11)
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
# ---- 5300 E1: declared course-corpus admission contract --------------------
def _corpus_contract_violations(root):
    """The Brain/courses/ non-Markdown corpus is ADMITTED BY DECLARATION only:
    an exact, hash-bound entry in COURSE_CORPUS_MANIFEST.json. Returns
    (violations, declared_path_set). A checksum is not a permission grant."""
    bad, declared = [], set()
    mp = os.path.join(root, "Brain", "courses", "COURSE_CORPUS_MANIFEST.json")
    if not os.path.isfile(mp):
        return (["Brain/courses/COURSE_CORPUS_MANIFEST.json missing — the declared "
                 "course-corpus contract (5300 E1) is not installed"], declared)
    try:
        m = json.load(open(mp, encoding="utf-8"))
    except Exception as e:
        return ([f"COURSE_CORPUS_MANIFEST.json unparseable: {e}"], declared)
    out: list[str] = []
    _schema_check(m, "course_corpus_manifest.schema.json", "course corpus manifest", out)
    bad.extend(out[:6])
    courses_real = os.path.realpath(os.path.join(root, "Brain", "courses")) + os.sep
    assets = m.get("assets") if isinstance(m.get("assets"), list) else []
    for a in assets:
        p = str(a.get("path", ""))
        declared.add(p)
        ap = os.path.join(root, p)
        if not os.path.isfile(ap):
            bad.append(f"{p}: declared asset missing")
            continue
        if os.path.islink(ap) or not os.path.realpath(ap).startswith(courses_real):
            bad.append(f"{p}: declared path escapes Brain/courses/ (traversal/symlink)")
            continue
        h = "sha256:" + hashlib.sha256(open(ap, "rb").read()).hexdigest()
        if h != a.get("sha256"):
            bad.append(f"{p}: digest drift — declared {str(a.get('sha256'))[:21]}…, on disk {h[:21]}…")
        if a.get("role") == "source_of_readable_derivative":
            d = a.get("derivative_path")
            if not d or not os.path.isfile(os.path.join(root, str(d))):
                bad.append(f"{p}: readable derivative missing ({d})")
    return (bad, declared)


# ---- 5300 E2: sanctioned replica contract ----------------------------------
def _replica_open_exception(rat):
    """5600 closure: fail-closed authority visibility.

    Only an explicit 'commander-ratified' status closes the open governed
    exception; anything else — including a MISSING ratification record —
    stays visibly open. A 'requested' review must never be indistinguishable
    from a ratified PASS (and must never self-ratify).
    """
    return rat != "commander-ratified"


def _replica_contract(root):
    """Exactly the declared pairs may be byte-identical; every other duplicate
    still fails. Both sides are hash-bound: drift fails, silence is not kept."""
    bad, allowed = [], set()
    mp = os.path.join(root, "scaffolding", "neurons", "REPLICA_MANIFEST.json")
    if not os.path.isfile(mp):
        return (["scaffolding/neurons/REPLICA_MANIFEST.json missing — replica "
                 "contract (5300 E2) not installed"], allowed)
    try:
        m = json.load(open(mp, encoding="utf-8"))
    except Exception as e:
        return ([f"REPLICA_MANIFEST.json unparseable: {e}"], allowed)
    out: list[str] = []
    _schema_check(m, "replica_manifest.schema.json", "replica manifest", out)
    bad.extend(out[:6])
    pairs = m.get("pairs") if isinstance(m.get("pairs"), list) else []
    for pr in pairs:
        c, r = str(pr.get("canonical_path", "")), str(pr.get("replica_path", ""))
        allowed.add(tuple(sorted((c, r))))
        if not all(os.path.isfile(os.path.join(root, q)) for q in (c, r)):
            bad.append(f"sanctioned replica side missing: {c} <-> {r}")
            continue
        hc = "sha256:" + hashlib.sha256(open(os.path.join(root, c), "rb").read()).hexdigest()
        hr = "sha256:" + hashlib.sha256(open(os.path.join(root, r), "rb").read()).hexdigest()
        if hc != hr or hc != pr.get("sha256"):
            bad.append(f"replica drift: {c} <-> {r} (hash-bound contract violated)")
    rat = m.get("ratification", {}).get("status") if isinstance(m.get("ratification"), dict) else None
    return (bad, allowed, rat)


def _dup_scan(root, allowed):
    """MD5 duplicate grouping over .md/.readme; declared exact pairs exempt."""
    hashes, bad, sets = {}, [], {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in {".git", ".github", "node_modules", "_local_backup", "__pycache__"}]
        for f in sorted(fn):
            if not (f.endswith(".md") or f == ".readme"):
                continue
            p = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
            txt = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            h = hashlib.md5(txt.encode()).hexdigest()
            if h in hashes:
                if tuple(sorted((p, hashes[h]))) not in allowed:
                    bad.append(f"{p} == {hashes[h]}")
            else:
                hashes[h] = p
            sets[p] = set(l for l in txt.splitlines() if l.strip())
    return (bad, sets)


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
# Amendment A2 (patch 3100): the committed LMS feed lives in the records region by
# Commander order (the hivemind needs the schedule data; GitHub rejects .ics uploads,
# so it is a .txt). It is DATA, not a record — one named exemption, identifier scan
# still applies to it, and everything else in the region stays records-only.
CV_ALLOW_DATA = {"Brain/courses/0_CALLENDER/TERM1_FEED.txt"}

# SD-3300-01: FAIL messages carry their remedy — a validator that names a wound
# without naming the treatment makes the Commander do the plumbing.
REMEDY_VEHICLES = " · REMEDY: inside Brain/courses/ declare the asset in Brain/courses/COURSE_CORPUS_MANIFEST.json (hash-bound, 5300 E1) or remove it; elsewhere in Brain/ move it out + git rm --cached"
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
def _brain_vehicle_violations(root, declared):
    """3400 HARDENING, 5300 E1 refinement — the vehicle rule stays GENERIC over
    all of Brain/: the corpus is INTENTIONAL and admitted BY DECLARATION
    (hash-bound manifest), never by deletion. Inside Brain/courses/ only exact
    manifest entries pass; elsewhere the rule is unchanged."""
    bad = []
    brain = os.path.join(root, "Brain")
    def sanctioned(p):
        if p == "Brain/courses/COURSE_CORPUS_MANIFEST.json":
            return True                                  # 5300 E1: the contract file itself
        # A2 feed: NO path-only escape since 5500 — it is digest-bound in the manifest
        if p.startswith("Brain/short_term/plan/") and p.endswith(".json"):
            return True                                  # the deadline register the planner eats
        if p.startswith("Brain/short_term/drills/"):
            return True                                  # drill fixtures (nota/export_anki own these)
        return False
    if os.path.isdir(brain):
        for dp, dn, fn in os.walk(brain):
            for f in sorted(fn):
                p = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
                if f.endswith(".md") or f == ".gitkeep" or sanctioned(p):
                    continue
                if p.startswith("Brain/courses/"):
                    if p not in declared:
                        bad.append(f"{p} (undeclared course-corpus asset — declare it in COURSE_CORPUS_MANIFEST.json or remove it)")
                else:
                    bad.append(f"{p} (unsanctioned vehicle)")
    return bad


def c25():
    bad = []
    c_bad, declared = _corpus_contract_violations(ROOT)
    bad.extend(c_bad)
    bad.extend(_brain_vehicle_violations(ROOT, declared))
    # Identifier scan: Brain/courses/ text records. Amendment A1 (patch 2600): the
    # Commander's own timetable is the one record where location identifiers are
    # permitted — a room may appear there, a name may not.
    root = os.path.join(ROOT, "Brain/courses")
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            for f in sorted(fn):
                p = os.path.relpath(os.path.join(dp, f), ROOT)
                if not (f.endswith(".md") or f.endswith(".txt")): continue
                if p in CV_ALLOW_DATA: continue
                t = read(p)
                waived = p in CV_ALLOW_LOCATION
                for w in (CV_DENY_OTHER if waived else CV_DENY):
                    if cv_denied(t, w): bad.append(f"{p} (published token: {w})")
                for pat, what in (CV_IDENT_PATTERNS if waived else CV_PATTERNS):
                    m = re.search(pat, t)
                    if m: bad.append(f"{p} ({what}: {m.group(0)[:24]})")
    rec(2.5, "FAIL", not bad, "Brain/ records-only + declared course corpus + no identifiers (generic vehicle rule, 3400; declared corpus 5300 E1)" + ("" if not bad else ": " + "; ".join(bad[:6])) + REMEDY_VEHICLES if bad else "Brain/ records-only + declared course corpus + no identifiers — clean (3400 generic rule; 5300 E1 declared corpus)")

# ---- check 3: forbidden transport artifacts (II.8.2) -----------------------
def c3():
    bad = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {".git", "_local_backup"}]
        for d in dn:
            if d in ("append_blocks","append-blocks"): bad.append(os.path.relpath(os.path.join(dp,d),ROOT)+"/")
        for f in fn:
            if "_REPLACEMENT" in f or "_STAGED" in f or "_DIFF" in f or f in ("PATCH_NOTES.md","APPLY.sh","APPLY.ps1"):
                bad.append(os.path.relpath(os.path.join(dp,f),ROOT))
    rec(3, "FAIL", not bad, "no transport artifacts or carriers in tree (II.8.2 + closure rule: *_STAGED/*_DIFF/PATCH_NOTES/APPLY runners)" + ("" if not bad else ": " + "; ".join(bad)) + (" · REMEDY: delete the carrier — it is transport, not record (APPLY removes it)" if bad else ""))
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
    # 5300 E2: the four declared active/archive replica pairs are exempt — but
    # hash-bound: a drifted twin fails via _replica_contract, and any duplicate
    # NOT declared as an exact sanctioned pair still fails below.
    r_bad, allowed, rat = _replica_contract(ROOT)
    # 5600 closure: the tranche's authority state is a VISIBLY open governed
    # exception while un-ratified — never a silently ratified PASS.
    if _replica_open_exception(rat):
        rec(11.6, "WARN", False,
            "replica tranche authority — OPEN GOVERNED EXCEPTION (status: "
            f"{rat or 'no ratification record'}): pairs admitted provisionally, NOT "
            "Commander-ratified; decision options: docs/REPLICA_DECISION.md")
    else:
        rec(11.6, "WARN", True, "replica tranche authority (Commander-ratified)")
    bad, sets = _dup_scan(ROOT, allowed)
    warn = []
    fl = list(sets)
    for i in range(len(fl)):
        for j in range(i+1, len(fl)):
            a, b = sets[fl[i]], sets[fl[j]]
            if not a or not b: continue
            jac = len(a & b) / len(a | b)
            if 0.9 <= jac < 1.0: warn.append(f"{fl[i]} ~ {fl[j]} ({jac:.2f})")
    bad = r_bad + bad
    rec(11, "FAIL", not bad, "duplicate files (declared replica pairs exempt, 5300 E2)" + ("" if not bad else ": " + "; ".join(bad[:4])))
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
        + (" · II.10 compression: ACTIVE" if "II.10 — LEDGER COMPRESSION" in read("docs/AI_RULES.md") else " · II.10 compression: OFF")
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
    # v3 (patch 3100): the feed is a COMMITTED FILE (TERM1_FEED.txt). Guards:
    #   - a URL inside the mirror is still a committed credential (FAIL, unchanged)
    #   - the FEED itself going stale (its newest event behind today) → WARN: re-export
    #   - mirror missing → WARN only (CI regenerates post-push; the human push must not go red first)
    pth = os.path.join(ROOT, "Brain/courses/CALENDAR.md")
    feed = os.path.join(ROOT, "Brain/courses/0_CALLENDER/TERM1_FEED.txt")
    import datetime as _dt
    msgs, ok = [], True
    if os.path.exists(feed):
        dates = [m.group(1) for m in re.finditer(r"DTSTART[^:\r\n]*:(\d{8})", read(feed).replace(" ", ""))]
        if dates:
            newest = max(dates)
            d = _dt.date(int(newest[:4]), int(newest[4:6]), int(newest[6:]))
            if d < _dt.date.today():
                msgs.append(f"FEED STALE — newest event {d.isoformat()} is behind today; re-export from the LMS and push")
    t = read(pth) if os.path.exists(pth) else ""
    if not t:
        msgs.append("CALENDAR.md not generated yet — CI regenerates it from the committed feed on push")
    else:
        urls = re.findall(r"https?://\S+", t)
        if urls:
            ok = False
            msgs.append("CREDENTIAL-CLASS: URL present in mirror: " + "; ".join(urls[:2]))
        m = re.search(r"\*\*Generated:\*\*\s*(\d{4})-(\d{2})-(\d{2})", t)
        if m:
            age = (_dt.date.today() - _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))).days
            if age > 7:
                msgs.append(f"mirror stale ({age}d) — feed push or CI lapsed")
    rec(22, "WARN" if ok else "FAIL", ok, "calendar feed + mirror" + (": " + "; ".join(msgs[:3]) if msgs else " — current"))

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
    import datetime as _dt
    _today = (_dt.date.today() + _dt.timedelta(days=1)).isoformat()
    # v3: activity dates cannot be in the future — ledger rows carry decay/plan dates too
    # (e.g. a card's decay lands in the ledger's evidence column and read as "activity
    # from next year", false-positiving the heartbeat lag). Tolerance = +1 day to absorb
    # timezone/clock skew between the committer's machine and whatever clock runs this
    # check (CI runs UTC; PH is UTC+8 — a late-night PH commit is "tomorrow" in UTC).
    dates = [d for d in re.findall(r"\d{4}-\d{2}-\d{2}", " ".join(rows)) if d <= _today]
    last_log = max(dates) if dates else None
    ldates = [d for d in re.findall(r"\d{4}-\d{2}-\d{2}", read("Brain/frontal_lobe/task_ledger.md")) if d <= _today]
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


# ---- check 25: standing-directive registry integrity (patch 3300) --------------
# The registry (cue/standing-directives.json) is the typed source of truth for the
# swarm's bounded autonomy. Prose never enforces; a directive that lost its
# enforcement mapping, authority, or provenance is not governance — it is a mood.
# Schema: unique active ids, known classes/authority, non-empty rule+scope, and an
# enforcement reference that resolves to a real mechanism (validator check number,
# repo file, or named law/protocol).
def c25reg():
    import json as _json
    pth = os.path.join(ROOT, "cue/standing-directives.json")
    if not os.path.exists(pth):
        rec(25, "WARN", True, "directive registry absent — @selfdirectives runs on prose only (patch 3300 ships it)"); return
    try:
        d = _json.load(open(pth, encoding="utf-8"))
    except Exception as e:
        rec(25, "FAIL", False, f"directive registry unparseable: {e}"); return
    bad, ids = [], set()
    classes = {"invariant", "constraint", "goal", "procedure", "preference", "lesson"}
    auths = {"root", "commander", "authorized_user", "user", "memory", "external"}
    for dr in d.get("directives", []):
        i = dr.get("id", "?")
        if i in ids: bad.append(f"{i}: duplicate id")
        ids.add(i)
        if dr.get("status") != "active": continue
        if dr.get("class") not in classes: bad.append(f"{i}: bad class {dr.get('class')!r}")
        if dr.get("authority") not in auths: bad.append(f"{i}: bad authority {dr.get('authority')!r}")
        if not dr.get("rule"): bad.append(f"{i}: empty rule")
        if not dr.get("scope"): bad.append(f"{i}: empty scope")
        en = dr.get("enforcement", "")
        if not en: bad.append(f"{i}: NO ENFORCEMENT — prose is not governance"); continue
        resolves = False
        for m in re.findall(r"checks? (\d+(?:\.\d+)?)", en):
            if any(str(r["check"]) == m for r in RESULTS): resolves = True
        for m in re.findall(r"([A-Za-z0-9_/\.\-]+\.(?:py|json|md|sh|ps1|yml))", en):
            if os.path.exists(os.path.join(ROOT, m)): resolves = True
        if re.search(r"surgeon|push|patch risk|II\.3|git credentials|ledger audit|never-manufacture|scan/curator", en):
            resolves = True
        if not resolves: bad.append(f"{i}: enforcement does not resolve: {en[:48]!r}")
    if not d.get("directives"): bad.append("registry holds no directives")
    rec(25, "FAIL", not bad, f"standing-directive registry ({len(ids)} directives)" +
        ("" if not bad else ": " + "; ".join(bad[:6])))

# ---- check 28: activation matrix integrity (patch 4200) --------------------
def c28matrix():
    t = read("docs/MODES.md")
    need = ["ACTIVATION MATRIX", "selfdirectives (active)", "scout (active)", "colony (active)",
            "fetch (active)", "overule (Commander-triggered)"]
    bad = [f"matrix row/section missing: {n}" for n in need if n not in t]
    rec(28, "FAIL", not bad, "activation matrix integrity (universal subskills pinned)" +
        ("" if not bad else ": " + "; ".join(bad) + " · REMEDY: restore the row in docs/MODES.md — canon must not silently regress (the universal ruling was lost once before this check existed)"))

# ---- check 27: neuron relay chain integrity (patch 3900, SD-3600-03) -------
def c27relay():
    nd = os.path.join(ROOT, "scaffolding", "neurons")
    if not os.path.isdir(nd):
        rec(27, "WARN", True, "neuron relay absent — Autopilot runs without persistent task records (3600 ships it)")
        return
    if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
    try:
        from radiation_core import relay as _relay
    except Exception as e:
        rec(27, "FAIL", False, f"relay engine unavailable: {e}")
        return
    findings = _relay.validate_active()
    stages = (("sensoryneurons","intake"),("interneurons","reasoning"),("motorneurons","orders"))
    tids = set()
    for stage, suffix in stages:
        sd = os.path.join(nd, stage)
        for f in (sorted(x for x in os.listdir(sd) if x.endswith(".md")) if os.path.isdir(sd) else []):
            mm = re.match(r"TID-(.+)_" + suffix + r"\.md$", f)
            if mm: tids.add(mm.group(1))
    legacy_active = len(tids & _relay.load_legacy())
    rec(27, "FAIL", not findings,
        f"neuron relay semantic ({len(tids)} active TIDs: {legacy_active} legacy_trace, {len(tids)-legacy_active} canonical bundle(s))" +
        ("" if not findings else ": " + "; ".join(findings[:6]) + " · REMEDY: fix the task bundle (evidence/tasks/<TID>/) or mark a pre-runtime trace legacy in evidence/tasks/legacy_manifest.json"))


# ---- check 29: Core card gate — real cards, real envelope, exact parity (4400) ----
def c29core():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import nota as _nota
    except Exception as e:
        rec(29, "FAIL", False, f"core card gate: nota import failed: {e}")
        return
    files = _nota.canonical_cards()
    problems, seen, parsed = [], {}, {}
    for path in files:
        c, probs, _w = _nota.parse_card(path)
        parsed[path] = c
        problems.extend(probs)
        if c and c.get("cid"):
            seen[c["cid"]] = seen.get(c["cid"], 0) + 1
    idx = _nota.index_rows()
    for cid, n in idx.items():
        if cid not in seen: problems.append(f"CORE_INDEX lists {cid} but no card file carries it")
        if n > 1: problems.append(f"CORE_INDEX has {n} rows for {cid}")
    for c in parsed.values():
        if c and c.get("status") == "ADMITTED" and c.get("cid") not in idx:
            problems.append(f"{c['cid']} is ADMITTED without a CORE_INDEX row")
    for cid, n in seen.items():
        if n > 1: problems.append(f"{cid}: {n} files carry the ID")
    admitted = sum(1 for c in parsed.values() if c and c.get("status") == "ADMITTED")
    rec(29, "FAIL", not problems,
        f"core cards: {len(files)} canonical ({admitted} admitted), envelope core-card/v1, index parity exact" +
        ("" if not problems else ": " + "; ".join(problems[:6]) + " · REMEDY: run nota.py --check and fix the envelope/index"))

# ---- check 26: shrine freshness (AI_RULES II.9 — THE SHRINE MANDATE) --------
def c26shrine():
    import subprocess
    lag = []
    import datetime as _dt2
    _today2 = (_dt2.date.today() + _dt2.timedelta(days=1)).isoformat()
    def dmax(txt):
        # v2 (4400): activity = the FIRST COLUMN of ledger/shrine TABLE rows only.
        # In-row dates (decay_at, evidence, plans) are not activity — a 2027 decay
        # date must never read as "a session worked in 2027" (auditor F-07).
        ds = []
        for ln in txt.splitlines():
            m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})", ln.strip())
            if m and m.group(1) <= _today2: ds.append(m.group(1))
        return max(ds) if ds else None
    d_log = dmax(read("docs/shrine/LOG.md"))
    d_led = dmax(read("Brain/frontal_lobe/task_ledger.md"))
    head = None
    try:
        head = subprocess.run(["git","-C",ROOT,"log","-1","--format=%cs"],
                              capture_output=True, text=True).stdout.strip() or None
    except Exception:
        pass
    if d_log is None:
        lag.append("LOG.md has no dated heartbeat")
    else:
        if d_led and d_led > d_log:
            lag.append(f"ledger activity {d_led} postdates last heartbeat {d_log}")
        if head and head > d_log:
            lag.append(f"HEAD commit {head} postdates last heartbeat {d_log}")
    ok = not lag
    rec(26, "WARN", ok,
        "shrine heartbeat current — II.9 MANDATE: every conversation files one" if ok
        else "shrine lags: " + "; ".join(lag) + " · REMEDY: append today's heartbeat row to docs/shrine/LOG.md (II.9)")

# ---- check 35: CAP records (4800 Attest) ------------------------------------
def c35cap():
    import subprocess
    problems = []
    if not os.path.exists(os.path.join(ROOT, "schemas", "cap_record.schema.json")):
        problems.append("schemas/cap_record.schema.json missing")
    else:
        try:
            json.load(open(os.path.join(ROOT, "schemas", "cap_record.schema.json"),
                           encoding="utf-8"))
        except Exception as e:
            problems.append(f"schema unparsable: {e}")
    r = subprocess.run([sys.executable, os.path.join("scripts", "cap_verify.py"),
                        "--self-test"], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("cap_verify --self-test failed: " + (tail[-1] if tail else "rc!=0"))
    # review-5100: EVERY tracked CAP record is enumerated and verified in CI
    # (seal + schema; live fidelity is proven at build time and recorded in
    # the bundle — the deliberate historical-records decision).
    r = subprocess.run([sys.executable, os.path.join("scripts", "cap_verify.py"),
                        "--tree"], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("cap_verify --tree failed: " + (tail[-1] if tail else "rc!=0"))
    rec(35, "FAIL", not problems,
        "CAP records verify (ALL tracked records enumerated, seal+schema · "
        "negative vectors · registry · identity null · C-4 redaction) — "
        "verifies records; authority flows only through the II.11 control "
        "plane; limits: docs/THREAT_MODEL.md" +
        ("" if not problems else ": " + "; ".join(problems[:4])))

# ---- check 36: CAP probe + host posture (4900 Probe) -------------------------
def c36probe():
    import subprocess
    problems = []
    if not os.path.exists(os.path.join(ROOT, "schemas", "host_profile.schema.json")):
        problems.append("schemas/host_profile.schema.json missing")
    if not os.path.exists(os.path.join(ROOT, "scaffolding", "hosts", "arena_agent_mode.json")):
        problems.append("host posture profile missing (scaffolding/hosts/)")
    else:
        try:
            r = subprocess.run([sys.executable, os.path.join("scripts", "cap_probe.py"),
                                "--profile", os.path.join("scaffolding", "hosts",
                                                          "arena_agent_mode.json")],
                               cwd=ROOT, capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                problems.append("host profile failed schema/posture check")
        except Exception as e:
            problems.append(f"profile check error: {e}")
    r = subprocess.run([sys.executable, os.path.join("scripts", "cap_probe.py"),
                        "--self-test"], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("cap_probe --self-test failed: " + (tail[-1] if tail else "rc!=0"))
    # review-5100 coherence: profile prose must not contradict the ratified
    # state, and declared postures must exist in the executed allowlist
    try:
        prof = json.load(open(os.path.join(ROOT, "scaffolding", "hosts",
                                           "arena_agent_mode.json"), encoding="utf-8"))
        allow = json.load(open(os.path.join(ROOT, "scaffolding", "control_plane",
                                            "allowlist.json"), encoding="utf-8"))
        allow_effects = {s.get("effect") for s in allow.get("operations", {}).values()
                         if isinstance(s, dict)}
        for phrase in ("STAGED (Product-2)", "awaits Product-2 ratification"):
            if phrase in json.dumps(prof):
                problems.append(f"profile staleness: {phrase!r} contradicts the "
                                "ratified control plane")
        for fx in prof.get("posture", {}).get("requested_effects", []):
            if fx not in allow_effects:
                problems.append(f"profile posture {fx!r} has no allowlist operation")
    except Exception as e:
        problems.append(f"profile coherence check error: {e}")
    rec(36, "FAIL", not problems,
        "CAP probe + host posture (read-only surface · containment · allowlist · "
        "profile schema-executed · coherence-linted) — OBSERVES only; authority "
        "flows only through the II.11 control plane; limits: docs/THREAT_MODEL.md" +
        ("" if not problems else ": " + "; ".join(problems[:4])))

# ---- check 37: control plane (II.11, ratified 5000) --------------------------
def c37control():
    import subprocess
    problems = []
    for f in ("radiation_core/control_plane.py",
              "scaffolding/control_plane/allowlist.json",
              "schemas/control_allowlist.schema.json",
              "schemas/control_decision.schema.json",
              "schemas/control_receipt.schema.json",
              "evidence/control_plane/receipts.ndjson"):
        if not os.path.exists(os.path.join(ROOT, f)):
            problems.append(f"missing: {f}")
    r = subprocess.run([sys.executable, "-m", "radiation_core.control_plane",
                        "verify"], cwd=ROOT, capture_output=True, text=True,
                       timeout=120)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("receipts chain broken: " + (tail[-1] if tail else "rc!=0"))
    r = subprocess.run([sys.executable, "-m", "radiation_core.control_plane",
                        "--self-test"], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("control_plane --self-test failed: " + (tail[-1] if tail else "rc!=0"))
    rec(37, "FAIL", not problems,
        "control plane (II.11, amended 5300): cooperative in-program policy flow · "
        "task-ID grammar schema-enforced (genesis exception) · receipts digest-bound · "
        "strict task grammar + pinned drafts base · content-bound single-use "
        "approvals · tamper-evident receipt chain · canonical = Commander motor "
        "act — in-program enforcement only, limits: docs/THREAT_MODEL.md" +
        ("" if not problems else ": " + "; ".join(problems[:4])))

# ---- check 38: provider activation layer (5200, review E4) -------------------
def c38agents():
    import subprocess
    problems = []
    for f in ("AGENTS.md", "agents/AGENT_INDEX.md", "agents/Arena_AI/BOOT.md",
              "agents/ChatGPT/BOOT.md", "agents/Gemini/BOOT.md",
              "agents/Grok/BOOT.md", "agents/Claude/BOOT.md",
              "agents/_common/radiation_pass.py"):
        if not os.path.exists(os.path.join(ROOT, f)):
            problems.append(f"missing: {f}")
    # coherence: folders on disk == providers named in the index
    idx = ""
    fp = os.path.join(ROOT, "agents", "AGENT_INDEX.md")
    if os.path.exists(fp):
        idx = open(fp, encoding="utf-8").read()
    disk = sorted(d for d in os.listdir(os.path.join(ROOT, "agents"))
                  if os.path.isdir(os.path.join(ROOT, "agents", d)) and d != "_common") \
        if os.path.isdir(os.path.join(ROOT, "agents")) else []
    for d in disk:
        if f"agents/{d}/" not in idx:
            problems.append(f"index does not route agents/{d}/")
    # claims lint: no first-person identity/power claims in any provider doc
    import re as _re
    bad_pat = _re.compile(r"\bI am (?:GPT|ChatGPT|Claude|Gemini|Grok)\b|\bmy (?:underlying|base) model\b|\bmy (?:tools|push access)\b|\bI can (?:commit|push)\b", _re.I)
    for d in disk:
        bp = os.path.join(ROOT, "agents", d, "BOOT.md")
        if os.path.exists(bp) and bad_pat.search(open(bp, encoding="utf-8").read()):
            problems.append(f"claims lint: agents/{d}/BOOT.md contains a first-person claim")
    # ── 5400 E6: research layer (non-boot) — dated profiles, sources, matrix ──
    research = ("ChatGPT", "Gemini", "Grok", "Claude", "Arena_AI")
    for d in research:
        pp = os.path.join(ROOT, "agents", d, "CAPABILITY_PROFILE.md")
        sp = os.path.join(ROOT, "agents", d, "SOURCES.md")
        if not os.path.exists(pp):
            problems.append(f"missing: agents/{d}/CAPABILITY_PROFILE.md")
            continue
        prof = open(pp, encoding="utf-8").read()
        if "reviewed_on:" not in prof or not __import__("re").search(r"reviewed_on:\s*2026-09-1[4-5]", prof):
            problems.append(f"agents/{d}/CAPABILITY_PROFILE.md: no reviewed_on date")
        if "Review trigger" not in prof:
            problems.append(f"agents/{d}/CAPABILITY_PROFILE.md: no review trigger")
        if not os.path.exists(sp):
            problems.append(f"missing: agents/{d}/SOURCES.md")
            continue
        srcs = open(sp, encoding="utf-8").read()
        if len(re.findall(r"2026-\d{2}-\d{2}", srcs)) < 3:
            problems.append(f"agents/{d}/SOURCES.md: fewer than 3 dated sources")
        if "retrieved" not in srcs.lower():
            problems.append(f"agents/{d}/SOURCES.md: no retrieval date")
        if bad_pat.search(prof) or bad_pat.search(srcs):
            problems.append(f"claims lint: agents/{d}/ research layer first-person claim")
    for f in ("agents/ROUTING_MATRIX.md", "agents/RESEARCH_METHOD.md"):
        if not os.path.exists(os.path.join(ROOT, f)):
            problems.append(f"missing: {f}")
    mp = os.path.join(ROOT, "agents", "ROUTING_MATRIX.md")
    if os.path.exists(mp):
        mt = open(mp, encoding="utf-8").read()
        for d in ("ChatGPT", "Claude", "Gemini", "Grok"):
            if d not in mt:
                problems.append(f"ROUTING_MATRIX.md does not cover {d}")
        if "Arena" not in mt:
            problems.append("ROUTING_MATRIX.md does not cover Arena")
    ap = os.path.join(ROOT, "agents", "Arena_AI", "CAPABILITY_PROFILE.md")
    if os.path.exists(ap):
        low = open(ap, encoding="utf-8").read().lower()
        if "unknowable" not in low:
            problems.append("Arena profile must state model identity is unknowable")
        if re.search(r"underlying model is (?:gpt|claude|gemini|grok)", low):
            problems.append("Arena profile makes a model-identity claim")
    r = subprocess.run([sys.executable, os.path.join("agents", "_common",
                        "radiation_pass.py"), "--self-test"], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()
        problems.append("radiation_pass --self-test failed: " + (tail[-1] if tail else "rc!=0"))
    rec(38, "FAIL", not problems,
        "provider activation (5200) + research layer (5400): exact folders · index "
        "coherence · RADIATION PASS handoff (deterministic, zero-write, claim-free) · "
        "dated provider profiles w/ sources + routing matrix — a handoff, NOT an elevation" +
        ("" if not problems else ": " + "; ".join(problems[:4])))

# ---- check 39: test harness + tool registry (5500 gate review) -------------
def c39gates():
    bad = []
    # (a) a harness that discovers ZERO tests is an explicit failure
    # RADIATION_VALIDATION_CTX tells the harness that validate.py is the
    # PARENT process: tests that would spawn validate again must skip —
    # validate→harness→validate is an infinite recursion, not a test.
    _ctx = {**os.environ, "RADIATION_VALIDATION_CTX": "1"}
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                       cwd=ROOT, capture_output=True, text=True, timeout=1200,
                       env=_ctx, stdin=subprocess.DEVNULL)
    m = re.search(r"Ran (\d+) tests?", r.stdout + r.stderr)  # unittest prints to stderr
    if not m or int(m.group(1)) < 1:
        bad.append("unittest discover found 0 tests — a harness that runs nothing is not a harness")
    elif r.returncode != 0:
        bad.append(f"unittest discover FAILED (rc={r.returncode}): "
                   + (r.stdout + r.stderr).strip().splitlines()[-1][:90])
    # (b) tool registry: ONE checker entry point — schema-executed + code-level
    # semantic rules (5600 closure Step 2; the checker self-carries its own
    # 13-vector negative battery)
    rchk = subprocess.run([sys.executable, "scripts/tool_registry_check.py"],
                          cwd=ROOT, capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
    if rchk.returncode != 0:
        tail = (rchk.stdout + rchk.stderr).strip().splitlines()
        bad.append("tool_registry_check FAILED: " + (tail[-1][:100] if tail else "rc=1"))
    rst = subprocess.run([sys.executable, "scripts/tool_registry_check.py", "--self-test"],
                         cwd=ROOT, capture_output=True, text=True,
                         timeout=300, stdin=subprocess.DEVNULL)
    if rst.returncode != 0 or "15/15" not in (rst.stdout + rst.stderr):
        bad.append("tool_registry_check self-test not 15/15")
    rec(39, "FAIL", not bad, "test harness + tool registry (5500+5600): discoverable tests "
        "exist and pass · registry is a bounded contract (schema-EXECUTED + code-level "
        "rules, self-tested)" + ("" if not bad else ": " + "; ".join(bad[:4])))

# ---- check 40: schema keyword coverage (5600 closure Step 3) ----------------
def c40():
    """Every shipped schema must use ONLY keywords the ONE executor executes
    (or documented annotations). A schema claim the executor cannot enforce
    is a silent freebie — a build failure, never a shrug."""
    bad = []
    n = 0
    sdir = os.path.join(ROOT, "schemas")
    for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
        if not f.endswith(".json"):
            continue
        n += 1
        try:
            spec = json.load(open(os.path.join(sdir, f), encoding="utf-8"))
        except Exception as e:
            bad.append(f"schemas/{f} unparseable: {e}")
            continue
        uk = unsupported_keywords(spec)
        if uk:
            bad.append(f"schemas/{f}: keywords the executor does not execute: {uk}")
    rec(40, "FAIL", not bad, f"schema keyword coverage (5600): {n} schemas within the "
        "executor's executed set + legal annotations" + ("" if not bad else ": " + "; ".join(bad[:4])))

# ---- check 41: model-research catalog (5700 Candidate C design) -------------
def c41():
    """The research layer is law at its own boundary: records schema-EXECUTED,
    uniqueness + date + confirmed-discipline enforced, and NON-BOOT asserted
    (no boot-tier file references the catalog)."""
    bad = []
    rchk = subprocess.run([sys.executable, "scripts/model_research_check.py"],
                          cwd=ROOT, capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
    if rchk.returncode != 0:
        tail = (rchk.stdout + rchk.stderr).strip().splitlines()
        bad.append("model_research_check FAILED: " + (tail[-1][:100] if tail else "rc=1"))
    rst = subprocess.run([sys.executable, "scripts/model_research_check.py", "--self-test"],
                         cwd=ROOT, capture_output=True, text=True,
                         timeout=300, stdin=subprocess.DEVNULL)
    if rst.returncode != 0 or "24/24" not in (rst.stdout + rst.stderr):
        bad.append("model_research_check self-test not 24/24")
    rec(41, "FAIL", not bad, "model-research catalog (5700+5710): records schema-EXECUTED · "
        "typed evidence bound to the register · real-date + 90-day-window discipline · "
        "filename-bound identifiers · non-boot scan over the BOOT_SEQUENCE-derived graph" +
        ("" if not bad else ": " + "; ".join(bad[:4])))

CHECKS = (c1,c2,c25,c3,c3b,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,
          c20,c205,c22,c23,c24,c27relay,c28matrix,c26shrine,c25reg,c29core,c21,c35cap,c36probe,c37control,c38agents,c39gates,c40,c41)

def run_all():
    """Structured entry point (4400): returns the findings list. Import-safe —
    importing this module never runs checks or writes files."""
    global RESULTS
    RESULTS = []
    for fn in CHECKS: fn()
    return RESULTS

def _summary(results):
    fails = [r for r in results if r["severity"] == "FAIL" and not r["ok"]]
    warns = [r for r in results if r["severity"] == "WARN" and not r["ok"]]
    return fails, warns

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    as_json = "--json" in argv
    results = run_all()
    fails, warns = _summary(results)
    if as_json:
        rev = None
        try:
            rev = subprocess.run(["git","-C",ROOT,"log","-1","--format=%H"],
                                 capture_output=True, text=True).stdout.strip() or None
        except Exception:
            pass
        print(json.dumps({"schema_version":"radiation.validation/1","revision":rev,
                          "results":results,
                          "summary":{"checks":len(results),"pass":len(results)-len(fails)-len(warns),
                                     "warn":len(warns),"fail":len(fails)}}))
    else:
        for r in results:
            icon = "✅ PASS" if r["ok"] else ("❌ FAIL" if r["severity"]=="FAIL" else "⚠️ WARN")
            print(f"{icon}  [check {r['check']}] {r['msg']}")
        print(f"\n{len(results)} checks run · {len(results)-len(fails)-len(warns)} pass · {len(warns)} warn · {len(fails)} fail")
    with open(os.path.join(ROOT,"validation_report.json"),"w") as fh:
        json.dump(results, fh, indent=1)
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
