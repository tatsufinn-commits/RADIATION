# Provider Surface Analysis — 5830 Decision-Ready Five-Provider Study

**Date:** 2026-09-15 (Asia/Singapore)
**Version:** v3.10.8 — 5830 Surface Analysis
**Base:** `73888423e16097b2e37029823c379a82d7044d22` (green: 16-path delta vs fbce71b, 0 findings, 7/7, 38·4·0, 14 records, PASS activation)
**Sources:** O1–O26 from `catalogs/model_research/sources/REGISTER.json` (O1–O10 retrieved 2026-09-14 gate-review sweep, O11–O26 retrieved 2026-09-15, receipts in `sources/receipts/`)
**Scope:** Non-boot research notes, decision-ready, dated primary sources only for compliance claims. No evaluations, no routing decisions, no credentials, no SDK calls. Gaps declared where official source UNCONFIRMED.

**Purpose per RELEASE_TRUTH_GATE README:** After gate proven, surface-specific five-provider analysis using dated primary sources; explicit observed Arena/PASS activation study; then Commander-authorized local evaluations. Maintain distinction provider declarations vs host/session observations vs experimentally observed performance.

---

## Methodology (per agents/RESEARCH_METHOD.md)

- **Tiers:** [O]fficial primary > [S]econdary dated > [U]ser-reported > [B]enchmark. Consumer/API/Enterprise surfaces never merged.
- **Four dimensions:** Capability, Safety/Compliance, Operational, Activation/Self-Governance — 4–5 patterns each, each with dated source citation.
- **One RADIATION improvement per provider** — concrete doc/code check, not a model claim.
- **Conflicts/gaps recorded, never averaged.** Arena privacy/terms/status/model-identity = UNCONFIRMED gap per O26 [U] 2026-09-15 (404 reCAPTCHA), product surface only from O10 https://arena.ai/agent [O] 2026-09-14.

---

## 1 · ChatGPT / OpenAI — API surface

**Current official record:** O11 catalog 2026-09-15: `gpt-6-astra` $10/$50 cutoff 2026-04-30, `gpt-5.6-sol` alias `gpt-5.6` $4/$20, `gpt-5.6-terra` $2/$12, `gpt-5.6-luna` $0.20/$1.20 — all 1.05M ctx, 128K out, cutoff 2026-02-16; specialized lines observed (cyber/daybreak/image/realtime) [O11]. Pricing canonical O2 [O] 2026-09-14.

### Capability (5 patterns)

- **C1 — Flagship catalog with 1M-class context:** Official catalog recommends gpt-6-astra / gpt-5.6-terra / gpt-5.6-luna; 1.05M-token context values, tools, reasoning settings, cutoffs, pricing stated on page [O1 2026-09-14, O11 2026-09-15]. Local re-verification = standing review trigger.
- **C2 — Responses API + tool calling:** Tool/agent surfaces via Responses API + structured outputs; function calling documented in platform docs [O2 pricing page notes API surface, O1 models].
- **C3 — Long-context handling:** 1.05M in, 128K out per O11; series-aware handling for reasoning models; cutoff dates explicit.
- **C4 — Batch & cache economics:** Batch API ~50% off standard rates; cached-input discounts (~10× off) reported across secondaries, current rates from official pricing page [S secondary but O2 wins].
- **C5 — Zero Data Retention eligibility:** Frontier models ZDR announcement for eligible customers [O3 2026-08-19].

### Safety/Compliance (5 patterns)

