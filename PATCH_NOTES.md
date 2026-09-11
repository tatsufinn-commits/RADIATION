# PATCH NOTES — Boot-Hardening-and-Doctrine-Precision
**Zip:** `RADIATION_PATCH_2026-09-12_1700_Boot-Hardening-and-Doctrine-Precision.zip`

1. **RISK LEVEL** : 🟠 CANON-AFFECTING — **REQUIRES EXPLICIT COMMANDER RATIFICATION**
   RISK BASIS   : touches docs/.readme (the constitutional First-Read Gate,
   III.1), a core scaffold (form_patch-notes.md), and doctrine text
   (STOCKPILE_DOCTRINE.md, annexed to law III.5). All three are canon.
   CANON CHECK  : YES — .readme, core scaffold, doctrine → 🟠.

2. **FILES TOUCHED** :
   1. docs/.readme — REPLACE (v1.1: adds "First 60 Seconds" tiered boot path
      by context-window size + §9 Degraded Operation binding rules; all
      existing sections retained verbatim, renumbered)
   2. docs/STOCKPILE_DOCTRINE.md — REPLACE (v1.1: adds §4 "Necessary vs
      Padding — the enforceable test" with the four recorded answers, the
      four padding conditions, the enforcement chain, and the floor-not-target
      rule; §§1–3, 5 unchanged)
   3. scaffolding/core/form_patch-notes.md — REPLACE (v1.1: adds RISK BASIS +
      CANON CHECK lines to field 1; renames field 2 to FILES TOUCHED with
      completeness rule — zip-file-not-listed invalidates the Patch;
      field 7 now requires the CHANGELOG entry)
   (Replacement contents ship as *_REPLACEMENT files; rename over targets.)

3. **AREAS TOUCHED**: [ ] Brain [x] laws (annexed doctrine + First-Read Gate)
   [x] scaffolds (core form) [ ] styles [ ] subskills [ ] cues [ ] modes/Scan

4. **RATIONALE** : Implements Grok v1.1 items 4 (boot experience), 9
   (stockpile clarification), 12 (context-window degradation playbook), and
   14 (patch template strengthening) — the full 🟠-classifiable remainder.
   Items 4+12 merged into .readme (degradation IS boot doctrine); item 9's
   necessary-vs-padding test makes III.8 mechanically enforceable; item 14
   makes risk misclassification and undeclared files detectable.

5. **CANON DIFFS** :
   - .readme OLD: no first-60-seconds section; degradation covered by one
     line in MODES.md → NEW: explicit load paths per context size + §9 five
     binding degradation rules (declare, no @Radiation, Brain write limits,
     mid-session handover procedure, silent degradation = III.1 violation).
     Rationale: small-context AIs previously had no lawful boot path.
   - STOCKPILE_DOCTRINE OLD §4 was three short rules → NEW: four-answer
     necessity test recorded in the Acquisition Plan + four explicit padding
     conditions + enforcement chain + floor-not-target rule.
     Rationale: "never pad" was law without a test; now it is testable.
   - form_patch-notes OLD field 1 was a bare flag → NEW: flag + basis +
     mandatory canon checklist. OLD field 2 listed changes → NEW: exhaustive
     FILES TOUCHED with invalidation rule.
     Rationale: closes the 🟢-smuggling seam (IV.5.3) mechanically.

6. **APPLICATION** :
   a. RATIFY FIRST — this is 🟠. If any single item is rejected, apply the
      others; each REPLACE is independent.
   b. Extract at repo root. Rename each *_REPLACEMENT file over its target:
      docs/dot-readme_REPLACEMENT → docs/.readme
      docs/STOCKPILE_DOCTRINE_REPLACEMENT.md → docs/STOCKPILE_DOCTRINE.md
      scaffolding/core/form_patch-notes_REPLACEMENT.md → scaffolding/core/form_patch-notes.md
   c. Delete the _REPLACEMENT files. No append-only files touched.
   d. Commit and push. Your push is legal effect (IV.5) and constitutes the
      IV.4 ratification record for these three canon changes.

7. **VERSION BUMP** : MINOR — v1.0.2 → v1.1.0 (canon change: core scaffold +
   gate + doctrine). Add CHANGELOG entry:
   "## v1.1.0 — Boot-Hardening-and-Doctrine-Precision (🟠): First-60-Seconds
   tiered boot + Degraded Operation rules in .readme; enforceable
   necessary-vs-padding test in Stockpile Doctrine; hardened Patch-notes form."

8. **DECLARATION** : "This Patch is a proposal. It has no effect until the
   Commander applies it. — Protocol Architect, update session, 2026-09-12."
