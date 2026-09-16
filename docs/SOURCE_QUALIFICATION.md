# 🔍 SOURCE QUALIFICATION ≠ CLAIM VERIFICATION (`docs/SOURCE_QUALIFICATION.md`)
**Version:** 1.0.0 · **Evidence lane placement** · **Base:** e547e30cba5398bc0c858299f9810551eea3b866 (LAW-6 seal) → v3.10.25 · **Classification:** doc-line bundle, NO NEW ANALYZER per desk S-2-LINK
**Lineage:** IP-Link-01 (ROUTING-01 §VI) + Gap-Report folds domains 2,4,9,14 + desk addendum attempt: marker

---

## I. LOAD-BEARING TRUTH (verbatim-capable)

*a source can be authentic and authoritative while still failing to support the specific claim for which it was retrieved. Source qualification concerns the source itself; claim verification concerns the relationship between the source and a particular claim.*

This is the qualification ≠ verification doctrine. A source's authenticity and authority do not entail that it supports a given claim. Qualification judges the source; verification judges the relationship between source and claim.

## II. THE LINK AS EVIDENCE CANDIDATE — VOCABULARY, NOT RUNTIME

The link as evidence candidate is judged across five dimensions (adopted as **vocabulary**, not as a runtime component):

- **identity** — what the source is (origin, type, provenance)
- **integrity** — has it been altered, truncated, or corrupted (hash, manifest, digest)
- **authority** — tier and standing (official, credentialed, community, anonymous per existing tier practice)
- **context** — when and where it was produced, access conditions, result state per ACCESS LOG vocabulary
- **claim-fit** — does its content actually support the specific claim for which it was retrieved (the relationship test)

Pipeline vocabulary (RESOLVE → IDENTIFY → INSPECT → QUALIFY → CLAIM-FIT) is adopted as **vocabulary** for discussing evidence handling, not as a runtime analyzer or engine. No new scripts, checkers, or tools are introduced in this tranche per S-2-LINK non-goals.

## III. MAP ONTO EXISTING MACHINERY (exactly one cross-ref each — never re-invent)

- **Existing machinery — claims carry `{decay}` + grade:** `docs/EVIDENCE_TAXONOMY.md` — claims are graded `[D]/[O]/[I]/[R]/[N]/[S]` and carry `{decay: YYYY-MM-DD | none}` per I.4; qualification does not replace grading, it precedes the relationship test.

- **Existing machinery — verification = the relationship test:** `06-triangulate/` gauntlet — verification is the relationship test between source content and a particular claim (triangulation is the ONLY elevator per EVIDENCE_TAXONOMY; even `[D]` needs independence check for Core admission). Qualification checks the source; triangulation checks the relationship.

## IV. P04 TRIANGULATION CROSS-REF (referenced, not ratified)

`08-overhaul/proposals/PROPOSAL_P04_source-tiers-ip.md` is the **staged, unratified** source-tier doctrine (II.6 rules 8–9 + SOURCE_TIERS); tier vocabulary stays awaiting the Commander's ratification word; this tranche does not adopt it — it points at it. Source tiers remain doctrine-in-waiting, referenced here for future triangulation work, not ratified in v3.10.25.

## V. ACCESS LOG VOCABULARY CROSS-REFS (Gap-4 fold)

- **Extended result vocabulary:** `scaffolding/core/form_external-collection.md` — Result states extend from `ACCESSIBLE / DEAD / AUTH-BLOCKED` to `ACCESSIBLE / DEAD / AUTH-BLOCKED / SOFT-404 / PAYWALL / REDIRECT-LOGGED` per Gap-4 fold.
- **JS-only honesty line:** dynamically-rendered sources that cannot be read are recorded as `INACCESSIBLE-UNKNOWN` with a note — never claimed read, never claimed dead (UNKNOWN grammar; no headless-browser ambition, LAW-2 mirror).
- **Same-source re-fetch supersession note (Gap-2 fold):** when a source is re-fetched and its content has changed, the ACCESS LOG row must carry a supersession note (prior state → new state hash/short-diff + supersession remark); prior acquisition records stay (II.4).
- **Open sources cross-ref:** `docs/OPEN_SOURCES.md` points at the extended result vocabulary (one line added in this tranche).

## VI. CLEANUP RIDERS (single lines — doctrine naming, not new behavior)

- **Gap-9 stopping philosophy (named):** `docs/STOCKPILE_DOCTRINE.md` — stopping philosophy = necessity test + floor-not-target + shortfall protocol (philosophy already enforced; this line names it per Gap-9).
- **Gap-14 replay-relevant inputs:** `scaffolding/core/proc_research-sortie.md` — sortie rows/closeout record replay-relevant inputs — base SHA · tool versions · evidence set (98% already true in task_ledger practice; line makes it doctrine per Gap-14).

## VII. ATTEMPT MARKER (desk addendum)

Task_ledger rows from this tranche onward carry the `attempt:` marker per AP-08 (check 20.5's WARN appeared on three newest rows; restore marker habit — WARN-class). See `Brain/frontal_lobe/task_ledger.md` rules.

---

**Non-goals honored (hard):** No link-analyzer component, no new scripts/checkers/tools, no cue/subskill/contract/registry edits, no headless browsing or JS rendering, no ACCESS-log schema work beyond vocabulary line, no adoption of P04 tiers (cross-ref only), no session capability state (S-2-ENV), no video Phase-R/E, no PPTX, no .gitignore, no Problem-1 items, no moves/renames.

**Witnesses:**
- Load-bearing truth: `DESK_DIRECTIVE_S2_LINK_2026-09-16.md:12` `*a source can be authentic and authoritative while still failing to support the specific claim for which it was retrieved. Source qualification concerns the source itself; claim verification concerns the relationship between the source and a particular claim.*`
- Vocabulary: `DESK_DIRECTIVE_S2_LINK_2026-09-16.md:13` `identity · integrity · authority · context · claim-fit` + `RESOLVE→IDENTIFY→INSPECT→QUALIFY→CLAIM-FIT`
- Cross-ref EVIDENCE_TAXONOMY: `docs/EVIDENCE_TAXONOMY.md:30` `claim [GRADE] (source) {decay}`
- Cross-ref triangulate: `06-triangulate/README.md` gauntlet (verification = relationship test)
- ACCESS LOG vocabulary: `scaffolding/core/form_external-collection.md:22` `ACCESSIBLE / DEAD / AUTH-BLOCKED / SOFT-404 / PAYWALL / REDIRECT-LOGGED` + `INACCESSIBLE-UNKNOWN`
- OPEN_SOURCES cross-ref: `docs/OPEN_SOURCES.md` line pointing at extended vocabulary
- STOCKPILE cross-ref: `docs/STOCKPILE_DOCTRINE.md` necessity test + floor-not-target + shortfall protocol
- Research sortie checklist: `scaffolding/core/proc_research-sortie.md` base SHA · tool versions · evidence set
- P04 cross-ref: `08-overhaul/proposals/PROPOSAL_P04_source-tiers-ip.md` staged unratified
- Attempt marker: `Brain/frontal_lobe/task_ledger.md` AP-08

— **S006 Architect Wing — S-2-LINK doc-line bundle v3.10.25**
