# 📦 THE PATCH PROTOCOL (`docs/PATCH_PROTOCOL.md`)
## Practical Workflow for System Evolution
**Version:** 1.0.0 | Constitutional basis: II.7 (The Patch Protocol) · IV.5 (Patch Authority)

## 1. FOR THE AI — when and how to emit a Patch
**WHEN:** at session close (or on Commander order), IF durable material exists:
Brain promotions ready · refined/improved scaffolds · new lexicon entries ·
cerebellum additions · proposed canon changes.
No durable material = no Patch. Never emit empty or ceremonial Patches.

**HOW:**
1. Assemble changed files in correct repo-relative structure.
2. Write `PATCH_NOTES.md` per `scaffolding/core/form_patch-notes.md`.
   Classify honestly: 🟢 ordinary / 🟠 canon-affecting.
   One Patch = one coherent purpose. NEVER mix 🟢 and 🟠 —
   canon changes travel alone so ratification decisions stay atomic.
3. Zip as `RADIATION_PATCH_YYYY-MM-DD_HHMM_<short-description>.zip`
4. Present to the Commander; state plainly: **"This is a PROPOSAL. Nothing is
   applied until you apply it."**
5. Record the Patch filename in `Brain/frontal_lobe/task_ledger.md` (II.3).

## 2. FOR THE COMMANDER — applying a Patch
1. Read `PATCH_NOTES.md` first. 🟠 = your explicit ratification is being
   requested; check the old-vs-new side-by-side diffs.
2. Extract the zip at repository root (structure is pre-aligned).
3. Follow the application instructions (add / replace / append per file).
4. Commit and push. **Your push is the moment of legal effect.**
5. Give the verdict next session: APPLIED / PARTIAL (what was kept) /
   REJECTED (one-line reason if you wish) → it enters the Patch Ledger and,
   where relevant, the lexicon.

## 3. THE PATCH LEDGER (`docs/PATCH_LEDGER.md` — append-only, II.2)
One line per Patch, appended on emission, updated with the verdict:
`| date | patch filename | risk | areas | verdict | lesson |`
Rejected Patches are never deleted — the Commander's "no" is training data (II.7.6).

## 4. APPEND-BLOCK RULE (protects II.2)
Append-only files (ledgers, registers, the lexicon, logbooks) travel in Patches
as **APPEND BLOCKS** — text to paste at file end — never as full-file
replacements. A Patch that full-replaces an append-only file is invalid.

## 5. ENFORCEMENT HOOKS
- **surgeon-passive:** blocks session close if durable material exists but no
  Patch was emitted and no Commander waiver given; treats bypass claims
  ("I updated the repo") as I.1 contamination of the system record (IV.5.4).
- **sentinel-passive:** verifies Patch structural integrity (paths resolve, no
  orphan files, notes match contents) before presentation.
- **Autonomous Scan:** a Commander prompt containing a Patch verdict
  (APPLIED/PARTIAL/REJECTED) triggers a ledger update before any new task.
