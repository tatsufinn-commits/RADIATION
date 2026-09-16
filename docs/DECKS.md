# 📊 DECKS (`docs/DECKS.md`)
## Deck Rules + Outline Schema + Lint + Verifier — Stages A–B (S-2-PPTX-A/B)
**Version:** v3.10.28 · **Base:** 46916c7ae7d1c34c60a7f49ad04550a3f373f5e8 (PPTX-A seal) · Previous: v3.10.27 base ea77a8a1dd4dcd385d0589b6659933af9f0dac78 (S-2-ENV seal)

## Two Pillars (verbatim and load-bearing)

> **Pillar 1:** *A deck is a Nota answer format, not a product.*
> **Pillar 2:** *No `.pptx`-alone delivery — the outline always ships with the deck.*

The outline is the receipt; the deck is its rendering. Budgets are computed at outline time so the box never decides silently later (F1/F2 lesson on record: a 4,000-char bullet saves silently).

## Theme-Lock Doctrine

- Theme registry v0: exactly two named palettes marked **PROVISIONAL (until the Commander's theme notes)**: `anchor` + `slate`, 5 fixed hexes each per `decks/DECK_RULES.json`
- `theme_lock: fixed hex set per theme` — doctrine: locked palettes, content decides count
- `R-005 theme ∈ theme_registry` · `R-006 fixed hex set per theme (theme_lock)` — rule file is the policy, he who edits the rule file edits the law, ledger rows record it
- Theme registry marked PROVISIONAL until Commander's theme notes — honesty row in ledgers

## Budgets-as-Rules (Data Form)

- `R-001 max_bullets_per_slide ≤6` · `R-002 max_chars_per_slide ≤400` · `R-003 max_chars_per_bullet ≤80` · `R-004 max_slides_per_deck: content decides (no cap) — claim-list slides may each cite ONE receipt` · `R-005 theme ∈ theme_registry` · `R-006 fixed hex set per theme (theme_lock)`
- Desk floors (floor, not ceiling — cc-slidev values may tighten): disparities vs cc-slidev logged in `decks/DECK_RULES.json` with sources
- Each rule `{id R-XXX, text ≤200, metric, threshold, class error|warn, source (cc-slidev / R&D F1-F2 / desk)}`

## Outline Discipline

- Schema `radiation.deck_outline/1` in `schemas/deck_outline.schema.json`
- Required: `schema_name` const · `id` OUTLINE-<slug> · `title` · `theme` {name from registry, theme_lock fixed hex set} · `slides[]` {ref, type enum title|section|content|compare|claim-list|closing, bullets[] {text, source_ref string|null}, notes string|null} · `constraints[]` (rule IDs) · `provenance` {task, date, source_refs[]} · `honesty_note` optional
- `source_ref` admissible only to register lanes (SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-… — data, nothing else); bullet without source_ref is claim awaiting one and lint may warn (never fail) as UNBACKED-BULLET
- Lint `scripts/deck_rules_check.py` validates outline vs schema and every declared constraint via DECK_RULES data-driven — finding text names OUTLINE-id · slide ref · rule id · observed vs threshold

## Cross-Refs (exactly three, no more)

- Nota (answer-format landing): `09-nota/CORE_INDEX.md` + `09-nota/CARD_001_bp344-accessibility.md` — deck is Nota answer format, not product
- SOURCE_QUALIFICATION (claim/source discipline for bullets): `docs/SOURCE_QUALIFICATION.md` — a source can be authentic and authoritative while failing to support specific claim; bullets carry source_ref to register lanes
- EVIDENCE_TAXONOMY state-mapping: `docs/EVIDENCE_TAXONOMY.md` §5 annex Gate-1 correspondence AVAILABLE↔primary+active · UNAVAILABLE↔deprecated/secondary/asserted/benchmark · UNKNOWN↔draft+honesty-grammar — bullets map to evidence grades

## Non-Goals (Stage A boundary)

- No `python-pptx` import anywhere (import pptx = policy FAIL-class)
- No renderer, no verify_deck verb (B), no plan/fill verbs (C), no dependency, no committed .pptx binary (decks derived in tempdir; tree holds outlines + rules + machinery, never renderings)
- No SKILL/skill-catalog edits, no mode changes, no template library, no cue rows unless demanded, no network, no WP-D canon text (🟠 word separately), no SOLVE/fonts/VLM (WP-E), no Problem-1 items

## Verifier (S-2-PPTX-B) — Outline-Level MATCH/DRIFT + Receipt Resolver

- **Canonicalize:** outline → canonical form (sorted keys, normalized whitespace, stable ordering by ref) → re-serialize → idempotence assert `canonical(canonical(o)) ≡ canonical(o)`, deterministic bytes → sha log (e.g. `OUTLINE-CARD001 · canonical · sha 4f89e41e1e6b`)
- **Receipt resolver (new FK edge):** every non-null `source_ref` must RESOLVE into tree — register lanes only `SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-, OUTLINE-` → grounding tables it consults `01-research/REFERENCES.md` rows, `09-nota/` files, `06-triangulate/` files, `Brain/` knowledge registry — witness-based resolution, no network; unresolved → finding `UNRESOLVED-RECEIPT` FAIL
- **Drift battery:** tamper outline copy (drop bullet, mutate text, swap source_ref) → verifier emits `DRIFT` per class named `DRIFT-text`, `DRIFT-structure`, `DRIFT-source_ref` (MATCH → DRIFT semantics from prototype, at outline level)
- **Render-half explicitly deferred to WP-C/D behind the 🟠 dependency word:** why receipts verify without render; render needs the canon — honest design constraint on record: R&D round-trip semantics (MATCH/DRIFT over rendered deck) needs python-pptx — gated 🟠 at WP-D. This stage verifies what stdlib can verify now: outline layer itself — canonical integrity, receipt resolvability, drift on tamper. Render-half verifier lands when dependency canon opens (stage C/D), unchanged in intent.
- **Rider S-2-PPTX-A message-language repair:** zero-findings witness line now truth-bearing `checked N outline file(s) — 0 findings` (N real); with 0 present, `no outlines present — checked DECK_RULES.json only — 0 findings (truth-bearing: checked 0 outline file(s))` allowed then and only then. Honesty row: "the button told the truth about verdicts and lied about coverage; now it tells both"

## Honesty

- Theme registry v0 PROVISIONAL until Commander's theme notes
- Rule floors sourced: R-001/R-002 desk floor matches cc-slidev, R-003/R-006 F1/F2 lesson 4,000-char bullet saves silently, R-004/R-005 desk
- Outline is receipt; deck is rendering; no .pptx-alone delivery
- No python-pptx anywhere (import pptx = policy FAIL-class) — stdlib-only, no renderer, no .pptx binary per S-2-PPTX-B non-goals
