# CAPABILITY PROFILE — Gemini / Google (DeepMind)

`reviewed_on: 2026-09-14` · `consolidated: 5600 (2026-09-14)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Current official record (exact IDs, lifecycle, and pricing live on these pages)
- **Models** [O, ai.google.dev/gemini-api/docs/models — retrieved 2026-09-14 via gate-review sweep]: stable line = **Gemini 3.8 / 3.7 / 3.6 / 3.5 Flash**; **Gemini 3.1 Pro is PREVIEW** — lifecycle status is part of the record. Long-context values are read per model from the page. **[Local re-verification = standing review trigger]**
- **Pricing** [O, ai.google.dev/gemini-api/docs/pricing]: exact per-ID entries; aggregator tables are historical comparison evidence only.
- **Tool/agent use:** function calling + Google ecosystem grounding (Search) [Official docs — ai.google.dev; verify current shape].
- **Status:** `status.cloud.google.com` [Official — canonical link].

## Safety, policy, privacy (three distinct surfaces — never merge them)
- **Paid Gemini API:** developer-owned logs private to the Cloud project; **default maximum 55-day retention (7/14/28/55-day settings)**; **abuse monitoring separately retains API prompts, context, and output up to 55 days** for policy enforcement; training only on data you explicitly contribute as datasets ("Unpaid Services" terms; human reviewers may process contributed data, disconnected from account/key/project) [**Official**, ai.google.dev/gemini-api/docs/logs-policy + abuse-monitoring docs, retrieved 2026-09-14]. "Private to the project" is NOT "not retained" and NOT "not reviewable under defined conditions" — record surface, purpose, and retention separately for any deployment decision.
- **Consumer Gemini apps:** human-review program with reviewed content retained up to ~3 years, disconnected from account but not anonymized; 72-hour processing window even with activity off [User-reported/Secondary — Reddit GDPR discussion 2025-11-28, hathr.ai 2026-07-22; Google's own consumer help pages are the review trigger]. Enterprise/Workspace carries the stricter terms [Secondary].
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
