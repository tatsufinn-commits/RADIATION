# RESEARCH METHOD — provider capability/routing studies (5400)

`reviewed_on: 2026-09-14` · Scope: how the profiles, sources, and matrix in `agents/` were produced, and how they must be maintained.

## Method (what was actually done)
1. **Fresh web sweep on 2026-09-14** (S005 session, Arena Agent Mode host) — search-engine discovery per provider over: current model lineup, API pricing, privacy/retention posture, status/reliability surfaces, and (for the host) product-launch coverage. No claim in the profiles comes from model memory alone; stale-memory facts were either verified by the sweep or marked unverified.
2. **Tier labeling on entry:** [O] official primary (the provider's own page/docs/status) · [S] secondary dated coverage (aggregators, reviews, policy analyses — always with publication/verification date) · [U] user-reported (forums; never treated as fact) · [B] benchmark/independent evaluation (kept separate from product claims).
3. **Conflict policy:** conflicting secondary rates are RECORDED AS CONFLICTS (e.g., Sonnet 5 pricing), never averaged, never silently resolved; the official page is named as the resolution trigger.
4. **Gap policy:** missing official surfaces (Arena privacy/pricing/status; xAI status) are DECLARED as gaps with review triggers — a declared gap is honest; an invented link is fabrication.

## Red lines enforced on this layer (check 38 lints these)
- No model-identity claims for any host — least of all Arena (blind-battle design makes identity unknowable in-session).
- No first-person power claims ("I can push", "my tools") anywhere in this layer.
- No private-access, billing, or retention claims without a dated source in the provider's `SOURCES.md`.
- API / consumer / enterprise surfaces are never merged into one claim.

## Maintenance
- **Expiry:** every volatile claim carries a 90-day review trigger (this generation: **2026-12-13**) or a shorter page-specific trigger where noted.
- **Update path:** a re-review edits the provider's `CAPABILITY_PROFILE.md` + `SOURCES.md` in place, bumps `reviewed_on`, and records the sweep date; conflicts get new dated rows, old rows stay for history.
- **What this layer is NOT:** it confers no access, binds no host, and never overrides `docs/THREAT_MODEL.md` or the II.11 boundary. It is research NOTES for the Commander's routing decisions — a handoff, like everything else in `agents/`.
