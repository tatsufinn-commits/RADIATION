# Canon Glossary with Anti-Terms (WP-1 1.3)
**Basis:** Repo E CONTEXT.md: term + definition + Avoid (facts+links only, prose rewritten per Rewrite-rule)
**Law:** Pure-additive, every canon term defined, scaffold docs link it, quarantine-before-delete, warn-and-justify
**Purpose:** Single-truth for canon vocabulary, prevents drift, supports prompt-composition governance per 1.6 checklist

## How to read
Each entry: **Term** — definition — **Avoid:** anti-term or misuse to avoid

---

### Core System Terms

**Patch** — A zip proposal containing changed files in repo-relative structure plus PATCH_NOTES.md per scaffolding/core/form_patch-notes.md, one coherent purpose, never mixing 🟢 and 🟠, Commander applies via push = legal effect. **Avoid:** "commit as patch" — Patch is proposal, not commit; Commander motor act required per II.11

**Shrine** — Shared judgment commons docs/shrine/ — full testaments (members/), heartbeat ledger LOG.md, CHARTER.md, mandatory per conversation per II.9. **Avoid:** "inheritance" or "successor" — swarm draws, none inherits per CHARTER §3

**Brain** — Memory system Brain/ — short_term, long_term, frontal_lobe, temporal_lobe, external_sources, subsidiary, cerebellum. Promotion Protocol governs short_term → long_term via triangulation. **Avoid:** "store in brain" without path — always use explicit Brain/ subpath

**Commander** — Mapúa University BS Architecture ALE-bound, sole permanent officer, outranks every law per IV.1, only motor act for canonical_apply/push per II.11. **Avoid:** "simulated Commander authority" — D4 law forbids simulated authority per agent contracts

**Architect** — Build bench role, builds per directive, emits Patch, files shrine testament per II.9. **Avoid:** "self-ratification" — Architect never ratifies own 🟠 canon, Commander only

**Desk** — Ruling chair, verifies landed main end-to-end, delivers SEAL, enforces three chairs (you build → Commander seals → Desk rules) per D1. **Avoid:** "desk as builder" — Desk never builds, only rules

**Control Plane** — II.11 ratified 5000, cooperative in-program policy flow, two keys per effect (policy + tool), chained decision + content-bound single-use approval, receipts digest-bound tamper-evident, canonical_apply/push remain Commander motor acts. **Avoid:** "auto-apply" — control plane never auto-applies

**CAP** — Capability record, attests tool effects, schema-executed, verifier registry, honest blocked/verified. **Avoid:** "CAP as permission" — CAP is attestation, not permission

**Cue** — Typed operational record cue/CUE_CATALOG.json, precedence law commander_order > ratified_policy > cue > heuristic > content, CONTENT-only isolation. **Avoid:** "cue as authority" — cue never elevates without explicit Commander ratification per P-11-B

**Skill** — Nine skills, jurisdiction in 01-09, loadout per Activation Matrix docs/MODES.md, mode wins over skill per III.2. **Avoid:** "skill as mode" — skill does work, mode governs

**Subskill** — Typed record subskills/SUBSKILL_CATALOG.json, FK to SKILL_CATALOG, hook trigger before_skill/after_skill/on_event/manual, scenario_ref proves contract, never autonomous per HOOK_PROTOCOL.md. **Avoid:** "self-firing subskill" — hooks invoked, never self-firing

**Mode** — Six Commander-declared modes @Radiation/@Data/@Gather/@Decode/@Review/@Autopilot, charter per docs/MODES.md, autonomous scan per III.3 when absent. **Avoid:** "infer mode at boot" — BOOT ASK law requires ask on low confidence per III.3

**Scaffold** — Process rigor scaffolding/ — core/ generated/ improved/ control_plane/ hosts/ neurons/, sidecar contracts *.contract.json, deterministic compile check via scaffold_check.py. **Avoid:** "scaffold as code" — scaffold is process rigor, not runtime

**Ledger** — Append-only history per II.2, sole overwrite exception docs/SYSTEM_STATE.md, travels as APPEND-BLOCKS in Patches. **Avoid:** "rewrite ledger" — rewriting history is first-order contamination per II.2

**Validator** — scripts/validate.py, form and resolvability only, 42 checks, never judges truth, never modifies files, exit 0 = no FAIL. **Avoid:** "validator as truth judge" — validator checks form/resolvability only

**Gate** — Release Truth Gate docs/RELEASE_TRUTH_GATE/ — EXPECTATION.json base_sha + allowed_changes + required deletions + generated artifacts + mandatory validations, gate live check + self-test. **Avoid:** "gate as bench" — CI is witness, never bench per §0

**Preflight** — scripts/push_preflight_check.py, LAW-5 BASE-PIN + PUBLIC-OBJECT + DELTA-≡-ALLOWED + CI-HYGIENE + LAW-6 WHITESPACE gate-mirror, 0 findings required. **Avoid:** "skip preflight" — motor preflight bypass is violation per P-12

**Patch Protocol** — docs/PATCH_PROTOCOL.md, practical workflow for system evolution, AI emits Patch when durable material exists, Commander applies, push = legal effect. **Avoid:** "Patch as commit" — Patch is proposal, Commander push is legal effect

**Decayed** — Claim past verification half-life per I.4, auto-downgrades one grade + [DECAYED] + listed in docs/DECAY_REGISTER.md, re-verification restores. **Avoid:** "delete decayed" — quarantine-before-delete, Commander disposes per Law 4

