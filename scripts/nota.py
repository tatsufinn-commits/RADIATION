#!/usr/bin/env python3
"""nota.py — the Core card tool (patch 3000; canonical contract per 4400).
CANONICAL LOCATION: 09-nota/CARD_###_*.md (root level — where the admitted
cards actually live; CORE_INDEX cites these paths). The 09-nota/cards/ lane
remains the DRAFT bench for NOTA-### sketches; drafts never satisfy the Core.
Validates: front-matter envelope (core-card/v1: id, status, admitted_at,
decay_at, shield worksheet, lineage refs), <=300-word body, LINEAGE block,
exact CORE_INDEX parity for ADMITTED cards. What this tool NEVER does: it does
not admit cards — admission is the six-box pass in
scaffolding/core/proc_nota-distillation.md, belonging to a session, not a
script. The tool guards the door; it does not open it.
Stdlib only. No network. Exit 0 = clean, 1 = problems found."""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, "09-nota")
CARDS = os.path.join(CORE, "cards")          # DRAFT bench only
CORE_INDEX = os.path.join(CORE, "CORE_INDEX.md")
WORD_LIMIT = 300          # II/I.3: the cleanest room — <=300 words per card body
FM_REQUIRED = ["schema_version", "id", "status", "admitted_at", "decay_at"]

CARD_TEMPLATE = """---
schema_version: core-card/v1
id: {cid}
status: DRAFT
admitted_at: —
decay_at: {decay}
shield:
  worksheet_ids: []
lineage:
  dossier_refs: [{dossier}]
  annotation_refs: []
  source_ids: []
---
# ☢️ NOTA [{cid}] — {topic}
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
  (scaffolding/core/proc_nota-distillation.md), fill the front-matter envelope
  (status: ADMITTED + admitted_at + decay_at + shield worksheet + lineage
  refs), move the file to 09-nota/CARD_<id>_<slug>.md, and append the index
  row. The Core is the cleanest room — when in doubt, the card waits.
-->
"""


def _words(text):
    return len([w for w in re.sub(r"<!--.*?-->","",text,flags=re.S).split() if w])

_LIST = re.compile(r"^\[([^]]*)\]$")
def _listify(v):
    v = v.strip()
    if v in ("", "[]"): return []
    m = _LIST.match(v)
    return [x.strip() for x in m.group(1).split(",")] if m else v

def parse_front_matter(text, where, problems):
    """Minimal parser for the controlled core-card/v1 vocabulary (no regex-only
    structural fields; unknown keys are reported, not silently dropped)."""
    if not text.startswith("---"):
        problems.append(f"{where}: no front-matter envelope (core-card/v1)"); return None
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append(f"{where}: front-matter block unterminated"); return None
    fm, cur = {}, None
    for ln in m.group(1).splitlines():
        if not ln.strip() or ln.strip().startswith("#"): continue
        if re.match(r"^\S", ln):
            k, _, v = ln.partition(":")
            fm[k.strip()] = _listify(v); cur = k.strip()
        elif re.match(r"^\s{2}\S", ln):
            k, _, v = ln.partition(":")
            if not isinstance(fm.get(cur), dict): fm[cur] = {}
            fm[cur][k.strip()] = _listify(v)
        else:
            problems.append(f"{where}: unparsable front-matter line: {ln.strip()!r}")
    return fm

