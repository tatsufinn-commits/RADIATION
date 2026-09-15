# CAPABILITY PROFILE — Gemini / Google (DeepMind)

`reviewed_on: 2026-09-15` · `consolidated: 5600 (2026-09-14) → 5830 (2026-09-15)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S006 (Architect) — 5820 compliance refresh + 5830 surface analysis

## Current official record (exact IDs, lifecycle, and pricing live on these pages)
- **Models** [O13, ai.google.dev/gemini-api/docs/models — retrieved 2026-09-15]: endpoint table captured — stable 3.8/3.7/3.6/3.5 Flash + Flash-Lite variants + media models; PREVIEW 3.1-pro-preview; numeric specs live on per-model pages [O13]. Prior sweep O6 2026-09-14: stable line = Gemini 3.8/3.7/3.6/3.5 Flash; Gemini 3.1 Pro is PREVIEW — lifecycle status is part of record. **[Local re-verification = standing review trigger]**
- **Pricing** [O7, ai.google.dev/gemini-api/docs/pricing — retrieved 2026-09-14]: exact per-ID entries; aggregator tables historical comparison evidence only.
- **Tool/agent use:** function calling + Google ecosystem grounding (Search) [Official docs — ai.google.dev; verify current shape].
- **Status:** `status.cloud.google.com` [Official — canonical link].

## Safety, policy, privacy (three distinct surfaces — never merge them — 5820 compliance refresh)

- **Paid vs Unpaid data-use split:** Unpaid Services: Google uses content to provide/improve/develop products + ML, human reviewers read disconnected; do NOT submit sensitive; Paid does NOT use prompts/responses to improve, processes per DPA, logs limited time for policy violations; safety features block harmful content; no competing models, no reverse engineer [O21 Effective Mar 23 2026, https://ai.google.dev/gemini-api/terms — receipt O21].
- **Abuse monitoring 55-day retention:** Trust and Safety automated + manual detection; retains prompts, contextual info, output for 55 days for detecting/preventing Prohibited Use Policy violations and legal disclosures; human review only by authorized via governance platform; NOT used to train/fine-tune except policy enforcement models [O22 Last updated 2026-06-09 UTC, https://ai.google.dev/gemini-api/docs/usage-policies — receipt O22, re-retrieval with publication date].
- **Logs policy:** Developer-owned logs private to Cloud project; default maximum 55-day retention (7/14/28/55-day settings); abuse monitoring separately retains API prompts, context, and output up to 55 days for policy enforcement; training only on data you explicitly contribute as datasets [O8 2026-09-14, O21+O22]. "Private to the project" is NOT "not retained" and NOT "not reviewable under defined conditions" — record surface, purpose, and retention separately for any deployment decision.
- **Consumer Gemini apps:** Human-review program with reviewed content retained up to ~3 years, disconnected from account but not anonymized; 72-hour processing window even with activity off [U/S — Reddit GDPR discussion 2025-11-28, hathr.ai 2026-07-22; Google's own consumer help pages are review trigger]. Enterprise/Workspace carries stricter terms [Secondary].
- **Do not paste personal data into consumer surfaces; prefer the paid API for repo-adjacent work.** [Assessment — ours]

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | grounding + long context |
| Corpus navigation | strong | long-context class over the corpus in one pass (unmeasured) |
| Scaffolding | strong | function calling + ecosystem |
| Governance/cue work | adequate | |
| Implementation/review | strong | Pro tier; Flash for volume |
| Documentation | strong | |
| Creative | strong | image/video generation models |

*Values are unmeasured impressions — no named RADIATION local evaluation exists yet; this table is never a routing decision rule (see `agents/ROUTING_MATRIX.md` header).*

**Routing:** load `agents/Gemini/` only when the host is explicitly known as Gemini/Google; otherwise the generic CAP path.

## History (superseded 2026-09-14 — secondary snapshots; comparison evidence only, NOT the current record)
- Gemini 3.1 Pro ($2/$12 ≤200K; $4/$18 >200K; 2M context — "industry-largest" claimed by aggregators); Gemini 3.5 Flash ($1.50/$9, new 2026-05-19); Gemini 3/3.1 Flash-Lite ($0.25–0.50 in); legacy 2.5 line [Secondary: getapipulse 2026-09-08, opslyft 2026-06-02, metacto 2026-06-11].
- The "3.1 Pro as current flagship line" framing is **corrected** by the official models page (3.1 Pro = PREVIEW; stable = 3.8/3.7/3.6/3.5 Flash).
- Batch ~50% off; generous free tier reported [Secondary].
