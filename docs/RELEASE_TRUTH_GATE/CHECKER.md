# Release Truth Checker — design

**Location:** `scripts/release_truth_check.py`
**Expectation:** `docs/RELEASE_TRUTH_GATE/EXPECTATION.json`

## Checks (must fail when)

1. **Base SHA wrong or not ancestor:** `base_sha` from EXPECTATION.json must exist and be ancestor of HEAD (or HEAD~1 == base for linear). If not, reject — prevents stale base / wrong root.
2. **Required deletion still present:** any path in `required_absent_on_disk` or `required_deletions` with `must_be_absent_on_disk` true must NOT exist on disk. If exists, reject — prevents ZIP extraction without applying deletion.
3. **Expected delete missing from git diff:** for each required deletion with `must_be_D_in_diff` true, `git diff --cached` or `git diff base..HEAD --name-status` must contain `D\t<path>`. If not, reject — prevents doc-only claim.
4. **Undeclared changed path:** `git diff base..HEAD --name-status` must only contain paths listed in `allowed_changes` with matching kind (A/M/D). Any extra path → reject — prevents undeclared changes.
5. **Stale generated artifact:** for each `required_generated_artifacts`, run its `freshness_check` command; must exit 0 and output must indicate current/fresh. Also compare file content vs generator output if applicable. If stale, reject — prevents generated-file drift.
6. **Missing DoD command/outcome:** for each `mandatory_validations`, run command, check expected_exit and must_contain substring. If exit mismatch or substring absent, reject — prevents doc claiming unverified CI.

## Self-test vectors (disposable negative fixtures)

- wrong base SHA → reject
- required deleted file still on disk → reject
- expected delete missing from git diff → reject
- undeclared changed path → reject
- stale generated artifact → reject
- missing DoD command/outcome → reject

Use Git-aware checks only where repo checkout exists; avoid treating directory names or narrative text as proof. Each vector creates a temp git repo or temp dir, sets up condition, runs checker, expects failure.

## Implementation notes

- Read EXPECTATION.json, validate schema (base_sha pattern, allowed_changes array)
- Git operations via subprocess, handle shallow clones
- No network, no provider calls, no credentials
- Returns 0 findings when clean, non-zero with findings list
- Self-test: `--self-test` creates 6+ disposable fixtures, each must be rejected, plus one positive clean fixture must pass
