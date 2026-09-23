# DATA_PATHS — Single-Truth Expanded (WP-1 1.2)
**Basis:** AGENTS.md single-truth section per 1.2, raise-only ratchet note
**Law:** Raise-only — may not be tuned downward later per Law 2, quarantine-before-delete, warn-and-justify
**Checklist:** Per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md

## Single-Truth Section — Canonical Data Locations

**Raise-only — may not be tuned downward later per Law 2 — score/floor fields carry ratchet note**

| Category | Path | Truth |
|---|---|---|
| Canon docs | docs/AI_RULES.md | Constitution Book.Law citation format, supreme laws |
| Canon docs | docs/PATCH_PROTOCOL.md | Patch workflow, AI emits, Commander applies |
| Canon docs | docs/CONTROL_PLANE.md | II.11 control plane, two keys, receipts |
| Canon docs | BOOT_SEQUENCE.md | Tiered mandatory load order |
| Canon docs | docs/.readme | AI entry gate, magic words |
| Agent entrypoint | AGENTS.md | Boundaries/workflow/contracts only per 1.2 layered cascade |
| Agent routing | agents/AGENT_INDEX.md | Exact routing decision, invariants check 38 |
| Agent boundaries | agents/BOUNDARIES.md | Expanded boundaries per-area per 1.2 (this layering) |
| Agent workflow | agents/WORKFLOW.md | Expanded workflow per-area per 1.2 |
| Agent contracts | agents/CONTRACTS.md | Expanded contracts per-area per 1.2 |
| Agent data paths | agents/DATA_PATHS.md | This file — single-truth expanded |
| Provider BOOT | agents/<Provider>/BOOT.md | Provider-specific posture, first act run pass |
| Provider profiles | agents/Arena_AI/CAPABILITY_PROFILE.md | Capability attestation per 5400 |
| Provider sources | agents/Arena_AI/SOURCES.md | Dated sources per 5400 |
| Machine posture | scaffolding/hosts/*.json | Machine-readable posture per agents |
| Contracts | agents/contracts/AGT-*.json | Typed contracts bounded by receipts per Dim-1/G4 |
| Brain memory | Brain/ | short_term, long_term, frontal_lobe, temporal_lobe, external_sources, subsidiary, cerebellum per II.6 |
| Brain ledgers | Brain/frontal_lobe/task_ledger.md | Append-only per II.2, one-line executive index |
| Patch ledger | docs/PATCH_LEDGER.md | Append-only per II.2, one line per Patch |
| Shrine log | docs/shrine/LOG.md | Heartbeat ledger per II.9, one line per session |
| Shrine members | docs/shrine/members/ | Full testaments per CHARTER §1 |
| Gate | docs/RELEASE_TRUTH_GATE/EXPECTATION.json | base_sha + allowed_changes + validations per §4, moving-base law base rides last green seal |
| Gate README | docs/RELEASE_TRUTH_GATE/README.md | Motor preflight section per P-12 |
| Policies root | CLAUDE.md, CURSOR.md, CODEX.md | Root machine-readable agent policy files ≤30 lines imperative tool-facing pointer to Patch protocol per 1.4 |
| Glossary | docs/GLOSSARY.md | Canon glossary term+definition+Avoid per 1.3 pure-additive |
| Checklists | scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md | Change-control checklist per 1.6 governs canon-doc touches |
| Patch manifest | docs/PATCH_SELF_CERTIFICATION_MANIFEST.md | Self-certification manifest six checkboxes ✅/❌ + teeth RETURNED not queued per 1.1 |
| Verification | subskills/SUBSKILL_CATALOG.json | Per-skill verification policies additive optional verify field per 1.5 |
| Verification | cue/CUE_CATALOG.json | Per-cue verification policies per 1.5 |
| Golden traces | evals/verify_policies/ | Three minimal golden traces one per policy class per 1.5, registered as WP-2.3 cassette seeds per J1 |
| Schemas | schemas/ | 24 schemas within executor's executed set per check 40 |
| Scripts | scripts/ | 35+ scripts, 12 exercised in CI per machine-facts |
| Tests | tests/ | 195 tests per §4 battery |
| Styles | styles/ | 10 deliverable skeletons [MANDATORY]/[FLEX] per III.4 |
| Evals | evals/ | Evaluation fixtures, hostile, brain, subskills, skills, etc. |

## Laws acknowledged
D1–D10 · six ratified laws D029 · FF-seal only · sequence as-written · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate

## Research-only venue pointers
None — zero network/venue/SaaS in WP-1 per Law 6
