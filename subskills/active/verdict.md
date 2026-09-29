# `/verdict` — bounded path-selection advisory
**ID:** SUB-010 · **Parent:** SKILL-022 · **Trigger:** manual · **Status:** active (catalog status only)

## MISSION
Frame one bounded objective, compare exactly two or three paths, select exactly one, and preserve the rejected residuals in a complete advisory record. `/verdict` is a manual declarative discipline, not a command, parser, runtime entrypoint, or grant of authority.

## TRIGGERS
A person manually requests `/verdict`, or Kitchen requests manual advisory entry. Neither request authenticates a Commander. Autonomous, event, and before-skill routes never fire it. “Active” means only that this card is admitted in the catalog.

## ACTIONS
1. State the objective, scope, and exclusions.
2. Describe two or three uniquely identified paths and their trade-offs.
3. Select one path and state one residual for every unselected path.
4. State capability limitations and retained blockers; choose `advisory`, `blocked`, `refused`, or `hold` honestly.
5. Complete the `radiation.verdict/0.1a` record shape and, only through a future manual admission process, append a new line to `evidence/verdict/records.jsonl`. A later veto or reversal is a linked new record; prior bytes are never rewritten.

## FORBIDDEN
Do not implement or execute a path; invoke `/analyze` or Origami; use AMF, CTP, or the control plane; run a tool; open network, credential, or subprocess access; activate child packages; clear blockers; grant permission; authenticate a Commander; claim Commander approval; or replace the Commander’s decision or repository seal. Kitchen cannot bypass completeness. Full V0.1 AMF/CTP execution remains blocked.

## FAILURE MODES
Unbounded objective; fewer than two or more than three paths; duplicate path IDs; absent or multiple selection; selection outside the considered set; missing or surplus rejected residual; hidden incapability; nonzero analyze count; execution/clearance/identity claim; a completeness seal misrepresented as approval; rewriting history instead of linking a new record. Any such condition is blocked or refused, never silently repaired into authority.

## OUTPUTS
One schema-bound advisory record. Its seal attests only record completeness. Commander visibility is unverified reporting. The record is advice and confers no execution, authentication, approval, ratification, merge, or repository authority.
