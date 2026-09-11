# PATCH NOTES — Planning Ingestion & Reviewer (first live Brain ingestion)

1. RISK LEVEL   : 🟢 ORDINARY
   RISK BASIS   : This Patch adds Brain CONTENT (a summary + a study reviewer)
                  and appends to append-only ledgers/registers. It touches NO
                  constitutional text, scaffolds, styles, mode definitions, or
                  Scan rules. Content-only → 🟢 per VERSIONING_GUIDE ("PATCH —
                  content growth").
   CANON CHECK  : does this Patch touch constitutional text / core scaffolds /
                  core styles / mode definitions / Scan rules / docs/.readme?
                  → NO. 🟢 is correct.

2. FILES TOUCHED: (complete list — every file in this zip)
   1. PATCH_NOTES.md                                          — ADD — this file.
   2. Brain/short_term/ingest/planning_collection_summary.md  — ADD — full
      master summary of all 8 Planning files (the stored knowledge).
   3. Brain/short_term/notes/PLANNING_reviewer.md             — ADD — 79-item
      study reviewer (Q&A, tables, glossary, mnemonics) for the Commander.
   4. append-blocks/planning_digest.append.md                 — APPEND BLOCK —
      populates the DIGEST + ACCESS LOG of
      Brain/external_sources/planning.md (append-only region, II.6).
   5. append-blocks/task_ledger.append.md                     — APPEND BLOCK —
      task-ledger entry (II.3).
   6. append-blocks/patch_ledger.append.md                    — APPEND BLOCK —
      patch-ledger emission record (II.7.6).
   7. append-blocks/changelog.append.md                       — APPEND BLOCK —
      CHANGELOG v1.3.2 entry.

3. AREAS TOUCHED: [x] Brain  [ ] laws  [ ] scaffolds  [ ] styles  [ ] subskills
                  [ ] cues  [ ] modes/Scan  [x] other: CHANGELOG + ledgers

4. RATIONALE    : Produced during the 2026-09-12 @Gather session the Commander
                  ordered ("access planning.md … summarize … store it in /brain"),
                  followed by "create a reviewer … create a .zip according to the
                  rules." This is RADIATION's first live ingestion and the first
                  durable knowledge worth persisting (SYSTEM_STATE had flagged
                  "Brain CONTENT … 🕳️ EMPTY — awaits first live sessions").

5. CANON DIFFS  : none (🟢).

6. APPLICATION  : extract the zip at the repository root, then:
   - Files 2 & 3: copy into place (they are new; no conflicts expected).
   - File 4: open Brain/external_sources/planning.md; replace the DIGEST
     placeholder line "(empty — no ingestion session has run…)" with the DIGEST
     block, and paste the ACCESS LOG row at the end of its table.
   - Files 5–7: paste each APPEND BLOCK at the END of its target file
     (task_ledger.md, PATCH_LEDGER.md) — EXCEPT changelog, which inserts the
     v1.3.2 entry at the TOP of the log (newest-at-top convention).
   - NEVER full-replace any append-only file (II.2).

7. VERSION BUMP : PATCH — v1.3.1 → v1.3.2 (content growth). CHANGELOG entry
                  included as append block 7.

8. DECLARATION  : "This Patch is a proposal. It has no effect until the
                  Commander applies it. — RADIATION @Gather session, 2026-09-12"
