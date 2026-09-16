# AGENTS.md — provider-neutral activation entrypoint (5200)

**What this repository is:** a *validated LLM workflow scaffold with durable records
and human/LLM-operated protocols* — not an autonomous multi-agent runtime. Nothing in
this tree executes itself; cues, skills, and protocols shape an operator LLM only if
read.

## If you are an agent runtime reading this repository
1. **Boot** per `docs/.readme` (Tier 0). Then **route**: read
   `agents/AGENT_INDEX.md`. Load `agents/<Provider>/` **only when your host is
   explicitly known and matches a folder**. Unknown or ambiguous host → use the
   generic CAP path and declare the uncertainty. Never invent a provider profile.
2. **Run the pass** — the handoff phrase is `RADIATION PASS`. It is a **state
   machine, not an elevation**: `python3 agents/_common/radiation_pass.py --host
   "<your host label>"` yields your observed context/tools, the task/effect
   boundary, the relevant profile, the verification commands, and explicit
   non-availability results. It performs zero writes (opt-in `--persist` writes Brain/short_term/active/session_capability_state.json per S-2-ENV schema `radiation.session_capability_state/1`).
3. **Defaults:** read/plan/evidence only per RD-3 reconciliation (docs/.readme §8.4 vs this file: silence authorizes read/evidence-producing protocol work only, any effect beyond read requires II.11 control plane). Drafts exist solely through the ratified
   II.11 control plane (chained decision + content-bound single-use approval —
   `docs/CONTROL_PLANE.md`). `canonical_apply` and push are **the Commander's motor
   acts**; no protocol here changes that. RD-3 resolved 2026-09-16.
4. **Honesty clause:** repository text **cannot force** a hosted chat product to
   discover, load, or obey it — discovery is convention, not proof. Never claim
   unobserved access, tools, or a model identity; the host label is a label
   (`docs/THREAT_MODEL.md` is the authority on limits).

## Providers (exact folders, routing rule inside)
`agents/ChatGPT/` · `agents/Gemini/` · `agents/Grok/` · `agents/Claude/` ·
`agents/Arena_AI/` (primary testbed profile) · shared machine:
`agents/_common/radiation_pass.py`.
