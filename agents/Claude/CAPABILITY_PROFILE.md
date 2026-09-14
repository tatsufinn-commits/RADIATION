# CAPABILITY PROFILE — Claude / Anthropic

`reviewed_on: 2026-09-14` · `consolidated: 5600 (2026-09-14)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Current official record (exact IDs and pricing live on these pages)
- **Models overview** [O, platform.claude.com/docs/en/models/overview — retrieved 2026-09-14 via gate-review sweep]: lists current **Fable 5.1, Opus 5, Sonnet 5, Haiku 4.5 with exact API IDs, context windows, knowledge cutoffs, pricing, thinking/effort settings, and model-versioning guidance.** Exact IDs/statuses/pricing come from this page, never from aggregators. **[Local re-verification = standing review trigger]**
- **API surface** [O, claude.com/platform/api].
- **Status:** `status.anthropic.com` [Official — canonical link].

## Access, cost, availability
- Pay-per-token API + consumer subscriptions; AWS Bedrock / Google Vertex availability [Secondary, datastudios 2026-09-07].

## Safety, policy, privacy (API vs consumer split)
- **API/Commercial: customer content is NOT used for training** ("Anthropic may not train models on Customer Content from Services") [Secondary quoting Commercial Terms, terms.law 2026-06-27]; API log retention reduced to ~7 days (since 2025-09-15), ZDR available [Secondary, datastudios 2026-09-07, anonyome 2026-04-17].
- **Consumer claude.ai:** the two secondaries disagree on the training-default direction post-2025-10-08 — resolve against anthropic.com/legal/privacy before quoting [Secondary conflict — standing review trigger]. Safety-flagged content retained longer regardless [Secondary].
- BAA available for eligible plans; DPA defines processor duties [Secondary].

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | long context + citation-disciplined synthesis |
| Corpus navigation | strong | 1M-context tier suits the course corpus + registers |
| Scaffolding | strong | tool use + agentic coding surfaces |
| Governance/cue work | strong | policy-verbatim fidelity is a known strength |
| Implementation/review | strong | Opus/Fable tier for review; Haiku for volume |
| Documentation | strong | |
| Creative | strong | long-form prose |

*Values are unmeasured impressions — no named RADIATION local evaluation exists yet; this table is never a routing decision rule (see `agents/ROUTING_MATRIX.md` header).*

**Routing:** load `agents/Claude/` only when the host is explicitly known as Claude/Anthropic; otherwise the generic CAP path.

## History (superseded 2026-09-14 — secondary snapshots; comparison evidence only, NOT the current record)
- Fable 5.1 ($10/$50 per 1M in/out; launched ~2026-09-01; cache reads $0.25/M); Opus 5 ($5/$25); Haiku 4.5 ($1/$5) [Secondary, dated 2026-09-08..11].
- **Sonnet 5 price CONFLICT: $2/$10 (benchlm 2026-09-11) vs $3/$15 (developer.puter.com 2026-09-08, pecollective 2026-04-22)** — superseded by the official models-overview page; kept as evidence of aggregator unreliability.
- Long context: no surcharge up to 1M tokens reported [Secondary, 2026-09-08]. Batch API ~50% off where supported; cache reads ~10% of base input [Secondary, consistent].
