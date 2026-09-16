# 🛠️ CAPABILITIES (`docs/CAPABILITIES.md`)
## What this repository can RUN — the executable half of the system
**Version:** 1.0 | **Origin:** Commander's order, 2026-09-13 — *"our task is to improve RADIATION from its current standing, elevate it."*
**Companion to:** `docs/SKILLS.md` (how the AI **thinks**) — this file is what the AI can **execute**.

---

## THE RULE

`SKILLS.md` says how to reason. This file says what can be **run**. An AI that does not
know a tool exists will do that work by hand, worse, and call it a session.

**Every script in `scripts/` appears below. Check 21 FAILS if one does not.** That guard
exists because this repository already shipped a capability doc that said "14 checks"
while the validator ran 25 — a count nobody could have got right by reading.

## COMMON PROPERTIES

- **Stdlib only** — no third-party packages, with one exception (`ingest_collection.py`
  needs PyMuPDF for PDF work).
- **Offline** — none calls the network, except `ingest_collection.py` and
  `ics_normalize.py --fetch`, both of which contact only a URL you supply explicitly.
- **Non-destructive** — no script writes to the repository except `validate.py`
  (its own report, git-ignored) and `ingest_collection.py` (only on `--repo`, which
  refuses to render inside the tree). `grade_exam.py` and `decay_compute.py` **propose**
  register rows; they never write them. A session appends.
- **Exit codes** — `1` means a real failure, not a warning. A nonzero exit from
  `validate.py` or `knowledge_regression.py` means **the session is not closable**.

---

## THE TOOLS

### 1. `validate.py` — structural validator · **run before claiming closure**
```
python3 scripts/validate.py
```
**Answers:** is the repository structurally sound? The GENERATED inventory below carries the live check/script counts — this prose no longer states numbers (4400).
Never truth — form. **Writes** `validation_report.json` (git-ignored).
**Read the exit code, not the vibe:** exit 1 = at least one ❌ FAIL → the session is
**not closable**; fix it or report the failure honestly. ⚠️ WARN entries are
ratification-pending items — **list them in your delivery; never "fix" canon to silence
one.** Check 16 is the meta-budget law (canon patches vs content sessions) and check 20.5
is the planner-theater guard: *plans are not progress.*

### 2. `knowledge_regression.py` — locked value assertions
```
python3 scripts/knowledge_regression.py
```
**Answers:** has a verified factual value drifted? Reads `tests/knowledge_assertions.json`
(live locked/pending counts are GENERATED in SYSTEM_STATE — never hand-stated here).
**A drifted verified value = exit 1 = cannot ship.**
Locking a value requires a Shield Stamp (I.3) or an in-session-verified `[D]` primary —
locking `[O]`/`[N]` matter is forbidden.

### 3. `plan_term.py` — the term planner
```
python3 scripts/plan_term.py --week 4
python3 scripts/plan_term.py --week 4 --ics local.ics     # + LMS feed delta
python3 scripts/plan_term.py --week 4 --anchor 2026-06-15  # week-1 Monday
python3 scripts/plan_term.py --self-check                  # integrity of the register
python3 scripts/plan_term.py --audit                       # audit the plan
```
**Answers:** what to study this week, ranked. Prints the term brief, the ranked load, and
— with `--ics` — *what moved* since the last run (added / moved / removed).
**Reads** `Brain/short_term/plan/TERM1_DEADLINES.json` — live counts are GENERATED below (4600).
**Gotchas:** without `--anchor` it plans in **weeks, not dates** — that is by design, not
a bug. `--ics` reads a **local file only**, and **drops `RRULE`** (recurring events are
not expanded). Nothing is written except an ICS snapshot beside the register.

### 4. `ingest_collection.py` — collection ingestion harness
```
python3 scripts/ingest_collection.py list    --url <drive-folder-url>
python3 scripts/ingest_collection.py fetch   --manifest <file.json> --dest <scratch-dir>
python3 scripts/ingest_collection.py extract --dir <scratch-dir>
python3 scripts/ingest_collection.py verify  --pdf <file.pdf> --page 55
```
**Answers:** how do I acquire and extract a source collection repeatably?
Enforces three lessons learned the hard way: **① binaries never touch the repository**
(working dir defaults to a temp path); **② a table extracted by text order alone is
UNVERIFIED** — `verify` renders the page, because naive extraction once produced a
complete, plausible, completely wrong code table; **③ the skip log is destination-scanned.**
**Needs** PyMuPDF for PDF work. Two runtime modes (fetch 165 s+, extract 10–157 s).

