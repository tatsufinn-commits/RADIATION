# PROPOSAL P-01 — canon companion (II.2 strike + II.8.5 + doc rewrites) · ratify: "ratify P-01 canon companion"
**Re-homed 2026-09-12 (Wave 1&2 closure): carriers moved from canonical dirs to lawful proposal homes per IV.2/IV.4/scaffolding-README §4. Text unchanged except path-reference hygiene. NOTHING below is applied until the Commander's ratification line.**


---
## ◈ Companion analysis

# P-01 PATCH 2 OF 2 (🟠) — BLOCKED ANALYSIS, AWAITING RATIFICATION
**REQUIRES EXPLICIT COMMANDER RATIFICATION — nothing below is applied.**
## What P-01 §4.2 + the closure clause require, with side-by-side text:
1. **II.2 final sentence — strike-through per IV.3:**
   OLD: "In Patches, append-only files travel as APPEND BLOCKS, never full-file replacements."
   NEW: "~~In Patches, append-only files travel as APPEND BLOCKS, never full-file replacements.~~ *(Struck 2026-09-12: superseded by II.8.1 — append-only files are appended IN PLACE and travel pre-merged.)*"
2. **NEW closure clause (proposed as II.8.5):** "No session closes while `scripts/validate.py` exits non-zero, unless the Commander waives it in writing. The surgeon treats an unwaived red run exactly as an unemitted Patch (II.8.4)."
3. **docs/PATCH_PROTOCOL.md §4** — replace the APPEND-BLOCK RULE with the Direct-Write rule (text mirrors II.8.1-2).
4. **scaffolding/core/form_patch-notes.md item 6** — "append block" instruction → "pre-merged full file (II.8.1)".
5. **proc_inspection-audit.md lines 17 & 23, proc_nota-distillation.md line 11** — "append block prepared" → "rows appended in place (II.8.1)".
6. **docs/PROMPT_PLAYBOOK.md lines ~44 & ~150** — template text "append block" → "updated register (in place)".
7. **Check 9 consequence:** upon ratification, these files leave docs/ARCHIVE_NOTES.md exemptions and the retired phrases become validator-enforced FAILs.
Ratify with: "ratify P-01 canon companion" (or amend items individually).

