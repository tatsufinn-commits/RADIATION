# 🪝 HOOK PROTOCOL (`subskills/HOOK_PROTOCOL.md`)
## Subskill Hooks — Declared, Machine-Checked, Never Autonomous (P-18 Dim-8/G4)

**Version:** 1.0.0 | **Basis:** III.7 Subskill Discipline + II.11 Control Plane + P-17 Skill Catalog Spine

### The Contract in One Screen

- **Declaration-only hooks:** every hook is declared in `subskills/SUBSKILL_CATALOG.json` with fields `{id, parent_skill FK→SKILL_CATALOG, entry_path, trigger enum before_skill|after_skill|on_event|manual, condition|null, description ≤200, scenario_ref, status, tests[]}`. No hook exists outside the catalog. Schema `radiation.subskill_card/1` enforces id pattern, FK, trigger enum, status discipline.

- **Invocation direction:** skill→subskill ONLY. A skill invokes its subskill hook; a subskill never self-fires, never invokes a skill, never invokes another subskill. Hook means INVOKED — never self-firing autonomous. The parent_skill FK proves the edge: subskill catalog references skill catalog (P-17), second FK edge for full graph (P-20 will check full graph).

- **Evidence capture on invocation:** every invocation appends a receipt to evidence/drafts/SUB-001/receipt.json (or task ledger row self/attempt marker). Receipt contains trigger, parent_skill, entry_path, condition evaluation, input sketch, fire/non-fire decision. Check subskill_check.py validates scenario_ref resolves and trigger enum valid; scenario fixtures under evals/subskills/ prove expected fire sequence and expected non-fires.

- **No self-modification:** a hook never rewrites its own catalog entry, never rewrites SUBSKILL_CATALOG.json, never rewrites SKILL_CATALOG.json, never modifies its own scenario fixture. The checker is read-only.

- **No network:** hook execution is stdlib-only, no `curl`, `urllib`, `requests`, no `https://`, no external calls. Evidence-only.

- **No authority elevation (II.11):** a hook is a skill-internal mechanism — never a cue, never a scope grant, never a commander order, never a ratified policy. It cannot elevate precedence, cannot bypass stop-lines, cannot grant canonical_apply. Commander-triggered subskills (overule, selfdirectives) still require explicit Commander trigger or declared+logged manual invocation — they are INVOKED, not autonomous. The control plane remains the sole authority for canonical writes.

- **Trigger discipline:**
  - `before_skill` — gate before skill executes (scout, surgeon)
  - `after_skill` — audit after skill completes (curator, sentinel)
  - `on_event` — reacts to event (colony bulk dump, compass drift)
  - `manual` — Commander or declared judgment (overule, selfdirectives)

- **Status discipline:** active must have scenario_ref resolving; declared must carry note; deprecated must carry superseded_by SUB-NNN. Honest declared beats invented coverage.

- **Non-goals hard:** no autonomous hook semantics ever, no moves/renames, no validator additions, no agent contracts (P-19), no cross-catalog linter (P-20 reserved).

### Checker

`scripts/subskill_check.py` deterministic house finding style exit 0/1 `--self-test ≥4`: schema valid, parent_skill FK resolves against `skills/SKILL_CATALOG.json`, scenario_ref resolves, trigger enum valid, status discipline.

### Scenario Fixture Shape

evals/subskills/ per active subskill e.g. evals/subskills/SUB-001.scenario.json:
```json
{
  "id": "SUB-001",
  "trigger": "on_event",
  "input_sketch": "bulk dump 50 URLs triggers RESEARCH",
  "expected_fire_sequence": ["skill declares", "skill to subskill invokes", "evidence captured"],
  "expected_non_fires": ["unrelated trigger does not fire"],
  "contract": "declaration-only, skill to subskill, evidence capture, no self-mod, no network, no elevation II.11"
}
```

One patch one purpose II.7.4 — subskills become typed records; hooks become declared, machine-checked, never-autonomous protocol.
