# 🔬 ACTIVATION CONFORMANCE (`docs/ACTIVATION_CONFORMANCE.md`)
## MAS-SCAN-NOTES revision 1 — contract, custody, limitations, non-authority
**Version:** v3.11.0 candidate · **Basis:** FIX TEAM 006 execution order 2026-09-29 · DESK RULING D144 (Option A) + the Desk's sidecar authorization · sixteen-path charter (6 A / 10 M)
**Evaluator:** `scripts/activation_conformance.py` · **Rule + custody:** `scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json` · **Schema:** `schemas/activation_conformance.schema.json` · **Tests:** `tests/test_activation_conformance.py` · **Sidecar contract:** `scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json.contract.json`

---

## 1. THE RULE — exactly one, revision 1

**MAS-SCAN-NOTES v1** states one requirement and nothing else:

> A supplied, task-bound **Scan Declaration** conforms only when its
> **Extraction Notes** field is *structurally nonempty* under the one canonical
> **custody object** recorded at a **fixed snapshot**.

The requirement itself is old law: the Scan Declaration's Extraction Notes field is
REQUIRED by `docs/AI_RULES.md` III.6, and a Declaration without it is INVALID — the
surgeon blocks work. That law lives in prose and in the template
`scaffolding/core/proc_scan-declaration.md`. This tranche adds **no new doctrine**: it
adds one small read-only evaluator that answers a structural question about an
artifact that already had to exist.

**Structural nonempty** is deliberately narrow: a string that is not blank and is not
one of the placeholder tokens (`none`, `n/a`, `na`, `tbd`, `-`, `—`). The evaluator
does not read meaning, quality, truth, sourcing, or completeness — it reads presence.

## 2. THE TRUTH BOUNDARY — the only six result values

| Result | Means exactly |
|---|---|
| `SATISFIED` | The fixed snapshot's structural evidence contract is met at its recorded cutoff. |
| `MISSING` | The submitted Declaration has no structurally nonempty Extraction Notes field. |
| `NOT APPLICABLE` | The rule's own applicability predicate recorded in the custody context is false. |
| `UNKNOWN` | Any custody, currentness, digest, schema, or submission fact that cannot be checked — or any live disposition. |
| `CONFLICT` | Two present facts disagree (e.g. submission revision vs custody revision). |
| `COMMANDER DISPOSITION` | Reserved vocabulary for a disposition record. **Never emitted live** — see §5. |

**`SATISFIED` explicitly means only this:** the fixed snapshot's structural evidence
contract is met at its recorded cutoff. It **never** means Scan completion, current
session truth, caller authentication, fresh observation, first use, replay prevention,
capability availability, or authority.

**The UNKNOWN default is absolute.** Any unavailable, stale, mismatched,
non-canonical, invalidated, superseded, or uncheckable custody/currentness fact
returns `UNKNOWN` — never `SATISFIED`. The evaluator has no path that turns an
unchecked fact into a satisfied one.

## 3. SOLE CUSTODY — one path, not configurable

The evaluator selects **only** the repository-relative path
`scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json`. No command option, task field,
environment value, history input, or purported disposition can substitute another
path: the path is a module constant, the CLI exposes no flag that reaches it, and
`--custody <anything>` is a usage error.

The custody object is **closed** and binds: identity · sole rule and revision ·
approval provenance · finite task/revision/session/declaration context ·
cutoff and use status · validity and supersession state · rule and contract digests.

**Digests prove bytes only.** They prove that the two normative artifacts referenced
by the snapshot — the declaration template and this contract document — are the same
bytes the snapshot recorded. **Neither labels, hashes, fixtures, nor local files prove
a Commander identity or grant permission.** The identity block is a *label
assertion* and carries `identity_proven: false` as a constant; a custody object that
claims a proven identity is treated as non-canonical and returns `UNKNOWN`.

## 4. THE RECEIPT — returned in memory, never persisted

Every evaluation returns a receipt object with the result, its reasons, the custody
path, the cutoff date, and the fixed limits list. Two fields are constants:
`persisted: false` and `authority: "none"`.

**No receipt is written to disk.** `mutation_scope` for this tool is `none` in
`tools/TOOL_REGISTRY.json`, and the evaluator imports no writer, no network client,
and no subprocess module. The absence of a stored receipt is deliberate: an
in-memory receipt cannot become a cross-invocation token.

## 5. WHAT THIS IS NOT — the limitation disclosure

The evaluator is **not an activation engine**. It does not, and cannot, do any of:

- **prove real-world work** — it inspects a text field, never a performance;
- **authenticate a caller** — it has no credential path, and the custody identity
  block is an unproven label;
- **identify a host or model** — it reads no host, no provider, no model surface;
- **invoke a tool** — it executes nothing and imports no executor;
- **grant a capability or permission** — an entry grants nothing; a result grants
  nothing;
- **use a network or credential** — offline by construction, credential handling
  `prohibited` in the registry;
- **persist a receipt** — receipts are returned in memory only;
- **provide cross-invocation replay protection** — a self-declared submission history
  is *structural*, not proof of a fresh or first use; evaluating the same submission
  twice is expected and yields the same structural result;
- **activate any child package** — no child package, no γ, no B4.2 behavior is
  touched or extended by this tranche.

**No live dynamic disposition path exists.** A task-supplied disposition is
`UNKNOWN`, always. The `COMMANDER DISPOSITION` value is a *declared vocabulary
member and schema shape only*: fixtures may exercise the record shape, and the
evaluator asserts in its own self-test that no live authenticated-disposition path
can be reached. An unauthenticated disposition record cannot become a result.

## 6. HOW TO RUN IT

```text
python3 scripts/activation_conformance.py --submission <submission.json>   # live evaluation
python3 scripts/activation_conformance.py --submission <file> --json       # receipt as JSON
python3 scripts/activation_conformance.py --self-test                      # bounded self-test
```

Exit codes: `0` = `SATISFIED` · `1` = evaluated but not satisfied (one of the other
five values, always printed) · `2` = usage error. The submission is the artifact
under inspection — the path to it is the *only* input the CLI accepts; the custody
object is selected by constant alone.

## 7. NON-AUTHORITY

This document, the rule, the schema, the tests, and the evaluator together describe
**a probe**. They do not create activation, they do not authenticate anyone, and
they do not confer permission. Authority in this repository flows only through the
Commander and the II.11 control plane — never through a checker's exit code, and
never through a green result. See `docs/CONTROL_PLANE.md` and
`docs/THREAT_MODEL.md` for the standing limits.