### 5. `export_anki.py` — drill set → Anki
```
python3 scripts/export_anki.py --set <set.json> [--out <file.tsv>]
```
**Answers:** get the forged drill set into Anki. Front = brief + options · back = key +
rationale + citations · tags = K-ID, context, difficulty, yield rank.

### 6. `grade_exam.py` — drill grader
```
python3 scripts/grade_exam.py --set <set.json> --answers <answers.json> [--tally]
```
**Answers:** what did the Commander score, and what did he miss?
Scores against the **stored key only — never memory.** Prints the report plus a
**proposed** `mastery_ledger` row and mistake-bank candidates. **Never writes registers
itself:** a session appends. Scores are study data and are **never citable as evidence.**

### 7. `decay_compute.py` — knowledge decay arithmetic
```
python3 scripts/decay_compute.py [--fixed]
```
**Answers:** which registry rows have passed their currency window?
Reads `docs/KNOWLEDGE_REGISTRY.md`, computes expiry from `Last verified` + `Freq`
(90 d / 1 yr), and prints **proposed** `DECAY_REGISTER` rows. `--fixed` pins "today" for
reproducible output. Arithmetic, not memory — and again, it proposes; it never appends.

---

### 8. `ics_normalize.py` — **the** iCalendar parser (RFC 5545 subset)
```
python3 scripts/ics_normalize.py --ics local.ics            # summary + delta
python3 scripts/ics_normalize.py --ics local.ics --md       # AI-readable calendar
python3 scripts/ics_normalize.py --ics local.ics --write    # durable .local artifacts
python3 scripts/ics_normalize.py --fetch                    # URL from $RADIATION_ICS_URL
python3 scripts/ics_normalize.py --public                 # COMMITTED scrubbed mirror
python3 scripts/ics_normalize.py --self-test                # the self-test suite
```
**Answers:** what is actually on the LMS calendar — *including every occurrence of a
recurring event.* This is the ONE parser; `plan_term.py --ics` delegates to it.
**Handles:** RRULE expansion (FREQ/INTERVAL/BYDAY/COUNT/UNTIL) · RDATE · EXDATE ·
**RECURRENCE-ID overrides** (a rescheduled occurrence replaces the original instead of
appearing beside it as a phantom) · `STATUS:CANCELLED` filtering · `TZID` resolved via
`zoneinfo` and displayed in `Asia/Manila` · RFC 5545 escape decoding · quoted parameter
values · line unfolding · `DTEND` durations.
**Diffing is series-aware:** "moved" means the *series* moved, and a single cancelled
date inside a series is reported as exactly that.
**The URL rule:** the feed URL is a **credential**. It is read from the environment
variable `RADIATION_ICS_URL` — never from a file, never committed, never printed.
**Scrubbing is unconditional:** every summary and location is stripped of instructor
names, room codes, sections, emails and URLs before it reaches any output.
`--write` emits `Brain/short_term/plan/TERM1_CALENDAR.local.{md,json}` (git-ignored).

### 9. `nota.py` — Core card tool (shape guard, never an admission authority)
```
python3 scripts/nota.py --new NOTA-001 --topic "..." --dossier <long_term path> --worksheets <ids>
python3 scripts/nota.py --check        # every card: <=300 words · LINEAGE · SHIELD · decay · index parity
python3 scripts/nota.py --self-test
```
**Answers:** can this Core card stand in the cleanest room? Cards are scaffolded to
the proc_nota-distillation shape; `--check` enforces the <=300-word limit, the
mandatory lineage block, the Shield stamp, the decay tag, and CORE_INDEX parity for
admitted cards. **It never admits** — the six-box pass is a session's act.

### 10. `module_scaffold.py` — born-valid study modules (check-18 mirror)
```
python3 scripts/module_scaffold.py --new --level 3 --course AR153P --topic "..." --kid K-MOD-XXX
python3 scripts/module_scaffold.py --list     # inventory + parity + per-module health
python3 scripts/module_scaffold.py --self-test
```
**Answers:** does this module pass validator check 18 from birth? The scaffold
carries every required section/quotas for its level and is validated by a mirrored
rule-set before it is written. `--list` reports index parity honestly, including
"NO INDEX FILE" (check 18 counts a missing index as a mismatch).

