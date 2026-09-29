# `/verdict` V0.1A — Manual Advisory Contract

## Purpose and status
`/verdict` is a **manual, declarative, non-executing advisory discipline**. It frames one bounded objective, compares exactly two or three paths, selects one, and preserves a rejected residual for every unselected path. “Active” is catalog status only. There is no parser, command, runtime entrypoint, self-fire, tool registration, implementation engine, authentication path, or runtime writer.

## Record semantics
A `radiation.verdict/0.1a` record states scope and exclusions, uniquely identified considered paths, one referenced selection, rejected residuals, capability limitations, and retained blockers. Its advisory seal means **record completeness only**—never Commander approval, ratification, or repository seal. `commander_visibility` is expressly unverified reporting and cannot authenticate identity. A later veto or reversal is represented by a new record linked through `history.supersedes_record_id`; the earlier JSONL bytes remain unchanged and ordered.

`evidence/verdict/records.jsonl` is empty and is only a declared destination for a future **manual** admission. V0.1A provides no writer. Tests use temporary files and never write to the tracked destination.

## Outcomes and incapability
`advisory`, `blocked`, `refused`, and `hold` are the only outcomes. Unknown or incapable conditions remain visible. Every record retains at least one blocker and limitation and fixes `analyze_invoked: 0`, `advisory_only: true`, `execution_authorized: false`, and `blockers_cleared: false`. Kitchen may request entry but cannot bypass completeness.

## D056 five pins retained
1. No path is implemented or executed.
2. `/analyze` is not invoked.
3. Origami is not invoked.
4. AMF, CTP, and control-plane execution are not used.
5. The discipline neither authenticates nor replaces Commander decision or seal.

These pins also forbid tool use, network, credential or subprocess access, child-package activation, permission grants, blocker clearance, and manufactured approval. Full V0.1 AMF/CTP execution remains blocked.

## Validation boundary
The closed JSON Schema uses only repository-executor-supported keywords. Relational invariants—unique path IDs, selection membership, exact residual coverage, linked non-rewriting history, and byte-identical append-only prefixes—are enforced in `tests/test_verdict_record.py`. Schema validity is necessary but never authority.
