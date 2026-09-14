# CAPABILITY PROFILE — Claude / Anthropic

`reviewed_on: 2026-09-14` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Capabilities
- **Model families (current line, [Secondary, dated 2026-09-08..11]):** Fable 5.1 ($10/$50 per 1M in/out; launched ~2026-09-01; cache reads $0.25/M), Opus 5 ($5/$25), Sonnet 5, Haiku 4.5 ($1/$5). **Source conflict on Sonnet 5 pricing: $2/$10 (benchlm 2026-09-11) vs $3/$15 (developer.puter.com 2026-09-08, pecollective 2026-04-22) — resolve against anthropic.com/pricing before any spend decision.** Long context: no surcharge up to 1M tokens reported [Secondary, 2026-09-08].
- **Reasoning:** extended-thinking modes across the line [Official docs — docs.anthropic.com; verify current shape].
- **Multimodality:** vision input across the line; no native image *generation* in the API [Secondary/Official docs — review trigger].
- **Tool/agent use:** tool use + agent SDK/Claude Code surfaces [Official docs — verify].
- **Batch economics:** Batch API ~50% off where supported; cache reads ~10% of base input (Fable: $0.25/M) [Secondary, consistent].

## Access, cost, availability
- Pay-per-token API + consumer subscriptions + AWS Bedrock / Google Vertex availability [Secondary, datastudios 2026-09-07].
- Status: `status.anthropic.com` [Official — canonical link].

## Safety, policy, privacy (API vs consumer split)
- **API/Commercial: customer content is NOT used for training** ("Anthropic may not train models on Customer Content from Services") [Secondary quoting Commercial Terms, terms.law 2026-06-27]; API log retention reduced to ~7 days (since 2025-09-15), ZDR available [Secondary, datastudios 2026-09-07, anonyome 2026-04-17].
- **Consumer claude.ai:** training on by default unless opted out (post-2025-10-08 choice model); safety-flagged content retained longer regardless [Secondary, terms.law 2026-06-27 — the two secondaries disagree on the default direction; resolve against anthropic.com/legal/privacy before quoting].
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

**Routing:** load `agents/Claude/` only when the host is explicitly known as Claude/Anthropic; otherwise the generic CAP path.
