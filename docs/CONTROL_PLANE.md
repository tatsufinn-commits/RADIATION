# THE CONTROL PLANE — II.11 (ratified 5000 · threat-boundary amended 5100)

**Ratification:** the Commander selected **"Product-2 package"** when asked which 5000
this should be (2026-09-14) — recorded as receipt chain entry 0.
**5100 amendment:** the research team's excellence review demonstrated a draft-root
escape and a caller-forged source label in the 5000 code. Both fail closed now, and
**every security-flavored claim in this document was rewritten to match the mechanism**.
`docs/THREAT_MODEL.md` is the authority on limits; where this file and that file
disagree, that file wins.

## The one-paragraph truth
The control plane is **operated, cooperative tooling**: a session that routes work
through it gets policy-enforced refusals and bounds; nothing schedules itself; and
`canonical_apply` — like push — remains the Commander's motor act, with no tool bound
at any source level. Its source labels are **assertions, not credentials**; it is not
a sandbox; its receipts are tamper-**evident**, not immutable. It bounds what flows
through it. Nothing more has ever been true.

## Components (`radiation_core/control_plane.py`, stdlib, one module)
| Component | What it does | Hard property (CI-tested) |
|---|---|---|
| **Typed resolver** `resolve()` | pure decision: effect × source-assertion → `authorized` / `refused` / `commander_motor_act` | two-key: policy key (source rank vs executed allowlist) AND tool key; strict task grammar for draft tasks |
| **Capability allowlist** | policy as data, schema-executed; `canonical.tool` is `const null` | tampering with the allowlist is a finding, not a posture change |
| **Approval boundary** | `canonical_apply` → `commander_motor_act`, no tool, ANY source level | structural, not prose |
| **Draft executor** `execute_draft()` | strict task grammar + pinned drafts base + component-wise containment (symlinks, dot-parts, absolute/backslash forms all refused); atomic same-dir writes; ≤20 files, ≤64 KiB/file, ≤256 KiB, extension allowlist; manifest schema EXECUTED | refuses without a chained authorized decision AND an unconsumed content-bound approval — manifest substitution and replay fail closed |
| **Receipts** | append-only, fsynced, hash-LINKED; v2 receipts get semantic verification (orphan executions, approval reuse, task mismatch → findings) | tamper-EVIDENT against unrecomputed edits — not immutable (THREAT_MODEL) |

## CLI
```bash
python3 -m radiation_core.control_plane resolve --effect read --source session_initiative
python3 -m radiation_core.control_plane decide  --task TID-… --effect workspace_draft --source commander_order
python3 -m radiation_core.control_plane approve --task TID-… --manifest M.json   # content-bound, single-use
python3 -m radiation_core.control_plane execute --task TID-… --manifest M.json
python3 -m radiation_core.control_plane verify                                   # structural + semantic
python3 -m radiation_core.control_plane --self-test                              # 38 vectors, check 37
```
No production path overrides (`--receipts` / `--drafts-root` were removed in 5100 —
the review's finding: they let a caller re-point the boundary; dependency injection
survives only inside the self-test).

## What would upgrade the honest ceiling (Commander's options, not sessions')
1. **Signing key in Commander custody** (outside the writable workspace) → approvals
   become credentials; `immutable` becomes claimable with signatures.
2. **Executor sandbox** (mount exposes only the approved draft root) → the ambient-shell
   bypass class closes.
3. **External chain anchoring** (signed tag / transparency head) → recompute attacks
   become detectable.
Until then, the accurate name for this module is the research team's: a **cooperative
audit-and-bounding protocol with in-program enforcement** — and it is a good one.

## Provenance
Staged since 4400 · external PoC (6/6 · 5/5) → 4800 verification → 4900 observation →
5000 landed by explicit ratification → **5100: boundary made true by the review that
broke it** (their two repros are now permanent fail-closed regression vectors).
