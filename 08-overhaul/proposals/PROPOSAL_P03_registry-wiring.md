# PROPOSAL P-03 — registry wiring (5 edits) · ratify: "ratify P-03 wiring"
**Re-homed 2026-09-12 (Wave 1&2 closure): carriers moved from canonical dirs to lawful proposal homes per IV.2/IV.4/scaffolding-README §4. Text unchanged except path-reference hygiene. NOTHING below is applied until the Commander's ratification line.**


---
## ◈ Wiring diffs

# STAGED DIFFS — P-03 registry wiring (apply on "ratify P-03 wiring")
**Status:** 🟠 — all four edits touch core scaffolds / canon-status docs.

## 1. `scaffolding/core/proc_ingestion-run.md` — APPEND after step 4 (GRADE CEILING)
```text
□ 4.5 K-ID ASSIGN     — object new? assign next K-<DOMAIN>-<NNN> + registry
     block (docs/KNOWLEDGE_REGISTRY.md, form_knowledge-record). Existing
     object? update its row (Last verified, Used by). K-ID = pointer, never grade.
```
## 2. `scaffolding/core/proc_nota-distillation.md` — REPLACE step 3 line
OLD: `□ 3. LINEAGE BLOCK    — cites: long_term dossier <path> + triangulation worksheet(s) <ids>`
NEW: `□ 3. LINEAGE BLOCK    — cites: long_term dossier <path> + triangulation worksheet(s) <ids> + K-ID(s) of the objects the card rests on (docs/KNOWLEDGE_REGISTRY.md)`
## 3. `scaffolding/core/form_external-collection.md` — APPEND one line to §5 DIGEST intro
NEW: `Every object extracted from a collection gets (or updates) a K-ID row in docs/KNOWLEDGE_REGISTRY.md — the collection keeps this file; the objects live in the registry.`
## 4. `docs/EVIDENCE_TAXONOMY.md` — APPEND one line after the six-grade table
NEW: `**K-IDs (docs/KNOWLEDGE_REGISTRY.md) are provenance pointers, never grades and never citations — a card still cites statute, rule and table (I.2).**`
## 5. PROMOTION — MOVE `scaffolding/improved/form_knowledge-record.md` → `scaffolding/core/` (rev-note removed)


---
## ◈ Original patch notes

# PATCH NOTES — RADIATION_PATCH_2026-09-13_1400_P03-Registry-Wiring-STAGED.zip
**Risk class:** 🟠 CANON-AFFECTING — STAGED, NOTHING APPLIED. Ratify: **"ratify P-03 wiring"**.
File-by-file (crit. 6): proc_ingestion-run.md APPEND step 4.5 · proc_nota-distillation.md REPLACE step-3 line · form_external-collection.md APPEND §5 line · EVIDENCE_TAXONOMY.md APPEND one line · form_knowledge-record.md MOVE improved/→core/.
DECAY_REGISTER wiring needs NO edit: computation shipped as scripts/decay_compute.py (🟢) — the register file itself is untouched by canon.
EVAL-FIRST self-application (voluntary; II.9 staged): INSTANCE = K-IDs exist in 28 rows but no scaffold tells sessions to assign them (registry rots without wiring). COST = 0 boot bytes, 4 small edits. DISPLACEMENT = edits live inside existing files; only move is a promotion, not an addition. CHECK = check 17 (dangling/duplicate/path/status integrity — break-tested).
On ratification: apply 5 edits · delete this carrier · re-run validator · bump version · AUTO-PATCH.

