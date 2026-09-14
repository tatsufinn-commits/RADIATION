# CAPABILITY PROFILE — Grok / xAI

`reviewed_on: 2026-09-14` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Capabilities
- **Model families (current line, [Secondary, dated 2026-09-11, benchlm.ai]):** Grok 4.6 ($2/$6 per 1M in/out; cached input $0.50; 500K context), Grok 4.5 / 4.20 ($2/$6), Grok 4.3 ($1.25/$2.50; 1M context), Grok 4.1 Fast ($0.20/$0.50; 2M context), Grok Code Fast 1 (~$0.20/$1.50; $0.02/M cached-input rate reported). Higher-context surcharges above 200K on flagship tiers [Secondary]. **Verify on the official xAI docs/pricing before spend decisions.**
- **Reasoning:** reasoning and non-reasoning variants of the Fast line [Secondary, intuitionlabs 2026-08-09].
- **Multimodality:** vision models reported (grok-2-vision class) [Secondary — verify current lineup].
- **Tool/agent use:** function calling + agent tooling in xAI docs [Official docs — docs.x.ai; verify current shape].
- **Differentiator:** X (Twitter) real-time grounding — a consumer-surface trait; **the API does not automatically include live X data** [Secondary — review trigger].

## Access, cost, availability
- Pay-per-token API + X consumer surfaces [Secondary].
- Status: xAI status page (canonical link not confirmed in this sweep — treat as **[Unverified — review trigger]**).

## Safety, policy, privacy (API vs consumer split)
- **API: "xAI never trains on your API inputs or outputs without your explicit permission"** [Official FAQ quote via secondary, aiprovidertrust.com verified 2026-08-25]; default ~30-day encrypted abuse-audit retention, auto-deleted after 30 days; enterprise ZDR available (sales-gated) [Secondary, meetily.ai 2026-06-29, aiprovidertrust 2026-07-05].
- **Consumer (X): public posts and Grok conversations used for training by default unless opted out** [Secondary — describes the consumer surface, NOT the API].
- Compliance posture: SOC 2 Type 2 claimed; trust center NDA-gated; signed only the Safety/Security chapter of the EU GPAI Code of Practice [Secondary, aiprovidertrust 2026-07-05].

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | strong on volume economics |
|---|---|---|
| Research | adequate | real-time grounding is consumer-surface; API research fine |
| Corpus navigation | strong | 1–2M-context tiers at low cost |
| Scaffolding | strong | Code Fast tier priced for agentic loops |
| Governance/cue work | adequate | |
| Implementation/review | strong | Code Fast + 4.6 for review |
| Documentation | strong | |
| Creative | adequate | |

**Routing:** load `agents/Grok/` only when the host is explicitly known as Grok/xAI; otherwise the generic CAP path.
