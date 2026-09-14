# CAPABILITY PROFILE — ChatGPT / OpenAI

`reviewed_on: 2026-09-14` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Capabilities
- **Model families (current line, [Secondary, dated 2026-06..09]):** GPT-5.x flagship line (GPT-5.4 ≈ $2.50/$15 per 1M in/out; GPT-5.5 reported at $5/$30), GPT-4.1 family ($2/$8; Mini $0.40/$1.60; Nano $0.10/$0.40), o-series reasoning (o3 $2/$8; o3-pro $20/$80; o4-mini $0.55/$2.20), realtime and image models, embeddings. Sources: metacto.com 2026-06-11, zylo.com 2026-08-13, pecollective.com (2026). **Verify on the official pricing page before spending decisions — aggregator rates drift.**
- **Reasoning:** dedicated o-series reasoning tier [Secondary]; long context reported at 200K–400K depending on model [Secondary — review trigger].
- **Multimodality:** realtime (audio in/out), image generation, vision [Secondary].
- **Tool/agent use:** Responses API + tool calling; agent-oriented surfaces [Official product docs — platform.openai.com/docs; verify current shape].
- **Batch economics:** Batch API at 50% of standard rates; cached-input discounts (~10× off input) [Secondary, multiple, consistent].

## Access, cost, availability
- Pay-per-token API + ChatGPT consumer subscriptions; batch/cached discounts above [Secondary, dated].
- Status/uptime: official status page `status.openai.com` [Official — canonical link, check live before relying].

## Safety, policy, privacy (the API/consumer split is the story)
- **API (your key): no training on API data by default**; ~30-day abuse-log retention; Zero Data Retention for eligible customers; enterprise data not used for training without opt-in [Official, openai.com/index/offering-zero-data-retention-for-frontier-models/, 2026-08-19]. Consumer ChatGPT differs (training on by default, opt-out) [Secondary, humla.team 2026-07-28].
- Fine-tuned models are private to the customer and not shared [Official enterprise-privacy page via secondary, 2025-03-30 — reverify].

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | web-connected product surfaces; reasoning tier for synthesis |
| Corpus navigation | strong | long-context + structured extraction |
| Scaffolding | strong | tool-calling agent surfaces |
| Governance/cue work | adequate | strong instruction-following; policy-verbatim work fine |
| Implementation/review | strong | o-series + flagship for review; mini tier for volume |
| Documentation | strong | |
| Creative | strong | image + long-form generation |

**Routing:** load `agents/ChatGPT/` only when the host is explicitly known as ChatGPT/OpenAI; otherwise the generic CAP path — never infer a provider from output style.