**Quarantine** — Fenced block ⚠️ QUARANTINE [date | reason | discovered-by] per I.1, excluded from retrieval/synthesis, listed in 07-inspect/DEBT_REGISTER.md, release requires re-verification or Commander purge. **Avoid:** "silent delete" — quarantine never silently deleted

**STALE** — Banner "⚠️ STALE — superseded by <new path> per 1.6 checklist — quarantine-before-delete, Commander disposes" — marks superseded specs, nothing deleted per Law 4. **Avoid:** "delete stale" — decay proposes, Commander disposes per Law 4

**Warn-and-justify** — Every gate WP-1 documents (incl. 1.6's teeth) speaks warning + recorded justification, never auto-reject per Law 3, evidence came from warnings per §4. **Avoid:** "auto-reject" — warn-and-justify never auto-rejects

**Raise-only ratchet** — No floor in WP-1 may be tunable downward later per Law 2, score/floor fields carry ratchet note "raise-only — may not be tuned downward later". **Avoid:** "tunable downward" — raise-only ratchet forbids downward tuning

**Rewrite-rule** — Any basis text from unlicensed source (Repo D) lands as facts+links only, prose rewritten never quoted per Law 5. **Avoid:** "quote unlicensed" — rewrite-rule requires facts+links only

**WP-D single gate** — Zero network, zero live venue, zero SaaS in WP-1 per Law 6, every venue mention is research pointer marked research-only. **Avoid:** "live venue in WP-1" — WP-D single gate forbids network/live venue/SaaS in WP-1

**FF-form seal** — Branch = one commit, sha-pin, no squash per D028 form-note, Commander FF seal only. **Avoid:** "squash merge" — FF-form seals only

**Stage-≡-allowed** — Delta equals allowed, fresh per tranche, δ-proof dies with its delta, enforced via push_preflight_check.py LAW-3. **Avoid:** "carry δ-proof" — stage-≡-allowed fresh per tranche

**ABSENT** — Lawful absence, stays lawful per §0, not a failure. **Avoid:** "treat ABSENT as FAIL" — ABSENT stays lawful

**Attempt marker** — task_ledger row contains attempt:/mastery:/drilled/@Review per check 20.5 planner theater guard. **Avoid:** "plan without attempt" — plans are not progress per AP-08

---

### Prompt-Composition Terms (Repo E governance)

**Agent Entrypoint** — Root AGENTS.md plus layered per-area files agents/AGENT_INDEX.md, agents/Arena_AI/BOOT.md etc., boundaries/workflow/contracts only in root, module detail downward. **Avoid:** "duplicate entrypoint" — cascade audit, not duplication per 1.2

**Boundaries** — What agent may/may not touch, defined in root AGENTS.md per 1.2. **Avoid:** "boundaries as detail" — boundaries are high-level, detail lives downward

**Workflow** — Steps agent follows, defined in root AGENTS.md per 1.2. **Avoid:** "workflow as module detail" — workflow is cascade-level, module detail downward

**Contracts** — Machine-checked agreements, per-area files, single-truth section for data paths per 1.2. **Avoid:** "contract duplication" — single-truth, not duplicated

**Data Paths** — Single-truth section listing canonical data locations, defined once per 1.2. **Avoid:** "duplicate data path definitions" — single-truth section only

**Incubation Lane** — Staging area for decay-proposed specs per quarantine-before-delete, banner STALE, Commander disposes per Law 4. **Avoid:** "delete incubation" — quarantine-before-delete

---

### Patch Certification Terms

**Self-Certification Manifest** — Six checkboxes with ✅/❌ example each, teeth incomplete manifests RETURNED not queued, Commander approval only sign-off per 1.1. **Avoid:** "queue incomplete" — teeth RETURNED not queued

**DCO Shape** — Developer Certificate of Origin shape, sign-off line per 1.1. **Avoid:** "missing sign-off" — DCO shape requires sign-off

**Return Rule** — Incomplete manifests are RETURNED not queued per 1.1 teeth, recorded in checklist. **Avoid:** "auto-queue incomplete" — return-rule forbids

---

### Verification Policy Terms

**Verify Policy Field** — Additive optional verify field on every subskill/cue, namespaced extension tolerating unknown keys, existing linters must not redden per 1.5. **Avoid:** "breaking verify field" — must tolerate unknown keys

**Required / Opt-in / Opt-out** — Router honors three policy classes per 1.5, three minimal golden traces one per class. **Avoid:** "behavioral grading" — format and deterministic checks only per 1.5

**Cassette SEED** — WP-2.3 cassette seed, J1 rule of travel build neither twice, 1.5 seed traces registered by name as WP-2.3 seeds. **Avoid:** "build twice" — J1 rule forbids

**Golden Trace** — Minimal stdlib-asserted trace proving verify policy class, three traces total per 1.5. **Avoid:** "networked trace" — zero network per Law 6

---

## Links
- Scaffold docs link this glossary per 1.3 acceptance
- Change-control checklist: scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md governs edits per 1.6
- Patch protocol: docs/PATCH_PROTOCOL.md pointer for agent policy files per 1.4
- Agent entrypoint cascade: AGENTS.md per 1.2

## Laws acknowledged
D1–D10 · six ratified laws D029 · FF-seal only · sequence as-written · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate · pure-additive per 1.3

## Research-only venue pointers
None — zero network/venue in WP-1 per Law 6
