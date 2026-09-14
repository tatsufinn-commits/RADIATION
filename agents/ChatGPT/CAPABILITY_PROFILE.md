# CAPABILITY PROFILE — ChatGPT / OpenAI

`reviewed_on: 2026-09-14` · `consolidated: 5600 (2026-09-14)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Current official record (exact IDs and pricing live on these pages)
- **Model catalog** [O, developers.openai.com/api/docs/models — retrieved 2026-09-14 via gate-review sweep]: the official API catalog currently recommends **`gpt-6-astra`**, **`gpt-5.6-terra`**, **`gpt-5.6-luna`** — exact IDs, ~1.05M-token context values, tools, reasoning settings, cutoffs, and pricing stated on the page. **[Local re-verification = standing review trigger]**
- **Pricing** [O, openai.com/business/pricing/#api]: per-ID prices are read from this page before any spend decision; never from aggregators.
- **Tool/agent surfaces:** Responses API + tool calling [Official product docs — platform.openai.com/docs; verify current shape].
- **Status/uptime:** `status.openai.com` [Official — canonical link, check live before relying].

## Safety, policy, privacy (the API/consumer split is the story)
- **API (your key): no training on API data by default**; Zero Data Retention for eligible customers [Official, openai.com/index/offering-zero-data-retention-for-frontier-models/, retrieved 2026-08-19]; ~30-day abuse-log retention [Secondary, consistent].
- Consumer ChatGPT differs (training on by default, opt-out) [Secondary, humla.team 2026-07-28]. Enterprise data not used for training without opt-in [Secondary quoting enterprise-privacy page, 2025-03-30 — reverify].

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | web-connected product surfaces; reasoning tier for synthesis |
| Corpus navigation | strong | long-context + structured extraction |
| Scaffolding | strong | tool-calling agent surfaces |
| Governance/cue work | adequate | strong instruction-following; policy-verbatim work fine |
| Implementation/review | strong | flagship for review; mini tier for volume |
| Documentation | strong | |
| Creative | strong | image + long-form generation |

*Values are unmeasured impressions — no named RADIATION local evaluation exists yet; this table is never a routing decision rule (see `agents/ROUTING_MATRIX.md` header).*

**Routing:** load `agents/ChatGPT/` only when the host is explicitly known as ChatGPT/OpenAI; otherwise the generic CAP path — never infer a provider from output style.

## History (superseded 2026-09-14 — secondary snapshots; comparison evidence only, NOT the current line)
- GPT-5.4 ≈ $2.50/$15 per 1M in/out; GPT-5.5 reported at $5/$30 [Secondary, dated 2026-06..09].
- GPT-4.1 family ($2/$8; Mini $0.40/$1.60; Nano $0.10/$0.40); o-series (o3 $2/$8; o3-pro $20/$80; o4-mini $0.55/$2.20) [Secondary].
- Long context reported at 200K–400K depending on model [Secondary — superseded by the official ~1.05M-class catalog values].
- Batch API at ~50% of standard rates; cached-input discounts (~10× off input) [Secondary, multiple, consistent — current rates: official pricing page].
- Sources: metacto.com 2026-06-11, zylo.com 2026-08-13, pecollective.com (2026).
