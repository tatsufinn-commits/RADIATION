# ROUTING MATRIX — RADIATION task classes × providers (5400)

**These values are UNMEASURED IMPRESSIONS (secondary-source impressions and session anecdotes). They are NOT a decision rule: routing on any "strong/strongest" cell requires a named RADIATION local evaluation with a declared confidence level (evaluation harness contract: see docs/CAPABILITIES.md §21). Until such an evaluation exists, routing follows host identity + task class only — never these words.**

`reviewed_on: 2026-09-14` · Companion to `agents/AGENT_INDEX.md` (the routing RULE lives there and in the pass; this matrix is decision support, not authority).

**Hard rules (unchanged by this matrix):**
1. Route by **observed/explicitly-known host only** — never infer a provider from output style, capability hints, or self-identification. Unknown/ambiguous → generic CAP path, uncertainty declared.
2. The pass (`agents/_common/radiation_pass.py`) is the only routing mechanism; cross-root invocation is refused (5300 E5).
3. Host ≠ model. Arena Agent Mode's model identity is unknowable from inside a session (blind-battle product design); no matrix cell may name an underlying model.

| Task class | ChatGPT | Claude | Gemini | Grok | Arena_AI (host) |
|---|---|---|---|---|---|
| Research | strong | strong | strong | adequate | strong (probe tools first) |
| Corpus navigation | strong | strong | strong (1–2M ctx) | strong | strong |
| Scaffolding | strong | strong | strong | strong | strong |
| Governance/cue work | adequate | **strong** | adequate | adequate | strong (this repo's home surface) |
| Implementation/review | strong | strong | strong | strong | strong |
| Documentation | strong | strong | strong | strong | strong |
| Creative | strong | strong | strong | adequate | adequate |
| Cost-sensitive volume | mini/nano tiers | Haiku tier | Flash-Lite tier | Fast tiers (cheapest) | session-contingent |
| Privacy-sensitive (repo work) | API posture [O/S] | API posture (no-training) [O/S] | paid-API posture [O] | API posture (no-training) [S] | **unverified — review trigger** |

Notes column discipline: every cell above is an [Assessment — ours] distilled from the dated profiles; volatile specifics (prices, context sizes) live in the profiles' SOURCES, not here. **Expiry: 2026-12-13** (90-day review trigger) or upon any cited official page change.
