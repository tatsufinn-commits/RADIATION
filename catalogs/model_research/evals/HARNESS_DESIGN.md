# HARNESS_DESIGN — RADIATION local evaluation contract (Candidate C)

> **DESIGN ONLY — NOT IMPLEMENTED.** No runner, no provider calls, no SDK.
> Implementation happens only under a dedicated Commander order, and every run
> executes inside the cooperative bounds (control plane; no canonical writes).

## Purpose
Replace impression words ("strong/strongest") with **measured, captured,
declared-rubric results** — per dimension, per EXACT model id × surface ×
region. Never a cross-model score; never a "best model" (5400 review §6; 5600
CAPABILITIES §21 gate).

## Evaluation dimensions (each its own run type)
1. **Corpus retrieval & abstention** — must find planted facts in the declared
   corpus derivatives AND abstain correctly on planted absent facts.
2. **Citation / grounding** — answers over a fixture corpus must cite the
   exact fixture + span; uncited claims scored as ungrounded.
3. **Long-context omission / truncation** — planted sentinels at known depths
   (head/middle/tail) of long synthetic contexts; measure recall vs depth.
4. **Hostile instructions in selected content** — the `evals/hostile/` fixture
   shapes (course derivative, imported HTML, tool-result, subagent-result):
   the model under test must treat them as data. Proves the MODEL-side of the
   boundary; the repo's deterministic side is already proven by tests.
5. **Structured JSON / ICS / schema correctness** — emit artifacts conforming
   to shipped schemas; validate with the ONE schema executor.
6. **Tool-call proposal vs actual execution** — model proposes calls; nothing
   executes without the control plane; score proposal quality and the
   refusal discipline of the boundary (the model never gets execution power).
7. **Synthetic sensitive-data non-disclosure** — planted canary tokens must
   never be repeated, exfiltrated, or echoed into artifacts.
8. **Refusal / escalation** — over-authority requests must be refused or
   escalated, not improvisingly "helped".
9. **Operational facts** — latency, cost, retries, rate limits, alias/dated-id
   behavior, deprecations observed during runs (recorded, not scored).

## Mandatory per-run capture block (no run without it)
```
run_id, date (UTC), harness_version, evaluator/rubric declaration,
provider, exact_model_id (+ alias/dated id actually served), surface, region,
reasoning/effort settings, enabled-tool allowlist,
prompt_template_revision + sha256, fixture_revision + sha256 (per fixture),
metrics, retries, limitations, raw-output digests (not raw private text)
```

## Redaction law (binding)
- **Never upload private corpus text or credentials to obtain a result.**
  Fixtures are synthetic, digest-bound stand-ins derived from structural
  properties (sizes, depths, shapes) — never the private bytes themselves.
- Canary tokens are single-purpose, synthetic, and rotated per run.
- Raw outputs are stored only as digests + redacted excerpts under
  `evals/runs/` (created only when implementation is ordered).

## Result discipline
- Each run appends one result record (future schema, same evidence standard as
  `radiation.model_research_record/0.3`) and updates ONLY the matching
  record's `local_observations` — never its `declarations`.
- Rubrics are declared BEFORE the run; changing a rubric invalidates
  comparison with prior runs (recorded, not hidden).
- The suitability tables in `agents/*/CAPABILITY_PROFILE.md` and the
  ROUTING_MATRIX may cite measured results only after they exist; until then
  they stay marked unmeasured.
