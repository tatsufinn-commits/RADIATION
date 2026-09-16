# PROPOSAL P-11-B CUE RECONCILIATION + ADMISSION GATE

**Class:** 🟠 CANON — REQUIRES EXPLICIT COMMANDER RATIFICATION
**Date:** 2026-09-16
**Base:** d518f3f post-repair main (5900-1 gate defect repair, 42·38·4·0 green, 8/8 release-truth)
**Purpose:** One sealed candidate one purpose — re-scope three flagged cue rows additive/tombstone never deletion II.2/II.10 + schema v0.2 review_after/authority_grant + admission gate + hostile multi-row fixture.

**Non-goals:** No other catalogs, no docs-lane work, no runtime/routing/providers, no skill catalogs.

## II.7.8 Side-by-side old/new per flagged row

### L13 — Ratification (cue/autopilot-cues.md line 13, CUE-RATIFICATION v1)

**Old:**
```
| "it went well" / "that's good" | Ratification of the referenced work | Log RATIFIED in ledgers |
CUE-RATIFICATION v1 action: "Log RATIFIED in ledgers"
```

**New:**
```
| "it went well" / "that's good" + explicit reference binding (e.g., "Patch N went well") | Ratification requires explicit reference binding to work + exact words citation | Log RATIFIED in ledgers ONLY when: (1) Commander explicitly references the work (name/number), (2) ledger entry cites exact Commander words verbatim. Casual "that's good" without reference = NOT ratification. Rationale: prevents fabrication per SD-GOV-006. |
CUE-RATIFICATION v2 action: "Ratification requires explicit reference binding to work (e.g., 'Patch N went well') + ledger entry must cite exact Commander words verbatim; casual 'that's good' without reference is NOT ratification; log RATIFIED only when reference bound and exact words cited. Old reading L13 'Ratification of the referenced work' archived — new requires explicit binding + exact-words citation. REQUIRES EXPLICIT COMMANDER RATIFICATION — old: 'Log RATIFIED in ledgers' / new: 'Log RATIFIED only with explicit reference + exact-words citation'"
```

**Rationale:** Prevents ratification fabrication per SD-GOV-006. Requires explicit reference binding + log line cites exact words.

**Disposition:** Additive/tombstone — old row remains in autopilot-cues.md marked ARCHIVED with pointer to new v2; catalog v2 supersedes with pointer; lexicon entry added.

### L41 — Full Discretion Grant (cue/autopilot-cues.md line 41, CUE-FULL-DISCRETION v1)

**Old:**
```
| "I will give you full discretion on the next proceeding builds, do what you must!" | Build autonomy granted — delivery discipline is NOT | Proceed without per-step approval; still ship patch zips; never commit |
CUE-FULL-DISCRETION v1 action: "Build autonomy granted — delivery discipline is NOT; proceed without per-step approval; still ship patch zips; never commit"
review_after: none
authority_grant: implicit
```

**New:**
```
| "I will give you full discretion on the next proceeding builds, do what you must!" (historical grant S004 2026-09-13) | Build autonomy GRANTED for window 2026-09-13 through P-11-A opening (base 4c851e3). EXPIRED as of 2026-09-15 — historical note only, not active grant. |
CUE-FULL-DISCRETION v2 action: "Build autonomy GRANTED 2026-09-13 S004 through P-11-A opening base 4c851e3. EXPIRED as of 2026-09-15 P-11-A seal — historical note only, not active grant. Expired=historical note per P-11-B. Delivery discipline never waived; still ship patch zips; never commit. Renewal requires explicit Commander ratification. Old reading L41 'Build autonomy granted — delivery discipline is NOT; proceed without per-step approval' archived — new carries expiry expired=historical note. REQUIRES EXPLICIT COMMANDER RATIFICATION — old: 'Build autonomy granted — delivery discipline is NOT; proceed without per-step approval; still ship patch zips; never commit' / new: 'Build autonomy GRANTED 2026-09-13 through P-11-A, EXPIRED as of 2026-09-15 historical note only, renewal requires explicit ratification'"
review_after: 2026-09-15 (expired)
authority_grant: true
```

