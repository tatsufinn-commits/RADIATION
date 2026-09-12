# PATCH NOTES — RADIATION_PATCH_2026-09-13_2100_Wave12-Closure-Green.zip
**Risk class:** 🟢 (reviewer closure directive — no new law; carriers relocated UNCHANGED in content). Pre-merged files. Version → v1.6.2.

## ⚠️ DELETION LIST (apply with the extract — the push must REMOVE these 18 tracked files)
PATCH_NOTES.md (root) · docs/AMENDMENT_ROWS_STAGED.md · docs/AMENDMENT_ROWS_STAGED_P04.md · docs/AMENDMENT_ROWS_STAGED_P05.md · docs/AMENDMENT_ROWS_STAGED_P07.md · docs/AMENDMENT_ROWS_STAGED_P09.md · docs/COPYRIGHT_ACCESS_BLOCKS_STAGED.md · docs/PLAYBOOK_EVALFIRST_TEMPLATE_STAGED.md · docs/QUICKREF_SECTION_STAGED.md · docs/SOURCE_TIERS_STAGED.md · docs/STOCKPILE_DOCTRINE_STAGED_DIFF.md · scaffolding/core/proc_drill-run_STAGED.md · scaffolding/core/proc_exam-forge_STAGED.md · scaffolding/core/proc_ingestion-run_STAGED_DIFF.md · scaffolding/core/proc_inspection-audit_STAGED_DIFF.md · scaffolding/core/proc_weak-spot-diagnostic_STAGED.md · subskills/active/scout_STAGED_DIFF.md · subskills/passive/surgeon_STAGED_DIFF.md
(git: `git rm` each, or extract-then-delete; check 3 now FAILS while any remains.)

## WHAT MOVED WHERE (content unchanged; path hygiene only)
Law/amendment carriers → 08-overhaul/proposals/PROPOSAL_P0{1,2,3,4,5,7,9}_*.md (7 consolidated files) · scaffold revs → scaffolding/improved/ (5) · subskill revs → subskills/proposals/ (2) · style carriers renamed *_PROPOSED/_SEED (3) · 🟡 memo → 08-overhaul/proposals/MEMO_P04_repo-exposure-decision.md.

## K-LAW-004 RULING (reviewer §3.1): the ingest file EXISTS
Brain/short_term/ingest/2026-09-12_bp344-statute-lawphil.md was built in the P-04 pass and shipped in _1000_P04-Demo-Ingestion-Evidence.zip — it was MISSING FROM THE PUSHED COMMIT, not from the frame. Root cause: 🟢 companion zips (_1000/_1200/_1300/_1500/_1800/_2000) were not all extracted before push. This zip carries every owed 🟢 file again: ANTI_PATTERNS, mistake_bank, mastery_ledger, grade_exam.py, export_anki.py, the rejection record, the ingest file, drills, module, registers.

## VALIDATOR CHANGES
- BUG FIX (reviewer §3.3): archive_exempt() read every backtick incl. ARCHIVE_NOTES' own title → the file exempted itself and phantom rows went unverified. Now: table-row first column only; ARCHIVE_NOTES never self-exempt; check 1.5 FAILS on phantom paths.
- check 3 extended: *_STAGED / *_DIFF / PATCH_NOTES.md anywhere in tree = FAIL.
- check 3.5 NEW: scaffolding/core/ is a closed set — unlisted file = FAIL.
- checks 8/9 narrowing: proposal homes exempt ONLY while listed in PENDING_RATIFICATIONS.md.
- check 19 refinement: a line naming ≥2 blocklisted domains is rule-text, not a citation (the P-07 proposal's own blocklist tripped it — fixed by shape, not by exemption).

## EVIDENCE (raw, this run)
Frame + clean-copy run: 22 checks · 21 pass · 1 warn (honest 15:3 meta-ratio) · 0 fail · exit 0. Regression: 4 locked · 5 pending · 0 failed · exit 0. Carrier scan: 0. core/: 9 files = 9 INDEX rows. Break proofs: x_STAGED.md → check 3 FAIL · stray core file → check 3.5 FAIL · phantom ARCHIVE row → check 1.5 FAIL; all restored → exit 0.

## JUDGEMENT CALL RECORDED (reviewer §7)
@Drill-as-seventh-mode stands; logged in ledger as the EVAL-FIRST presumption working.