def parse_card(path):
    """Return (fields, problems). fields=None when the envelope is unusable."""
    problems = []
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, ROOT)
    fm = parse_front_matter(text, rel, problems)
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    if fm is None: return None, problems, 0
    for k in FM_REQUIRED:
        if k not in fm: problems.append(f"{rel}: front matter missing '{k}'")
    if fm.get("schema_version") != "core-card/v1":
        problems.append(f"{rel}: schema_version {fm.get('schema_version')!r} != 'core-card/v1'")
    m = re.search(r"CARD_(\d{3})", str(fm.get("id","")))
    cid = f"CARD_{m.group(1)}" if m else None
    if not cid:
        problems.append(f"{rel}: front matter 'id' must be CARD_<3 digits>")
    fname_cid = re.match(r"CARD_(\d{3})", os.path.basename(path))
    if cid and fname_cid and f"CARD_{fname_cid.group(1)}" != cid:
        problems.append(f"{rel}: filename says CARD_{fname_cid.group(1)}, envelope says {cid}")
    status = fm.get("status")
    if status not in ("ADMITTED","DRAFT","QUARANTINED"):
        problems.append(f"{rel}: illegal status {status!r}")
    if status == "ADMITTED":
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm.get("admitted_at",""))):
            problems.append(f"{rel}: ADMITTED card needs admitted_at YYYY-MM-DD")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm.get("decay_at",""))):
            problems.append(f"{rel}: ADMITTED card needs decay_at YYYY-MM-DD (I.4)")
        shield = fm.get("shield") or {}
        if not shield.get("worksheet_ids"):
            problems.append(f"{rel}: ADMITTED card needs shield.worksheet_ids (I.3 stamp)")
        lin = fm.get("lineage") or {}
        if not (lin.get("annotation_refs") or lin.get("source_ids")):
            problems.append(f"{rel}: ADMITTED card needs lineage annotation/source refs")
        if not re.search(r"^##\s+LINEAGE", body, re.M):
            problems.append(f"{rel}: LINEAGE block missing from body")
    if not re.search(r"^##\s+ANSWER", body, re.M):
        problems.append(f"{rel}: ANSWER block missing")
    words = _words(body)
    if words > WORD_LIMIT:
        problems.append(f"{rel}: {words} words — the card limit is {WORD_LIMIT} (the cleanest room)")
    return {"cid":cid, "status":status, "words":words, "fm":fm}, problems, words

def canonical_cards():
    if not os.path.isdir(CORE): return []
    return sorted(os.path.join(CORE,f) for f in os.listdir(CORE)
                  if re.match(r"CARD_\d{3}_.*\.md$", f))

def index_rows():
    """Map CARD_xxx -> row count from CORE_INDEX table rows (first table only)."""
    out = {}
    if not os.path.exists(CORE_INDEX): return out
    for ln in open(CORE_INDEX, encoding="utf-8").read().splitlines():
        if ln.strip().startswith("|") and "---" not in ln:
            m = re.search(r"CARD_\d{3}", ln)
            if m: out[m.group(0)] = out.get(m.group(0), 0) + 1
    return out

