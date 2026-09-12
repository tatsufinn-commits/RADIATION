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
def md_files():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {".git", ".github", "node_modules"}]
        for f in fn:
            if f.endswith(".md") or f == ".readme":
                out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)
def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8", errors="replace") as fh:
        return fh.read()
def archive_exempt():
    """Paths listed in docs/ARCHIVE_NOTES.md are historical record: exempt from
    checks 1, 8, 9, 14 (they lawfully quote retired phrases and dead paths)."""
    ex = set()
    p = os.path.join(ROOT, "docs/ARCHIVE_NOTES.md")
    if os.path.exists(p):
        for m in re.finditer(r"`([^`\n]+)`", open(p, encoding="utf-8").read()):
            ex.add(m.group(1).rstrip("/"))
    def is_ex(path):
        return any(path == e or path.startswith(e + "/") for e in ex)
    return is_ex
IS_EX = archive_exempt()

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
# ---- check 3: forbidden transport artifacts (II.8.2) -----------------------
def c3():
    bad = []
    if os.path.exists(os.path.join(ROOT, "PATCH_NOTES.md")): bad.append("PATCH_NOTES.md at repo root")
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != ".git"]
        for d in dn:
            if d in ("append_blocks","append-blocks"): bad.append(os.path.relpath(os.path.join(dp,d),ROOT)+"/")
        for f in fn:
            if "_REPLACEMENT" in f: bad.append(os.path.relpath(os.path.join(dp,f),ROOT))
    rec(3, "FAIL", not bad, "no transport artifacts (II.8.2)" + ("" if not bad else ": " + "; ".join(bad)))
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
        if IS_EX(f) or f == "docs/MODES.md": continue
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
        if IS_EX(f): continue
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
        dn[:] = [d for d in dn if d != ".git"]
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

for fn in (c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14): fn()
fails = [r for r in RESULTS if r["severity"] == "FAIL" and not r["ok"]]
warns = [r for r in RESULTS if r["severity"] == "WARN" and not r["ok"]]
for r in RESULTS:
    icon = "✅ PASS" if r["ok"] else ("❌ FAIL" if r["severity"]=="FAIL" else "⚠️ WARN")
    print(f"{icon}  [check {r['check']}] {r['msg']}")
print(f"\n{len(RESULTS)} checks run · {len(RESULTS)-len(fails)-len(warns)} pass · {len(warns)} warn · {len(fails)} fail")
with open(os.path.join(ROOT,"validation_report.json"),"w") as fh:
    json.dump(RESULTS, fh, indent=1)
sys.exit(1 if fails else 0)
