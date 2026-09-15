# CAPABILITY PROFILE — Grok / xAI

`reviewed_on: 2026-09-15` · `consolidated: 5600 (2026-09-14) → 5830 (2026-09-15)` · Review trigger: official pricing/model-page change, or 90 days (re-review by 2026-12-13) · Maintainer: S006 (Architect) — 5820 compliance refresh + 5830 surface analysis

## Current official record (exact IDs live on this page)
- **Model page** [O14, docs.x.ai/developers/models — retrieved 2026-09-15]: grok-4.6 re-confirmed 500K $2/$6 cutoff 2026-02-01 alias policy classes + search-tools requirement + Imagine/Voice ids observed (media surfaces, own records required) [O14]. Prior sweep O9 2026-09-14 lists grok-4.6 with 500K context, $2/$6 per MTok, configurable reasoning, tool features, Feb 1 2026 cutoff; real-time data requires search tools; alias vs dated-ID behavior. Every additional Grok model needs its own live status/ID record before routing use. **[Local re-verification = standing review trigger]**
- **Status:** xAI status page (canonical link not confirmed in this sweep — **[Unverified — review trigger]**).

## Safety, policy, privacy (API vs consumer split — 5820 compliance refresh)

- **API privacy scope — does NOT apply to API business offerings or X platform:** “This Privacy Policy does NOT apply to our API or X platform (X Privacy Policy governs Grok on X)”; ask NOT to include personal info in prompts; collects account data (name, contact, credentials, DOB, third-party logins X/Google/Apple), payment via third-party, communication, user content, feedback, social; retention legitimate business need or legal; conversations queued deletion within 30 days unless legal/compliance/safety [O23 Effective Aug 24 2026, https://x.ai/legal/privacy-policy — receipt O23].
- **Consumer terms:** Last updated Sept 11 2026; governs Grok, Grokipedia, other individual services; Enterprise Terms govern APIs; Europe EST for EEA/UK/CH; disputes Tarrant/Wichita County TX, waiver class action; min age 13, 13-17 parental consent; controls for undesirable training data/output [O24 Last updated Sept 11 2026, https://x.ai/legal/terms-of-service — receipt O24].
- **AUP effective Aug 14 2026:** Prohibits modifying/copying/reverse engineer, jailbreaking/prompt injection, viruses/malware/spam/DDoS, stripping provenance, developing competing ML models, scraping/harvesting, disrupting safety/rate limits, harming human life, IP violation, privacy/right of publicity (nudifying, impersonation, pornographic likeness, defamation), sexualizing children, high-stakes automated decisions without human review, misleading AI use [O25 Effective Aug 14 2026, https://x.ai/legal/acceptable-use-policy — receipt O25].
- **API: "xAI never trains on your API inputs or outputs without your explicit permission"** [Official FAQ quote via secondary, aiprovidertrust.com verified 2026-08-25]; default ~30-day encrypted abuse-audit retention, auto-deleted after 30 days; enterprise ZDR available (sales-gated) [Secondary, meetily.ai 2026-06-29, aiprovidertrust 2026-07-05].
- **Consumer (X): public posts and Grok conversations used for training by default unless opted out** [Secondary — describes consumer surface, NOT API].
- Compliance posture: SOC 2 Type 2 claimed; trust center NDA-gated; signed only Safety/Security chapter of EU GPAI Code of Practice [Secondary, aiprovidertrust 2026-07-05].

## RADIATION task suitability [Assessment — ours]
| Task class | Suitability | Note |
|---|---|---|
| Research | adequate | real-time grounding is consumer-surface; API research fine |
| Corpus navigation | strong | long-context tiers at low cost |
| Scaffolding | strong | Code Fast tier priced for agentic loops |
| Governance/cue work | adequate | |
| Implementation/review | strong | Code Fast + 4.6 for review |
| Documentation | strong | |
| Creative | adequate | |

*Values are unmeasured impressions — no named RADIATION local evaluation exists yet; this table is never a routing decision rule (see `agents/ROUTING_MATRIX.md` header).*

**Routing:** load `agents/Grok/` only when the host is explicitly known as Grok/xAI; otherwise the generic CAP path.

## History (superseded 2026-09-14 — secondary snapshots; comparison evidence only, NOT the current record)
- Grok 4.5 / 4.20 ($2/$6), Grok 4.3 ($1.25/$2.50; 1M context), Grok 4.1 Fast ($0.20/$0.50; 2M context), Grok Code Fast 1 (~$0.20/$1.50; $0.02/M cached-input rate reported) [Secondary, benchlm.ai 2026-09-11 — corroborated by the official 4.6 entry; each additional model still needs its own live record].
- Higher-context surcharges above 200K on flagship tiers; reasoning/non-reasoning variants of the Fast line [Secondary, intuitionlabs 2026-08-09]. Vision models reported (grok-2-vision class) [Secondary — verify current lineup].
