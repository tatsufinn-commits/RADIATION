# THE CONTROL PLANE — II.11 (ratified 5000, "Product-2 package")

**Ratification:** the Commander selected **"Product-2 package"** when asked which 5000
this should be (2026-09-14) — the explicit F4/Product-2 ratification the 4400+ architecture
reviews required. The genesis receipt of the chain records it:
`evidence/control_plane/receipts.ndjson`, entry 0.

## What this is — and is not (the honest-identity line still governs)
RADIATION remains a *validated LLM workflow scaffold with durable records and
human/LLM-operated protocols*. The control plane is **OPERATED tooling**: a session
invokes it deliberately, per task. It never schedules itself, never watches, never
triggers. There is no daemon, no autonomous loop, no self-granted authority anywhere
in this tree.

## Components (`radiation_core/control_plane.py`, stdlib, one module)
| Component | What it does | Law it executes |
|---|---|---|
| **Typed resolver** `resolve()` | pure decision: effect × source → `authorized` / `refused` / `commander_motor_act` | two-key: policy key (source rank vs allowlist) AND tool key (a least-privilege tool must exist) |
| **Capability allowlist** `scaffolding/control_plane/allowlist.json` | policy as data, schema-executed | `canonical.tool` is `const null` — the approval boundary is structural, not prose |
| **Approval boundary** | `canonical_apply` → `commander_motor_act`, no tool, at ANY source level — even a commander_order cannot make it executable by the runtime | the Commander's motor act stays outside every runtime path |
| **Isolated draft-only executor** `execute_draft()` | writes ONLY under `evidence/drafts/<task_id>/`; no subprocess, no network, no canonical writes; **refuses to run without a chained authorized decision receipt** | no execution without a decision (mechanical) |
| **Immutable receipts** | append-only `receipts.ndjson`, hash-chained (`prev` links, self-binding digests); `verify` recomputes the whole chain | tamper-evident by construction |

## Schemas (EXECUTED, not decorative)
`control_allowlist` (check 37 + tamper vector) · `control_decision` (checked in
`decide()`) · `control_receipt` (checked per entry in `verify()`). All executed by the
one relay schema executor — no second implementation.

## CLI
```bash
python3 -m radiation_core.control_plane resolve --effect read --source session_initiative
python3 -m radiation_core.control_plane decide  --task TID --effect workspace_draft --source commander_order
python3 -m radiation_core.control_plane execute --task TID --manifest M.json
python3 -m radiation_core.control_plane verify
python3 -m radiation_core.control_plane --self-test   # 11 vectors, CI check 37
```

## II.11 (annex text, ratified)
1. The control plane is operated tooling; it executes only what a session explicitly
   requests through it, and never schedules itself.
2. Two keys before any effect: policy allows AND a least-privilege tool exists; and no
   execution without a chained decision receipt.
3. `canonical_apply` (and push) remain the Commander's motor acts — no source level,
   ratification, or receipt can make them runtime-executable.
4. The draft executor is bounded to `evidence/drafts/<task_id>/`; containment is
   enforced against symlink resolution.
5. Every decision and execution is receipted; the chain is immutable and verified in
   CI (check 37).

## Provenance
Staged since 4400 (the reviewers' item 5) · external PoC proved the pattern (CAP 6/6 ·
5/5) · 4800 admitted verification · 4900 admitted observation · 5000 lands enforcement,
bounded exactly as the research memo's Phase C anticipated — by separate,
explicitly-ratified patch.