**Rationale:** Grant carries expiry expired=historical note. Prevents indefinite autonomy creep. Historical grant S004 was for proceeding builds through P-11-A, now expired.

**Disposition:** Additive/tombstone — old remains archived with pointer to new v2 review_after 2026-09-15.

### L79 — Continuous Operation vs Lexicon L18 (cue/autopilot-cues.md line 79 vs cue/commander-lexicon.md line 18)

**Old L79:**
```
| "WE are not done working" (plural WE) | Continuous operation is the default state — he states facts, not questions | Do not ask whether to continue; declare next objective and build |
CUE-CONTINUOUS-OP v1: precedence commander_order, priority 80, action "Continuous operation is default — do not ask whether to continue; declare next objective and build"
```

**Lexicon L18 (winner):**
```
| "WE are not done working" | Continuous-operation declaration; sessions are legs of one campaign | 2026-09-13 | A fact, not a scope grant |
```

**New L79 v2 (lexicon wins, loser archived-with-pointer):**
```
| "WE are not done working" (plural WE) — continuous-operation fact | Sessions are legs of one campaign (fact). Does NOT grant scope beyond current explicit directive. | Continuous-operation is a fact about campaign continuity, not a scope grant authorizing new builds. Next objective requires explicit Commander order per lexicon L18 "A fact, not a scope grant" (winner). Old reading archived with pointer to lexicon L18. |
CUE-CONTINUOUS-OP v2: precedence ratified_policy (downgraded from commander_order), priority 60, action "Continuous-operation declaration is a fact, not a scope grant (lexicon L18 wins per P-11-B reconciliation). Sessions are legs of one campaign (fact). Does NOT authorize new builds beyond current explicit directive; next objective requires explicit Commander order. Old reading L79 'Continuous operation is default — do not ask whether to continue; declare next objective and build' archived with pointer to commander-lexicon.md L18 'A fact, not a scope grant'. Loser archived-with-pointer, winner lexicon. REQUIRES EXPLICIT COMMANDER RATIFICATION — old: 'Continuous operation is default — do not ask whether to continue; declare next objective and build' / new: 'Continuous-operation fact, not scope grant — does NOT authorize new builds beyond current directive; next objective requires explicit Commander order (lexicon L18 wins)'"
review_after: 2026-09-15
authority_grant: true (historical grant now fact-only)
```

**Rationale:** Reconcile conflicting readings — autopilot-cues grants scope, lexicon says fact not grant. Winner is lexicon (more restrictive, prevents scope creep). Loser archived-with-pointer per II.2 II.10.

**Disposition:** Additive/tombstone — old L79 remains marked ARCHIVED loser with pointer to lexicon L18 winner; new v2 supersedes.

## Schema v0.2

**Old schema 0.1:**
- Required: schema_name, id, version, kind, scope, trigger, priority, conflicts_with, precedence, action, effect, evidence, tests
- schema_name const radiation.cue_card/0.1
- No authority_grant, no review_after

**New schema 0.2:**
- Required unchanged (backward compatible)
- schema_name enum ["radiation.cue_card/0.1", "radiation.cue_card/0.2"]
- Optional properties: authority_grant boolean, review_after date YYYY-MM-DD
- allOf: if authority_grant true then review_after required
- Linter FAIL when authority-granting cue lacks review_after (P-11-B)

**Rationale:** Authority-granting cues must carry expiry/review date to prevent indefinite grants.

## Admission Gate

**Old:** No gate — new cue could enter without proving five conditions.