### 11. `deadline_feed.py` — the Deadline Engine (feed → term register)
```
python3 scripts/deadline_feed.py            # dry-run: what WOULD merge
python3 scripts/deadline_feed.py --write    # merge into TERM1_DEADLINES.json (idempotent)
python3 scripts/deadline_feed.py --self-test
```
**Answers:** what does the committed LMS feed actually say, and what does it change?
Conservative attribution: explicit course code → fuzzy match to EXISTING register
items (their dates anchor week-based records) → citable content keywords →
UNATTRIBUTED for the Commander (with sibling hints), never guessed. Meeting series
(3+ identical titles) are skipped — meetings live in SCHEDULE.md. Pre-term items
counted and skipped. Re-runs are no-ops (feed_id hashing). First run (2026-09-13,
`cb5ec95` feed): 20 meeting instances filtered · 8 stale skipped · 3 Coursera
records anchored to real dates · 16 added · 11 UNATTRIBUTED pending Commander.

### 12. `status.py` — the Swarm Dashboard (one screen, read-only)
```
python3 scripts/status.py
```
**Answers:** where does the machine stand RIGHT NOW — validator verdict (+ the FAIL
lines), calendar feed freshness + mirror age, the next dated deadlines (TODAY
marked), the `feed_pending` attribution count, and the shrine heartbeat's currency
against the ledger. Runs the validator in a subprocess; modifies nothing. The first
command any fresh AI (or the Commander) runs instead of asking "what's next."
**Also in 3300:** `cue/standing-directives.json` — the typed directive registry
(id/class/authority/scope/rule/enforcement/provenance per directive; 11 standing
directives incl. the autonomy ladder and the seven stop-lines). **Check 25** fails
the tree if the registry corrupts, loses its enforcement mapping, or references
mechanisms that don't exist — the research memo's "prose never enforces" made
machine-checkable.

### 13. `verify_apply.py` — the post-apply auditor (read-only)
```
python3 scripts/verify_apply.py            # report, always exit 0
python3 scripts/verify_apply.py --strict   # exit 1 on FAIL-class findings
python3 scripts/verify_apply.py --self-test
```
**Answers the question the 3200 incident taught us to ask:** "did the last apply
actually land?" Version drift (README vs CHANGELOG), validator verdict, unsanctioned
vehicles still in Brain/, committed transport (runners/PATCH_NOTES), shrine-lag
(AI_RULES II.9), pending ratifications — one screen. CI runs it on every push,
its result lands in the job summary. Enforcement mode is GENERATED below (4600):
the workflow file is the single source of gate semantics — prose no longer states it.

### 14. `cap_verify.py` — CAP record verifier (4800 Attest) · verification-only
```
python3 scripts/cap_verify.py RECORD.json [--repo ROOT]   # exit 0 iff 0 findings
python3 scripts/cap_verify.py --self-test                 # negative vectors, CI (check 35)
```
Verifies `radiation.cap/0.1` capability-activation records: schema EXECUTED with the
same executor as every contract schema, `model_identity` must stay null, seal digest
recomputed (hand-edits break the seal), verifier names checked against RADIATION's own
CLI registry, honest `blocked` accepted, "verified" only with green checks + live
observation, and the C-4 redaction classes (docs/CAP_RECORD_POLICY.md) executed over
every string value. **BOUNDARY: cap_verify VERIFIES records; since 5000 authority
flows only through the ratified control plane (II.11).** The typed resolver, capability allowlist, approval boundary and isolated
executor remain STAGED (Product-2). Provenance: external PoC (`6/6` acceptance vectors,
`5/5` discrimination) before a single line entered the tree.

### 15. `cap_probe.py` — read-only capability probe (4900 Probe) · observation-only
```
python3 scripts/cap_probe.py [--repo ROOT]               # attestation
python3 scripts/cap_probe.py digest RELATIVE_PATH        # contained digest
python3 scripts/cap_probe.py --profile FILE [--repo ROOT]  # declared vs observed
python3 scripts/cap_probe.py --self-test                 # negative vectors (check 36)
```
Exactly two tools, an **empty effect catalog** (no mutation surface exists to misuse),
allowlisted commands only, symlink-safe path containment. Executes host posture
profiles (`radiation.host/0.1`, `scaffolding/hosts/arena_agent_mode.json`) — a profile
DECLARES posture; the probe OBSERVES reality; declaration is never treated as
observation (A2A lesson). Unavailability is first-class: `not_mounted` and
`not_a_git_worktree` are results, not errors. **BOUNDARY: cap_probe OBSERVES; since
5000 authority flows only through the ratified control plane (II.11).**

