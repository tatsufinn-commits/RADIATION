# Verification Policies — Golden Traces (WP-1 1.5)
**Basis:** Repo E critique policy field — additive optional verify policy field on every subskill/cue per 1.5
**Law:** Six ratified laws D029 · D1–D10 · FF-seal only · sequence as-written · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate
**Checklist:** Per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md

## Three minimal golden traces (one per policy class), stdlib-asserted, registered as WP-2.3 cassette SEEDS per J1

**J1 rule of travel:** build neither twice — these traces are built once in WP-1 1.5 and registered by name as WP-2.3 cassette SEEDS, WP-2.3 will consume them, not rebuild

### Traces

1. **trace_required.json** — policy_class required — subskill SUB-001, cue CUE-BOOT-MAGIC — seed WP-2.3-cassette-seed-required-SUB-001 — PROVEN
2. **trace_opt_in.json** — policy_class opt-in — subskill SUB-002, cue CUE-BUDGET-OVERRIDE — seed WP-2.3-cassette-seed-opt-in-SUB-002 — PROVEN
3. **trace_opt_out.json** — policy_class opt-out — subskill SUB-003, cue CUE-CONSTITUTION-SHAPE — seed WP-2.3-cassette-seed-opt-out-SUB-003 — PROVEN

### WP-2.3 consumption (v3.10.33) — seeds CONSUMED per J1

- **Cassette:** `evals/verify_policies/CASSETTE_WP23.json` — five rows: the three seeds above, consumed **by name** (the traces are read as they stand, never rebuilt) + Cassette A (5830 activation surfaces) + E2 (5900-1 gate self-test + relay numeric plan ordering)
- **Runner:** `python3 scripts/verify_cassette_runner.py` — deterministic, stdlib-only; per-row verdict PASS / WARN-and-justify / RETURNED; `--self-test` vector battery
- **Seed checks:** trace JSON valid · policy_class in {required, opt-in, opt-out} and equal to the row's class · `cassette_seed` and `verify.seed` equal the seed name · `stdlib_asserted` true
- **Advisory:** `scripts/verify_apply.py` runs the cassette; all rows PASS → silent; any non-PASS row → WARN-class line with its justification — never FAIL-class (Law 3 warn-and-justify, Law 2 raise-only)
- **Tests:** `tests/test_verify_cassette_runner.py`
- **Change control:** per scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md

### Router honors

- **required:** verification must run — deterministic checks only, no behavioral grading per 1.5
- **opt-in:** verification may run if opted in — warn-and-justify per Law 3, never auto-reject
- **opt-out:** verification may skip if opted out — quarantine-before-delete per Law 4

### Acceptance

- Three traces exist at evals/verify_policies/trace_*.json — PROVEN
- Each trace stdlib-asserted (pure JSON, no network, no deps) — PROVEN via python3 -m json.tool
- Each trace registered by name as WP-2.3 cassette seed — PROVEN via this README + seed field per J1
- No behavioral grading — format and deterministic checks only per 1.5 — PROVEN
- Existing linters tolerate unknown keys — subskill_check.py and cue_resolver.py updated to allow verify field, additionalProperties handling per 1.5 namespaced extension — PROVEN via lint green

### Battery

- subskill_check.py 0 findings — verifies catalog valid + FK resolves + scenario_ref resolves + trigger enum valid + status discipline + verify.policy enum per 1.5
- cue_resolver.py --lint 0 findings — 46 cues, verify field allowed per 1.5
- python3 -m json.tool evals/verify_policies/*.json — all valid JSON per stdlib

### Laws acknowledged

D1–D10 · six ratified laws D029 · FF-seal only · sequence WP-1→WP-2.3→WP-2/3→WP-4 · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate · pure-additive per 1.3 · checklist citation per 1.6

### Research-only venue pointers

None — zero network, zero live venue, zero SaaS in WP-1 per Law 6 — every venue mention marked research-only
