# 📊 DECKS (`docs/DECKS.md`)
## Deck Rules + Outline Schema + Lint + Verifier + Dependency Canon + Renderer + Round-Trip — Stages A–D (S-2-PPTX-D stage 4 of 5)
**Version:** v3.10.31 · **Base:** f3a4f304f65db8a693b0faad7818f50b3ef129c6 (PPTX-C seal, main v3.10.30) per DESK_DIRECTIVE_S2_PPTX_D_2026-09-17.md — canon ratified by Commander relay — relay-as-word · Previous: v3.10.30 base 4fa588c fix rebuild clean from same base minus report-as-doc penetration

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

## Non-Goals (Stage D boundary — hard)

- No template library · no SOLVE/fonts/VLM (WP-E, deferred-research) · no committed `.pptx` anywhere ever (`.gitignore` `*.pptx` already) · no deck-alone delivery (receipt law: outline ships with deck always) · no theme-registry edits (PROVISIONAL stands until Commander notes) · no cue/skill/mode changes · no network at runtime (CI pip-install only) · no Problem-1
- Single import site law holds: ONLY `scripts/deck_pptx_adapter.py` may contain `import pptx`, never at module level, always inside guarded probe / call-sites — fence law walks ALL ship-files (scripts/, tests/, Brain/, cue/, skills/) and FAILs otherwise
- Renderer `deck_render.py` stdlib + python-pptx only, never writes into repo tree, budgets re-asserted pre-render, speaker notes carry source_ref set, theme as-is PROVISIONAL

## Verifier (S-2-PPTX-B) — Outline-Level MATCH/DRIFT + Receipt Resolver

- **Canonicalize:** outline → canonical form (sorted keys, normalized whitespace, stable ordering by ref) → re-serialize → idempotence assert `canonical(canonical(o)) ≡ canonical(o)`, deterministic bytes → sha log (e.g. `OUTLINE-CARD001 · canonical · sha 4f89e41e1e6b`)
- **Receipt resolver (new FK edge):** every non-null `source_ref` must RESOLVE into tree — register lanes only `SRC-, ANNOT_, TRI_, CARD_, GAP-, R2-, OUTLINE-` → grounding tables it consults `01-research/REFERENCES.md` rows, `09-nota/` files, `06-triangulate/` files, `Brain/` knowledge registry — witness-based resolution, no network; unresolved → finding `UNRESOLVED-RECEIPT` FAIL
- **Drift battery:** tamper outline copy (drop bullet, mutate text, swap source_ref) → verifier emits `DRIFT` per class named `DRIFT-text`, `DRIFT-structure`, `DRIFT-source_ref` (MATCH → DRIFT semantics from prototype, at outline level)
- **Render-half completion (S-2-PPTX-D):** `scripts/deck_verify.py` gains `--verify-rendered <outline> --out <pptx|tempdir>` — render outline to tempdir via `deck_render.py` → parse the `.pptx` back via adapter → derive structure → compare vs outline → verdict MATCH or DRIFT-text / DRIFT-structure / DRIFT-source_ref (named classes preserved from B). Self-test gains ≥3 render vectors: render+round-trip MATCH, text mutation → DRIFT-text, structure mutation → DRIFT-structure (render vectors skipUnless AVAILABLE when probe ABSENT-UNKNOWN).
- **Rider S-2-PPTX-A message-language repair:** zero-findings witness line now truth-bearing `checked N outline file(s) — 0 findings` (N real); with 0 present, `no outlines present — checked DECK_RULES.json only — 0 findings (truth-bearing: checked 0 outline file(s))` allowed then and only then. Honesty row: "the button told the truth about verdicts and lied about coverage; now it tells both"

## Dependency Canon — python-pptx (WP-D) — Ratified by Commander Relay (relay-as-word)

**Adopt `python-pptx` (MIT license-logged) as the SOLE presentation dependency.** Governance, and only this, is canon — ratified by Commander relay per DESK_DIRECTIVE_S2_PPTX_D_2026-09-17.md §I, §V gate note live only upon Commander relay, relay itself ratifies canon:

