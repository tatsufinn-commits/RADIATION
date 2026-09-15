# Definition of Done — Release Truth Gate (template)

**Base SHA:** `fbce71bbfe4c62da71e6b347d36617474f840297` (or newer exact base, record new exact base if main advanced)
**Expected delta:** list allowed A/M/D paths including required deletions, generated artifacts
**Risk register:** must at least name:
- wrong root — package applied to different working directory than repo root
- stale base — base SHA not ancestor or not exact pinned SHA
- ZIP extraction without applying deletion — file still on disk after extraction
- generated-file drift — INVENTORY.generated.txt stale vs live records/
- documentation claiming unverified CI — CHANGELOG says green but validator red
- host/provider/surface confusion — Arena gap treated as official policy
- unavailable credentials/remote verification — push attempted without Commander motor act

## Pre-push DoD (must all PASS)

- [ ] `python3 scripts/model_research_check.py` → 0 findings
- [ ] `python3 scripts/model_research_check.py --self-test` → 24/24 vectors
- [ ] `python3 scripts/validate.py` → 42·39·3·0
- [ ] `python3 -m unittest discover -s tests -v` → 25 OK
- [ ] `python3 scripts/verify_apply.py --strict` → FAIL-CLASS none
- [ ] `python3 scripts/release_truth_check.py` → release-truth gate: 0 finding(s)
- [ ] `python3 scripts/release_truth_check.py --self-test` → 6/6 negative vectors + 1 positive
- [ ] `git diff --check` → clean
- [ ] `git status --short` → clean or only expected staged changes
- [ ] `git diff --cached --name-status` includes required D for `anthropic__fable-5-1__api__undeclared.json` when applicable
- [ ] `test ! -e catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json`
- [ ] `find catalogs/model_research/records -maxdepth 1 -type f -name '*.json' | wc -l` = 14
- [ ] Base SHA `fbce71b` is ancestor of HEAD (or HEAD~1 == base)

## Post-push receipt (must be filled after Commander push)

- Remote SHA: `__________________`
- Fresh clone commands:
  ```bash
  git clone https://github.com/tatsufinn-commits/RADIATION.git fresh-remote-check
  cd fresh-remote-check
  git rev-parse HEAD # must equal remote SHA above
  test ! -e catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json
  find catalogs/model_research/records -maxdepth 1 -type f -name '*.json' | wc -l # 14
  python3 scripts/model_research_check.py
  python3 scripts/model_research_check.py --self-test
  python3 scripts/validate.py
  python3 scripts/verify_apply.py --strict
  python3 scripts/release_truth_check.py
  ```
- Results:
  - stale absent: PASS/FAIL
  - count 14: PASS/FAIL
  - catalog checker 0 findings: PASS/FAIL
  - self-test 24/24: PASS/FAIL
  - validator 42·39·3·0: PASS/FAIL
  - strict no FAIL-class: PASS/FAIL
  - release-truth checker 0 findings: PASS/FAIL

- Public Actions URLs:
  - validate: `https://github.com/tatsufinn-commits/RADIATION/actions/runs/________` → success/failure
  - apply-report: `https://github.com/tatsufinn-commits/RADIATION/actions/runs/________` → success/failure

- Conclusions:
  - Remote SHA matches fresh clone HEAD: YES/NO
  - Both Actions success: YES/NO
  - Only then may release docs describe delivery as public/green: YES/NO

**Evidence, not privilege grant — Commander authority unchanged.**
