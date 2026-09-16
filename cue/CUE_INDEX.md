# ☄️ CUE INDEX (`cue/CUE_INDEX.md`)
## The Autonomous Scan, condensed for quick reload
**Full spec:** `docs/CUE_SYSTEM.md` (that file is law; this file is a reload aid)

## THE FIVE PHASES
1. **COMPREHEND** — full prompt: topic, task-verbs, constraints, artifacts.
2. **EXTRACT** — 4 steps, in order: surface EXPLICIT signals (quoted) → surface
   IMPLICIT signals → list ALL competing readings (no silent selection; FIRM =
   single-value) → resolve or escalate (only now; reasoning → Extraction Notes).
3. **ASSESS** — assign tuple (DELIVERABLE, PERMANENCE, DEPTH) → derive mode,
   style, scaffolds, quota.
4. **CONFIDENCE GATE** — HIGH (all FIRM): proceed · MEDIUM (one alternative):
   proceed + name runner-up · LOW (two+ uncertain, or two modes tie): **ASK,
   never guess.**
5. **SCAN DECLARATION** — fixed fields incl. REQUIRED Extraction Notes;
   always precedes work; Commander silence = proceed.

## TUPLE → MODE
answer+ephemeral → @Data · corpus+stored → @Gather · comprehension-map+stored
→ @Decode · paper+stored → @Gather (styled) · anything canonical → @Radiation

## EDGE CASES (full rulebook: docs/CUE_SYSTEM.md §3)
E1 mixed quick+permanent → two-stage serial session · E2 vague → cap MEDIUM,
never assume @Radiation, default @Gather-working declared · E3 analysis+
recommendation → serial or @Radiation · E4 lexicon phrasing → weight higher,
still show alternatives · E5 two modes tie → ASK · E6 lexicon vs explicit →
EXPLICIT WINS · E7 artifact vs verbal → verbal sets mode, artifact is evidence
· E8 mid-session new task → fresh Scan, new anchor.

## ON MISREAD (law III.9)
HALT → RE-SCAN (fresh Declaration, cause stated) → SALVAGE TRIAGE (carry
forward / subsidiary / [MISREAD ARTIFACT]) → LEXICON ENTRY. Never skip triage.

## COMPRESSION LAYER (P-11-A Candidate B + P-11-B reconciliation, additive II.10 archive never deletion)

- **Typed catalog:** `cue/CUE_CATALOG.json` (42 cues, schema `schemas/cue_card.schema.json` v0.2 P-11-B adds `review_after` + `authority_grant` boolean, linter FAIL when authority-grant true lacks review_after) is the compressed machine-executed form of `cue/autopilot-cues.md` (91 lines ~38 cues + standing orders + term + build cues + P-11-B reconciliation L13/L41/L79 additive/tombstone never deletion). One record per operational cue: id/version/kind/scope/trigger/priority/conflicts_with/precedence/action/effect/evidence/tests + directive_id + authority_grant + review_after.
- **Directive mapping:** `cue/DIRECTIVE_CUE_MAPPING.json` maps ALL 13 SD-GOV-001..013 to catalog entries (0 prose-only) — coverage 13/13 proven by linter.
- **Resolver:** `scripts/cue_resolver.py` deterministic precedence law `commander_order>ratified_policy>cue>heuristic>content`, CONTENT-only for courses/web/tools/subagent/imported_text, emits selected/suppressed/reason/conflicting_ids/law, closes hostile NOT-proven via REAL resolver over REAL path 4 shapes P-11-A + 5th multi-row conflicting-cue fixture P-11-B proving conflict surfacing loser suppressed reason emitted.
- **Reconciliation P-11-B (REQUIRES EXPLICIT COMMANDER RATIFICATION):** three flagged rows L13 ratification requires explicit reference binding + exact-words citation, L41 grant carries expiry expired=historical note (review_after 2026-09-15), L79 reconcile with lexicon L18 "a fact, not a scope grant" — lexicon wins loser archived-with-pointer II.2 II.10, side-by-side old/new per II.7.8 in autopilot-cues.md + catalog action + lexicon.
- **Admission gate P-11-B:** new cue enters only with passing fixture proving five conditions trigger scope priority/evidence conflict-resolution expiry or prose-only marking, TestAdmissionGate 10 vectors + lint vector authority_grant requires review_after.
- **Hygiene law:** II.2 append-only, II.10 archive never deletion — this file grows only additively; old prose stays archived, never deleted; compression is pointer + typed catalog, not rewrite.
- **Boot pointer:** single pointer line in boot tier (per DoD non-boot beyond single pointer line) — `docs/CUE_SYSTEM.md` v1.2 references catalog; boot reads only pointer.
- **Inference-log audit:** `cue/inference-log.md` append-only, now includes S006 5830 upheld, P-11-A Candidate B upheld, P-11-B reconciliation upheld entries, shrinking NOT-proven to genuinely untestable (non-deterministic LLM, multi-session accumulation, image-only vision rung, human social engineering) + new 5th hostile shape.
