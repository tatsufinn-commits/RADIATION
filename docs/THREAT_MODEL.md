# THREAT MODEL — the control plane and CAP layer (5100; supersedes 5000 wording)

**Law of the last resort:** where any document claims more than this file,
this file wins. Written because the v3.3.0 excellence review demonstrated a
draft-root escape and a caller-forged source label in the 5000 code — both
now fail closed (regressions in check 37's self-test) — and because claims
must match mechanisms, always.

## What the control plane IS
A **cooperative, in-program policy flow**: a session that routes work THROUGH
`radiation_core/control_plane.py` gets refused or bounded by these rules:

1. strict task-ID grammar (`TID-YYYY-MM-DD-slug`) + pinned drafts base —
   no `task_id` or manifest path can leave `evidence/drafts/<task_id>/`
   (traversal, absolute, backslash, dot-component, symlink escapes: fail closed);
2. no execution without a chained **authorized decision** receipt;
3. no execution without an **unconsumed content-bound approval** receipt
   (exact manifest digest + bounds + nonce; one approval executes once —
   manifest substitution and replay fail closed);
4. manifest shape is schema-EXECUTED and resource-bounded (≤20 files,
   ≤64 KiB/file, ≤256 KiB aggregate, extension allowlist, UTF-8);
5. canonical_apply answers `commander_motor_act` and binds **no tool** at any
   source level.

## What it is NOT (read before quoting it)
- **Not caller authentication.** A `--source commander_order` label is an
  ASSERTION of provenance, not a credential. Any process that can run the CLI
  can assert any source. The policy flow bounds *routed work*; it does not
  verify *who* is routing it.
- **Not a sandbox.** An agent with ambient shell/filesystem access can write
  anywhere it likes without ever invoking this module. Only a mount/executor
  sandbox that exposes nothing else could enforce that — out of scope here.
- **Not cryptographic immutability.** Receipts are append-only, fsynced, and
  hash-LINKED: any edit that does not recompute the whole chain is detected.
  A writer able to rewrite the file CAN recompute every digest. There is no
  signature, no external anchor, no append-only storage layer. Accurate
  claim: **tamper-evident against unrecomputed edits; tamper-permitting
  against a determined local writer.**
- **Not concurrency-safe beyond O_APPEND.** Single-writer discipline is
  assumed; simultaneous writers could interleave (detectable as a broken
  chain, not prevented).
- **No trusted clock.** Approvals carry a nonce and single-use semantics but
  no expiry; expiry requires a trusted time source RADIATION does not have.

## Key custody (the honest gap)
Approvals bind content and are single-use, but **creating an approval is not
itself authenticated**. A Commander-controlled signing key (GPG/hardware/CI
secret, held OUTSIDE the writable workspace) would upgrade approvals to real
credentials. Until the Commander provisions one, the accurate description of
this module is: **a cooperative audit-and-bounding protocol with in-program
enforcement** — the research team's own proposed downgrade, adopted.

## The ambient-authority truth
The Commander's real boundaries do not live in this file's code alone:
- II.1 (AI does not modify the live repository; patches only) — governs sessions;
- the Commander's sole custody of push — the one boundary that matters finally;
- CI (checks 35–37 + validator) — detects, after the fact, in public.
This module adds *receipted, bounded, replay-proof* handling for the narrow
class of work a session chooses to route through it. That is all it has ever
been able to promise; now the promises say so.