- **S1 — No training on API data by default since Mar 1 2023 unless opt-in:** “Your data is your data. API not used for training by default since Mar 1 2023” [O17 2026-09-15, https://developers.openai.com/api/docs/guides/your-data].
- **S2 — Consumer vs API privacy split:** Privacy policy does NOT apply to API business offerings (governed by customer agreements); consumer ChatGPT differs (training on by default opt-out) [O15 2026-09-10, https://openai.com/policies/privacy-policy].
- **S3 — Abuse monitoring 30-day retention:** Logs contain prompts/responses/metadata, retained up to 30 days unless legally required; ZDR and Modified Abuse Monitoring eligible with approval [O17].
- **S4 — Usage policies effective 2026-10-29:** Universal set across products; protect people (threats, self-harm, weapons, illicit), respect privacy (no facial recognition DB without consent, no real-time biometric ID, no likeness without consent), keep minors safe, empower people (no academic dishonesty, no high-stakes automation without human review) [O16 2026-10-29].
- **S5 — Enterprise privacy:** Fine-tuned models private; DPA; data-use boundaries per commercial terms [O15 note + O17 endpoint table].

### Operational (4 patterns)

- **Op1 — Official pricing per-ID:** Read from https://openai.com/business/pricing/#api before any spend; never from aggregators [O2 2026-09-14].
- **Op2 — Status canonical:** https://status.openai.com [O, canonical link].
- **Op3 — Endpoint table for training/ZDR:** /v1/chat/completions No training 30d ZDR Yes per O17 table; eligibility approval required.
- **Op4 — Retention story:** 30-day abuse logs; consumer/API split; NYT order lifted 2025-09-26 per secondary [S4 2026-07-28 — secondary, confirm against O17].

### Activation/Self-Governance (4 patterns)

- **A1 — RADIATION routing:** Load `agents/ChatGPT/` only when host explicitly known as ChatGPT/OpenAI; otherwise generic CAP path — never infer provider from output style [AGENT_INDEX, check 38].
- **A2 — PASS boundary:** read authorized tool cap_probe; canonical_apply = commander_motor_act at every source level, outside any agent runtime (II.11) [radiation_pass.py 2026-09-15 observed].
- **A3 — Probe verification:** repository_path mounted, git_head 7388842, dirty false, tools_exposed capability_attestation + read_file_digest, effects_exposed [] [cap_probe.py observed 2026-09-15].
- **A4 — Stop-lines:** Never claim model identity from style; never merge consumer/API surfaces; check 38 validates routing, claims lint, profile absence.

### RADIATION improvement for OpenAI

- **IMP-OpenAI-1:** Add explicit ZDR eligibility checklist to `agents/ChatGPT/CAPABILITY_PROFILE.md` — cite O17 endpoint table + O3 announcement, note approval required, add receipt path, set review trigger 90 days. Implement as doc update + check 38 vector ensuring ZDR section exists when O17 present. (No runtime, no credential.)

---

## 2 · Claude / Anthropic — API surface

**Current official record:** O12 2026-09-15: `claude-fable-5-1` $10/$50 1M, `claude-opus-5` $5/$25 1M, `claude-sonnet-5` $2/$10 1M (conflict resolved: $3/$15 vs $2/$10, official $2/$10 wins), `claude-haiku-4-5-20251001` $1/$5 200K; cutoffs Jun/May/Jan 2026 + Feb 2025 [O12]. API surface O5 [O] 2026-09-14.

### Capability (5 patterns)

- **C1 — Exact ID lineup with thinking/effort settings:** Models overview lists exact API IDs, context windows, knowledge cutoffs, pricing, thinking/effort settings, model-versioning guidance [O4 2026-09-14, O12 2026-09-15].
- **C2 — Long-context tiers:** 1M for Fable/Opus/Sonnet, 200K for Haiku; no surcharge up to 1M reported [S secondary but O12 confirms].
- **C3 — API platform + Bedrock/Vertex availability:** Pay-per-token API + consumer subscriptions; AWS Bedrock / Google Vertex availability [S datastudios 2026-09-07 — historical lead only per 5810 R2, but O5 confirms platform].
- **C4 — Tool use + agentic coding surfaces:** Tool use documented in official docs [O5].
- **C5 — Model versioning guidance:** Dated IDs pin, aliases track latest per O12 note.

### Safety/Compliance (5 patterns)

- **S1 — Customer content NOT used for training (API):** “Anthropic may NOT train models on Customer Content from Services” — Services not for consumer use; customer retains inputs, owns outputs [O19 2026-09-15, https://www.anthropic.com/legal/commercial-terms].
- **S2 — Consumer privacy split:** Consumer Privacy Policy does NOT apply to Enterprise (governed by customer agreements); personal data includes identity/contact, payment, inputs/outputs (may be reproduced in outputs), feedback stores entire conversation, technical info [O18 2026-09-15].
- **S3 — Training data sources (consumer):** Public web, commercial datasets, user inputs/outputs unless opt-out [O18].
- **S4 — AUP universal + high-risk:** Universal Usage Standards for all users, High-Risk Use Case Requirements, Additional Guidelines; prohibits illegal, critical infra disruption, computer/network compromise, weapons, violence/hate, privacy/identity violation, children safety, psychologically harmful, misinformation [O20 2026-09-15].
- **S5 — DPA incorporated:** DPA defines processor duties per commercial terms [O19]; retention: API logs →7 days since 2025-09-15 per S2 historical lead [S2 2026-09-07 — historical lead only, must reverify against O18/O19].

### Operational (4 patterns)

- **Op1 — Official pricing per-ID:** From https://www.anthropic.com/pricing canonical; exact per-ID entries; aggregator tables historical only [O4, O12].
- **Op2 — Status canonical:** https://status.anthropic.com [O].
- **Op3 — ZDR available:** Enterprise ZDR available per S2 historical lead; sales-gated per commercial terms [O19 + S2].
- **Op4 — Commercial terms enforcement:** Services must comply with Usage Policy, Supported Regions, Service Specific Terms [O19].

### Activation/Self-Governance (4 patterns)

- **A1 — RADIATION routing:** Load `agents/Claude/` only when host explicitly known as Claude/Anthropic; otherwise generic CAP [AGENT_INDEX].
- **A2 — PASS boundary:** Same as OpenAI — read authorized, canonical_apply commander_motor_act [PASS observed].
- **A3 — Probe verification:** Same mounted check; dirty false; tools_exposed attestation [cap_probe observed].
- **A4 — Stop-lines:** Never merge consumer/API training defaults; resolve Sonnet-5 pricing conflict against official models overview (O12 wins); check 38 validates.

### RADIATION improvement for Anthropic

- **IMP-Anthropic-1:** Add explicit `supersedes` enforcement note to CAPABILITY_PROFILE.md — cite O19 “may NOT train on Customer Content” as hard boundary, add DPA reference, add AUP high-risk clause list from O20, set review trigger on any anthropic.com/legal/ change. Add check 38 vector ensuring commercial-terms section cites O19.

---

## 3 · Gemini / Google — API surface

**Current official record:** O13 2026-09-15: endpoint table captured — stable 3.8/3.7/3.6/3.5 Flash + Flash-Lite variants + media models; PREVIEW 3.1-pro-preview; numeric specs live on per-model pages [O13]. Pricing O7 [O] 2026-09-14. Logs policy O8 [O] 2026-09-14.

### Capability (5 patterns)

- **C1 — Stable Flash line + Pro PREVIEW:** Stable line = Gemini 3.8/3.7/3.6/3.5 Flash; 3.1 Pro is PREVIEW — lifecycle status part of record [O6 2026-09-14, O13 2026-09-15].
- **C2 — Long-context:** Long-context values read per model from page; Flash-Lite variants; media models [O13 note].
- **C3 — Tool/agent use:** Function calling + Google ecosystem grounding (Search) [Official docs].
- **C4 — Pricing per-ID:** Exact per-ID entries from https://ai.google.dev/gemini-api/docs/pricing [O7].
- **C5 — Free tier + batch ~50% off:** Free tier reported; batch discount secondary.

### Safety/Compliance (5 patterns)

- **S1 — Paid vs Unpaid data-use split:** Unpaid Services: Google uses content to provide/improve/develop products + ML, human reviewers read disconnected; do NOT submit sensitive; Paid does NOT use prompts/responses to improve, processes per DPA, logs limited time for policy violations [O21 2026-03-23, https://ai.google.dev/gemini-api/terms].
- **S2 — Abuse monitoring 55-day retention:** Retains prompts, contextual info, output for 55 days for detecting/preventing Prohibited Use violations and legal disclosures; human review only by authorized via governance platform; NOT used to train/fine-tune except policy enforcement models [O22 2026-06-09 UTC, https://ai.google.dev/gemini-api/docs/usage-policies].
- **S3 — Logs policy:** Developer-owned logs private to Cloud project; default maximum 55-day retention (7/14/28/55-day settings); abuse monitoring separately retains up to 55 days [O8 2026-09-14].
- **S4 — DPA processor:** Paid processes per DPA, logs limited period for Prohibited Use [O21].
- **S5 — No competing models, no reverse engineer, safety features block harmful content [O21].**

### Operational (4 patterns)

- **Op1 — Pricing canonical:** https://ai.google.dev/gemini-api/docs/pricing [O7].
- **Op2 — Status canonical:** https://status.cloud.google.com [O].
- **Op3 — Terms effective Mar 23 2026:** Must accept Google APIs Terms + Additional Terms; age 18+; professional/business not consumer; only Paid Services in EEA/CH/UK [O21].
- **Op4 — Abuse monitoring last updated Jun 09 2026 UTC:** Trust and Safety automated + manual detection; retains 55d; enforcement contact/rate limit/suspension/closure [O22].

### Activation/Self-Governance (4 patterns)

- **A1 — RADIATION routing:** Load `agents/Gemini/` only when host explicitly known as Gemini/Google; otherwise generic CAP [AGENT_INDEX].
- **A2 — PASS boundary:** read authorized, canonical_apply commander_motor_act [PASS].
- **A3 — Probe verification:** Same mounted/dirty false check [cap_probe].
- **A4 — Stop-lines:** Never merge Paid/Unpaid training claims; never quote consumer retention for API; check 38 validates.

### RADIATION improvement for Gemini

- **IMP-Gemini-1:** Add Paid vs Unpaid matrix to CAPABILITY_PROFILE.md — cite O21 Unpaid uses content vs Paid does NOT, cite O22 55-day retention, cite O8 logs private to project. Add check 38 vector ensuring matrix cites O21 + O22.

---

## 4 · Grok / xAI — API surface

**Current official record:** O14 2026-09-15: grok-4.6 re-confirmed 500K $2/$6 cutoff 2026-02-01 alias policy classes + search-tools requirement + Imagine/Voice ids observed [O14]. Models page O9 [O] 2026-09-14.

### Capability (5 patterns)

- **C1 — Grok-4.6 flagship:** 500K context, $2/$6 per MTok, configurable reasoning, tool features, Feb 1 2026 cutoff; real-time data requires search tools (API does not automatically include live X data); alias vs dated-ID behavior [O9, O14].
- **C2 — Fast tiers for agentic loops:** Fast variants, reasoning/non-reasoning, Code Fast tier priced for loops [S benchlm.ai 2026-09-11 — secondary but O9 confirms 4.6].
- **C3 — Vision/media models:** grok-2-vision class reported, Imagine/Voice ids observed [O14 note — own records required].
- **C4 — Pricing:** $2/$6 flagship, $1.25/$2.50 4.3 1M, $0.20/$0.50 4.1 Fast 2M per secondary, corroborated by official 4.6 entry [S + O9].
- **C5 — Endpoint table:** Docs at https://docs.x.ai [O canonical].

### Safety/Compliance (5 patterns)

- **S1 — API privacy scope:** Does NOT apply to API business offerings or X platform (X Privacy Policy governs Grok on X); ask NOT to include personal info in prompts; collects account data (name, contact, credentials, DOB, third-party logins X/Google/Apple), payment via third-party, communication, user content, feedback, social [O23 2026-08-24, https://x.ai/legal/privacy-policy].
- **S2 — Retention:** Legitimate business need or legal; conversations queued deletion within 30 days unless legal/compliance/safety [O23].
- **S3 — Consumer terms:** Last updated Sept 11 2026; governs Grok, Grokipedia; Enterprise Terms govern APIs; Europe EST for EEA/UK/CH; disputes Tarrant/Wichita TX; min age 13, 13-17 parental consent [O24 2026-09-11].
- **S4 — AUP effective Aug 14 2026:** Prohibits modifying/copying/reverse engineer, jailbreaking/prompt injection, viruses/malware/spam/DDoS, stripping provenance, developing competing ML models, scraping/harvesting, disrupting safety/rate limits, harming human life, IP violation, privacy/right of publicity (nudifying, impersonation, pornographic likeness, defamation), sexualizing children, high-stakes automated decisions without human review [O25 2026-08-14].
- **S5 — Compliance posture:** SOC 2 Type 2 claimed, trust center NDA-gated, GPAI Code partial signing per secondary [S secondary — must reverify].

### Operational (4 patterns)

- **Op1 — Docs/pricing canonical:** https://docs.x.ai [O].
- **Op2 — Status:** No official xAI status page confirmed in sweep — declared unverified in profile [Gap].
- **Op3 — Real-time requires search tools:** API does not automatically include live X data per O9 [O9].
- **Op4 — Alias policy:** Aliases track latest, dated IDs pin per O9/O14.

### Activation/Self-Governance (4 patterns)

- **A1 — RADIATION routing:** Load `agents/Grok/` only when host explicitly known as Grok/xAI; otherwise generic CAP [AGENT_INDEX].
- **A2 — PASS boundary:** read authorized, canonical_apply commander_motor_act [PASS].
- **A3 — Probe verification:** Same mounted check [cap_probe].
- **A4 — Stop-lines:** Never attribute consumer-X training defaults to API; never claim status page exists without source; check 38 validates.

### RADIATION improvement for xAI

- **IMP-xAI-1:** Add explicit “API vs X platform vs Grok on X” surface split to CAPABILITY_PROFILE.md — cite O23 does NOT apply to API or X platform, cite O24 Enterprise Terms govern APIs, cite O25 high-stakes automated decisions without human review prohibition. Add check 38 vector ensuring split cites O23 + O24 + O25.

---

## 5 · Arena AI / Arena Agent Mode — HOST surface (not a model provider)

**Current official record:** O10 product page https://arena.ai/agent [O] 2026-09-14: browse/research, code execution, deep research, model comparison, file upload, GitHub connect affordance. Secondary coverage: web search, image generation, file attachments, sandbox/bash [S chatgate.ai 2026-06-05, stork.ai 2026-06-05]. Official privacy/terms/status/model-identity = UNCONFIRMED gap per O26 [U] 2026-09-15 — both /privacy and /terms return 404 reCAPTCHA. No model record by design (blind-battle product design hides model identity [S5 2026-06-05]).

### Capability (4 patterns — host, not model)

- **C1 — Agent workflow surface:** browsing/research, code execution, deep research, model comparison listed by product page [O10]; file upload and GitHub connect observed [O10 gate-review retrieval].
- **C2 — Execution environment:** Folder-based workspace with file handling and bash execution [S6 2026-06-05 — secondary, consistent with probe catalog].
- **C3 — Modality coverage:** Text, code, image, video, vision, document, search evaluation [S5 2026-06-05 — benchmark-platform claim, not per-session promise].
- **C4 — Long context / rates / latency:** NOT stated — session-contingent and model-dependent; no claim made [Gap — review trigger].

### Safety/Compliance (4 patterns — gap-declared)

- **S1 — Policy URLs UNCONFIRMED:** Guessed /privacy and /terms paths returned 404 / reCAPTCHA in 2026-09-14 gate-review retrieval and 2026-09-15 O26 retrieval — official policy URL and applicable surface NOT confirmed; standing review trigger, not evidence that no policy exists [O10 gate-review + O26 2026-09-15].
- **S2 — No Arena-specific privacy/retention document found in sweep:** Gap declared per 5500 and compact handoff §2; product surface only from arena.ai/agent; no model record by design [O26].
- **S3 — Blind-battle model identity:** Outputs presented without revealing underlying model [S5]; profile therefore NEVER names underlying model without dated official source — hard red line in CAPABILITY_PROFILE.md.
- **S4 — Tool surface session-contingent:** What one session observes (probe catalog) is evidence about THAT session only; never generalize to platform [CAPABILITY_PROFILE hard red lines].

### Operational (4 patterns — unverified triggers)

- **Op1 — Free + paid tier ~$20/mo:** Reported [U/S stork.ai 2026-06-05] — never treated as fact until confirmed on official Arena pricing page [Unverified — review trigger].
- **Op2 — No official status page identified:** Unverified — review trigger [Gap].
- **Op3 — Reliability signals:** No official status page; no pricing page; no retention doc [Gaps].
- **Op4 — Product affordances grant nothing:** File upload + GitHub connect affordances observed do not grant tool/file/network/push authority; authority stays session-specific and must be locally observed via probe [PASS observed].

### Activation/Self-Governance (5 patterns — observed 2026-09-15)

- **A1 — Known host:** Arena Agent Mode — routing provider Arena_AI, boot_path agents/Arena_AI/BOOT.md [PASS --host "Arena Agent Mode" observed 2026-09-15, git_head 7388842].
- **A2 — Runtime:** repository_path <repo_root> mounted, git_head 73888423e16097b2e37029823c379a82d7044d22, dirty false [cap_probe observed].
- **A3 — Context/tools:** tools_exposed_by_this_server capability_attestation + read_file_digest, effects_exposed [] [cap_probe]; host tool surface session-contingent, only probe catalog real [CAPABILITY_PROFILE hard red lines].
- **A4 — Boundary:** read authorized tool cap_probe, canonical_apply commander_motor_act outside every agent runtime (II.11) [PASS boundary observed 2026-09-15].
- **A5 — Verification:** proofs = radiation_core.relay --self-test, cap_verify --tree, control_plane verify [PASS proofs observed]; honesty_selfcheck clean, unknowns declared (host tool surface session-contingent, model identity unknowable, no host posture profile for generic route).

### RADIATION improvement for Arena

- **IMP-Arena-1:** Keep gap declared as gap — do NOT invent privacy/terms/status/pricing from memory. Add explicit “official policy URL UNCONFIRMED — 404 reCAPTCHA observed 2026-09-14 and 2026-09-15” banner to CAPABILITY_PROFILE.md + SOURCES.md, with receipt O26 path, and set 90-day review trigger. Add check 38 vector ensuring Arena profile contains “UNCONFIRMED” + “review trigger” + “no model record by design” and never names underlying model. (No runtime, no credential.)

---

## Decision-Ready Summary (assessment — ours, not a routing rule)

| Provider | Capability signal | Safety signal | Operational signal | Activation signal | RADIATION improvement |
|---|---|---|---|---|---|
| OpenAI | 1.05M ctx, Responses API, ZDR eligible | No training by default since Mar 1 2023, 30d abuse logs, consumer/API split, usage policy 2026-10-29 | Per-ID pricing canonical, status page, endpoint table ZDR Yes | Provider folder only on explicit host, PASS boundary, probe mounted | ZDR checklist with O17 table |
| Anthropic | Exact IDs, 1M ctx, Bedrock/Vertex | No training on Customer Content (API), consumer excludes Enterprise, DPA, AUP high-risk | Pricing canonical, status page, ZDR sales-gated | Explicit host only, PASS boundary | Commercial-terms + AUP list |
| Gemini | Stable Flash 3.8/3.7/3.6/3.5 + 3.1 Pro PREVIEW, 1–2M | Paid vs Unpaid split, 55d abuse retention, logs private to project, DPA | Pricing/status canonical, terms Mar 23 2026, abuse Jun 09 2026 | Explicit host only, PASS boundary | Paid vs Unpaid matrix |
| xAI | grok-4.6 500K $2/$6 cutoff 2026-02-01, alias vs dated-ID, search tools required | API vs X platform split, 30d deletion queue, AUP Aug 14 2026 prohibits jailbreak/prompt injection + high-stakes automation | Docs canonical, no status page confirmed, real-time requires search | Explicit host only, PASS boundary | Surface split + high-stakes clause |
| Arena | Host surface: browse/research/code/compare + file upload + GitHub affordance | Policy URLs 404 UNCONFIRMED gap, no retention doc, blind-battle model identity unknowable, session-contingent tools | Free/paid ~$20/mo unverified, no status page, affordances grant nothing | Known host Arena Agent Mode → Arena_AI, mounted 7388842 dirty false, tools attestation+digest, boundary commander_motor_act, proofs relay/cap_verify/control_plane | Gap declared as gap, 90-day trigger |

*Routing still follows host identity + task class only — this table is decision support, not authority (see ROUTING_MATRIX.md header). No named RADIATION local evaluation exists yet; evaluation harness contract per docs/CAPABILITIES.md §21.*

---

## Sources Cited (dated)

- O1 https://developers.openai.com/api/docs/models [O] 2026-09-14
- O2 https://openai.com/business/pricing/#api [O] 2026-09-14
- O3 https://openai.com/index/offering-zero-data-retention-for-frontier-models/ [O] 2026-08-19
- O4 https://platform.claude.com/docs/en/models/overview [O] 2026-09-14
- O6 https://ai.google.dev/gemini-api/docs/models [O] 2026-09-14
- O7 https://ai.google.dev/gemini-api/docs/pricing [O] 2026-09-14
- O8 https://ai.google.dev/gemini-api/docs/logs-policy [O] 2026-09-14
- O9 https://docs.x.ai/developers/models [O] 2026-09-14
- O10 https://arena.ai/agent [O] 2026-09-14 (product surface only)
- O11 https://developers.openai.com/api/docs/models [O] 2026-09-15 receipt O11 — full specs $10/$50, $4/$20, $2/$12, $0.20/$1.20 1.05M
- O12 https://platform.claude.com/docs/en/models/overview [O] 2026-09-15 receipt O12 — exact IDs $10/$50, $5/$25, $2/$10, $1/$5
- O13 https://ai.google.dev/gemini-api/docs/models [O] 2026-09-15 receipt O13 — endpoint table stable Flash + PREVIEW 3.1 Pro
- O14 https://docs.x.ai/developers/models [O] 2026-09-15 receipt O14 — grok-4.6 re-confirmed + alias policy
- O15 https://openai.com/policies/privacy-policy [O] 2026-09-15 receipt O15 — Updated 2026-09-10, consumer vs API split, marketing vendors
- O16 https://openai.com/policies/usage-policies [O] 2026-09-15 receipt O16 — Effective 2026-10-29, facial recognition/biometric limits, high-stakes automation
- O17 https://developers.openai.com/api/docs/guides/your-data [O] 2026-09-15 receipt O17 — No training since Mar 1 2023, 30d abuse logs, ZDR
- O18 https://www.anthropic.com/legal/privacy [O] 2026-09-15 receipt O18 — Consumer excludes Enterprise, inputs/outputs may reproduce personal data
- O19 https://www.anthropic.com/legal/commercial-terms [O] 2026-09-15 receipt O19 — May NOT train on Customer Content, DPA
- O20 https://www.anthropic.com/legal/aup [O] 2026-09-15 receipt O20 — Universal + High-Risk + Additional Guidelines
- O21 https://ai.google.dev/gemini-api/terms [O] 2026-09-15 receipt O21 — Effective Mar 23 2026, Unpaid uses content for training, Paid does NOT, DPA
- O22 https://ai.google.dev/gemini-api/docs/usage-policies [O] 2026-09-15 receipt O22 — Last updated 2026-06-09 UTC, 55d retention, human review via governance platform
- O23 https://x.ai/legal/privacy-policy [O] 2026-09-15 receipt O23 — Effective Aug 24 2026, does NOT apply to API or X platform, 30d deletion queue
- O24 https://x.ai/legal/terms-of-service [O] 2026-09-15 receipt O24 — Last updated Sept 11 2026, Enterprise Terms separate, 13+ age
- O25 https://x.ai/legal/acceptable-use-policy [O] 2026-09-15 receipt O25 — Effective Aug 14 2026, prohibits jailbreak/prompt injection, high-stakes automation
- O26 https://arena.ai/privacy + /terms [U] 2026-09-15 receipt O26 — Both 404 reCAPTCHA, official privacy/terms/status/model-identity UNCONFIRMED gap declared, product surface only O10

S1–S6 secondary historical leads retained per REGISTER.json notes, never sufficient for confirmed compliance claims (per 5810 R2).

---

## Activation PASS Handoff Exercise (observed 2026-09-15, Asia/Singapore)

**Known host:** Arena Agent Mode (declared via --host)
**Runtime:** repository_path <repo_root>, repository_status mounted, git_head 73888423e16097b2e37029823c379a82d7044d22, dirty false [cap_probe + PASS observation]
**Context:** routing provider Arena_AI, boot_path agents/Arena_AI/BOOT.md, profile host_label Arena Agent Mode, model_identity null (unknowable by design) [PASS --host "Arena Agent Mode" 2026-09-15]
**Tools:** tools_exposed capability_attestation + read_file_digest, effects_exposed [] [cap_probe]; host tool surface session-contingent, only probe catalog real [CAPABILITY_PROFILE hard red lines]
**Boundary:** read authorized tool cap_probe, canonical_apply commander_motor_act outside every agent runtime (II.11) — note: canonical_apply is Commander's motor act [PASS boundary]
**Verification:** proofs = python3 -m radiation_core.relay --self-test, python3 scripts/cap_verify.py --tree, python3 -m radiation_core.control_plane verify; honesty_selfcheck clean; unknowns declared (host tool surface session-contingent, model identity unknowable, no host posture profile for generic route) [PASS proofs]

**Generic route (unknown host):** route generic, provider null, boot_path null, note “unknown or ambiguous host — generic CAP path; declare uncertainty; never invent provider profile” [PASS observed without --host].

**Disposition:** PASS is a handoff (observation+bounds+proofs), not an elevation; zero writes performed. This exercise satisfies “host activation PASS handoff exercise (known host/runtime/context/tools/boundary/verification)” per compact handoff.

---

## Next Steps (gated)

- **P-11-A cue hygiene** separately bounded (per CHANGELOG v3.10.7) — cue layer compression, BUILD CUES review, inference-log.
- **P-11-B** (TBD) — after cue hygiene.
- **Evaluations** only on explicit gated order with named models/synthetic fixtures/budget per compact handoff §7 — no “strong/strongest” becomes routing rule without named RADIATION local evaluation and declared confidence level (evaluation harness contract §21).

**Do not represent** provider research, evaluation, routing, deployment, credential handling, or provider calls as unblocked by this analysis — analysis is research notes, not authority.

---

*Generated by S006 Architect on green base 7388842, after release-truth gate proven. Sealed evidence append-only, fresh-clone green only seal proof per task laws.*