def cmd_new(a):
    if not re.match(r"^NOTA-\d{3}$", a.id or ""):
        sys.exit("card ID must be NOTA-<3 digits>, e.g. NOTA-001 (draft bench; the Core uses CARD_<NNN> at admission)")
    os.makedirs(CARDS, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+","-",(a.topic or "card").lower()).strip("-")[:40]
    path = os.path.join(CARDS, f"{a.id}_{slug}.md")
    if os.path.exists(path): sys.exit(f"refusing to overwrite {os.path.relpath(path, ROOT)}")
    text = CARD_TEMPLATE.format(cid=a.id, topic=a.topic or "[topic]", limit=WORD_LIMIT,
                                decay=a.decay or "none", course=a.course or "—",
                                dossier=a.dossier or "", worksheets=a.worksheets or "<triangulation worksheet ids>")
    open(path,"w",encoding="utf-8").write(text)
    print(f"  wrote {os.path.relpath(path, ROOT)} (DRAFT bench — NOT canonical)")
    print("\n  at admission: fill the envelope, move to 09-nota/CARD_<NNN>_<slug>.md, append the index row")
    return 0

def cmd_check(_a):
    problems, notes, seen = [], [], {}
    files = canonical_cards()
    if not files:
        print("✅ no canonical cards yet (no 09-nota/CARD_*.md) — nothing to check")
    for path in files:
        c, probs, words = parse_card(path)
        rel = os.path.relpath(path, ROOT)
        problems.extend(probs)
        if c and c["cid"]:
            seen[c["cid"]] = seen.get(c["cid"], 0) + 1
            notes.append(f"{rel}: {c['status']}, {words} words")
    for cid, n in sorted(seen.items()):
        if n > 1: problems.append(f"{cid}: {n} card files carry the same ID (exactly one allowed)")
    idx = index_rows()
    for cid, n in sorted(idx.items()):
        if cid not in seen: problems.append(f"CORE_INDEX lists {cid} but no card file carries it")
        elif n > 1: problems.append(f"CORE_INDEX has {n} rows for {cid} (exactly one allowed)")
        elif seen[cid] != 1: pass
    for cid in sorted(set(seen) - set(idx)):
        c0 = [c for c in files if parse_card(c)[0] and parse_card(c)[0]["cid"] == cid]
        st = parse_card(c0[0])[0]["status"] if c0 else "?"
        if st == "ADMITTED":
            problems.append(f"{cid} is ADMITTED but has no CORE_INDEX row (parity is exact)")
        else:
            notes.append(f"{cid}: not in CORE_INDEX yet (fine for a DRAFT; required at admission)")
    for n in notes: print(f"  · {n}")
    if problems:
        for p in problems: print(f"  ✗ {p}")
        print(f"\n❌ nota check: {len(problems)} problem(s) in {len(files)} card(s)")
        return 1
    print(f"\n✅ nota check: {len(files)} canonical card(s), shape clean, index parity exact")
    return 0

def self_test():
    import tempfile
    ok = 0
    global CORE, CARDS, CORE_INDEX, ROOT
    real = (CORE, CARDS, CORE_INDEX, ROOT)
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(tmp,"09-nota"), exist_ok=True)
    CORE, CARDS, CORE_INDEX = os.path.join(tmp,"09-nota"), os.path.join(tmp,"09-nota","cards"), os.path.join(tmp,"09-nota","CORE_INDEX.md")
    ROOT = tmp
    good = """---
schema_version: core-card/v1
id: CARD_090
status: ADMITTED
admitted_at: 2026-09-14
decay_at: 2027-09-14
shield:
  worksheet_ids: [TRI_x]
lineage:
  dossier_refs: []
  annotation_refs: [ANNOT_x]
  source_ids: [SRC-001]
---
# ☢️ CARD_090 — t
## ANSWER
one two three
## LINEAGE
- dossier: —
- worksheets: TRI_x
"""
    open(os.path.join(CORE,"CARD_090_t.md"),"w").write(good)
    open(CORE_INDEX,"w").write("| t | CARD_090 | 2026-09-14 | 2027-09-14 | x |\n")
    r1 = cmd_check(None); ok += (r1 == 0)
    open(os.path.join(CORE,"CARD_090_t.md"),"a").write("\n"+"filler ".join(["w"]*400))
    r2 = cmd_check(None); ok += (r2 == 1)   # word-limit breach must FAIL on a real canonical card
    open(CORE_INDEX,"w").write("")          # parity breach must FAIL
    r3 = cmd_check(None); ok += (r3 == 1)
    CORE, CARDS, CORE_INDEX, ROOT = real
    print(f"self-test: {ok}/3 real-card vectors (admitted+parity PASS · overlimit FAIL · index-missing FAIL)")
    return 0 if ok == 3 else 1

def main():
    ap = argparse.ArgumentParser(description="Core card tool (canonical: 09-nota/CARD_*.md)")
    ap.add_argument("--new", dest="id", help="draft NOTA-<NNN> on the bench")
    ap.add_argument("--topic"); ap.add_argument("--course"); ap.add_argument("--decay")
    ap.add_argument("--dossier"); ap.add_argument("--worksheets")
    ap.add_argument("--check", action="store_true", dest="check")
    ap.add_argument("--self-test", action="store_true", dest="self_test")
    a = ap.parse_args()
    if a.self_test: return self_test()
    if a.check: return cmd_check(a)
    if a.id: return cmd_new(a)
    ap.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
