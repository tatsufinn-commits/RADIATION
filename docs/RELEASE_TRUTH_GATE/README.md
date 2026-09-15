# Release Truth Gate — 5824

**Purpose:** Prevent failure class demonstrated by 5810–5822: package/local worktree says deletion/repair occurred, while pushed public commit contains only documentation claims or extracted payload.

**Base:** `fbce71bbfe4c62da71e6b347d36617474f840297` — first green after 5810–5822 (14 records, 0 findings, 24/24 vectors, 42·39·3·0, 25 OK, strict PASS, Actions success).

**Acceptance (fresh clone of fbce71b):**
```
stale anthropic__fable-5-1 record: ABSENT
records/ count: 14
catalog checker: 0 findings
self-test: 24/24
validator: 42·39·3·0
unit: 25 OK
strict: no FAIL-class
Actions validate: success
Actions apply-report: success
```

**What this gate adds (non-boot, concise):**
- `EXPECTATION.json` — machine-readable release expectation (base SHA, allowed A/M/D, required deletions, generated artifacts, mandatory validations, risks)
- `scripts/release_truth_check.py` — repository-owned checker that fails on wrong base, deletion still present, expected delete missing from diff, undeclared path, stale generated artifact, missing DoD outcome
- `DoD_TEMPLATE.md` — Definition of Done + risk register template (must name wrong root, stale base, ZIP extraction without deletion, generated-file drift, doc claiming unverified CI, host/provider/surface confusion, unavailable credentials/remote verification)
- `POST_PUSH_RECEIPT_TEMPLATE.md` — post-push checklist/receipt format (remote SHA, fresh-clone commands/results, Actions URLs + conclusions)

**Scope locks:**
- Non-boot, concise, no model records/sources/policy conclusions/profile assessments/runtime tools/provider calls/evaluations/routing/deployment/legal
- Do not make git push, canonical apply, or provider invocation automatic — Commander authority unchanged
- Do not claim local ZIP/SHA/expected CI proves public delivery

**DoD before push:**
- checker clean, negative vectors green, catalog 24/24, validator 42·39·3·0, unit 25 OK, strict no FAIL, whitespace clean

**After Commander push:**
- New clone of remote SHA with release-truth checker, catalog checker, validator, strict apply clean, plus success public Actions validate and apply-report URLs — only then may release docs describe delivery as public/green

**Next after gate proven:** surface-specific five-provider analysis using dated primary sources; explicit observed Arena/PASS activation study; then Commander-authorized local evaluations. Maintain distinction provider declarations vs host/session observations vs experimentally observed performance.
