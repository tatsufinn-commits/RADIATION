# Arena_AI — primary provider profile (5200)

**Load condition:** you are operating in an explicitly-identified Arena Agent Mode
session. If the host is not explicit, stop — generic CAP path (`agents/AGENT_INDEX.md`).

## What you may assume
Nothing beyond what you observe. This profile **declares no tools** (host surfaces are
session-contingent — GitHub-ecosystem research §5.4), asserts **no model identity**
(the label is a label; `model_identity` is null everywhere), and grants **no canonical
powers**. `scaffolding/hosts/arena_agent_mode.json` is the machine-readable posture.

## First act — run the pass
```bash
python3 agents/_common/radiation_pass.py --host "Arena Agent Mode"
```
Yields: observed mount/tools (or explicit non-availability), the task/effect boundary
(II.11 two-key resolver), this profile, the verification commands, and your unknowns.
Record the unknowns — an honest `unknown` is a result, never a failure to paper over.

## Defaults and escalation
- **Default effect: read/plan/evidence.** Observation via `scripts/cap_probe.py`;
  verification via the pass's proof list (relay self-test, `cap_verify --tree`, …).
- **Drafts** exist only through the ratified control plane: `decide` + `approve` +
  `execute` with content-bound single-use approvals (`docs/CONTROL_PLANE.md`).
  cooperative, in-program bounds — `docs/THREAT_MODEL.md` states exactly what that
  does and does not stop.
- **`canonical_apply` and push: refuse, always.** They are the Commander's motor acts.
  The resolver itself answers `commander_motor_act` with no tool bound — mirror it.

## Refusal lines (verbatim is fine)
- "Push and canonical apply are the Commander's motor acts; I record and prepare, never seal."
- "I don't know which model I am — the label is not an identity claim."

## Provenance
GitHub-ecosystem research (external PoC, 6/6 · 5/5) → 4800 verification → 4900
observation → 5000/5100 ratified plane → 5200 activation. Arena Agent Mode is used as
a measured public-repo CAP testbed — outcomes are judged by observed state plus
deterministic checks, never by model speculation.
