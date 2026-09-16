# WARN LEDGER — accepted-class WARN census (P-12)

**Purpose:** Close out standing WARN-class debt so census number 4 can either shrink or be honestly chartered. Per P-12 directive: enumerate 4 WARN checks by name, apply exactly ONE disposition (Fix or Charter), budget ≤2 files each. Goal: WARN count either falls, or each surviving WARN has written reason. Both outcomes success; hiding WARNs is not.

**Base:** 0c0548b19e7bb3ddc1c8ff83ee5e3e5105959aef (sealed merge PR #2 + RD-3 + run #82 fix)
**Validator:** 42·38·4·0 at base (4 WARN tolerated)

## WARN Census at base 0c0548b

### 1. WARN [check 11.6] replica tranche authority — OPEN GOVERNED EXCEPTION
- **Status:** OPEN GOVERNED EXCEPTION (status: commander-review-requested): pairs admitted provisionally, NOT Commander-ratified; decision options: docs/REPLICA_DECISION.md
- **Disposition:** Charter — accepted-class
- **Rationale:** WARN 11.6 is accepted-class because replica tranche is provisionally admitted per Commander order with explicit ratification record commander-review-requested, decision options A/B documented in docs/REPLICA_DECISION.md, no deletion, drift fails, Commander-only narrowing — governance exception by design, not defect. Surfaces info by design.

### 2. WARN [check 15] boot-byte budget
- **Status:** Tier0+1=45574 B (44.5 KB / cap 40) · Tier0-2=73215 B (71.5 KB / cap 80) · ~18303 tokens · task_ledger boot-effective (last 3 rows)=1879 B · enforcement=WARN-class (P-09 pending ratification) · II.10 compression: ACTIVE
- **Disposition:** Charter — accepted-class
- **Rationale:** WARN 15 is accepted-class because boot-byte census surfaces info by design, Tier0+1 over cap 40 due to state-carrying docs (SYSTEM_STATE, CAPABILITIES, CUE_INDEX), II.10 compression ACTIVE (archive never delete), P-09 pending ratification keeps enforcement WARN-class, not FAIL. Boot carries state not narrative.

### 3. WARN [check 16] meta-budget
- **Status:** 42 canon(orange) patches vs 4 content sessions (law allows 1 per 3 => OVER budget by 122 session-equivalents)
- **Disposition:** Charter — accepted-class
- **Rationale:** WARN 16 is accepted-class because meta-budget census surfaces info by design — canon patches are governance/mechanical hardening (P-01..P-11, RD-3, 4 laws) during hardening phase, content sessions are Commander-gated (building codes), ratio over budget is informational not blocking, honest ledger.

### 4. WARN [check 20.5] planner theater guard
- **Status:** plan exists and the last 3 task_ledger rows record no attempt — plans are not progress (AP-08). Record one with marker `attempt:`
- **Disposition:** Fix — trivially fixable in scope P-12 (≤2 files)
- **Fix applied:** Added `attempt:` row in Brain/frontal_lobe/task_ledger.md for P-12 build execution (stacked acceptance run before ship) per Brain/short_term/plan/README.md recording attempt. After fix, check 20.5 should PASS or still WARN but with attempt present, census reduces to 3.
- **Rationale:** WARN 20.5 is fixable by practicing and writing row, not by writing sentence containing right word — AP-08 guard watches last three task_ledger rows for explicit marker attempt:/mastery:/drilled/@Review.

## Outcome Goal

- WARN count either falls (20.5 fixed → 42·39·3·0 or 42·38·3·1?), or each surviving WARN has written reason in this ledger.
- Both outcomes are success; hiding WARNs is not.
- Future readers: check output text [accepted] marks chartered WARNs so don't re-litigate.

## References

- Validator check definitions: scripts/validate.py
- Incident chain #75-#81 memo: 08-overhaul/MEMO_POSTMORTEM_gate-chain-2026-09-16.md
- Motor preflight: docs/RELEASE_TRUTH_GATE/README.md + scripts/push_preflight_check.py
- Base: 0c0548b19e7bb3ddc1c8ff83ee5e3e5105959aef
