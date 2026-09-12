#!/usr/bin/env python3
"""RADIATION knowledge-regression suite — P-01 §3.
A LOCKED assertion asserts a verified value's pattern exists in its primary
source file and is uncontradicted in every card that cites it. Locking is only
lawful for Shield-Stamped (I.3) or [D]-primary claims. PENDING assertions are
reported and skipped. Exit 1 on any locked-assertion failure."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sys.argv[sys.argv.index("--file")+1] if "--file" in sys.argv else os.path.join(ROOT,"tests/knowledge_assertions.json")
data = json.load(open(path, encoding="utf-8"))
fails, locked_n, pending_n = [], 0, 0
for a in data["assertions"]:
    if not a.get("locked"):
        pending_n += 1
        print(f"⏸  PENDING [{a['id']}] {a['claim'][:70]} — {a.get('pending_reason','awaiting lock')}")
        continue
    locked_n += 1
    src = os.path.join(ROOT, a["assert_in"])
    if not os.path.exists(src):
        fails.append(a["id"]); print(f"❌ FAIL [{a['id']}] source missing: {a['assert_in']}"); continue
    text = open(src, encoding="utf-8", errors="replace").read()
    if not re.search(a["value_pattern"], text):
        fails.append(a["id"]); print(f"❌ FAIL [{a['id']}] pattern /{a['value_pattern']}/ ABSENT from {a['assert_in']}"); continue
    ok = True
    for card in a.get("appears_in", []):
        cp = os.path.join(ROOT, card)
        if os.path.exists(cp) and not re.search(a["value_pattern"], open(cp, encoding="utf-8", errors="replace").read()):
            fails.append(a["id"]); print(f"❌ FAIL [{a['id']}] {card} cites K but lacks /{a['value_pattern']}/ — value drifted"); ok = False
    reg = os.path.join(ROOT, "docs/KNOWLEDGE_REGISTRY.md")
    if a.get("source_kid") and not (os.path.exists(reg) and a["source_kid"] in open(reg, encoding="utf-8").read()):
        print(f"⚠️ WARN [{a['id']}] source_kid {a['source_kid']} not in registry (P-03 pending)")
    if ok: print(f"✅ PASS [{a['id']}] {a['claim'][:70]}")
print(f"\n{locked_n} locked · {pending_n} pending · {len(fails)} failed")
sys.exit(1 if fails else 0)
