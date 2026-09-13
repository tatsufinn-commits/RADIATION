#!/usr/bin/env python3
"""nota.py — the Core card tool (patch 3000).
Validates the SHAPE of Core cards (09-nota/): the constitution's cleanest room,
<=300 words, lineage mandatory, Shield-Stamped claims. What this tool NEVER does:
it does not admit cards. Admission is the six-box pass in
scaffolding/core/proc_nota-distillation.md (eligibility -> surgeon pass), and it
belongs to a session, not to a script. The tool guards the door; it does not open it.
Stdlib only. No network. Exit 0 = clean, 1 = problems found.
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, "09-nota", "cards")
CORE_INDEX = os.path.join(ROOT, "09-nota", "CORE_INDEX.md")
WORD_LIMIT = 300          # II/I.3: the cleanest room — <=300 words per card

CARD_TEMPLATE = """# ☢️ NOTA [{cid}] — {topic}
**status:** DRAFT · **admitted:** — · **decay:** {decay} · **course:** {course}
**claim:** C1: "<one answerable claim>" SHIELD[S-ids, date]

## ANSWER
<!-- answer-first, plain language, grade markers kept inline ([D]/[R]/[O]);
     the WHOLE card must stay <= {limit} words — nota.py --check enforces it -->
[to be distilled by the session running proc_nota-distillation.md]

## LINEAGE
- dossier: {dossier}
- worksheets: {worksheets}
- sources: [K-IDs or citations]

<!--
  ADMISSION: this tool never admits. Run the six-box pass
  (scaffolding/core/proc_nota-distillation.md), flip status to ADMITTED with the
  date, and append the index row this command printed. The Core is the cleanest
  room in the facility — when in doubt, the card waits.
