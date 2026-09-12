#!/usr/bin/env python3
"""P-05 Anki exporter (stdlib port of TAMAKEE export-anki.js).
Usage: export_anki.py --set <set.json> [--out <file.tsv>]
front = brief · back = key + rationale + citations · tags = K-ID, context, difficulty, yield."""
import json, sys
def arg(f, d=None): return sys.argv[sys.argv.index(f)+1] if f in sys.argv else d
S = json.load(open(arg("--set"), encoding="utf-8"))
rows = []
for it in S["items"]:
    opts = "  ".join(f"({k}) {v}" for k, v in it["options"].items())
    front = f"{it['brief']}  {opts}".replace("\t", " ").replace("\n", " ")
    back = f"KEY: ({it['key']}) {it['options'][it['key']]} — {it['rationale']} [{'; '.join(it['citations'])}]".replace("\t", " ").replace("\n", " ")
    tags = " ".join([it["k_id"], S["context"].replace(" ", "_").replace("/", "-"), it["difficulty"], f"yield{it['yield_rank']}"])
    rows.append(f"{front}\t{back}\t{tags}")
out = arg("--out")
data = "\n".join(rows) + "\n"
open(out, "w", encoding="utf-8").write(data) if out else sys.stdout.write(data)
print(f"# {len(rows)} cards exported", file=sys.stderr)
