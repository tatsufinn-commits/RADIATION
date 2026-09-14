# PROPOSAL — Candidate C: structured model research for RADIATION

> **RESEARCH DESIGN ONLY · NO RUNTIME / DEPLOYMENT AUTHORITY.**
> This proposal asks for nothing to be executed against any provider. It
> designs the *knowledge structure* (records), the *evaluation contract*
> (harness design), and the *decision structure* (deployment matrix) — to be
> built out only under the Commander's orders, one gated step at a time.

**Status:** delivered as patch 5700 "Atlas" (v3.9.0), non-boot.
**Binds:** 5400 gate review §5 (catalog schema), §6 (evaluation matrix),
§7 (deployment matrix); 5600 closure order (Deliverable B).
**Records:** 5 seed records (5700) expanded to **14 executed records** by the
5800 Almanac re-retrievals (2026-09-15) — exact IDs and official values captured
for the OpenAI/Anthropic flagship lines and the Gemini endpoint table
(`catalogs/model_research/sources/SOURCES_2026-09-14.md`, addendum).

## 1 · What already exists (this patch)
- **Record schema** `radiation.model_research_record/0.1` — EXECUTED (check 40
  keeps every keyword within the one schema executor; check 41 runs the
  catalog checker). 22 required fields, including the closure order's full
  list: provider, family, exact_model_id, surface, region, status,
  retrieved_on, context_window, knowledge_cutoff, modalities,
  reasoning/effort, tools, retention/training mode, license/AUP, safety
  evidence, independent evidence, local observations, known gaps,
  documentation completeness, confidence, review_after — plus
  `exact_id_verified` (strict boolean) and separate `aliases` / `dated_ids`.
- **14 records** (5700 seeds expanded 5800: OpenAI flagship four incl. `gpt-5.6-sol`; Anthropic four with exact IDs — the Sonnet-5 price conflict resolved by the official page; Gemini stable line + 3.1 Pro PREVIEW with captured endpoint IDs; xAI re-confirmed). Origins:
  Anthropic `fable-5-1` provisional — id string not captured; Google
  `gemini-3-1-pro-preview` provisional — PREVIEW lifecycle declared; xAI
  `grok-4.6` confirmed with cutoff 2026-02-01). Every gap is a named gap;
  `local_observations` are empty everywhere — **no local evaluation has run**,
  and the records refuse to pretend otherwise.
- **The host that gets NO record:** Arena Agent Mode — model identity
  unknowable from inside a session; a record would fabricate one (README rule
  6). This is the catalog's first proof of discipline: the most-used host in
  this repo's history is the one it refuses to model.
- **Checker** `scripts/model_research_check.py` — schema-executed + code-level
  rules (uniqueness on exact_model_id × surface × region, date sanity,
  confirmed⇒verified id + register-bound official declaration, real-date +
  90-day-window discipline, typed evidence, filename binding, non-boot scan),
  with its own negative-vector self-test (21 vectors); wired into validate check 41 and the tool
  registry (22 tools).

## 2 · What is designed but deliberately NOT built (the gates)
### a. Local evaluation harness (`catalogs/model_research/evals/HARNESS_DESIGN.md`)
Nine evaluation dimensions (corpus retrieval & abstention, citation/grounding,
long-context omission, hostile instructions in selected content, structured
JSON/ICS correctness, tool-call proposal vs execution, sensitive-data
non-disclosure, refusal/escalation, latency/cost/retries/rate limits/aliases/
deprecations) with a mandatory per-run capture block (exact model id, provider,
host/surface, region, effort, enabled-tool allowlist, prompt/contract/fixture
revisions + digests, date, harness version, evaluator/rubric, metrics, retries,
limitations). **Redaction law:** private corpus text and credentials are never
uploaded merely to obtain a result; fixtures are synthetic, digest-bound
stand-ins. **No cross-model score, no "best model"** — per-dimension results
with declared rubrics only.
### b. Task-to-deployment matrix (`catalogs/model_research/decision_matrices/DEPLOYMENT_MATRIX_DESIGN.md`)
Four deployment classes (local/open-weight, enterprise-hosted, cloud-managed,
read-only hosted inference) × analysis axes (provider / controller / processor
/ deployer / application / tool / data-subject roles; data flow; retention;
transfers; copyright; license; contracts) — analyzed **separately per
deployment**, as structure and method, never as a ranked score. License/AUP
questions are recorded as questions with official pointers; the matrix renders
no legal conclusions.
### c. Expansion rule
DeepSeek, Qwen, Cohere, Amazon/Bedrock, and any other provider get records
**only when they meet the same evidence standard** — never because a list
mentioned them.

## 3 · What this layer will never do
- Grant a tool, effect, identity, privacy guarantee, or legal conclusion.
- Enter boot context (check 41 scans the BOOT_SEQUENCE-derived graph; hits fail the build).
- Replace `agents/<Provider>/BOOT.md` host/session handoff files.
- Call any provider, ship an SDK, or host an endpoint (standing law).

## 4 · Decisions this proposal leaves with the Commander
1. Whether to **fund actual evaluation runs** under the harness design (each
   run = its own gated order; captures are evidence, results are records).
2. Which **exact records** to expand first once re-verification triggers fire
   (every seed carries `review_after: 2026-12-13`).
3. Whether the eventual **deployment matrix** should be populated for a
   specific, named deployment — one deployment per order, per §7.