1. **Single import site:** the ONLY file permitted to contain `import pptx` is `scripts/deck_pptx_adapter.py` — still never at module level, always inside the guarded probe / call-sites. The fence law extends: policy test walks ALL ship-files (scripts/, tests/, Brain/, cue/, skills/) and FAILs on any other occurrence. `import pptx` = FAIL-class outside `deck_pptx_adapter.py` guarded block — this file contains guarded probe only, never at module level. Exempt from tool_registry coverage closure per S-2-PPTX-C (optional adapter, now sole import site).
2. **Pinned version floor:** canon declares one minimum version `python-pptx>=0.6.21`; CI installs exactly the pin `pip install python-pptx==0.6.21` (one step, pinned); tests must `skipUnless(probe AVAILABLE)` so stdlib-only environments degrade honestly (ABSENT-UNKNOWN), never crash — OPTIONAL-dependency law.
3. **No transitive scope:** python-pptx brings `lxml>=4.9` (BSD-licensed), `Pillow>=9.0` (HPND MIT-class), `XlsxWriter>=3.0` (BSD) — logged as licensed (audit MIT/BSD-class; **no GPL anywhere**, hard fail). One line each in ledgers: lxml BSD, Pillow HPND, XlsxWriter BSD, python-pptx MIT.
4. **The receipt law holds verbatim:** **a deck is never delivered alone — its outline ships with it**, always (house non-goal standing). `deck_render.py` NEVER writes into repo tree; no `.pptx` is ever committed (add `.pptx` to `.gitignore` as LAW-6-era idiom precedent — already present `*.pptx` in .gitignore since P-10 containment).

**Canon text:** `docs/DECKS.md` new § Dependency canon — python-pptx (WP-D) four rules above verbatim-core; README + CAPABILITIES capability lines one each "pptx render: AVAILABLE when dependency present, else ABSENT-UNKNOWN — constraint grammar per IP-ENV-01".

## Renderer (S-2-PPTX-D) — `scripts/deck_render.py`

- Outline + theme registry → `.pptx` to explicit `--out` path (default tempdir) — NEVER writes into repo tree; no `.pptx` is ever committed (`.gitignore` already `*.pptx`).
- Slide shape: `title` + `bullets` content; **speaker notes carry the `source_ref` set** (receipts embedded, two-pillar doctrine honored inside artifact); theme taken from `decks/DECK_RULES.json` registry as-is (anchor — still PROVISIONAL pending Commander notes; architecture reads it untouched).
- Budgets re-asserted pre-render (run DECK_RULES check internally; refuse render on FAIL — guards, not verbs).
- Stdlib + python-pptx only, no other deps, no network at runtime (CI pip-install only).
- License: python-pptx MIT license-logged, clean-room adapter, no GPL.

## Verbs Promotion (S-2-PPTX-D) — `fill_template` Unfrozen

- With adapter AVAILABLE: performs the render (via `deck_render.py`), emits `{rendered: <out-path or ABSENT>, sha, receipts_embedded: slides-with-notes count}` — receipts embedded as speaker notes per slide.
- With ABSENT: keeps today's honest report shape, no fake, never — `{adapter: ABSENT-UNKNOWN, would_render: <plan>, blocked_at: dependency canon (WP-D 🟠)}`.

## Honesty

- Theme registry v0 PROVISIONAL until Commander's theme notes
- Rule floors sourced: R-001/R-002 desk floor matches cc-slidev, R-003/R-006 F1/F2 lesson 4,000-char bullet saves silently, R-004/R-005 desk
- Outline is receipt; deck is rendering; no .pptx-alone delivery — receipt law holds verbatim, deck never delivered alone, outline ships with it always
- Dependency canon ratified by Commander relay per DESK_DIRECTIVE_S2_PPTX_D_2026-09-17.md §I gate note live only upon Commander relay, relay itself ratifies canon — method confessed: relay-as-word
- Single import site: ONLY `scripts/deck_pptx_adapter.py` may contain `import pptx`, never at module level, always inside guarded probe / call-sites — fence law walks ALL ship-files (scripts/, tests/, Brain/, cue/, skills/) and FAILs otherwise — policy test enforces
- Pinned version floor: `python-pptx>=0.6.21` minimum, CI installs exactly `python-pptx==0.6.21` one step pinned, tests skipUnless AVAILABLE so stdlib-only degrades honestly ABSENT-UNKNOWN never crash — OPTIONAL-dependency law
- No transitive scope: python-pptx brings lxml BSD, Pillow HPND, XlsxWriter BSD — logged MIT/BSD-class, no GPL anywhere hard fail — one line each in ledgers
- Renderer `deck_render.py` stdlib + python-pptx only, NEVER writes into repo tree, no `.pptx` ever committed (`.gitignore` `*.pptx` already since P-10), budgets re-asserted pre-render, speaker notes carry source_ref set, theme as-is PROVISIONAL
- Round-trip completion: `deck_verify.py --verify-rendered` render to tempdir → parse back via adapter → MATCH or DRIFT-text / DRIFT-structure / DRIFT-source_ref — deferred render-half unchanged-in-intent now lands
- `fill_template` unfrozen: AVAILABLE → render via deck_render emits rendered path sha receipts_embedded count, ABSENT → honest blocked report shape no fake
- Windows-agent reality: CP1252/console + symlink limits documented blockers (fix-team exhibits) — local red on env-class grounds is not defect if CI-Ubuntu green — env class declared honestly in report, never mute real finding
- License: python-pptx MIT license-logged, clean-room adapter, no GPL — GenSlide skeleton MIT, mcp-office Output Contract governance pattern MIT
