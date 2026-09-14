# CAPABILITY PROFILE — Gemini / Google (DeepMind)

`reviewed_on: 2026-09-14` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

## Capabilities
- **Model families (current line, [Secondary, dated 2026-06..09]):** Gemini 3.1 Pro ($2/$12 ≤200K; $4/$18 >200K; 2M context — "industry-largest" claimed by aggregators), Gemini 3.5 Flash ($1.50/$9, new 2026-05-19), Gemini 3/3.1 Flash-Lite ($0.25–0.50 in), legacy 2.5 line. Sources: getapipulse 2026-09-08, opslyft 2026-06-02, metacto 2026-06-11. **Verify on ai.google.dev/pricing before spend decisions.**
- **Long context:** 1M standard; 2M on 3.1 Pro [Secondary — the differentiating strength].
- **Multimodality:** native multimodal input (text/image/audio/video) across the line; image/video generation on dedicated models [Secondary — verify per model].
- **Tool/agent use:** function calling + Google ecosystem grounding (Search) [Official docs — ai.google.dev; verify current shape].
- **Batch economics:** Batch ~50% off; generous free tier reported [Secondary].

## Access, cost, availability
- Pay-per-token API (AI Studio / Vertex) + consumer Gemini subscriptions + Workspace enterprise [Secondary].
- Status: `status.cloud.google.com` [Official — canonical link].

## Safety, policy, privacy (three distinct surfaces — never merge them)
- **Paid Gemini API:** developer-owned logs private to the Cloud project; separate from abuse monitoring; training only on data you explicitly contribute as datasets ("Unpaid Services" terms; human reviewers may process contributed data, disconnected from account/key/project) [**Official**, ai.google.dev/gemini-api/docs/logs-policy, retrieved 2026-09-14].
- **Consumer Gemini apps:** human-review program with reviewed content retained up to ~3 years, disconnected from account but not anonymized; 72-hour processing window even with activity off [User-reported/Secondary — Reddit GDPR discussion 2025-11-28, hathr.ai 2026-07-22; Google's own consumer help pages are the review trigger]. Enterprise/Workspace carries the stricter terms [Secondary].
- **Do not paste personal data into consumer surfaces; prefer the paid API for repo-adjacent work.** [Assessment — ours]

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | grounding + long context |
| Corpus navigation | strongest | 1–2M context over the whole corpus in one pass |
| Scaffolding | strong | function calling + ecosystem |
| Governance/cue work | adequate | |
| Implementation/review | strong | 3.1 Pro tier; Flash for volume |
| Documentation | strong | |
| Creative | strong | image/video generation models |

**Routing:** load `agents/Gemini/` only when the host is explicitly known as Gemini/Google; otherwise the generic CAP path.
