# 🎛️ THE MODE SYSTEM (`docs/MODES.md`)
## The Four Commander-Declared Modes & The Activation Matrix
**Version:** 1.0.0 | Constitutional basis: III.2 (Mode Supremacy), III.3 (Mode Compliance)

The Commander declares exactly ONE mode per session (serial multi-stage sessions
are declared in one Scan Declaration). Modes are the ONLY lawful way to activate
skills. When a mode's constraint conflicts with a skill's normal behavior,
**the mode wins** and the constraint is logged in the Scan Declaration.

**Invocation syntax:** `@[MODE] | STYLE: [style-name or AUTO] | TOPIC: [the task]`

---

## ☢️ @Radiation — Full-Spectrum Protocol
- **Purpose:** the complete 9-skill pipeline for maximum-rigor research culminating in canonical answers.
- **Skill loadout:** ALL NINE — prospector → decomposer → archivist → incubator → annotator → triangulator → inspector → surgeon → scribe.
- **Deliverable:** full dossier + Nota answer cards admitted to the Core (`09-nota/`).
- **Citations:** full reference list, evidence-graded, triangulation worksheets included.
- **Stockpile:** min 12 primary + 20 secondary. Triangulation floor for Core-bound claims: **3 independent sources**.
- **Curator:** PASSIVE — every source touched is automatically ingested to the Brain.
- **When:** the Commander needs deep, permanent, reusable knowledge.

## ⚡ @Data — Rapid Answer Mode
- **Purpose:** researching information for answering quizzes and questions. Quick but source-accurate.
- **Skill loadout:** prospector (lean), decomposer (lean), triangulator (stripped gauntlet: claim row → independence → verdict), scribe (answer-only; NO Core writes).
- **Source conduct:** USES real sources for verification but does **NOT list them** in the deliverable.
- **Stockpile:** min 2 primary + 3 secondary per answered question-set. Triangulation floor: 2 independent.
- **Footprint:** no dossiers, no annotation files, no incubation, no Brain writes (curator dormant). One-line task-ledger entry allowed.
- **Scaffolds:** exempt except the stripped triangulation gauntlet.
- **When:** exams, quizzes, quick factual questions, rapid-fire study.

## 📡 @Gather — Information Acquisition Mode
- **Purpose:** gathering information for research and internet-related tasks. GATHERING is the mission — no concluding.
- **Skill loadout:** prospector, decomposer, archivist, incubator, annotator, triangulator, inspector, surgeon. **NO scribe / NO NOTA.**
- **Stockpile (Commander-fixed):** minimum **10 primary + 18 secondary** sources. Shortfall = `[STOCKPILE SHORTFALL]` logged; surgeon adjudicates closure.
- **Style:** MANDATORY — one format from `/styles/` per the Commander's prompt or AUTO. Default: `research.md`.
- **Deliverable:** style-formatted corpus + dossiers + annotated stockpile + full reference list.
- **When:** building the knowledge arsenal on any topic.

## 🔬 @Decode — Repository Comprehension Mode
- **Purpose:** @Gather's sibling aimed at GitHub repositories — understanding infrastructures, architectures, code, scaffolding, concepts.
- **Skill loadout:** identical to @Gather (8 skills, NO scribe / NO NOTA).
- **Stockpile:** target repo tree(s) read in full = primary; minimum **8 supporting secondary sources** (docs, issues, papers, comparable repos).
- **Mandatory outputs:** architecture map · infrastructure inventory · concept extraction · pattern/anti-pattern register · dependency graph.
- **Style:** default `msr.md` (Mining Software Repositories).
- **When:** studying repositories for reference, reuse, or comprehension.

---

# 🗂️ THE ACTIVATION MATRIX (constitutional annex to III.2)

| Skill / Organ | @Data | @Gather | @Decode | @Radiation |
|---|:---:|:---:|:---:|:---:|
| prospector (Research) | ✅ lean | ✅ full | ✅ full (repo=1°) | ✅ full |
| decomposer (Analyze) | ✅ lean | ✅ | ✅ | ✅ |
| archivist (Dossier) | ❌ | ✅ | ✅ | ✅ |
| incubator (Incubate) | ❌ | ✅ | ✅ | ✅ |
| annotator (Annotate) | ❌ | ✅ | ✅ | ✅ |
| triangulator (Triangulate) | ✅ stripped | ✅ full | ✅ full | ✅ full (floor 3) |
| inspector (Inspect) | ❌ | ✅ | ✅ | ✅ |
| surgeon (Overhaul-authoring) | ❌ | ✅ | ✅ | ✅ |
| scribe (Nota) | ✅ answer-only, no Core | ❌ | ❌ | ✅ |
| surgeon-passive (enforcement) | ✅ always | ✅ always | ✅ always | ✅ always |
| sentinel-passive | ✅ | ✅ | ✅ | ✅ |
| compass-passive | ✅ | ✅ | ✅ | ✅ |
| curator | ❌ dormant | ⚙️ invocable | ⚙️ invocable | ✅ passive |
| scout (active) | ❌ | ⚙️ | ⚙️ | ⚙️ |
| colony (active) | ❌ | ⚙️ | ⚙️ | ⚙️ |

✅ = active per loadout · ⚙️ = invocable on declared judgment · ❌ = not available

**Degradation rule:** an AI that cannot load Boot Tier 2 must declare it and may
NOT run @Radiation. It operates @Data or @Gather-lean only, and says so in its
Scan Declaration.
