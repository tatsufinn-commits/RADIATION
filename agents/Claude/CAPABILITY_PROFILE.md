# CAPABILITY PROFILE — Claude / Anthropic

`reviewed_on: 2026-09-15` · `consolidated: 5600 (2026-09-14) → 5830 (2026-09-15)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S006 (Architect) — 5820 compliance refresh + 5830 surface analysis

## Current official record (exact IDs and pricing live on these pages)
- **Models overview** [O12, platform.claude.com/docs/en/models/overview — retrieved 2026-09-15]: exact IDs captured: claude-fable-5-1 $10/$50 1M, claude-opus-5 $5/$25 1M, claude-sonnet-5 $2/$10 1M (conflict resolved $3/$15 vs $2/$10 → $2/$10 official), claude-haiku-4-5-20251001 $1/$5 200K; cutoffs Jun/May/Jan 2026 + Feb 2025 [O12]. Prior sweep O4 2026-09-14 lists Fable 5.1, Opus 5, Sonnet 5, Haiku 4.5. **[Local re-verification = standing review trigger]**
- **API surface** [O5, claude.com/platform/api — retrieved 2026-09-14].
- **Status:** `status.anthropic.com` [Official — canonical link].

## Access, cost, availability
- Pay-per-token API + consumer subscriptions; AWS Bedrock / Google Vertex availability [Secondary, datastudios 2026-09-07 historical lead only per 5810 R2, but O5 confirms platform].

## Safety, policy, privacy (API vs consumer split — 5820 compliance refresh)

- **API/Commercial: customer content is NOT used for training** — “Anthropic may NOT train models on Customer Content from Services” — Services not for consumer use; customer retains all rights to inputs, owns outputs; DPA incorporated [O19 2026-09-15, https://www.anthropic.com/legal/commercial-terms — receipt O19]. This supersedes secondary quote via terms.law [S3].
- **Consumer privacy split:** Consumer Privacy Policy does NOT apply to Enterprise (governed by customer agreements); personal data: identity/contact, payment, inputs/outputs (may be reproduced in outputs), feedback stores entire conversation, technical info (device, usage, logs, cookies); training data from public web, commercial datasets, user inputs/outputs unless opt-out [O18 2026-09-15, https://www.anthropic.com/legal/privacy — receipt O18].
- **AUP — Universal + High-Risk + Additional Guidelines:** Prohibits illegal activity, critical infrastructure disruption, computer/network compromise, weapons development, violence/hate, privacy/identity violation, children safety, psychologically harmful, misinformation, throttling/suspension [O20 2026-09-15, https://www.anthropic.com/legal/aup — receipt O20].
- **Retention:** API logs →7 days since 2025-09-15 per S2 historical lead [S2 2026-09-07 — historical lead only per 5810 R2, must reverify against O18/O19 official]; safety-flagged content retained longer regardless [Secondary]; BAA available for eligible plans; DPA defines processor duties [O19].

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
