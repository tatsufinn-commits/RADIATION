#!/usr/bin/env python3
"""module_scaffold.py — born-valid study modules (patch 3000).
Emits Brain/long_term/modules/ skeletons that PASS validator check 18 from birth:
every depth_level's required sections, trap/worked-example/glossary/drill quotas,
K-ID, yield_rank, LIMITS. A scaffold that is born invalid is how conventions die —
so the tool mirrors check 18's rules and refuses to write anything that would fail.
Stdlib only. No network.
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MDIR = os.path.join(ROOT, "Brain", "long_term", "modules")

L2_SECTIONS = ["WHY THIS MATTERS", "CORE CONTENT", "AUTHORITY TABLE",
               "NUMBERS TO KNOW", "EXAM TRAPS", "LINEAGE"]      # + WORKED EXAMPLE (h3)
TRAPS = {3: 4, 4: 8, 5: 8}
WORKED = {3: 1, 4: 2, 5: 2}
GLOSSARY_MIN = 10
DRILL_MIN = 10


def build(level, course, topic, kid, yield_rank="5"):
    L = []
    L.append(f"# {course} — {topic} (L{level} module)")
    L.append(f"depth_level: {level}")
    L.append(f"yield_rank: {yield_rank}")
    L.append(f"K-ID: {kid or 'K-MOD-XXX'}")
    L.append("")
    L.append("LIMITS: [what this module deliberately does NOT cover — mandatory line]")
    L.append("")
    L.append("## WHY THIS MATTERS")
    L.append("[why this module earns its place in the vault]")
    L.append("")
    L.append("## CORE CONTENT")
    L.append("[the module's actual teaching content — graded claims only (I.2)]")
    L.append("")
    L.append("## AUTHORITY TABLE")
    L.append("| Claim | Grade | Source |")
    L.append("|---|---|---|")
    L.append("| [claim] | [D]/[R]/[O] | [K-ID or citation] |")
    L.append("")
    L.append("## NUMBERS TO KNOW")
    L.append("- **[value]** — [what it governs]")
    L.append("")
    n_traps = TRAPS.get(level, 2)
    L.append("## EXAM TRAPS")
    for i in range(1, n_traps + 1):
        L.append(f"**TRAP {i}** — [the wrong answer everyone picks, and why]")
    L.append("")
    L.append("## WORKED EXAMPLE")
    for w in range(1, WORKED.get(level, 1) + 1):
        L.append(f"### Worked Example {w}")
        L.append("[problem -> reasoning -> answer, every number cited]")
        L.append("")
    L.append("## GLOSSARY")
    for i in range(1, GLOSSARY_MIN + 1):
        L.append(f"- **Term {i}** — [definition]")
    L.append("")
    L.append("## LINEAGE")
    L.append("- dossier: [Brain/long_term/... path this module was distilled from]")
    L.append("- worksheets: [triangulation worksheet ids]")
    L.append("")
    if level >= 5:
        L.append("## DRILL")
        for q in range(1, DRILL_MIN + 1):
            L.append(f"Q{q}. [question]")
        L.append("")
        L.append("## CASE STUDIES")
        L.append("- [case 1: brief -> requirement -> resolution]")
        L.append("")
    return "\n".join(L) + "\n"


def validate_module(text, level):
    """Mirror of validator check 18 — kept in step deliberately; the comment in
    validate.py points here and vice versa. Change both together."""
    bad = []
    if not re.search(rf"depth_level:\s*{level}", text): bad.append(f"depth_level: {level} missing")
    if not re.search(r"yield_rank:\s*(?!\|)[0-9]", text): bad.append("yield_rank empty/non-numeric")
    if not re.search(r"K-(?:MOD|LAW|STD|CUR|BK|REF|MTH|EXT)\S*", text): bad.append("no K-ID")
    if "LIMITS" not in text: bad.append("LIMITS line missing")
    if level >= 2:
        for h in L2_SECTIONS + ["WORKED EXAMPLE"]:
            if h not in text: bad.append(f"L{level} missing section {h}")
    traps = len(re.findall(r"\*\*TRAP \d", text))
    worked = len(re.findall(r"### Worked Example", text))
    gloss = len(re.findall(r"- \*\*[A-Za-z]", text.split("GLOSSARY", 1)[1])) if "GLOSSARY" in text else 0
    if level >= 3 and (traps < 4 or gloss < GLOSSARY_MIN or worked < 1):
        bad.append(f"L{level} needs >=4 traps/>={GLOSSARY_MIN} glossary/>=1 worked (has {traps}/{gloss}/{worked})")
    if level >= 4 and (traps < 8 or worked < 2):
        bad.append(f"L{level} needs >=8 traps & >=2 worked (has {traps}/{worked})")
    if level == 5:
        drill = len(re.findall(r"^\s*Q\d+", text, re.M))
        if not re.search(r"^##\s+DRILL\b", text, re.M) or drill < DRILL_MIN:
            bad.append(f"L5 claims but drill absent/short ({drill} items)")
        if "CASE STUD" not in text.upper():
            bad.append("L5 without case studies")
    return bad


def index_state():
    """(files, rows, index_path). rows = -1 when MODULES_INDEX.md is absent —
    the same sentinel check 18 uses — so 'no index file' can never read as parity.
    (Probe-caught bug: the 0,0 early-return told cmd_new 'parity OK' right after
    writing the first module, masking the exact mismatch check 18 flags.)"""
    idx = os.path.join(MDIR, "MODULES_INDEX.md")
    files = len([f for f in os.listdir(MDIR) if f.endswith(".md") and f != "MODULES_INDEX.md"]) \
        if os.path.isdir(MDIR) else 0
    if not os.path.exists(idx):
        return files, -1, idx
    rows = len([l for l in open(idx, encoding="utf-8").read().splitlines()
                if l.strip().startswith("|") and "---" not in l.replace("|", "")]) - 1
    return files, rows, idx


def cmd_new(a):
    level = a.level
    if level not in (1, 2, 3, 4, 5):
        sys.exit("level must be 1-5")
    text = build(level, a.course, a.topic, a.kid, str(a.yield_rank))
    bad = validate_module(text, level)
    if bad:
        sys.exit("scaffold would be born invalid — refusing to write:\n  " + "\n  ".join(bad))
    os.makedirs(MDIR, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", f"{a.course}-{a.topic}".lower()).strip("-")[:60]
    path = os.path.join(MDIR, f"L{level}_{slug}.md")
    if os.path.exists(path) and not a.force:
        sys.exit(f"refusing to overwrite {os.path.relpath(path, ROOT)} (use --force)")
    open(path, "w", encoding="utf-8").write(text)
    print(f"  wrote {os.path.relpath(path, ROOT)} (validated against the check-18 mirror)")
    files, rows, idx = index_state()
    if rows == -1:
        print(f"  ⚠ no MODULES_INDEX.md yet — check 18 counts that as a mismatch. Create it with this row:")
        print(f"    # 🏗️ MODULES INDEX (Brain/long_term/modules/MODULES_INDEX.md)")
        print(f"    | Module | Level | K-ID | File |")
        print(f"    |---|---|---|---|")
        print(f"    | {a.course} — {a.topic} | L{level} | {a.kid or 'K-MOD-XXX'} | {path.split('/')[-1]} |")
    elif files != rows:
        print(f"  ⚠ MODULES_INDEX.md parity: {files} file(s) vs {rows} row(s) — add the row "
              f"(check 18 enforces parity). Suggested row:")
        print(f"    | {a.course} — {a.topic} | L{level} | {a.kid or 'K-MOD-XXX'} | {path.split('/')[-1]} |")
    else:
        print(f"  index parity OK ({files} file(s))")
    return 0


def cmd_list(_a):
    if not os.path.isdir(MDIR):
        print("  no modules yet (Brain/long_term/modules/ absent)")
        return 0
    files, rows, idx = index_state()
    status = "OK" if files == rows and rows != -1 else \
        ("NO INDEX FILE — check 18 counts -1 rows: mismatch" if rows == -1
         else "MISMATCH — check 18 will flag this")
    print(f"  modules: {files} file(s) · index rows: {rows} · parity: {status}")
    for f in sorted(os.listdir(MDIR)):
        if f.endswith(".md") and f != "MODULES_INDEX.md":
            t = open(os.path.join(MDIR, f), encoding="utf-8").read()
            m = re.search(r"depth_level:\s*(\d)", t)
            bad = validate_module(t, int(m.group(1))) if m else ["no depth_level"]
            mark = "✅" if not bad else "✗ " + "; ".join(bad[:2])
            print(f"  {mark} {f}")
    return 0


def self_test():
    ok, fails = 0, []
    def check(name, cond):
        nonlocal ok
        if cond: ok += 1
        else: fails.append(name)
    for lvl in (1, 2, 3, 4, 5):
        t = build(lvl, "TEST", "self-test module", "K-MOD-999")
        bad = validate_module(t, lvl)
        check(f"L{lvl} scaffold is born valid", not bad)
    # a sabotaged scaffold must fail its own mirror
    t = build(3, "TEST", "sabotage", "K-MOD-999").replace("**TRAP 1**", "TRAP ONE")
    check("sabotaged traps detected", bool(validate_module(t, 3)))
    t = build(5, "TEST", "sabotage2", "K-MOD-999").replace("## DRILL\n", "## DRILLS\n")
    check("'## DRILLS' rejected (word-boundary rule, mirrors hardened check 18)", bool(validate_module(t, 5)))
    print(f"✅ module_scaffold self-test: {ok} passed, {len(fails)} failed" + (f" — {fails}" if fails else ""))
    return not fails


def main():
    p = argparse.ArgumentParser(description="Born-valid module scaffolds (check-18 mirror).")
    p.add_argument("--new", action="store_true", help="emit a new module scaffold")
    p.add_argument("--level", type=int, help="depth level 1-5")
    p.add_argument("--course", required="--new" in sys.argv, help="e.g. AR153P")
    p.add_argument("--topic", help="module topic")
    p.add_argument("--kid", help="K-MOD-XXX id (placeholder if omitted)")
    p.add_argument("--yield-rank", dest="yield_rank", type=int, default=5)
    p.add_argument("--force", action="store_true")
    p.add_argument("--list", action="store_true", help="module inventory + parity")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        sys.exit(0 if self_test() else 1)
    if a.list:
        sys.exit(cmd_list(a))
    if a.new:
        sys.exit(cmd_new(a))
    p.print_help()


if __name__ == "__main__":
    main()
