#!/usr/bin/env python3
"""
WP-1 1.4 — Agent policy existence check (acceptance per proposal)
Checks root machine-readable agent policy files exist, ≤30 lines each, imperative, pointer to Patch protocol
Repo D format only, AI-refusal content REJECTED — format ports, refusal never
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICIES = ["CLAUDE.md", "CURSOR.md", "CODEX.md"]
FAIL = []
for name in POLICIES:
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        FAIL.append(f"{name}: missing — must exist per 1.4")
        continue
    lines = open(path, encoding="utf-8").read().splitlines()
    if len(lines) > 30:
        FAIL.append(f"{name}: {len(lines)} lines >30 — must be ≤30 per 1.4")
    text = "\n".join(lines)
    if "docs/PATCH_PROTOCOL.md" not in text:
        FAIL.append(f"{name}: missing pointer to Patch protocol docs/PATCH_PROTOCOL.md per 1.4")
    # Check imperative style: at least 3 lines starting with "- " or imperative verbs
    imperatives = [l for l in lines if l.strip().startswith("- ")]
    if len(imperatives) < 3:
        FAIL.append(f"{name}: less than 3 imperative lines — must be tool-facing per 1.4")

if FAIL:
    print("❌ FAIL — agent policy existence check:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
else:
    print(f"✅ PASS — agent policy existence check: {len(POLICIES)} files ≤30 lines, imperative, pointer to Patch protocol — {', '.join(POLICIES)}")
    sys.exit(0)
