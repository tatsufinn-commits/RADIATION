#!/usr/bin/env python3
"""P-03: compute decay expiries FROM registry rows (arithmetic, not memory).
Reads docs/KNOWLEDGE_REGISTRY.md; any row with Last verified + Freq(90d|1yr)
past expiry is reported. Output is a proposed DECAY_REGISTER row; a human/
session appends it (register stays append-only, script never writes)."""
import datetime, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
today = datetime.date(2026, 9, 12) if "--fixed" in sys.argv else datetime.date.today()
txt = open(os.path.join(ROOT, "docs/KNOWLEDGE_REGISTRY.md"), encoding="utf-8").read()
blocks = re.split(r"\n## (?=K-)", txt)
n = 0
for b in blocks[1:]:
    kid = b.split(" ")[0].strip()
    lv = re.search(r"Last verified:\s*(\d{4}-\d{2}-\d{2})", b)
    fq = re.search(r"Freq:\s*(90d|1yr|none)", b)
    if not lv or not fq or fq.group(1) == "none": continue
    d = datetime.date.fromisoformat(lv.group(1))
    exp = d + datetime.timedelta(days=90 if fq.group(1) == "90d" else 365)
    if exp < today:
        n += 1
        print(f"EXPIRED  {kid}: last_verified {d} + {fq.group(1)} -> expired {exp}")
        print(f"  proposed row: | {today} | currency of {kid} past {fq.group(1)} window | docs/KNOWLEDGE_REGISTRY.md {kid} | grade currency aspect -> [DECAYED] | {fq.group(1)} expired {exp} | AWAITING RE-VERIFICATION |")
print(f"\n{n} expired object(s) computed from registry")