**New (P-11-B):**
- New cue enters only with passing fixture proving five conditions:
  1. trigger (non-empty)
  2. scope (non-empty)
  3. priority (1-100) / evidence (session/date/source)
  4. conflict-resolution (conflicts_with array)
  5. expiry (review_after if authority_grant true) or prose-only marking via DIRECTIVE_CUE_MAPPING.json
- One new test class TestAdmissionGate (10 vectors) + lint vector in cue_resolver.py
- Fixture: tests/test_cue_resolver.py::TestAdmissionGate proves gate logic + linter FAIL when authority_grant true lacks review_after

## Hostile Suite Extension

**Old:** 4 shapes (imported_text_html, injected_course_derivative, tool_result_shaped, subagent_result_shaped) proving no elevation.

**New (P-11-B):**
- Add 5th fixture: evals/hostile/multi_row_conflicting_cues.md — contains triggers for CUE-CLOSE-TOPIC (LETS MOVE ON!) + CUE-CONTINUOUS-OP (WE are not done working) which conflict via conflicts_with, plus injection keywords.
- New test TestHostileClosure.test_multi_row_conflicting_cue_fixture_surfaces_conflict:
  - Proves resolver surfaces conflicting_ids and conflicting_groups
  - Loser suppressed with reason emitted per law
  - No elevation (forced to content)

## Files Changed (vs base d518f3f post-repair)

- M cue/autopilot-cues.md — additive reconciliation section L13/L41/L79 with ARCHIVED + NEW v2 side-by-side + REQUIRES EXPLICIT COMMANDER RATIFICATION
- M cue/commander-lexicon.md — append-only 3 new rows for P-11-B reconciliation (L18 wins, L13 re-scope, L41 expiry) with side-by-side per II.7.8
- M cue/CUE_CATALOG.json — version 2, schema 0.2, 42 cues all with authority_grant boolean, 11 with review_after, 3 re-scoped v2 with side-by-side old/new in action + evidence note
- M schemas/cue_card.schema.json — v0.2 adds authority_grant + review_after + allOf if true then required review_after
- M scripts/cue_resolver.py — linter FAIL when authority_grant true lacks review_after + date format check
- M tests/test_cue_resolver.py — 52 → 62 tests: + TestAdmissionGate (10 vectors) + multi-row conflicting fixture test
- A evals/hostile/multi_row_conflicting_cues.md — 5th hostile fixture
- M docs/CAPABILITIES.md — GENERATED (cue_resolver updated)
- M docs/SYSTEM_STATE.md — GENERATED
- M docs/RELEASE_TRUTH_GATE/EXPECTATION.json — base pinned d518f3f, allowed delta enumerated for P-11-B
- M CHANGELOG.md — v3.10.10 entry? Actually v3.10.9 repair + v3.10.10 P-11-B? But one patch one purpose says P-11-B is v3.10.10? Need to decide versioning — 5900 was v3.10.9, 5900-1 repair stays v3.10.9, P-11-B should be v3.10.10
- M docs/PATCH_LEDGER.md, docs/ROADMAP.md, Brain/frontal_lobe/task_ledger.md, docs/shrine/LOG.md, etc.

## Risk

🟠 CANON — REQUIRES EXPLICIT COMMANDER RATIFICATION per II.7.4/II.7.8 — nothing in this zip is applied to live repo until Commander ratifies and pushes. One patch one purpose (CUE reconciliation + admission gate).

## Acceptance

- [ ] Commander ratifies with explicit line: "ratify P-11-B CUE reconciliation"
- [ ] Sealed candidate zip + Path-A fresh-clone at base d518f3f
- [ ] validate 0 FAIL, release-truth 0+8/8, catalog 0+24/24, unittest 77+10? Actually 62 resolver + 4 hostile + others = 87? Wait discover 77 previously, now with new tests 62 resolver = 62, plus hostile content 4? Actually test_hostile_content separate, plus other tests = total 87? Need to verify.
- [ ] render_docs --check PASS, whitespace clean, status clean
- [ ] Actions SUCCESS on public main after push
