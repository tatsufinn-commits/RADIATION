# 🎯 THE NINE SKILLS (`docs/SKILLS.md`)
## Capabilities of the One Superior AI — not personas, not agents
**Version:** 1.0.0 | Constitutional basis: III.2 (activation via modes only)

Skills are development-oriented capabilities the AI wields. Each is
jurisdiction-bound: it writes only to its own folder (+ the task ledger).
Cross-jurisdiction writes require a logged handoff. Passives police all of them
(III.7): skills do the work; passives police the work.

---

## 1. RESEARCH — `prospector` → writes to `01-research/`
Acquire knowledge from primary/secondary sources. Every acquisition logged with
source, date, type (1°/2°), authority tier, and per-claim grades (I.2).
Executes scout's Source Acquisition Plan (III.8) — never acquires unvetted.
**Core scaffold:** `proc_research-sortie.md`.

## 2. ANALYZE — `decomposer` → writes to `02-analyze/`
Decompose findings into build-ready structures: claim tables, comparison
matrices, dependency maps. Every row traces to a Research finding ID.

## 3. DOSSIER — `archivist` → writes to `03-dossier/`
Stockpile intelligence into complete, reusable subject dossiers (style:
`dossier.md`). No ungraded claims. Dossiers are the reference arsenal —
finished dossiers settle in `Brain/long_term/dossiers/` after triangulation.

## 4. INCUBATE — `incubator` → writes to `04-incubate/`
Sandbox promising-but-unproven findings ([S]-grade matter lives here and ONLY
here). Every ticket carries explicit promote/kill criteria. Graduations are
logged in `04-incubate/GRADUATION_LOG.md`.

## 5. ANNOTATE — `annotator` → writes to `05-annotate/`
Attach margin notes, evidence grades, and citation anchors to every source.
100% of claims graded before the source leaves annotation.

## 6. TRIANGULATE — `triangulator` → writes to `06-triangulate/`
Cross-verify claims against ≥2 independent sources (3 for Core-bound under
@Radiation). Independence = different author/organization AND different channel.
Conflicts logged side-by-side in `CONFLICT_REGISTER.md`, never resolved by
deletion (I.5). **Triangulation is the ONLY grade elevator** (I.3).
**Core scaffold:** `proc_triangulation-gauntlet.md`.

## 7. INSPECT — `inspector` → writes to `07-inspect/`
Audit gathered material and the repository itself for drift, debt,
contradiction. Findings classified 🟥 critical / 🟧 debt / 🟨 drift / 🟩 clean.
Debt appended to `DEBT_REGISTER.md`. **Core scaffold:** `proc_inspection-audit.md`.

## 8. OVERHAUL — `surgeon` → writes to `08-overhaul/` + veto everywhere
⚡ **DUAL CITIZENSHIP.** As Skill #8: authors restructuring proposals in
`08-overhaul/proposals/`; ratified proposals ship as Patches (IV.2).
As CHIEF PASSIVE (spec: `subskills/passive/surgeon.md`): unconditional
enforcement of the Constitution, mode discipline, style compliance, and quotas
in EVERY mode — the only organ authorized to halt a pipeline mid-run.

## 9. NOTA — `scribe` → writes to `09-nota/`
ANSWER. Distill triangulated knowledge into final deliverables and Core cards:
≤300 words per card, answer-first, plain language, grade markers kept, lineage
block citing the long_term dossier + triangulation worksheet IDs. Only
Shield-Stamped (triangulated) claims are admissible (I.3).
**Core scaffold:** `proc_nota-distillation.md`.

---

## THE PIPELINE
```text
scout (vet) → 1 RESEARCH → 2 ANALYZE → 3 DOSSIER ─┐
                   ▲                              ├→ 6 TRIANGULATE → 9 NOTA
        4 INCUBATE (branch, [S] matter)           │        │           │
        5 ANNOTATE (continuous on sources) ───────┘        ▼           ▼
        7 INSPECT → 8 OVERHAUL (maintenance loop)    CONFLICT_REG   the Core
Memory: curator → Brain/short_term → (triangulated) → Brain/long_term
```
R→A→D is the intake spine · Incubate branches anywhere · Annotate+Triangulate
run continuously on sources · Inspect→Overhaul is the maintenance loop ·
Nota is terminal distillation — nothing enters the Core untriangulated.
