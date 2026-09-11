# 📦 PATCH NOTES TEMPLATE (`form_patch-notes.md`) — v1.1
**Use:** mandatory format for PATCH_NOTES.md in every Patch (II.7.3a)

```markdown
# PATCH NOTES — <short description>
1. RISK LEVEL   : 🟢 ORDINARY | 🟠 CANON-AFFECTING — REQUIRES EXPLICIT
                  COMMANDER RATIFICATION
   RISK BASIS   : <one line: WHY this classification — which areas are/are
                  not canon. Misclassification is an IV.5.3 violation.>
   CANON CHECK  : does this Patch touch ANY of: constitutional text /
                  core scaffolds / core styles / mode definitions /
                  Scan rules / docs/.readme? YES → 🟠, no exceptions.
2. FILES TOUCHED: <complete numbered list — EVERY file in this zip:
                  path — ADD / REPLACE / APPEND-BLOCK — one-line why.
                  A file in the zip but not in this list invalidates
                  the Patch (sentinel structural check).>
3. AREAS TOUCHED: [ ] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
                  [ ] cues [ ] modes/Scan [ ] other: ___
4. RATIONALE    : <why this should persist — cite the session/task that
                  produced it>
5. CANON DIFFS  : (🟠 only) per change: OLD TEXT → NEW TEXT side-by-side,
                  with rationale (II.7.8). 🟢 Patches write "none".
6. APPLICATION  : exact steps. For append-only files (ledgers, registers,
                  lexicon, testament): the Patch carries an APPEND BLOCK to
                  paste at file end — NEVER a full-file replacement (II.2).
7. VERSION BUMP : MAJOR / MINOR / PATCH (per VERSIONING_GUIDE.md) + update
                  root CHANGELOG.md entry included in this Patch.
8. DECLARATION  : "This Patch is a proposal. It has no effect until the
                  Commander applies it. — <session/model id, date>"
```
Rules: one Patch = one coherent purpose · never mix 🟢 and 🟠 · zip name:
RADIATION_PATCH_YYYY-MM-DD_HHMM_<short-description>.zip
