# TID-2026-09-14-k — REASONING · RENDERED PROJECTION (4700)
> Rendered from `evidence/tasks/TID-2026-09-14-k/` by `radiation_core.relay.render_neuron`.
> Projection, not the record: hand edits FAIL check 27 (file must equal render output).

- **Task:** TID-2026-09-14-k · **Mode hint:** autopilot · **Base revision:** b1e92bf
- **Source:** commander · chat: 'proceed to 4700!' · trust=root
- **Received:** 2026-09-14T23:55:00+08:00
- **Plan:** PLAN-4700 · 5 step(s)
- **Commands:** 5 · outcomes succeeded: 5/5 · **Events:** 31 · **Final state:** COMPLETE

## NOTES — REASONING

Their list, verbatim: (1) seal — runner auto-commits (already live; their test reproduced it); (2) APPLY exits nonzero on failed auto-commit — fixed both runners, die() on commit failure; (3) planner block drifted (3/2 vs real 6/3) — generator now PARSES plan_term --self-check output, owns zero counting logic; (4) bundle authority — render_neuron(): neurons MUST equal render(bundle), h/i/j migrated (narrative moved into operator_notes), vector 12 added, 'the bundle is the record' wording adopted into boot docs + neurons README; (5) control plane — stays STAGED (Product-2). Legacy-count precision in docs (7 traces; f+g active legacy). Version v3.0.0: the first version whose Markdown cannot lie about its own bundles.
