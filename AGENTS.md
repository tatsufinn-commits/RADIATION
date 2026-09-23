# AGENTS.md — Layered Agent-Entrypoint Cascade (WP-1 1.2)
**Version:** v3.10.32 · **Basis:** Repo E AGENTS idiom (facts+links only, prose rewritten per Rewrite-rule Law 5)
**Law:** Six ratified laws D029 (2026-09-22) · D1–D10 · FF-seal only · sequence as-written · raise-only ratchet · warn-and-justify · quarantine-before-delete · WP-D single gate
**Checklist:** Per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — this edit cites checklist for canon-doc touches per 1.2 acceptance
**Glossary:** docs/GLOSSARY.md defines every canon term + anti-terms per 1.3 — pure-additive

## Boundaries (what agent may/may not touch)

- **May touch:** Read/plan/evidence per RD-3 reconciliation (docs/.readme §8.4 vs AGENTS.md: silence authorizes read/evidence-producing protocol work only, any effect beyond read requires II.11 control plane)
- **May not touch:** canonical_apply/push are Commander motor acts per II.11 — refuse always, record and prepare never seal
- **May not invent:** Provider profile only when host explicitly known and matches folder per agents/AGENT_INDEX.md — unknown/ambiguous → generic CAP path, declare uncertainty, never invent provider
- **May not claim:** Model identity, tools, unobserved access — honesty clause per docs/THREAT_MODEL.md, label is label

## Workflow (steps agent follows)

1. **Boot** per docs/.readme Tier 0 per III.1, then BOOT_SEQUENCE.md
2. **Route** per agents/AGENT_INDEX.md — read routing decision, load agents/<Provider>/ only when host explicitly known
3. **Pass** — handoff phrase RADIATION PASS → python3 agents/_common/radiation_pass.py --host "<label>" — state machine not elevation, zero writes (opt-in --persist writes Brain/short_term/active/session_capability_state.json per S-2-ENV)
4. **Defaults:** read/plan/evidence only per RD-3, drafts via II.11 control plane docs/CONTROL_PLANE.md — decide + approve + execute with content-bound single-use approvals
5. **Verify:** python3 scripts/validate.py 0-fail, gate 0 findings, Ran 195 OK, preflight 0 findings, render_docs ✓, verify_apply strict FAIL-CLASS none per §4 battery
6. **File shrine:** heartbeat docs/shrine/LOG.md per II.9 every conversation, testament per build

## Contracts (machine-checked agreements)

- **Two-key resolver:** Policy (source rank vs executed allowlist) AND tool per II.11 — --source label is assertion not credential, no execution without chained decision + unconsumed approval
- **Receipts:** Tamper-evident hash-linked per II.11, limits docs/THREAT_MODEL.md, CI check 37
- **Task-ID grammar:** Schema-enforced per II.11, genesis exception, strict task grammar + pinned drafts base
- **Provider contracts:** agents/contracts/AGT-<slug>.json typed contracts bounded by receipts, D4 law no_simulated_commander_authority true, machine-checked per check 38
- **Tool registry:** tools/TOOL_REGISTRY.json bounded contract schema-EXECUTED + code-level rules self-tested per check 39

## Data Paths — Single-Truth Section (1.2 requirement, raise-only ratchet note)

**Raise-only — may not be tuned downward later per Law 2**

| Path | Truth |
|---|---|
| Canon docs | docs/AI_RULES.md, docs/PATCH_PROTOCOL.md, docs/CONTROL_PLANE.md, BOOT_SEQUENCE.md, docs/.readme |
| Agent entrypoint | AGENTS.md (this file) — boundaries/workflow/contracts only — plus per-area files agents/AGENT_INDEX.md, agents/BOUNDARIES.md, agents/WORKFLOW.md, agents/CONTRACTS.md, agents/DATA_PATHS.md |
| Provider profiles | agents/<Provider>/BOOT.md, agents/AGENT_INDEX.md routing, scaffolding/hosts/*.json machine-readable posture |
| Brain memory | Brain/ — short_term, long_term, frontal_lobe, temporal_lobe, external_sources, subsidiary, cerebellum per II.6 Promotion Protocol |
| Ledgers | Brain/frontal_lobe/task_ledger.md, docs/PATCH_LEDGER.md, docs/shrine/LOG.md — append-only per II.2 |
| Gate | docs/RELEASE_TRUTH_GATE/EXPECTATION.json base_sha + allowed_changes + mandatory validations per §4 |
| Policies | CLAUDE.md, CURSOR.md, CODEX.md root machine-readable agent policy files ≤30 lines imperative tool-facing pointer to Patch protocol per 1.4 |
| Glossary | docs/GLOSSARY.md term+definition+Avoid per 1.3 |
| Checklists | scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md governs canon-doc touches per 1.6 |
| Patch manifest | docs/PATCH_SELF_CERTIFICATION_MANIFEST.md six checkboxes ✅/❌ + teeth RETURNED not queued per 1.1 |
| Verification policies | Subskill/cue verify field additive optional namespaced extension tolerating unknown keys per 1.5 |

## Per-Area Files (module detail migrated downward per 1.2 — cascade audit, not duplication)

- **Routing:** agents/AGENT_INDEX.md — exact routing decision, invariants tested check 38
- **Boundaries detail:** agents/BOUNDARIES.md — expanded boundaries per area
- **Workflow detail:** agents/WORKFLOW.md — expanded workflow steps per area
- **Contracts detail:** agents/CONTRACTS.md — expanded contracts per area
- **Data paths detail:** agents/DATA_PATHS.md — single-truth expanded
- **Provider BOOT:** agents/<Provider>/BOOT.md — provider-specific posture, first act run the pass, defaults and escalation, refusal lines
- **Research layer:** agents/ROUTING_MATRIX.md, agents/RESEARCH_METHOD.md — dated provider CAPABILITY_PROFILE.md + SOURCES.md per 5400 non-boot

## STALE Banners (quarantine-before-delete Law 4 — nothing deleted)

- Any superseded spec in agents/ or docs/ gets banner: "⚠️ STALE — superseded by <new path> per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — quarantine-before-delete, Commander disposes"
- No deletions, only banners, incubation lanes, quarantine notes — decay proposes, Commander disposes per Law 4
- Current STALE: none — this cascade is first layering, prior AGENTS.md content preserved in per-area files

## Links

- Change-control checklist: scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md governs edits per 1.6 — cited in this commit per 1.6
- Glossary: docs/GLOSSARY.md defines every canon term + anti-terms per 1.3 — scaffold docs link it
- Patch protocol: docs/PATCH_PROTOCOL.md — pointer for agent policy files per 1.4
- Patch self-certification: docs/PATCH_SELF_CERTIFICATION_MANIFEST.md per 1.1 — six checkboxes + teeth
- Verification policies: subskills/SUBSKILL_CATALOG.json + cue/CUE_CATALOG.json verify field per 1.5 — three golden traces as WP-2.3 cassette seeds

## Laws acknowledged

D1–D10 · six ratified laws D029 (2026-09-22) · FF-seal only · sequence WP-1→WP-2.3→WP-2/3→WP-4→WP-5/WP-D · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate · pure-additive per 1.3 · checklist citation per 1.6

## Research-only venue pointers

None — zero network, zero live venue, zero SaaS in WP-1 per Law 6 — any venue mention marked research-only
