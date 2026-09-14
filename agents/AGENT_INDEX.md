# AGENT INDEX — the exact routing decision (5200)

**Rule.** A runtime reads its matching provider folder **only when its host is
explicitly known/observed**. Unknown or ambiguous identity takes the generic CAP path
and declares uncertainty. An invented provider profile is a violation of the honesty
clause.

| Observed host label | Load | Posture |
|---|---|---|
| `Arena Agent Mode` (or explicit Arena Agent Mode session) | `agents/Arena_AI/BOOT.md` | primary testbed; read/plan/evidence default |
| explicitly-declared ChatGPT host session | `agents/ChatGPT/BOOT.md` | generic read-default; session-contingent only |
| explicitly-declared Gemini host session | `agents/Gemini/BOOT.md` | generic read-default; session-contingent only |
| explicitly-declared Grok host session | `agents/Grok/BOOT.md` | generic read-default; session-contingent only |
| explicitly-declared Claude host session | `agents/Claude/BOOT.md` | generic read-default; session-contingent only |
| anything else — unknown, ambiguous, or undeclared | **no provider folder** | generic CAP path; run the pass; declare uncertainty |

**The pass (all routes):** `RADIATION PASS` → `python3 agents/_common/radiation_pass.py
--host "<label>"`. Deterministic, read-only; yields observed context/tools, the
effect boundary, the relevant profile (or its explicit absence), verification
commands, and non-availability results.

**Invariants (tested, check 38):** unknown-host fallback is safe and neutral · no
folder or pass output claims identity, tools, or canonical powers · the pass never
writes · Arena's declared posture is read-only.

**Limitation:** this index binds *sessions that choose to read it*. It cannot make a
hosted product auto-discover anything — convention, not proof.

RESEARCH LAYER (5400, non-boot): per-provider `CAPABILITY_PROFILE.md` + `SOURCES.md` (dated, tier-labeled), plus `agents/ROUTING_MATRIX.md` and `agents/RESEARCH_METHOD.md`. Notes for routing decisions — not authority, not boot context. Reviewed 2026-09-14; expiry 2026-12-13.
