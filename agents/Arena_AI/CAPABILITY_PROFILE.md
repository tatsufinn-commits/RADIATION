# CAPABILITY PROFILE — Arena AI / Arena Agent Mode (HOST profile)

`reviewed_on: 2026-09-15` · `consolidated: 5600 (2026-09-14) → 5830 (2026-09-15)` · Review trigger: any Arena product/policy change, or 90 days (re-review by 2026-12-13) · Maintainer: S006 (Architect) — 5820 compliance refresh gap re-confirmed + 5830 PASS activation observed

**What this profile is:** research notes about a SESSION-CONTINGENT HOST, written for routing decisions inside this repository. It is not a claim about any model, and it confers no access.

## Hard red lines (this section outranks everything below)
- **Model identity is treated as UNKNOWABLE from inside a session.** Arena's own product design centers on blind, side-by-side comparison — outputs are presented *without* revealing the underlying model [Secondary, stork.ai 2026-06-05]. This profile therefore NEVER names an underlying model, and no "powered by X" claim may be inserted here without a dated official source.
- **Tool surface is session-contingent.** What one session observes (probe catalog) is evidence about THAT session only. Never generalize it to the platform.
- **No claims about private file access, network reach, billing, or retention beyond what a dated source in `SOURCES.md` states.**
- **No conflation with unrelated products** that share the name "arena" (battle/arena games, LMS tools, other comparison sites) — connection claims require dated evidence.

## Capabilities (as attributable to the HOST, not to any model)
- **Agent workflow surface:** browsing/research, code execution, deep research, model comparison are listed by the product's own page [Official, arena.ai/agent, retrieved 2026-09-14 O10]; the same retrieval observed **file upload** and a **"Connect your GitHub"** affordance — product affordances grant nothing; tool/file/network/push authority stays session-specific and must be locally observed (probe). Third-party coverage describes web search, image generation, file attachments, and a sandbox/bash environment [Secondary, chatgate.ai 2026-06-05; stork.ai 2026-06-05].
- **Execution environment:** folder-based workspace with file handling and bash execution [Secondary, chatgate.ai 2026-06-05] — consistent with what an in-session probe may catalog; verify per session via `scripts/cap_probe.py`.
- **Modality coverage:** text, code, image, video, vision, document, search evaluation [Secondary, stork.ai 2026-06-05 — benchmark-platform claim, not a per-session capability promise].
- **Long context / rates / latency:** NOT stated — session-contingent and model-dependent; no claim made. **[Unverified — review trigger]**

## Access, pricing, availability
- Free tier + paid tier reported at ~$20/mo [User-reported/Secondary, stork.ai 2026-06-05] — **never treated as fact until confirmed on an official Arena pricing page**. **[Unverified — review trigger]**
- Reliability signals: no official status page identified in this sweep. **[Unverified — review trigger]**

## Safety, policy, privacy (gap re-confirmed 2026-09-15)
- **Policy URLs UNCONFIRMED — 404 reCAPTCHA observed 2026-09-14 and 2026-09-15:** guessed `/privacy` and `/terms` paths returned **404 / reCAPTCHA** in the 2026-09-14 gate-review retrieval and 2026-09-15 O26 retrieval. Catalog value: **unverified — official policy URL and applicable surface NOT confirmed**; a standing review trigger, not evidence that no policy exists. No Arena-specific privacy/retention document was found in this sweep. **Do not paste what you cannot lose; treat session content per the platform's terms when published.** **[Unverified — review trigger: official privacy/terms link needed — O26 2026-09-15 receipt O26, both https://arena.ai/privacy + /terms 404 reCAPTCHA, tier U so it cannot satisfy official confirming/policy evidence, product surface only from O10 https://arena.ai/agent].**

## Activation PASS observed 2026-09-15 (Asia/Singapore)

- **Known host:** Arena Agent Mode — routing provider Arena_AI, boot_path agents/Arena_AI/BOOT.md [PASS --host "Arena Agent Mode" observed 2026-09-15, git_head 73888423e16097b2e37029823c379a82d7044d22].
- **Runtime:** repository_path <repo_root> mounted, git_head 7388842, dirty false [cap_probe + PASS observation].
- **Context/tools:** tools_exposed capability_attestation + read_file_digest, effects_exposed [] [cap_probe]; host tool surface session-contingent, only probe catalog real.
- **Boundary:** read authorized tool cap_probe, canonical_apply commander_motor_act outside every agent runtime (II.11) [PASS boundary observed].
- **Verification:** proofs = radiation_core.relay --self-test, cap_verify --tree, control_plane verify; honesty_selfcheck clean; unknowns declared (host tool surface session-contingent, model identity unknowable, no host posture profile for generic route) [PASS proofs observed 2026-09-15].
- **Generic route (unknown host):** route generic, provider null, boot_path null, note “unknown or ambiguous host — generic CAP path; declare uncertainty; never invent provider profile” [PASS observed without --host].

**Disposition:** PASS is a handoff (observation+bounds+proofs), not an elevation; zero writes performed. This satisfies host activation PASS handoff exercise (known host/runtime/context/tools/boundary/verification) per compact handoff.

## RADIATION task suitability [Assessment — ours, based on the observed session + sources above]
| Task class | Suitability | Note |
|---|---|---|
| Research | strong | web search + deep-research surface confirmed by sources |
| Corpus navigation | strong | file workspace + this repo's derivative layer |
| Scaffolding | strong | bash + file writes in sandbox |
| Governance/cue work | strong | the repo's control plane runs inside the sandbox |
| Implementation/review | strong | coding reported as the platform's dominant task class |
| Documentation | strong | file workspace + rendering |
| Creative | adequate | image generation reported; per-session tool check required |

*Values are unmeasured impressions — no named RADIATION local evaluation exists yet; this table is never a routing decision rule (see `agents/ROUTING_MATRIX.md` header).*

**Routing:** load `agents/Arena_AI/` ONLY when the host is explicitly known/observed as Arena Agent Mode; verify the tool surface with the probe before promising anything; record unknowns in the pass output.
