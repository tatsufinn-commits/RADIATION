# 📦 PATCH NOTES TEMPLATE (`form_patch-notes.md`)
**Use:** mandatory format for PATCH_NOTES.md in every Patch (II.7.3a)

```markdown
# PATCH NOTES — <short description>
1. RISK LEVEL   : 🟢 ORDINARY | 🟠 CANON-AFFECTING — REQUIRES EXPLICIT
                  COMMANDER RATIFICATION
2. WHAT CHANGES : <numbered list, one line per file:
                  path — add/replace/append — why>
3. AREAS TOUCHED: [ ] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
                  [ ] cues [ ] modes/Scan [ ] other: ___
4. RATIONALE    : <why this should persist — cite the session/task that
                  produced it>
5. CANON DIFFS  : (🟠 only) per change: OLD TEXT → NEW TEXT side-by-side,
                  with rationale (II.7.8)
6. APPLICATION  : exact steps. For append-only files (ledgers, registers,
                  lexicon): the Patch carries an APPEND BLOCK to paste at
                  file end — NEVER a full-file replacement (protects II.2).
7. VERSION BUMP : MAJOR / MINOR / PATCH (per VERSIONING_GUIDE.md)
8. DECLARATION  : "This Patch is a proposal. It has no effect until the
                  Commander applies it. — <session/model id, date>"
```
Rules: one Patch = one coherent purpose · never mix 🟢 and 🟠 · zip name:
RADIATION_PATCH_YYYY-MM-DD_HHMM_<short-description>.zip
