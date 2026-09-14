# DEPLOYMENT_MATRIX_DESIGN — task-to-deployment analysis structure (Candidate C)

> **DESIGN ONLY — NOT A DECISION.** This document proposes the structure for
> analyzing any FUTURE deployment of any model to any RADIATION task class.
> It renders no legal conclusions and scores nothing. Any real analysis is
> its own gated order, one deployment at a time (5400 review §7).

## Deployment classes (kept distinct — never averaged)
1. **Local / open-weight** — weights and runtime under local control.
2. **Enterprise-hosted** — provider-run, under a enterprise agreement.
3. **Cloud-managed platform** — provider-run managed endpoint (incl. agent
   platforms).
4. **Read-only hosted inference** — consumer/comparison surfaces with no
   contractual data guarantees (incl. blind-comparison hosts).

## Analysis axes (applied to EACH deployment separately)
| Axis | What must be established (with official pointers, or "unresolved") |
|---|---|
| Provider | who operates the model/service; which entity is contracted |
| Controller / processor | data-control roles under applicable law for THIS data flow |
| Deployer / application / tool roles | who deploys, who is the application provider, what tools act |
| Data-subject position | whose personal data could enter the flow (Commander, corpus-mentioned persons) |
| Data flow | what leaves the local boundary, in what form, to where |
| Retention | per-surface, per-purpose retention facts (from the record's `retention_training_mode` + official pages) |
| Transfers | routing/region facts, transfer mechanisms — `region: undeclared` blocks analysis, honestly |
| Copyright | what is submitted (corpus derivatives are Commander conversions of third-party originals), what the terms claim about inputs/outputs |
| License | model license / AUP for THIS use; open questions recorded, never concluded |
| Contracts | which terms govern; enterprise vs consumer divergence; what is sales-gated |

## Method rules
- One deployment = one analysis = one gated order. No composite rankings.
- Every cell cites a source tier ([O]/[S]/[U]) or reads "unresolved — trigger:
  <official page>".
- Any cell that would require a legal conclusion instead records the QUESTION
  and the official pointer; conclusions belong to qualified human review.
- The matrix output is evidence for a Commander decision; it never executes,
  configures, or connects anything.