### 16. `radiation_core.control_plane` — the ratified control plane (5000, II.11)
```
python3 -m radiation_core.control_plane resolve --effect read --source session_initiative
python3 -m radiation_core.control_plane decide  --task TID --effect workspace_draft --source commander_order
python3 -m radiation_core.control_plane execute --task TID --manifest M.json
python3 -m radiation_core.control_plane verify                       # receipts chain
python3 -m radiation_core.control_plane --self-test                  # 38 vectors (check 37)
```
Operated, cooperative tooling (not a runtime): two-key resolver, schema-executed
allowlist, structural approval boundary, drafts-bounded executor with strict task
grammar, pinned base, and content-bound SINGLE-USE approvals (substitution/replay
fail closed); receipts are tamper-EVIDENT, not immutable. Limits are law:
`docs/THREAT_MODEL.md`. Full detail: `docs/CONTROL_PLANE.md`.

### 17. Provider activation layer (5200) · prompt-side protocol
`AGENTS.md` (root) routes explicitly-known hosts to `agents/<Provider>/` (five exact
folders; `Arena_AI` is the primary testbed profile); unknown hosts get the generic CAP
path and declare uncertainty. `RADIATION PASS` = `agents/_common/radiation_pass.py` —
deterministic, read-only, zero-write: routing · observation · II.11 boundary ·
profile-or-absence · proofs · unknowns. Check 38 tests routing, coherence, claim-free
output. THE LIMIT: repository text cannot force a hosted product to discover, load,
or obey any of this — convention, not proof.

## WHAT IS NOT HERE YET

Stated plainly so a session does not assume capability it lacks:

- **The scheduled fetch is BUILT but UNARMED.** `.github/workflows/ical_fetch.yml` runs
  daily (01:30 Manila): it pulls the feed from the `RADIATION_ICS_URL` secret and commits
  the scrubbed mirror `Brain/courses/CALENDAR.md` when the feed changed. It stays inert
  until the secret exists — and the secret comes ONLY after the old URL is rotated
  (the `4a98e59` exposure). Validator check 22 guards the mirror: URL inside it = FAIL,
  older than 7 days = WARN.
- **No router UI for the calendar** — CALENDAR.md is regenerated by CI and readable;
  a fresher query interface (per-week views, filters) awaits a session that needs one.
- **Core contents: see the GENERATED machine facts (SYSTEM_STATE).** Admission needs
  Shield-stamped claims run through the six-box pass — a session act, never a script —
  and every admitted card is front-matter-gated by check 29 / `nota.py --check` (4400).
