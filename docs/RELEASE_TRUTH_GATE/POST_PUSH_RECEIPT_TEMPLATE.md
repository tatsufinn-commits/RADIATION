# Post-Push Receipt — Release Truth Gate (template)

**Purpose:** Evidence, not privilege grant. Must be filled after Commander push.

## Remote

- Remote SHA reported after push: `__________________`
- Push date (Asia/Singapore): `__________________`
- Pusher: Commander / trusted maintainer (name): `__________________`

## Fresh clone verification (must be new clone of remote, not local worktree)

```bash
git clone https://github.com/tatsufinn-commits/RADIATION.git RADIATION-post-push-check
cd RADIATION-post-push-check
git rev-parse HEAD
# Expected: must equal remote SHA above
# Actual: __________________

test ! -e catalogs/model_research/records/anthropic__fable-5-1__api__undeclared.json
# Expected: file absent
# Actual: PASS/FAIL

find catalogs/model_research/records -maxdepth 1 -type f -name '*.json' | wc -l
# Expected: 14
# Actual: __________________

python3 scripts/model_research_check.py
# Expected: 0 findings
# Actual: __________________

python3 scripts/model_research_check.py --self-test
# Expected: 24/24 vectors
# Actual: __________________

python3 scripts/validate.py
# Expected: 42·39·3·0
# Actual: __________________

python3 -m unittest discover -s tests -v
# Expected: 25 OK
# Actual: __________________

python3 scripts/verify_apply.py --strict
# Expected: FAIL-CLASS none
# Actual: __________________

python3 scripts/release_truth_check.py
# Expected: 0 finding(s)
# Actual: __________________

python3 scripts/release_truth_check.py --self-test
# Expected: 6/6 negative + 1 positive
# Actual: __________________
```

## Public Actions

- validate job URL: `https://github.com/tatsufinn-commits/RADIATION/actions/runs/________`
  - Conclusion: success / failure / pending
  - Actual: __________________
- apply-report job URL: `https://github.com/tatsufinn-commits/RADIATION/actions/runs/________`
  - Conclusion: success / failure / pending
  - Actual: __________________

## Conclusions

- [ ] Remote SHA equals fresh clone HEAD: YES/NO
- [ ] Stale file absent: YES/NO
- [ ] Count 14: YES/NO
- [ ] Catalog checker 0 findings: YES/NO
- [ ] Self-test 24/24: YES/NO
- [ ] Validator 42·39·3·0: YES/NO
- [ ] Unit 25 OK: YES/NO
- [ ] Strict no FAIL-class: YES/NO
- [ ] Release-truth checker 0 findings: YES/NO
- [ ] Both Actions success: YES/NO

Only when all YES may release docs describe delivery as public/green. Commander authority unchanged — this receipt is evidence, not a privilege grant.

**Filled by:** __________________ **Date:** __________________