-->
"""


def _words(text):
    return len([w for w in re.sub(r"<!--.*?-->", "", text, flags=re.S).split() if w])


def cmd_new(a):
    if not re.match(r"^NOTA-\d{3}$", a.id or ""):
        sys.exit("card ID must be NOTA-<3 digits>, e.g. NOTA-001")
    os.makedirs(CARDS, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", (a.topic or "card").lower()).strip("-")[:40]
    path = os.path.join(CARDS, f"{a.id}_{slug}.md")
    if os.path.exists(path):
        sys.exit(f"refusing to overwrite {os.path.relpath(path, ROOT)}")
    text = CARD_TEMPLATE.format(cid=a.id, topic=a.topic or "[topic]", limit=WORD_LIMIT,
                                decay=a.decay or "none", course=a.course or "—",
                                dossier=a.dossier or "<Brain/long_term/... path>",
                                worksheets=a.worksheets or "<triangulation worksheet ids>")
    open(path, "w", encoding="utf-8").write(text)
    rel = os.path.relpath(path, ROOT)
    print(f"  wrote {rel}")
    print(f"\n  append to 09-nota/CORE_INDEX.md when ADMITTED:")
    print(f"  | {a.topic} | {a.id} | — | {a.decay or 'none'} | dossier: {a.dossier or '<path>'} |")
    print(f"\n  next: distill the answer, run the six-box pass, then nota.py --check")
    return 0


def parse_card(text):
    """Extract the fields --check asserts on. Tolerant: reports what is missing."""
    first = text.splitlines()[0] if text else ""
    m = re.search(r"NOTA-(\d{3})", first)
    cid = f"NOTA-{m.group(1)}" if m else None
    status = "ADMITTED" if re.search(r"\*\*status:\*\*\s*ADMITTED", text) else "DRAFT"
    words = _words(text)
    has_lineage = bool(re.search(r"^##\s+LINEAGE", text, re.M)) and \
        bool(re.search(r"- dossier:\s*\S+", text)) and \
        bool(re.search(r"- worksheets:\s*\S+", text))
    has_stamp = bool(re.search(r"SHIELD\[[^\]]+\]", text))
    has_decay = bool(re.search(r"\*\*decay:\*\*\s*\S+", text))
    return {"cid": cid, "status": status, "words": words, "lineage": has_lineage,
            "stamp": has_stamp, "decay": has_decay}


def index_ids():
    if not os.path.exists(CORE_INDEX):
        return set()
    return set(re.findall(r"NOTA-\d{3}", open(CORE_INDEX, encoding="utf-8").read()))


def cmd_check(_a):
    problems, notes = [], []
    if not os.path.isdir(CARDS):
        print("✅ no cards yet (09-nota/cards/ absent) — nothing to check")
        return 0
    files = sorted(f for f in os.listdir(CARDS) if f.endswith(".md"))
    seen_ids = set()
    for f in files:
        text = open(os.path.join(CARDS, f), encoding="utf-8").read()
        c = parse_card(text)
        rel = f"09-nota/cards/{f}"
        if not c["cid"]:
            problems.append(f"{rel}: no NOTA-<NNN> id in the title")
            continue
        seen_ids.add(c["cid"])
        if c["words"] > WORD_LIMIT:
            problems.append(f"{rel}: {c['words']} words — the card limit is {WORD_LIMIT} (the cleanest room)")
        if not c["lineage"]:
            problems.append(f"{rel}: LINEAGE block incomplete (dossier + worksheets are mandatory)")
        if not c["stamp"]:
            problems.append(f"{rel}: no SHIELD[...] stamp on the claim — not eligible for admission (I.3)")
        if not c["decay"]:
            problems.append(f"{rel}: no **decay:** tag (I.4)")
        if c["status"] == "ADMITTED":
            notes.append(f"{rel}: ADMITTED, {c['words']} words")
        else:
            notes.append(f"{rel}: DRAFT, {c['words']} words")
    idx = index_ids()
    for cid in sorted(idx - seen_ids):
        problems.append(f"CORE_INDEX lists {cid} but no card file carries it")
    for cid in sorted(seen_ids - idx):
        notes.append(f"{cid}: not in CORE_INDEX yet (fine for a DRAFT; required at admission)")
    for n in notes:
        print(f"  · {n}")
    if problems:
        for p in problems:
            print(f"  ✗ {p}")
        print(f"\n❌ nota check: {len(problems)} problem(s) in {len(files)} card(s)")
        return 1
    print(f"\n✅ nota check: {len(files)} card(s), shape clean")
    return 0


def self_test():
    ok, fails = 0, []
    def check(name, cond):
        nonlocal ok
        if cond: ok += 1
        else: fails.append(name)
    good = CARD_TEMPLATE.format(cid="NOTA-001", topic="t", limit=WORD_LIMIT, decay="none",
                                course="c", dossier="Brain/long_term/x.md", worksheets="W-1")
    c = parse_card(good)
    check("valid scaffold parses", c["cid"] == "NOTA-001" and c["lineage"] and c["stamp"] and c["decay"])
    check("scaffold is within the word limit", c["words"] <= WORD_LIMIT)
    over = good.replace("[to be distilled by the session running proc_nota-distillation.md]",
                        " ".join(["word"] * (WORD_LIMIT + 1)))
    check("over-limit card detected", parse_card(over)["words"] > WORD_LIMIT)
    nolineage = good.replace("## LINEAGE\n- dossier: Brain/long_term/x.md\n- worksheets: W-1\n", "")
    check("missing lineage detected", not parse_card(nolineage)["lineage"])
    nostamp = good.replace("SHIELD[S-ids, date]", "(unstamped)")
    check("missing SHIELD stamp detected", not parse_card(nostamp)["stamp"])
    admitted = good.replace("**status:** DRAFT", "**status:** ADMITTED")
    check("status flip detected", parse_card(admitted)["status"] == "ADMITTED")
    print(f"✅ nota self-test: {ok} passed, {len(fails)} failed" + (f" — {fails}" if fails else ""))
    return not fails


def main():
    p = argparse.ArgumentParser(description="Core card tool — validates shape, never admits.")
    p.add_argument("--new", dest="id", metavar="NOTA-NNN", help="scaffold a new card")
    p.add_argument("--topic"); p.add_argument("--course"); p.add_argument("--decay")
    p.add_argument("--dossier", help="long_term dossier path for the lineage block")
    p.add_argument("--worksheets", help="triangulation worksheet ids")
    p.add_argument("--check", action="store_true", help="validate every card's shape + index parity")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        sys.exit(0 if self_test() else 1)
    if a.check:
        sys.exit(cmd_check(a))
    if a.id:
        sys.exit(cmd_new(a))
    p.print_help()


if __name__ == "__main__":
    main()
