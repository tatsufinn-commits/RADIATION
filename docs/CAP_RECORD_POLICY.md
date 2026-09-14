# CAP RECORD POLICY — content rules for capability records (C-4, 4900)

**Law text for what a `radiation.cap/0.1` record may contain.** The mechanical
classes below are EXECUTED by `scripts/cap_verify.py` (redaction scan; every
string value in a record is scanned) and exercised in its self-test — check 35
in CI. This document states the policy; the tool enforces it; the schema
executes structure. Prose never enforces alone.

## Allowed content
- repository paths (repo-relative), git heads (40-hex), dirty bits
- sha256 digests (sealed evidence), byte counts
- tool names from a server's own catalog, verifier names from the registry
- exit codes, timestamps, blocker vocabulary, state-machine event names
- quotes of COMMANDER ORDERS (the input.received chain) — those are already record

## Forbidden content (executed classes)
| Class | Pattern family | Finding |
|---|---|---|
| GitHub tokens | `ghp_…`, `github_pat_…` | redaction violation (C-4) |
| Cloud keys | `AKIA…` (AWS access key id) | redaction violation (C-4) |
| Private keys | `-----BEGIN … PRIVATE KEY-----` | redaction violation (C-4) |
| Bearer/URL tokens | `Bearer <token>`, `x-access-token:` | redaction violation (C-4) |
| Embedded passwords | `password=…` / `password: …` | redaction violation (C-4) |

## Forbidden by schema or identity law (already executed since 4800)
- `declared.model_identity` must be `null` — the model behind a host label is
  unknowable; no pattern in any record may assert otherwise.
- verifier names outside RADIATION's own CLI registry are invalid references.
- a record may not claim `verified` without observation, green checks, and a
  binding seal digest.

## Forbidden by policy (prose law — judgment classes, not mechanically detectable)
- **Prompt bodies / conversation transcripts.** Records carry *what was
  ordered* (the order chain) and *what was observed* — never raw session text.
- **Model speculation.** No field may guess which model ran, why a host
  behaved a way, or rank providers. Calibration data belongs to the Phase-A
  harness, not to evidence records.
- **Personal data** beyond the Commander's title and session IDs already in
  the ledger system.

## Retention & placement
- CAP records live inside canonical task bundles (`evidence/tasks/<TID>/artifacts/`)
  and inherit bundle immutability: file==render, digests in outcomes, seal on
  the record itself. They are never written outside bundles.
- A record's seal breaks on any hand-edit (4700 law applied to records):
  re-render/re-probe, never hand-edit.

## Boundary
`cap_verify` VERIFIES records and `cap_probe` OBSERVES surfaces. Since the
Commander's Product-2 ratification (5000, II.11), effect authority flows ONLY
through `radiation_core.control_plane` — the two-key resolver, the drafts-root-
bounded executor, and the hash-chained receipts. `canonical_apply` remains the
Commander's motor act, outside every runtime path.
