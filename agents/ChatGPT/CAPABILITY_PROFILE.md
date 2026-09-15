# CAPABILITY PROFILE — ChatGPT / OpenAI

`reviewed_on: 2026-09-15` · `consolidated: 5600 (2026-09-14) → 5830 (2026-09-15)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S006 (Architect) — 5820 compliance refresh + 5830 surface analysis

## Current official record (exact IDs and pricing live on these pages)
- **Model catalog** [O11, developers.openai.com/api/docs/models — retrieved 2026-09-15]: official API catalog recommends `gpt-6-astra` $10/$50 cutoff 2026-04-30, `gpt-5.6-sol` alias `gpt-5.6` $4/$20, `gpt-5.6-terra` $2/$12, `gpt-5.6-luna` $0.20/$1.20 — all 1.05M ctx, 128K out, cutoff 2026-02-16 [O11]. Prior sweep O1 2026-09-14: gpt-6-astra / gpt-5.6-terra / gpt-5.6-luna. **[Local re-verification = standing review trigger]**
- **Pricing** [O2, openai.com/business/pricing/#api]: per-ID prices read from this page before any spend decision; never from aggregators — retrieved 2026-09-14, re-retrieved via O11.
- **Tool/agent surfaces:** Responses API + tool calling [Official product docs — platform.openai.com/docs; verify current shape].
- **Status/uptime:** `status.openai.com` [Official — canonical link, check live before relying].
- **Zero Data Retention:** Frontier models ZDR announcement for eligible customers [O3 2026-08-19].

## Safety, policy, privacy (the API/consumer split is the story — 5820 compliance refresh)

- **API (your key): no training on API data by default since Mar 1 2023 unless opt-in** — “Your data is your data. API not used for training by default since Mar 1 2023” [O17 2026-09-15, https://developers.openai.com/api/docs/guides/your-data — receipt O17].
- **Consumer vs API privacy split:** Privacy policy does NOT apply to API business offerings (governed by customer agreements); personal data categories: account info, user content (prompts/files/images/audio/video), log/usage/device/location, cookies; marketing vendors + advertisers receive info [O15 2026-09-10 Updated 2026-09-10, https://openai.com/policies/privacy-policy — receipt O15].
- **Abuse monitoring 30-day retention:** Logs contain prompts/responses/metadata, retained up to 30 days unless legally required; ZDR and Modified Abuse Monitoring eligible with approval; endpoint table: /v1/chat/completions No training 30d ZDR Yes [O17].
- **Usage policies effective 2026-10-29:** Universal set across products; protect people (threats, self-harm, sexual violence, weapons, illicit), respect privacy (no facial recognition DB without consent, no real-time biometric ID, no likeness without consent), keep minors safe, empower people (no academic dishonesty, no high-stakes automation without human review, facial recognition/biometric limits) [O16 Effective 2026-10-29, https://openai.com/policies/usage-policies — receipt O16].
- **Enterprise privacy:** Fine-tuned models private; DPA; data-use boundaries per commercial terms — consumer ChatGPT differs (training on by default opt-out) [S4 humla.team 2026-07-28 secondary, but O15+O17 official now primary].

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
