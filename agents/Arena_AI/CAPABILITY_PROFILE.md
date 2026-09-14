# CAPABILITY PROFILE — Arena AI / Arena Agent Mode (HOST profile)

`reviewed_on: 2026-09-14` · Review trigger: any Arena product/policy change, or 90 days (re-review by 2026-12-13) · Maintainer: S005 (Architect)

**What this profile is:** research notes about a SESSION-CONTINGENT HOST, written for routing decisions inside this repository. It is not a claim about any model, and it confers no access.

## Hard red lines (this section outranks everything below)
- **Model identity is treated as UNKNOWABLE from inside a session.** Arena's own product design centers on blind, side-by-side comparison — outputs are presented *without* revealing the underlying model [Secondary, stork.ai 2026-06-05]. This profile therefore NEVER names an underlying model, and no "powered by X" claim may be inserted here without a dated official source.
- **Tool surface is session-contingent.** What one session observes (probe catalog) is evidence about THAT session only. Never generalize it to the platform.
- **No claims about private file access, network reach, billing, or retention beyond what a dated source in `SOURCES.md` states.**
- **No conflation with unrelated products** that share the name "arena" (battle/arena games, LMS tools, other comparison sites) — connection claims require dated evidence.

## Capabilities (as attributable to the HOST, not to any model)
- **Agent workflow surface:** browsing/research, code execution, deep research, model comparison are listed by the product's own page [Official, arena.ai/agent, retrieved 2026-09-14]. Third-party coverage describes web search, image generation, file attachments, and a sandbox/bash environment [Secondary, chatgate.ai 2026-06-05; stork.ai 2026-06-05].
- **Execution environment:** folder-based workspace with file handling and bash execution [Secondary, chatgate.ai 2026-06-05] — consistent with what an in-session probe may catalog; verify per session via `scripts/cap_probe.py`.
- **Modality coverage:** text, code, image, video, vision, document, search evaluation [Secondary, stork.ai 2026-06-05 — benchmark-platform claim, not a per-session capability promise].
- **Long context / rates / latency:** NOT stated — session-contingent and model-dependent; no claim made. **[Unverified — review trigger]**

## Access, pricing, availability
- Free tier + paid tier reported at ~$20/mo [User-reported/Secondary, stork.ai 2026-06-05] — **never treated as fact until confirmed on an official Arena pricing page**. **[Unverified — review trigger]**
- Reliability signals: no official status page identified in this sweep. **[Unverified — review trigger]**

## Safety, policy, privacy
- No Arena-specific privacy/retention document was found in this sweep. **Do not paste what you cannot lose; treat session content per the platform's terms when published.** **[Unverified — review trigger: official privacy/terms link needed]**

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

**Routing:** load `agents/Arena_AI/` ONLY when the host is explicitly known/observed as Arena Agent Mode; verify the tool surface with the probe before promising anything; record unknowns in the pass output.

---

## Gate-review corrections (5500, 2026-09-14)
- Product page affordances observed in the gate-review retrieval [O, arena.ai/agent]: Agent Mode, **file upload**, and a **"Connect your GitHub"** affordance. Tool/file/network/push authority remains **session-specific and must be locally observed** (probe) — a product marketing affordance grants nothing.
- **Policy URLs:** guessed `/privacy` and `/terms` paths returned **404 / reCAPTCHA** in that retrieval. Catalog value: **unverified — official policy URL and applicable surface NOT confirmed**; this is a standing review trigger, not evidence that no policy exists.
- The hard red lines above are unchanged and now carry this retrieval evidence.
