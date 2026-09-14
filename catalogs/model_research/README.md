# catalogs/model_research — the Candidate C research layer (5700 "Atlas")

> **RESEARCH DESIGN ONLY · NO RUNTIME / DEPLOYMENT AUTHORITY.**
> This layer records, organizes, and gates *knowledge about models*. It grants
> nothing: no tool, no effect, no identity, no privacy guarantee, no legal
> conclusion. It is **non-boot** — check 41 runs a non-boot SCAN over the
> BOOT_SEQUENCE-derived boot graph (incl. the docs/.readme First-Read Gate and
> transitive passive specs); a hit is a build failure.

## What this layer is
The 5400 gate review (§5) and the 5600 closure order (Deliverable B) require a
structured alternative to prose profiles: **one record per EXACT model ×
surface × region**, with provider declarations, independent evidence, and local
observations kept separate; unknowns explicit; aliases and dated IDs separate.

## The evidence standard (binding for every record)
1. **Exact ids only.** `exact_model_id` is the provider's own id token.
   `exact_id_verified: true` requires that the id string was read from an
   official surface on `retrieved_on`. Otherwise `status` is `provisional` or
   `unverified`.
2. **Aliases ≠ dated IDs.** Aliases track "latest"; dated ids pin. Separate
   fields (`aliases`, `dated_ids`).
3. **Never merge evidence tiers.** `declarations` ([O, URL, date]),
   `independent_evidence` ([S/U, source, date]), `local_observations`
   (session-contingent, never generalized).
4. **Region never guessed.** `region: "undeclared"` unless a source pins one.
5. **Surfaces stay distinct:** api / consumer_app / enterprise / cloud_managed /
   comparison_host — never average across them.
6. **No session-identity claims.** A host label does not identify a model.
   **Arena Agent Mode has NO model record by design** — its model identity is
   unknowable from inside a session (standing law); a record would fabricate
   one.
7. **No new providers on mentions.** DeepSeek, Qwen, Cohere, Amazon/Bedrock,
   etc. get records only when they meet this same evidence standard — never
   because a list mentioned them.
8. **Confidence + review_after mandatory.** Every record decays; each carries a
   re-review date.

## Layout (14 records as of 5810 Recount, 2026-09-15)

> **Integrity note (5810, per the 5800 research-track review):** the pushed 5800
> tree (`027c786`) briefly held **15** active records — the zip cannot delete
> files, and the runner's retirement of the superseded candidate
> (`anthropic__fable-5-1…`) never executed there. Repair: the record schema is
> 0.3; the confirmed record declares `supersedes` and the checker rejects any
> declared target still active; `INVENTORY.generated.txt` is GENERATED from
> `records/` and drift-checked on every run. Provenance stays in git history +
> bundle evidence; exactly one active record per model × surface × region.
```
schemas/    model_research_record.schema.json (EXECUTED — check 40 + 41)
records/    one JSON record per exact model × surface × region
sources/    dated, tier-labeled source registers
evals/      HARNESS_DESIGN.md — the local evaluation contract (DESIGN ONLY)
decision_matrices/  DEPLOYMENT_MATRIX_DESIGN.md — per-deployment analysis (DESIGN ONLY)
```

## Tooling
`scripts/model_research_check.py` (registry: `model_research_check`) —
schema-executed via the ONE executor, plus code-level rules: record uniqueness
on (identifier, surface, region) with verified tokens and candidate labels in
disjoint namespaces, REAL calendar dates + the 90-day review window, typed
evidence bound to `catalogs/model_research/sources/REGISTER.json` (tier + date), filename binding,
`confirmed` ⇒ verified id + register-bound official declaration, and the
**non-boot scan** over the BOOT_SEQUENCE-derived graph. Executed by validate
check 41. 5710 review rule 6 in force: Arena has no record by design.
