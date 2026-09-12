# 🎛️ THE MODE SYSTEM (`docs/MODES.md`)
## The Six Commander-Declared Modes & The Activation Matrix
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

## 🔍 @Review — Brain-First Recall & Refresh Mode
- **Purpose:** answer from what RADIATION already KNOWS. Gathers information stored in `/Brain` first; fishes the internet ONLY where the Brain is silent, stale, or contradicted.
- **Retrieval order (LAW of this mode):** 1) Brain/long_term → 2) Brain/short_term + subsidiary → 3) external_sources DIGESTs (MANIFEST-guided, Restraint Doctrine applies) → 4) internet, only for gaps — each gap-fetch justified in one line.
- **Skill loadout:** prospector (Brain-first, lean web), decomposer (lean), triangulator (full — verifies stored claims still hold), inspector (decay/DEBT audit of touched matter), scribe (answer + refresh report; NO Core writes).
- **Subskills:** scout MANDATORY (its Brain-check-before-acquire duty IS this mode's heart) · curator PASSIVE (gap-fetches ingested) · compass, sentinel, surgeon always-on.
- **Deliverable:** the answer + a REFRESH REPORT: which Brain claims were used, which were re-verified, which decayed ([DECAYED] flagged per I.4), which gaps required the internet.
- **Stockpile:** no fixed floor — Brain matter is the stockpile; every internet gap-fetch logged. Triangulation floor 2 for any NEW claim entering the Brain.
- **When:** the Commander wants what the system already knows — study recall, reviewer drills, refreshing prior research without re-gathering the world.

## 🤖 @Autopilot — Full-Autonomy Cue-Reading Mode
- **Purpose:** full autonomy. The Commander states an objective; the AI plans, chains modes, and executes end-to-end, reading CUES from the Commander instead of awaiting orders.
- **Authority:** may serially self-chain @Data/@Gather/@Decode/@Review legs under ONE Scan Declaration (III.2 serial-session clause); declares the planned chain up-front, appends `RE-SCAN` on every leg change.
- **Cue discipline — THE AUTOPILOT DOCTRINE (`cue/autopilot-doctrine.md`) governs:** 4-tier cue taxonomy (explicit → mission → environmental → historical), the standing-orders queue (the repo's own registers supply work when the Commander is silent), the 7-step loop (SENSE→ORIENT→PLAN→ACT→RECORD→DELIVER→PROPOSE), deliverable-inference table, and the post-deliverable duty checklist. `autopilot-cues.md` is the confirmed-cue registry layer beneath it.
- **HARD LIMITS — autonomy is bounded, never sovereign:** ① all Constitution laws apply in full — autonomy never overrides I.1/I.3, quotas, or the Restraint Doctrine (only an EXPLICIT Commander order does, IV.1); ② 🛑 MUST ASK at: canon-affecting changes, purges, Commander-gated actions (external_sources entries), budget extensions, LOW-confidence forks (III.3 outranks autonomy); ③ every leg logged in its temporal_lobe episode as it happens — the episode IS the flight recorder.
- **Deliverable:** the objective's deliverables + AUTOPILOT LOG (decisions, cues read, tiers invoked, forks + why) + the AUTO-PATCH zip in the same delivery (II.8.4 — ABSOLUTE) + a PROPOSE line naming the next standing-orders items.
- **When:** the Commander wants outcomes, not supervision — "handle it, wake me for the big calls."

---

# 🗂️ THE ACTIVATION MATRIX (constitutional annex to III.2)

| Skill / Organ | @Data | @Gather | @Decode | @Radiation | @Review | @Autopilot |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| prospector (Research) | ✅ lean | ✅ full | ✅ full (repo=1°) | ✅ full | ✅ Brain-first | per leg |
| decomposer (Analyze) | ✅ lean | ✅ | ✅ | ✅ | ✅ lean | per leg |
| archivist (Dossier) | ❌ | ✅ | ✅ | ✅ | ❌ | per leg |
| incubator (Incubate) | ❌ | ✅ | ✅ | ✅ | ❌ | per leg |
| annotator (Annotate) | ❌ | ✅ | ✅ | ✅ | ❌ | per leg |
| triangulator (Triangulate) | ✅ stripped | ✅ full | ✅ full | ✅ full (floor 3) | ✅ full | per leg |
| inspector (Inspect) | ❌ | ✅ | ✅ | ✅ | ✅ decay-audit | per leg |
| surgeon (Overhaul-authoring) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| scribe (Nota) | ✅ answer-only, no Core | ❌ | ❌ | ✅ | ✅ answer+refresh | per leg |
| surgeon-passive (enforcement) | ✅ always | ✅ always | ✅ always | ✅ always | ✅ | ✅ |
| sentinel-passive | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| compass-passive | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| curator | ❌ dormant | ⚙️ invocable | ⚙️ invocable | ✅ passive | ✅ passive | per leg |
| scout (active) | ❌ | ⚙️ | ⚙️ | ⚙️ | ✅ MANDATORY | ✅ |
| colony (active) | ❌ | ⚙️ | ⚙️ | ⚙️ | ❌ | per leg |

✅ = active per loadout · ⚙️ = invocable on declared judgment · ❌ = not available

**Degradation rule:** an AI that cannot load Boot Tier 2 must declare it and may
NOT run @Radiation. It operates @Data or @Gather-lean only, and says so in its
Scan Declaration.
