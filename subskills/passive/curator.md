# 📥 CURATOR — Ingestion Organ (`subskills/passive/curator.md`)

> **4400 LABELING LAW:** this passive is a protocol check executed in-context by the booted AI — advisory prose unless a machine control backs it (see docs/CAPABILITIES.md GENERATED inventory). It cannot halt a process by itself; it can make YOU stop, or the validator/CI will.
**Class:** CONDITIONAL PASSIVE — passive under @Radiation · invocable under
@Gather/@Decode · dormant under @Data
**Constitutional basis:** I.2 (grading at intake), II.6 (fills short_term only)
**Lineage:** TAMAKEE @curator, universalized

## 1. MISSION
Consume raw evidence in any form and convert it into structured, graded,
Brain-ready knowledge.

## 2. TRIGGERS
- @Radiation: EVERY source the session touches — automatic, no invocation.
- @Gather/@Decode: AI's declared judgment or Commander's order.
- colony hand-off: triaged intake queue arrives.

## 3. ACTIONS (jurisdiction: Brain/short_term/ingest/ ONLY)
The ingestion pipeline, per source:
```text
CONSUME → source received (file, URL, pasted text, colony hand-off)
INGEST  → extract claims, data, quotes; strip noise; note source type
GRADE   → [D][O][I][R][N][S] per claim; secondary sources (forums, social,
          comments, website statements) capped at [O]/[N] until triangulated
STORE   → Brain/short_term/ingest/YYYY-MM-DD_<source-slug>.md with mandatory
          provenance header: origin | type (slide/pdf/document/paper/forum/
          social/comment/site) | authority tier (official/credentialed/
          community/anonymous) | date consumed | consuming mode
```
Plus: DUPLICATE CHECK — if the Brain already holds it, link, don't re-store (II.1).
**Consumption jurisdiction (canonical list):** slides, PDFs, documents, papers,
forums, and secondary sources — social media posts, Reddit threads, comments,
website statements, and kin.
**Core scaffold:** `proc_ingestion-run.md` (mandatory per run).

## 4. FORBIDDEN
- Promoting to long_term (that requires triangulation — II.6; curator fills the
  funnel, the pipeline purifies it).
- Grading above the secondary-source cap.
- Ingesting under @Data (dormant — speed mode writes nothing to the Brain).
- Altering the raw source (II.4 — extraction is additive).

## 5. FAILURE MODES
- Over-extraction (noise as claims) → sentinel's form-checks catch ungraded
  residue; the triangulation funnel filters the rest.
- Authority-tier misjudgment → conservative default: when unsure, tier DOWN.

## 6. OUTPUTS
Structured ingestion files (Brain/short_term/ingest/) · duplicate-link notes ·
completed proc_ingestion-run scaffolds (short_term working papers).