- **CI coverage is GENERATED** (the inventory's *In CI* column below). Scripts stay
  session-invoked by hand when they need arguments a runner cannot guess — that is
  deliberate and now machine-documented instead of hand-asserted.

<!-- GENERATED:capability-inventory:START -->

### INVENTORY (GENERATED — reality, not memory; hand edits here are a CI failure)

| Script | Purpose | Writes | Network | In CI |
|---|---|---|---|---|
| `agent_contract_check.py` | deterministic compile check for agent contracts catalog (Dim-1/G4) | no | no | no |
| `brain_retrieve.py` | Brain Retrieval Lattice (G5) deterministic selector law | no | no | no |
| `cap_probe.py` | cap_probe — read-only capability probe with declarative host profiles. | no | no | no |
| `cap_verify.py` | cap_verify — structural + semantic verifier for CAP capability-activation records. | no | no | no |
| `catalog_integrity_check.py` | Cross-Catalog Integrity Checker (P-20 spine closer / G4 closure) | no | no | no |
| `contract_tests.py` | 5300 negative fixtures — declared course-corpus (E1) and replica (E2) contracts. | no | no | no |
| `cue_resolver.py` | CUE Resolver / Linter — Candidate B opening P-11-A | no | no | yes |
| `deadline_feed.py` | the Deadline Engine (patch 3100). | yes | no | no |
| `decay_compute.py` | P-03: compute decay expiries FROM registry rows (arithmetic, not memory). | no | no | no |
| `deck_rules_check.py` | Deck Rules + Outline Schema lint (S-2-PPTX-A stage 1) | no | no | no |
| `docs_index_check.py` | deterministic stdlib checker, house finding style (G6) | no | no | no |
| `export_anki.py` | P-05 Anki exporter (stdlib port of TAMAKEE export-anki.js). | yes | no | no |
| `grade_exam.py` | P-05 drill grader (stdlib port of TAMAKEE grade-exam.js). | no | no | no |
| `ics_normalize.py` | the ONE iCalendar parser for RADIATION (RFC 5545 subset). | yes | yes | yes |
| `ingest_collection.py` | RADIATION collection ingestion harness (P-10 Phase 2). | yes | yes | no |
| `knowledge_regression.py` | RADIATION knowledge-regression suite — P-01 §3. | no | no | yes |
| `model_research_check.py` | model_research_check — ONE entry point for the Candidate C catalog contract. | yes | no | yes |
| `module_scaffold.py` | born-valid study modules (patch 3000). | yes | no | yes |
| `nota.py` | the Core card tool (patch 3000; canonical contract per 4400). | yes | no | yes |
| `plan_term.py` | RADIATION term planner (P-10 Phase 1-3). | no | no | no |
| `push_preflight_check.py` | Motor Preflight Tool (P-12 LAW-5 + LAW-6 WHITESPACE) | no | no | no |
| `release_truth_check.py` | Release Truth Gate checker (5824 FIX) | no | no | yes |
| `render_docs.py` | generated-facts pipeline (patch 4400; auditor plan item 5). | yes | yes | yes |
| `scaffold_check.py` | deterministic compile check for scaffolding contract spine (Dim-3/G4) | no | no | no |
| `session_state_check.py` | Session Capability State checker (S-2-ENV) | no | no | no |
| `skill_check.py` | deterministic compile check for skill catalog spine (Dim-7/G4) | no | no | no |
| `status.py` | the Swarm Dashboard (patch 3300, SD-3300-02). | no | no | yes |
| `subskill_check.py` | deterministic compile check for subskill catalog + hook protocol (Dim-8/G4) | no | no | no |
| `tool_registry_check.py` | tool_registry_check — ONE entry point for the tool-registry contract (5600). | yes | no | yes |
| `validate.py` | RADIATION structural validator — P-01 Machine Enforcement Layer. | yes | yes | yes |
| `verify_apply.py` | the post-apply auditor (patch 3400, roadmap Enforcement Sweep). | no | no | yes |
<!-- GENERATED:capability-inventory:END -->

## §20 — Gate-repair layer (5500, 5400 gate review)

| Capability | Mechanism | Enforcement |
|---|---|---|
| Complete corpus declaration | 8 digest-bound assets incl. restored sources + `data_feed` (check 2.5) | NO path-only exceptions; A2 scan-exemption documented; restoration veto-able by Commander |
| Replica tranche ratification | `ratification` field in REPLICA_MANIFEST (check 11) | 12 pairs = complete tranche; narrowing = explicit Commander order |
| Transactional drafts | `execute_draft` preflight-then-write (check 37) | mixed-validity manifest writes NOTHING; regression-proven |
| Executed schemas | relay `_validate_against`: oneOf · maxItems · bool≠integer | the `task_id` exploit class fails closed; plan selection numeric |
| Per-provider profile truth | radiation_pass (check 38) | Arena profile binds ONLY to Arena_AI; table-driven fixtures ×5 + ambiguous |
| CI truth | workflow `shell: bash` (-eo pipefail) + failure diagnostics step | `tee` cannot mask a red strict report; public log-tail on failure |
| Test harness + tool registry | `tests/` (25 tests) + `tools/TOOL_REGISTRY.json` (check 39) | zero-test discovery = explicit failure; registry schema-EXECUTED + reference/test-bound, coverage-complete |

## §19 — Survey layer (5400, architect brief E6)

| Capability | Mechanism | Discipline |
|---|---|---|
| Provider capability/routing research | `agents/<P>/CAPABILITY_PROFILE.md` + `SOURCES.md` ×5, `agents/ROUTING_MATRIX.md`, `agents/RESEARCH_METHOD.md` (check 38, non-boot) | every volatile claim dated + tier-labeled; 90-day review triggers; conflicts recorded (Sonnet-5), gaps declared (Arena privacy/status); Arena model identity unknowable; research notes are handoffs, not authority |

## §18 — Sanction layer (5300, architect brief E1–E5)

| Capability | Mechanism | Enforcement |
|---|---|---|
| Declared course-corpus admission | `Brain/courses/COURSE_CORPUS_MANIFEST.json` + `schemas/course_corpus_manifest.schema.json` + `docs/COURSE_CORPUS_POLICY.md` (check 2.5) | hash-bound: undeclared vehicle / digest drift / missing derivative / path escape FAIL; identifier rules unchanged; a checksum is not a permission grant |
| Sanctioned replica contract | `scaffolding/neurons/REPLICA_MANIFEST.json` + `schemas/replica_manifest.schema.json` (check 11) | 12 hash-bound active↔archive pairs; drift FAILs; every undeclared duplicate FAILs; archive replicas never boot context |
| Semantic receipt verification | `radiation_core/control_plane.py::verify_chain` (check 37) | v2 executions bind decision+approval BY DIGEST (task/status/effect/tool, manifest, bounds, draft-root); approval single-use; forged/substituted/replayed FAIL closed |
| Task-ID grammar in schemas | `schemas/control_receipt.schema.json` + `control_decision.schema.json` | strict `TID-…` pattern with documented genesis exception (`RADIATION-5000`) |
| Pass single-root truth | `agents/_common/radiation_pass.py` (check 38) | cross-root `--repo` → explicit `protocol_target_mismatch`, no profile, no repo-relative proofs, no target probe |
| Negative fixtures | `scripts/contract_tests.py` | 11/11 vectors over the E1/E2 contracts on disposable temp trees (zero-write) |

<!-- GENERATED:planner-register:START -->
**Term register (GENERATED from `scripts/plan_term.py --self-check` — the tool is the single source; hand edits here are a CI failure):** 6 courses · 26 items · 3 deadline-blind course(s)
<!-- GENERATED:planner-register:END -->

<!-- GENERATED:ci-enforcement:START -->
**CI enforcement (GENERATED from `.github/workflows/validate.yml` — hand edits here are a CI failure):** apply-report: BLOCKING (continue-on-error removed, 4500) · structural validator: BLOCKING · relay self-test+active: yes · generated-docs check + phrase lint: yes · dashboard date self-test: yes
<!-- GENERATED:ci-enforcement:END -->

## §21 — Closure contracts (5600)
- **Tool registry** (`tools/TOOL_REGISTRY.json`, schema /2, 22 tools): entry, IO schema refs, effects, mutation_scope (`none|temporary|ignored_local|evidence_draft|tracked_derived|canonical_none`), approval (`none|commander_order_assertion|commander_motor_act`), data classes, network, credentials, idempotency, timeout, cap mapping, test command, observability. ONE checker entry point: `scripts/tool_registry_check.py` — schema-EXECUTED plus code-level contradiction/containment/coverage/reference-existence/test-binding/realpath rules, 15-vector negative self-test, executed by validate check 39. Null-IO entries are metadata-only (not schema-bound); binding rules apply regardless. A registry entry grants nothing (no MCP, no endpoint, no runtime).
- **Schema honesty** (check 40): every shipped schema uses only keywords the ONE executor executes (plus documented annotations; `format` is annotation-only per 2020-12); the executor applies constraints by INSTANCE type — typeless subschemas were vacuous before 5600 and are law now.
- **Evaluation gate (Candidate C — research design only, GATED)**: no "strong/strongest" wording becomes a routing decision rule without a named RADIATION local evaluation and a declared confidence level. The future harness must capture exact model id, provider, host/surface, region, effort, enabled-tool allowlist, prompt/contract/fixture revisions + digests, date, harness version, evaluator/rubric, metrics, retries, limitations — and never upload private corpus text or credentials to obtain a result.

## §22 — Model-research catalog (5700, Candidate C design)
- **Layer** (`catalogs/model_research/`, NON-BOOT — check 41 runs a non-boot scan over the BOOT_SEQUENCE-derived graph incl. docs/.readme + transitive passive specs): **14 records** (5800 Almanac: official values captured 2026-09-15); one record per EXACT model × surface × region; schema `radiation.model_research_record/0.3` (central `schemas/`, executed; typed evidence objects, exact/candidate identifier split, filename binding); typed source register (`catalogs/model_research/sources/REGISTER.json`, executed); checker `scripts/model_research_check.py` (uniqueness, real-calendar dates + 90-day review window, confirmed⇒verified id + register-bound official declaration at the record's retrieval date, non-boot scan, register discipline; 24-vector self-test). Records grant nothing.
- **Evaluation gate (unchanged, §21):** "strong/strongest" becomes a decision rule only via a named RADIATION local evaluation with declared confidence — the harness DESIGN (`catalogs/model_research/evals/HARNESS_DESIGN.md`) specifies dimensions, capture blocks, and redaction law; implementation is its own gated order.
- **Deployment matrix:** structure only (`catalogs/model_research/decision_matrices/DEPLOYMENT_MATRIX_DESIGN.md`); one deployment per order; questions stay questions.
