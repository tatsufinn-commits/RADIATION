# Validation evidence — 5610 proposal

**Base checked against:** public `main` =
`78c01ded97e94c14de411b533dba457c0ac70db6` (confirmed again before packaging).

## Executed against the proposed working tree

- `python3 scripts/validate.py` → **41 checks; 39 PASS; 2 WARN; 0 FAIL**.
  - WARN 11.6: replica tranche still `commander-review-requested`.
  - WARN 16: pre-existing/genuine meta-budget imbalance, now 33 orange patches vs
    four content sessions. No warning was hidden or waived.
  - Check 15 boot budget passes: Tier 0+1 = 40,912 B / 40 KiB; Tier 0–2 = 69,384 B /
    80 KiB.
  - Check 20.5 now passes because this was a genuine recorded `attempt:` task, not a
    synthetic marker.
- `python3 -m unittest discover -s tests -v` → **25 tests, OK**.
- `python3 -m radiation_core.relay --self-test` → **25/25**.
- `python3 scripts/tool_registry_check.py` → **21 tools, 0 findings**.
- `python3 scripts/tool_registry_check.py --self-test` → **18/18**.
  - Includes external-symlink entrypoint and existing-but-unsupported nested-schema
    negative vectors.
- `python3 scripts/contract_tests.py` → **11/11**.
- `python3 -m radiation_core.control_plane --self-test` → **38/38**.
- `python3 scripts/cap_verify.py --tree` → **9/9**.
- `python3 agents/_common/radiation_pass.py --self-test` → **16/16**.
- `python3 scripts/knowledge_regression.py` → **11 locked, 5 pending, 0 failed**.
- `python3 scripts/ics_normalize.py --self-test` → **22 passed, 0 failed**.
- `python3 scripts/nota.py --check` → **2 canonical cards, shape/index clean**.
- `python3 scripts/module_scaffold.py --self-test` → **7 passed**.
- `python3 scripts/render_docs.py --check` → generated blocks match.
- `python3 -m radiation_core.relay` → **0 findings**.
- `python3 scripts/status.py --self-test` → **3/3**.
- `python3 -m compileall -q scripts radiation_core agents` → success.
- `python3 scripts/verify_apply.py --strict` → exit 0 / no FAIL-class finding.
- `git diff --check` → clean.

## Direct negative probes added by the patch

```text
unsupported_keywords({'$defs': {'bad': {'contains': {'type':'string'}}}})
  -> ['contains']
unsupported_keywords({'if': {'type':'string'},
                      'then': {'contains': {'type':'string'}}})
  -> ['contains']
```

The result establishes only the stated mechanism. It does not certify a model,
provider, retrieval pipeline, or Commander decision.
