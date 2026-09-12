#!/usr/bin/env python3
"""P-05 drill grader (stdlib port of TAMAKEE grade-exam.js).
Usage: grade_exam.py --set <set.json> --answers <answers.json> [--tally]
Scores against the STORED key only (never memory). Prints report + proposed
mastery_ledger row; never writes registers itself."""
import json, sys, datetime
def arg(f): return sys.argv[sys.argv.index(f)+1]
S = json.load(open(arg("--set"), encoding="utf-8"))
A = json.load(open(arg("--answers"), encoding="utf-8"))
answers, meta = A["answers"], A.get("meta", "")
score, cats, misses = 0, {}, []
print(f"═══ DRILL REPORT — {S['set_id']} ({S['context']}) ═══")
if meta: print(f"⚠ answer provenance: {meta}")
for it in S["items"]:
    given = answers.get(it["id"], "—")
    ok = given == it["key"]
    score += ok
    if ok:
        print(f"✅ {it['id']} {given}  correct — {it['citations'][0]}")
    else:
        mb = it["distractors"].get(given, {})
        cat = mb.get("category", "D") if isinstance(mb, dict) else "D"
        cats[cat] = cats.get(cat, 0) + 1
        misses.append((it["id"], given, it["key"], cat))
        why = mb.get("mistake", "not a listed distractor — possible misread (D)") if isinstance(mb, dict) else str(mb)
        print(f"❌ {it['id']} {given} → key {it['key']} [cat {cat}] {why}")
        print(f"     rationale: {it['rationale'][:120]}")
n = len(S["items"]); pct = 100*score//n
interval = 7 if pct >= 90 else (3 if pct >= 70 else 1)
nxt = (datetime.date(2026,9,12) + datetime.timedelta(days=interval)).isoformat()
catstr = ", ".join(f"{k}×{v}" for k, v in sorted(cats.items())) or "—"
print(f"\nSCORE: {score}/{n} ({pct}%) · error cats: {catstr} · next review: {nxt} (+{interval}d)")
print(f"proposed mastery row: | {S['target']} | 2026-09-12 | {score}/{n} | {catstr} | +1 attempt | {nxt} | (compare prior) |")
for i, g, k, c in misses:
    print(f"mistake-bank candidate: {i} answered {g} (key {k}, cat {c}) — file if genuine, tagged with attempt provenance")
