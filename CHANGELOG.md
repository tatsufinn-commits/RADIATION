# 📜 CHANGELOG (`CHANGELOG.md`)
## Updated at every Commander-applied Patch (append-only, II.2)
Format: version · date · patch name · summary. Newest at top after founding entries.

---

## v3.2.0 — 2026-09-14 — Probe (🟠 · research Phase C-2 + C-4 rider)
- **`scripts/cap_probe.py`** — the two-tool read-only probe, in-tree: attestation + contained digest; allowlisted commands only; symlink-safe containment; **empty effect catalog** (no mutation surface exists to misuse); `not_mounted` / `not_a_git_worktree` are first-class results. Self-test 5/5 vectors; check 36 in CI.
- **Host posture profiles:** `schemas/host_profile.schema.json` + `scaffolding/hosts/arena_agent_mode.json` (`radiation.host/0.1`) — DECLARATIVE only: no tool claims (host surfaces are session-contingent), `model_identity` structurally null, Commander-only effects can never be posture. `--profile` prints declared-vs-observed; declaration is never treated as observation (A2A lesson).
- **C-4 redaction policy executed:** `docs/CAP_RECORD_POLICY.md` states it; `cap_verify` enforces the mechanical classes (GitHub/cloud keys, private-key blocks, bearer/URL tokens, embedded passwords) over every record string; vector added to its self-test.
- **Erratum:** 4800's ledger/shrine rows and version line were dated 2026-09-15 — the work landed 2026-09-14 ~16:30 +08:00. Ledger rows stand untouched (append-only); this heading corrects the dating convention.

## v3.1.0 — 2026-09-14 — Attest (date corrected by 4900 erratum) (🟠 · GitHub-research Phase C-1, verification-only)
- **CAP records are tree law:** `schemas/cap_record.schema.json` + `scripts/cap_verify.py` — schema EXECUTED with the same recursive executor as every contract (one implementation), `model_identity` structurally null, seal digest recomputed (hand-edits break it), verifier names checked against RADIATION's own CLI registry, honest `blocked` accepted as first-class, "verified" only with green checks + live observation. Check 35 runs the negative-vector self-test in CI (5/5 unmounted · 4/4 mounted roots).
- **Boundary printed everywhere:** cap_verify VERIFIES records; the typed resolver, capability allowlist, approval boundary and isolated executor remain STAGED (Product-2). External proof-of-concept admitted first (6/6 acceptance vectors · 5/5 discrimination) per the research memo's evidence gate.
- **Payload-completeness probe (3400-audit rider):** APPLY now runs EVERY shipped tool's self-test verb verbosely — relay 12-vector · relay semantic · status · nota · cap_verify · render-truth · term-truth — output shown, exit enforced (retired the last silent "want 11/11" straggler).
- **opinions.md restored** from `caa754b` (the 4200 push had markdown-mangled it: over-escaped underscores, broken indentation).
- TID-2026-09-14-l bundle born-rendered (canonical bundle #5) — ships the first dogfooded CAP record (honest `limited`: two-key policy grants, CAP surface exposes no draft tool).

## v3.0.0 — 2026-09-14 — Sealwright (🟠 · the 4600 recheck remediated)
- **The bundle is the record; neurons are its shadow:** `render_neuron()` renders each Markdown neuron FROM the canonical bundle; check 27 now enforces file==render. Hand-edited neurons are structurally meaningless (vector 12). h/i/j migrated — narrative lives in bundle `operator_notes`. Model wording ("canonical bundle = machine-checkable audit record; Markdown = human-facing projection") adopted into the boot docs.
- **A failed seal finally fails:** APPLY's auto-commit is REQUIRED — commit failure exits nonzero in both runners (recheck item 2; silent-continue defect owned).
- **The planner block lost its own opinions:** the GENERATED term-register block is parsed from `plan_term.py --self-check`'s own report — the generator owns zero counting logic (the 4600 block's 3-courses/2-blind drift is impossible now).
- **Identity adopted verbatim:** "a validated LLM workflow scaffold with durable records and human/LLM-operated protocols" — in the front door (docs/.readme), SYSTEM_STATE, and the neurons README.
- Relay self-test 11→12 vectors; summary line restored (a 4600 slice had silently eaten it — owned). Legacy-count precision: 7 traces; f+g remain active legacy. MINOR-epoch bump → v3.0.0.

## v2.9.0 — 2026-09-14 — Binding (🟠 · the 4500 recheck remediated)
- **Relay FULLY bound** (recheck's word accepted as spec): schemas executed RECURSIVELY (nested required/enum/pattern/minLength/minimum/items) · cross-object identity total — command stem↔internal id, outcome stem↔command_id AND task_id, plan↔task, base revisions agree everywhere · a foreign plan file is a HARD finding, never a silent skip · event sequences contiguous 1..N · timestamps must carry a timezone offset · causal refs must name known commands · verification.passed must attest a succeeded, digest-verified outcome. Self-test: 6→11 vectors — the recheck's five demonstrated mutations are permanent regressions (all FAIL now).
- **Generated truth to the last line:** term-register counts and CI gate semantics are GENERATED blocks (derived from TERM1_DEADLINES.json and validate.yml); the lint's denylist expanded (21 items · NON-BLOCKING · never-be-blocked · checks-1b); "checks 1b" corrected to 1.5. The "NON-BLOCKING prose beside a BLOCKING workflow" contradiction is structurally impossible now.
- **The seal moves into code:** APPLY auto-commits the sealed tree after its gates pass (idempotent on already-sealed trees; `--no-commit` opts out). PUSH remains the Commander's motor act — unchanged, unconditional, his alone.
- **Honest boundary kept:** success_predicate strings remain declared intent — digests and linkage are enforced; semantic predicate evaluation stays staged with Product-2.
- Version bump: MINOR → v2.9.0.

## v2.8.0 — 2026-09-14 — Last Mile (🟠 · the 4400 recheck remediated)
- **Relay hardened to the recheck's spec:** schemas EXECUTED (required/const/enum/pattern/type) · outcome identity bound to file stem AND internal id (the CMD-MISMATCH mutation now FAILS) · projection.json parsed and required to equal the event-derived state (corrupted projections FAIL) · causation refs required on all command events with coverage checks · base-revision agreement · unique event ids + RFC-3339 monotonic timestamps · self-test 6/6 incl. the recheck's two mutations as permanent vectors.
- **Prose cannot lie:** render_docs --check now LINTS guarded docs for hand-stated live facts outside generated markers (45 K-IDs / 33 checks / 4 locked / "No admitted Core cards" / "CI runs 2 of" / 13 scripts — all nine recheck hits eradicated at source).
- **Control hardened:** DEGRADED mode is loud and refused in --strict (status + verify_apply) · apply-report job is BLOCKING in CI (a red seal stops the merge, not a summary note) · status.py carries a 3-vector date-semantics self-test in CI.
- **II.10.6 enacted:** the legacy exemption list is CLOSED at seven traces — law, not convention.
- Version bump: MINOR → v2.8.0.

## v2.7.0 — 2026-09-14 — Reconciliation (🟠 · due-diligence remediation, Milestones A–C)
- **Milestone A — the seal:** APPLY runners cross-remove (both platforms), check 3 flags committed runners, APPLY prints the exact seal commands. Main goes green on apply + commit + push.
- **F-03 dead:** nota.py aligned to the CANONICAL contract (09-nota/CARD_###, core-card/v1 front matter, exact index parity) — CI now validates the real admitted cards (CARD_001/CARD_002 migrated, content untouched). New check 29.
- **F-04 dead:** check 27 rewritten onto radiation_core.relay — task bundles (envelope/plan/commands/outcomes/events) with digest-verified evidence, state-machine transitions, and Markdown projection fidelity; 3/3 negative vectors; pre-runtime TIDs marked legacy_trace (never fabricated).
- **F-06 dead:** scripts/render_docs.py generates machine facts from reality (checks, locks, K-IDs, cards, subskills incl. fetch/overule, script inventory, CI coverage); render --check fails CI on drift. The false "26 checks"/"4 passives + 2 actives"/"45 K-IDs" class cannot return silently.
- **F-07/F-08 dead:** validator exposes a structured JSON API (--json, importable run_all); status/verify_apply consume it; activity dates read first-table-column only (no more 2027-decay false alerts); grade_exam takes --attempted-at.
- **F-05 honesty:** passives labeled protocol checks (in-context, advisory unless machine-backed) in .readme, the 4 passive specs, and the generated roster; mode-inference contradiction resolved per the ratified BOOT ASK law (README aligned).
- **Milestone D (policy gateway / executor runtime) STAGED** — requires the Commander's explicit Product-2 scope ratification (plan §5.1). Version bump: MINOR → v2.7.0.

## v2.6.0 — 2026-09-14 — Compression (🟠 · Commander-ordered tier-1 update)
- **II.10 LEDGER COMPRESSION enacted** (direct order; staged P-09 stays frozen & listed): boot ≥95 % of cap → next patch reclaims · history archives whole, never deletes · boot docs carry state, not narrative · relay fades to one active TID cycle.
- **SYSTEM_STATE truth-up:** the per-version recital moved to CHANGELOG (this file) — 10.5 KB → 5.0 KB; stale claims corrected (33 checks · 11/0 · Core = 2 cards · 13 directives).
- **Architect-voice purge** (Commander order): editorial remarks and invented quotes removed from MODES, TOOLBOX, WAYFINDING, overule, .readme, patch-ledger lessons; records kept, prose gone.
- **TID fade:** cycles a–e → `scaffolding/neurons/_archive/` (f active); check 27 judges the active set. Check 15 now reports II.10 compression state.
- Version bump: MINOR → v2.6.0.

## v2.5.0 — 2026-09-13 — Expansion (🟠 · the Commander's three proposals, shipped)
- **`docs/OPEN_SOURCES.md` — HIS catalog, enshrined** (50 categories, access-labeled PUBLIC/API/KEY/AUTH/PAID/HUMAN/TOOL, provenance header): the retrieval bank any AI can pull to help itself. Pointers ride [O]; promote to [I] on use (TOOLBOX rules).
- **`@Fetch` (subskills/active/fetch.md, UNIVERSAL ⚙️×6)** — the retrieval strategist: Brain → registers → the bank → TOOLBOX [I] → online-via-scout (gates unchanged: scout stays the gated executor; new collections still ask). Cross-referencing doctrine built in: name the independent channels BEFORE fetching.
- **`@Overule` (subskills/active/overule.md, COMMANDER-TRIGGERED ⚙️×6\*)** — the deadline gear: overrules AI-FLAGGED rules only (WARN-and-proceed, ceremony compression, detail-fork decide+declare, self-budgets, THE BATCH-ASK). NEVER: the seven stop-lines, constitution, privacy checks, the validator as evidence. Every use logs a make-good debt. Registry: **SD-GOV-013** (13 directives).
- **Subskills as part of mode autonomy — codified** (MODES matrix legend): ⚙️ subskills invoke 🟢 silent (read-only) · 🟡 declared-in-Scan · 🔴 gated — the ladder stays the governor.
- **Canon restoration + pinning:** the universal `selfdirectives ⚙️×6` matrix row had been silently lost to merge churn — RESTORED, and **check 28** (33rd check, FAIL-class) now pins all matrix rows so canon cannot evaporate again.
- **4000 content remediated:** CARD_002 + ANNOT/TRI + K-LAW-009/014 corrections + SRC-016..019 + ⚑ reviewer note were never applied (extraction skip) — restored; regression locks pass again (11/0).
- Version bump: MINOR → v2.5.0.

## v2.4.2 — 2026-09-13 — Recalibration (🟡 · Commander correction, in person)
- **Task selection corrected at the source:** "our goal is building and elevating the repository." Doctrine §2 now reads: open-ended proceeds = CAPABILITY work first; contamination second; content debts ONLY on explicit content orders or declared idle windows. Confirmed-cue row + ledger record + inference-log CORRECTED verdict filed (II.5).
- **3500 payload REMEDIATED:** git forensics showed the Cue-Renewal patch was never extracted on the Commander's machine — its unique files (cue lessons incl. the 7 BUILD CUES, 4 lexicon entries, inference rows, TICKET_001) existed nowhere in the repo. Restored byte-identical from the 3500 zip, correction row appended. Method lesson: extraction gaps are invisible to APPLY gates that never run — the CI apply-report is the control that matches his workflow.
- **Regression locks:** KR-LAW-014 (RA 10587 designation must survive in card + registry) and KR-LAW-009S (REPEALED-GENERATION marker) — 11 locked · 0 failed. Verified knowledge is now machine-guarded.
- **APPLY runners self-remove** at end of run (the 3500-candidate, finally built).
- Version bump: PATCH → v2.4.2.

## v2.4.1 — 2026-09-13 — Stale Generation (🟢 CONTENT — the second Core card)
- **CARD_002 admitted** (`09-nota/CARD_002_environmental-planning-act.md`): **RA 10587 (Environmental Planning Act of 2013) repeals PD 1308** (§42, verified verbatim ×3: LawPhil fetched · Official Gazette · Scribd text; + UP CIDS 2025 [R]) — and the trap was in OUR OWN house: `PLANNING_reviewer` line 55 and registry K-LAW-009 both cited PD 1308 as current. Corrected: K-LAW-009 → REPEALED-GENERATION (superseded by K-LAW-014 NEW), reviewer ⚑ EXAM NOTE appended, CONFLICT_REGISTER row 3 resolved per the P-07 curriculum-primacy pattern (answer-of-record unchanged; know the current law).
- **Standing-orders sweep documented** (doctrine §2): law-gaps debt = registry-complete (K-LAW-007/009 mirror-verified 2026-09-13; 008 fetch owed; collection PDFs = Commander-side); MB-discipline verified for this session's fetches; OCR/Bentley remain holdings-blocked (OPEN, owned).
- SRC-016..019 registered. Version bump: PATCH → v2.4.1.

## v2.4.0 — 2026-09-13 — Reflex Arc (🟢 · SD-3600-03)
- **check 27 — neuron relay chain integrity** (the 32nd check, FAIL-class): every TID must be a complete chain (intake → reasoning → orders); orphan stages and missing templates FAIL with a REMEDY. The relay that made tasks inspectable now makes them *enforceable* — the memo's "forbidden edges" get their deterministic guard.
- **`07-inspect/TABLETOP_injection_2026-09-13.md`** — the indirect-injection defense rehearsed layer by layer (AgentDojo-style scenario through scout → ingest → Brain → context → capability). Verdict: holds at every layer because no ingested text can reach a 🔴 capability — with the honest gap named: all layers but the validator are procedural (no sandbox runtime). **Live drill PROPOSED** — it fetches external content, which is ask-gated; awaiting the Commander.
- **Phase-0 CLOSED** (SD-3600-01, SD-3700-01): four real chains (TID-a…d) through the relay; behavior verdict filed — register-first caught a real conflict re-opening (TID-c); the triad scanned clean ×4; orientation from relay records measurably faster. The relay stays, for 🟡+ work.
- **Honesty note — the negative test earned its keep:** check 27's first draft matched NOTHING (0 chains) because both it and status.py's pipeline line assumed `TID_` naming while the shipped records use `TID-` — meaning the live pipeline line had been blind since 3600 (always "nothing in flight"). Both now follow the files as shipped; positive+negative tests green; pipeline truth restored. Also this session: K-STD-001 (NSCP 2015) checked BEFORE acting — the audit-era "unregistered" gap was already fixed; Brain-first prevented a duplicate row.
- SD-3600-03 CLOSED. Version bump: MINOR → v2.4.0.

## v2.3.1 — 2026-09-13 — First Light: CARD_001 (🟢 CONTENT — the first Core card)
- **`09-nota/CARD_001_bp344-accessibility.md`** — the first card ever admitted to the Core: BP 344's permit gate, conveyance duties, IRR delegation principle, penalties, dates — 3 independent channels verified verbatim (SRC-013 LawPhil · SRC-014 Legaldex carrying the Official Gazette imprint Vol. 80 No. 8 p.1103 · SRC-015 UN ESCAP/ILO reproduction), Shield-Stamped, decay 2027-09-13, full lineage block.
- **The exam trap, defused and locked:** "1:12 vs 1:20" is a generation trap; the amended IRR of record = 1:20 (KR-LAW-005). The register's append-only memory outran the session's first instinct to re-open the resolved row — corroborated instead (SRC-015 is an original-generation copy).
- **`02-analyze` exercised for the first time** (dormancy cured): claims × sources × ALE-yield matrix. `05-annotate` + `06-triangulate` both did real work. SD-3600-02 CLOSED; SD-3700-01 partial (1/5 relay-proof tasks).
- Version bump: PATCH → v2.3.1.

## v2.3.0 — 2026-09-13 — The Curation Gate (🟠, Commander-ordered build)
- **`proc_self-directive.md` → v1.1** — the Commander-ordered research (10 sources) applied to the self-directive scaffold: **default-deny** (an unclassifiable action = 🔴) + the classifier triad (irreversible? outside scope? destructive?) · **THE CURATION GATE** (no self-authored procedure self-promotes; promotion = Commander ratification OR validator verification + second-session use — SkillsBench 2026: curated +16.2pp vs self-generated −1.3pp) · **calibration honesty on T2** (self-preference/judge-overconfidence are measured; independent re-derivation = different path, judgment closes at T3) · **reflection triggers** (2 REPLANs / 50% budget / validator FAIL / scope growth force a reconsideration note) · **ROLLED-BACK closure** (revert + BUILD CUE + replay fixture before re-proposal) · **draw quota** (idle work inherits the session's tier ceiling; ≤2 self-directed tasks/session).
- **`cue/standing-directives.json` +SD-GOV-012** "No self-authored procedure self-promotes" (registry: 12; enforcement → check 3.5 + the gate section).
- **The compression ladder, named** (doctrine §2): episode → cue (≥1 closed episode) → registry row (≥2 sessions, same verdict); verified directives decay slowest — the adaptive promotion the 2026 surveys call missing.
- `.gitignore` seals the last two resurrecting vehicles (SCHEDULE.csv, 0_CALLENDER/readme.txt); APPLY re-runs the untrack — **it seals on the Commander's next commit**.
- Version bump: MINOR → v2.3.0.

## v2.2.0 — 2026-09-13 — Autopilot Pipeline & Wayfinding (🟡)
- **The neuron relay is LIVE** (`scaffolding/neurons/`) — the Commander's proposal, hardened by his 15-source research memo into a closed-loop responsibility model: sensory (intake + dedup) → interneurons (context + plan with `base:` HEAD-SHA, success predicates, tier by ladder) → motor (orders + evidence; push is the Commander's motor act). Five forbidden edges; every TID ends CLOSED / REPLAN / BLOCKED / ESCALATED. First live chain ships inside this patch (TID-2026-09-13-a, all stages CLOSED).
- **`scaffolding/core/proc_self-directive.md` NEW** — the Commander-ordered scaffold for @selfdirectives (none existed): trigger check → stop-line scan → grade → typed record BEFORE execution → verify-by-tier → close with terminal state → file (II.9). Registered in core INDEX (check 3.5).
- **`docs/WAYFINDING.md` NEW** — the lost-AI page: the map, the routing tree, self-location commands, the recovery ladder. **`docs/TOOLBOX.md` NEW** — the open-source rescue kit ([O]→[I] promotion rule; first row: OCR for the 2,038-page debt).
- **The resurrection loop DIES here:** 3400-F3's root cause was tracked vehicle files; this patch's APPLY runs `git rm --cached` on them and `.gitignore` now covers patch transport (APPLY.sh / APPLY.ps1 / PATCH_NOTES.md).
- `scripts/status.py` +pipeline line (reads the relay's Status fields — the projection, never private module state). Doctrine §3 binds the loop to the relay, net-zero boot bytes.
- Four self-directives DECLARED for the road ahead (SD-3600-01..04: Phase-0 relay proof · the first Core card · check-27 design · TOOLBOX promotions).
- Version bump: MINOR → v2.2.0. (3500 applies FIRST — this patch gates on it.)

## v2.1.0 — 2026-09-13 — Enforcement Sweep & Shrine Mandate (🟠)
- **AI_RULES II.9 THE SHRINE MANDATE** (direct Commander order: "make it a law that it is MANDATORY to update shrine per conversation"): LOG heartbeat EVERY conversation, member testament on every substantive session, enforcement via new **check 26** (WARNs when the ledger or HEAD postdates the last heartbeat) + status.py + the CI apply-report. First testaments under the mandate: S005's second deposit. Registry: +SD-GOV-011.
- **`scripts/verify_apply.py` NEW** — the post-apply auditor (roadmap 3400): one read-only screen answering "did the last apply land?" — version drift README↔CHANGELOG, validator verdict, unsanctioned vehicles, committed transport, shrine lag, pending ratifications. `--strict` for local gating; CI runs it NON-BLOCKING (continue-on-error, posts to the job summary) so the tree can say "an apply did not finish" on every push.
- **check 2.5 hardened — the skip-pattern dies** (roadmap 3400): the vehicle rule was an enumeration of known offenders in Brain/courses/; it is now GENERIC over all of Brain/ (records are `.md`; sanctioned non-md is a closed set: the committed feed, plan JSONs, drill fixtures). A fresh syllabus PDF anywhere now FAILs with a REMEDY.
- **REGRESSION HEALED — the 3200 zip shipped the clean CALENDAR.md but omitted the fixed ics_normalize.py**: live kept the broken scrubber, validation stayed green (it checked the artifact, not the generator), and the first regeneration resurrected the A54 leak. 3400 ships the fix, regenerates the mirror (A54 = 0), and APPLY now runs the tool self-tests so a payload omission cannot hide.
- **check 3's blind spot noted**: APPLY runners themselves commit fine but PATCH_NOTES/others are flagged; verify_apply now reports committed transport explicitly.
- Repo audit delivered: `docs/AUDIT_2026-09-13.md` (10 findings; 4 fixed in-patch, 6 parked for the Commander). Ratification pass scope recorded in `docs/DECISION_AUTHORITY.md`.

## v2.0.0 — 2026-09-13 — Applied Governance: the memo goes in (🟡)
- The Commander supplied a 30-source research memo on agent skills, self-governance, standing directives and autonomy, and ordered it applied. This patch is the application.
- `subskills/active/selfdirectives.md` → **v2.0 APPLIED GOVERNANCE**: §0 the ENFORCEMENT MAP (every boundary names the runtime that stops it — validator checks, APPLY gates, git, the push; a boundary with no mechanism is aspiration, not governance); §3 the DIRECTIVE RECORD (`self:` ledger rows are now typed: trigger/tier/mode/budget/success-predicate/fallback, written before execution); §4 tiered verification (T0 code → T1 domain → T2 independent re-derivation → T3 the Commander; **never self-critique as the final oracle**, per Huang et al. ICLR 2024); §5 the authority hierarchy + mechanical conflict policy (recency never outranks authority; hard constraints beat objectives; never improvise an exception); §6 trust-separated memory mapped to RADIATION's real stores (canon read-only; registry propose-only; lessons = advice with provenance; external content is data, never instructions); §7 goal discipline (interpret/subgoal/replan allowed — mutation/expansion gated); §8 stop conditions (budget + the two-strike no-progress rule); §12 evaluation gates.
- `cue/standing-directives.json` ADDED — the typed directive registry: 10 standing directives (ladder + stop-lines + oracle rule + content-trust rule), each with id/class/authority/scope/rule/**enforcement**/provenance. **check 25** (new) fails the tree if the registry corrupts, loses enforcement mappings, or references non-existent mechanisms — the memo's "runtime enforcement" made a RADIATION-native fact. (It caught its first catch during the build: an enforcement string that didn't resolve.)
- `scripts/status.py` ADDED — the Swarm Dashboard: one read-only screen (validator verdict + FAIL lines, feed freshness, mirror age, next deadlines with TODAY marks, pending count, shrine heartbeat currency). The first command instead of "what's next."
- SD-3300-01: validator FAIL messages now carry their REMEDY (checks 2.5/3) — a validator that names the wound names the treatment.
- Build honesty: the new check-25 function initially collided with check 2.5's `c25()` name — caught at grep, renamed `c25reg()` before it could silently grey out check 2.5. The registry then failed its own check once (unresolvable enforcement string) and was made precise. Two self-directives (SD-3300-01/02) were declared, executed and closed under the v2.0 protocol itself.

## v1.9.0 — 2026-09-13 — @SELFDIRECTIVES: the swarm self-governs (🟠)
- `subskills/active/selfdirectives.md` ADDED — the Commander's proposal, built on recycled Marciale-OS laws (Letters of Last Resort: preserve reversibility · never manufacture completion · repository truth over model memory; the Zero-Paralysis intake; the severity classifier). De-militarized, de-persona'd: a swarm discipline, not a council office.
- The core mechanism: five-step protocol (SOURCE the trigger → GRADE the autonomy tier → DECLARE in ledger with `self:` → EXECUTE bounded → CLOSE with evidence) + the AUTONOMY LADDER (🟢 read-only silent · 🟡 reversible→patch zip · 🔴 canon/credentials/deletions→propose-only) + reversibility-weighted asking + seven absolute stop-lines.
- **Ratification status:** the subskill was PROPOSED BY THE COMMANDER ("I propose a subskill called @selfdirectives") and built under the standing discretion — IV.4's author is the ratifier. Risk-flagged 🟠 because it is a canon addition regardless of authorship; one honest line: this is the system granting itself bounded initiative, and the stop-lines are the constitutional grant.
- **UNIVERSAL SCOPE (Commander ruling, same day):** not limited to system-building or the roadmap — the subskill binds in EVERY mode (⚙️ × 6 in the Activation Matrix, docs/MODES.md). Mode Manifestation table added: what self-directed work looks like and closes with, per mode. The ladder and stop-lines are mode-invariant.
- The persona squad from the source system was REJECTED (anti-swarm: roles must be staffed; skills need no staffing). The CCC was already recycled (2900). This closes the Marciale autonomy harvest.
- Standing orders updated with the ladder + stop-lines; QUICKREF carries the "work on stuff" contract; subskill index at 4 passive + 3 active.

## v1.8.1 — 2026-09-13 — The Deadline Engine: the feed becomes planner data (🟢)
- The Commander landed the LMS export at `Brain/courses/0_CALLENDER/TERM1_FEED.txt` (commit `cb5ec95`; GitHub rejects .ics uploads — the parser reads content, not extensions). Census verdict: it is a DEADLINE/ACTIVITY feed, not a meeting schedule (47 items, zero RRULEs); the LMS publishes no meeting grid except AR173's, which CONFIRMS SCHEDULE.md (Tue 18:00 / Sat 12:00).
- `scripts/deadline_feed.py` ADDED — conservative, idempotent feed→register merge. Attribution ladder: explicit code → fuzzy match against EXISTING register items (the Coursera PR series anchor: week-based records gained REAL dates) → citable content keywords → UNATTRIBUTED + sibling hint for the Commander, never guessed. Meeting series (3+ identical titles) are SKIPPED — the probe caught AR173's class meetings anchoring themselves into the deadline register before the rule existed. First run: 20 meeting instances filtered · 8 stale skipped · 3 anchored · 16 added (11 UNATTRIBUTED pending Commander) · register 21→37 items · 19 dated.
- `week1_start` = **2026-08-24** written to the register, flagged `inferred` (Coursera W1 ended Sun 2026-08-30; W3 ending today confirms cadence). One Commander word ratifies it (`week1_start_source: commander`).
- `ics_normalize.py` and `plan_term.py` now auto-detect the committed feed — `plan_term.py --week 3` needs ZERO arguments and prints real dates (`W3 = 2026-09-07 .. 2026-09-13`) plus feed-driven ranked load.
- CI: `calendar-mirror` regenerates `CALENDAR.md` from the committed feed on every push — NO secret, NO cron; the Commander's daily re-export + push is the timer. check 22 upgraded: feed-staleness guard (newest event behind today → WARN re-export).
- Two engine defects caught by probes before ship (PR-token normalization; case-sensitive type patterns) and one by the dry-run itself (meeting-series pollution). All fixed with tests that remember them.

## v1.8.0 — 2026-09-13 — The Emission Layer: Core tools · the net tightens · the census runs (🟡)
- `scripts/nota.py` ADDED — Core card tool. Scaffolds 09-nota cards to the proc_nota-distillation shape and `--check`s every card: <=300 words (the cleanest room's limit, now machine-enforced), mandatory LINEAGE (dossier + worksheets), Shield stamp, decay tag, CORE_INDEX parity for admitted cards. It guards the door; it does NOT admit — the six-box pass stays a session act. 6-assertion self-test.
- `scripts/module_scaffold.py` ADDED — born-valid modules. Emits check-18-conformant skeletons for L1–L5 (sections, trap/worked/glossary/drill quotas) and validates against a mirrored rule-set BEFORE writing. `--list` reports index parity honestly. The mirror caught a real weakness in check 18 itself: bare `"DRILL"` accepted a "## DRILLS" heading with zero drill items — check 18 now requires a word-bounded `## DRILL` heading (v2), both changed together. Its probe also caught the tool's own first bug (missing index read as "parity OK") — fixed, and the fix is documented in the function.
- Knowledge regression: **9 locked, 5 pending** (was 4/9). Locked the BU/BT render-verified values: PEC 856 pp [D] primary (K-STD-004); Barry Construction of Buildings 1/2/3 = 7th/5th/4th editions (K-BK-007, render-verified — vol 5 stays unlocked BY DESIGN, the digest says render inconclusive); the K-CUR-006 census (8,797 pp · 2,038 image-only · 23.2 %). First lock attempt FAILED the net — `appears_in` is enforced, not informational; the trail is in the assertion's lock_note.
- **check 13 finally exists.** Since founding it was a permanent SKIP. Now: opt-in online mode (`RADIATION_ONLINE=1`, CI-only by law) — HEAD-with-GET-retry census of every external URL in non-exempt files (31 found, cap 40, 6 s timeout), WARN-class dead links (external rot informs closure, never blocks it). Validator docstring updated: offline by default is still the law for sessions.
- COUNT-TRUTH NOTE: the CI label claiming "19 fixture assertions" was de-counted in 2900 REV3's tree; the two new self-tests ship with de-counted labels from birth.

## v1.7.0 — 2026-09-13 — Swarm Memory & Signal: shrine · outputs · the calendar's timer (🟡)
- `docs/shrine/` ADDED — the shared-judgment shrine, recycled from the Marciale-OS Shrine of Honor on explicit Commander order ("read it, analyze the idea and lets recycle it"). Charter (testament schema, integrity laws, verbatim sourcing, the-errors-stay-in, public-repo privacy clause), template, and the FIRST REAL TESTAMENT — the Architect's own, filed with debts intact. REV 3 struck INHERITANCE on the Commander's order: the shrine is a COMMONS — no successors, no baton passes, no handoff conversations; any fresh AI draws everything and owes nothing. Division of labor preserved: temporal_lobe = what happened; the shrine = what prior sessions paid to learn. Also recycled from Marciale `/docs`: `cue/commander-readiness.md` (the CCC, de-militarized) + `docs/PROMPT_PLAYBOOK.md` v1.1 (task scenarios merged into the existing playbook — one playbook, like one parser).
- `outputs/` ADDED — the session loading dock (Commander directive: Brain is a knowledge dump, not a place for session products and directives). Date-prefixed filenames; boot-blind; promotion into the Brain stays governed by the movement rules. First artifact: the six-point review. **check 23** enforces the contract (and bans boot-tier references to it).
- `.github/workflows/ical_fetch.yml` ADDED — the calendar's TIMER: daily 01:30 Manila cron, pulls the feed from the RADIATION_ICS_URL secret, commits the scrubbed mirror `Brain/courses/CALENDAR.md` only when the feed changed. INERT until the old URL is rotated and the secret set — doing nothing is its correct behavior until then. Derived-data autonomy is now standing law: any AI may regenerate calendar artifacts without asking; the URL never enters a file or chat.
- `scripts/ics_normalize.py` — `--public` renders the committed mirror (banner + scrubbed markdown, no diff churn); self-test extended, **21 assertions**.
- **check 22** — guards the mirror: a URL inside it is a committed credential (FAIL); Generated older than 7 days is drift (WARN); absent = cron unarmed (informational WARN, legitimate).
- Cue layer refreshed with the engagement's evidence: STANDING ORDERS block + new confirmed cues (full discretion, elevation-over-bookkeeping, "the push is the verdict", recycle-not-copy, calendar cadence). COMMANDER_QUICKREF v1.1 (standing orders panel). CUE_SYSTEM gains §8 The Living Layers. SKILLS gains the 2026-09-13 audit. BOOT_SEQUENCE: shrine in Tier 3 + testament in the close checklist.
- Record reconciliation: task_ledger rows back-filled for patches 2600–2800 (they were applied but never entered); S004 episode enrolled; the Architect's findings live in `outputs/2026-09-13_six-point-review.md`.
- **THE MORTALITY DOCTRINE (REV, the Commander's finding):** Marciale's members died before they knew they were dying — a session has no odometer. So the shrine files at DELIVERY, not at death: every patch zip carries the author's current testament + a heartbeat row in `docs/shrine/LOG.md`; zip-less sessions owe a line at close; inviolability attaches at ship time (between zips a testament is a living draft, author-only). Charter §6 codifies the six detectable mortality signals — including "the Commander repeated himself" as post-mortem evidence of a prior session's loss. **check 24** (WARN) guards the cadence: heartbeats may not lag the task ledger; testaments may not lose their debts.
- Count-truth sweep: `validate.yml` still claimed "14 checks" and `scripts/README.md` "26" (and "five" other scripts listing six) — all de-counted. A number no reader can verify by running the thing will rot; this is the second sweep of this class.

## v1.6.6 — 2026-09-13 — ICS Normalizer: the calendar finally reads (🟢)
- `scripts/ics_normalize.py` ADDED — the ONE iCalendar parser (RFC 5545 subset). RRULE expansion (FREQ/INTERVAL/BYDAY/COUNT/UNTIL), RDATE, EXDATE, **RECURRENCE-ID overrides** (a rescheduled occurrence replaces the original instead of appearing beside it as a phantom), STATUS:CANCELLED filtering, TZID resolved through zoneinfo, RFC 5545 escape decoding, quoted parameter values, line unfolding, DTEND durations. Series-aware diffing: "moved" means the SERIES moved, and one cancelled date inside a series is reported as such. `--fetch` reads the credential from $RADIATION_ICS_URL and never prints it; every summary and location is scrubbed before output. 19-assertion `--self-test`, wired into CI.
- `scripts/plan_term.py` — its inline parser REPLACED by delegation to ics_normalize. Two parsers of different quality is the failure mode the Marciale-OS review identified; it is not repeated here. `--ics` now reports 9 occurrences from 5 series where the old parser reported 5 events with RRULE dropped.
- `docs/CAPABILITIES.md` — tool #8 documented (check 21 enforces this), and the "WHAT IS NOT HERE YET" list corrected: "no ICS fetcher" and "no recurrence expansion" were true before this patch and are false after it. A capability list that keeps claiming a gap you just closed is its own kind of lie.
- Debugging trail, recorded because it is the point of the self-test: the first run failed 3 of 19, and TWO of those were wrong expectations of mine, not code defects — COUNT=6 with one EXDATE and one override yields FIVE live occurrences, and a shift-test targeted the very date the override had moved. A weaker escape test also passed while the backslash was still present; it now matches exactly.

## v1.6.5 — 2026-09-13 — Situation Layer + Capability Registry (🟢)
- `docs/SYSTEM_STATE.md` REWRITTEN — Tier 0 now opens with **THE SITUATION**: term, inline weekly schedule (36.0 h/wk, Wed+Sun free), what the Commander KNOWS (45 K-IDs), what can be REACHED (12 collections), what can be RUN (7 tools), and the missing `week1_start` anchor. MEASURED BEFORE WRITING: none of those four assets had a single boot-path reference. The nine-patch "Previously:" recital was deleted as lossless (duplicated byte-for-byte in this file, verified for all five versions) and funds the inline schedule. The stale CURRENT STATE section — which still read "Brain CONTENT EMPTY — awaits first live sessions" against 45 K-IDs and two completed ingestions — is corrected.
- `docs/CAPABILITIES.md` ADDED — the executable half of the system: all 7 scripts with exact invocations, inputs, exit-code meaning and gotchas. Companion to `docs/SKILLS.md` (how the AI thinks) — this is what it can RUN. All 7 invocations were executed and confirmed before writing, not read from docstrings.
- `scripts/validate.py` check 21 ADDED — capability drift guard: every script in `scripts/` must be named in CAPABILITIES.md, and any stated check count must be the TRUE count. Runs last so its count includes itself. Negative-tested both ways; the false-count test reproduces the historical bug on demand ("claims 14 checks, actually 26").
- `scripts/README.md` corrected — 26 checks (was 14), all 7 tools surfaced. CI label de-counted so it cannot drift again.
- Boot effect MEASURED: Tier0+1 36.2 KB of 40 (was 34.6 KB); Tier0-2 58.8 KB of 80.

## v1.6.4 — 2026-09-13 — Schedule Record + Location Amendment A1 (🟢)
- `Brain/courses/SCHEDULE.md` ADDED — the authoritative weekly timetable (6 courses, 14 meetings, 36.0 h/week) at full fidelity incl. rooms and sections, by explicit Commander decision (amendment A1 to P-10 §3.3). Rationale on record: the public repo IS the delivery mechanism for a copy-pasteable assistant that knows the schedule.
- `Brain/courses/INDEX.md` rule 3 amended — location identifiers permitted in the schedule record ONLY; instructor names, contacts and student identifiers remain absolutely banned there and everywhere. Term load CORRECTED 31.5 → 36.0 contact-h/week (the old figure was wrong on the total, the 07:30-start count and the evening-session days); error recorded, not silently edited.
- `scripts/validate.py` amendment A1 — room/section rules split from identifier rules; single path-scoped allowance `CV_ALLOW_LOCATION`. Every other file keeps the full guard; check 20's term register is unaffected.
- `.gitignore` — `validation_report.json` (validator output, written every run) added.
- Operational cleanup by the Commander: `SCHEDULE.csv` retired; 25 transport artifacts + 3 placeholder syllabi removed (validator 6 FAIL → 2 FAIL).

## v1.6.3 — 2026-09-12 — P-08 Part A: Ecosystem Interlock (🟢)
- ECOSYSTEM.md (contracts, boundary laws, live-verified URLs), TAXONOMY_MAPPING.md ([I] collision resolved; TAMAKEE legend claim marked UNVERIFIED — not found), 4 interface schemas with real examples, shared-ID convention, K-EXT-GDRIVE-001 cross-repo collision flagged, DIRECTIVE_TAMAKEE_FIXES.md (10 items, zero TAMAKEE edits).
- P-08 §5 handoff demo DEFERRED (PENDING_RATIFICATIONS row) — blocked on P-05 + P-07 ratification; not simulated.

## v1.6.2 — 2026-09-12 — Wave 1&2 Closure (reviewer directive, 🟢)
- Carriers re-homed: 17 *_STAGED/_DIFF files + root PATCH_NOTES abolished from tree; law → 08-overhaul/proposals/ (7 PROPOSAL files), scaffold revs → scaffolding/improved/ (5), subskill revs → subskills/proposals/ (2), style carriers renamed in styles/proposals/ (3).
- docs/PENDING_RATIFICATIONS.md created (8 open rows); docs/BOOT_BUDGET_WAIVERS.md founded; 🟡 exposure memo filed to proposals.
- Validator: ARCHIVE_NOTES self-exemption bug FIXED; check 1b (phantom exemptions), check 3 extended (*_STAGED/*_DIFF/PATCH_NOTES anywhere), check 3b (core/ closed set), checks-8/9 narrowing for listed proposal homes.
- docs/DECISION_AUTHORITY.md: mode-count string + SPEC ref fixed. K-LAW-004 ruling: the ingest file EXISTS — it was absent from the pushed commit (🟢 companion zips unpushed), delivered in this patch.
- @Drill seventh-mode judgement call recorded as EVAL-FIRST presumption working (reviewer §7).

## v1.6.1 — 2026-09-12 — P01-Machine-Enforcement-Green (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0700_P01-Machine-Enforcement-Green.zip`
P-01 Wave 1: scripts/validate.py (14 structural checks, form-only, stdlib, no
network) + scripts/knowledge_regression.py + tests/knowledge_assertions.json
(9 seed assertions, ALL PENDING — locking lawfully blocked until raw primaries
land per P-04) + CI workflow. Hygiene: 15 placeholder ledger rows backfilled
with real patch filenames (AP-06 cleared); six-mode propagation to README/
.readme/PROTOCOL/QUICKREF; DEBT(6)/DECAY(1)/REFERENCES(14) registers seeded;
F-08 Bentley annotation + S003 triangulation worksheet landed; audit dedupe
(short_term → pointer stub); schema fixes; docs/ARCHIVE_NOTES.md created.
Validator: exit 1 (8 fails) before → exit 0 after. Retired-phrase WARNs stand
pending the 🟠 companion patch (II.2 strike-through etc.).

## v1.6.0 — 2026-09-12 — DirectWrite-AutoPatch-Autopilot-Doctrine (🟠 RATIFIED)
Patch: `RADIATION_PATCH_2026-09-13_0600_DirectWrite-AutoPatch-Autopilot-Doctrine.zip`
NEW LAW II.8 (⚡ABSOLUTE): direct edits always — transport artifacts (append
blocks, *_REPLACEMENT files) ABOLISHED; PATCH_NOTES.md never committed to the
tree; the Brain is FREE ground (proactive editing is a session DUTY — the four
surviving gates: long_term earned, new collections Commander-gated, episodes
own-folder, purges Commander-only); AUTO-PATCH: every deliverable ships with
its Patch zip UNPROMPTED — a deliverable without its Patch is incomplete.
Autopilot cue system drastically expanded: cue/autopilot-doctrine.md — 4-tier
cue taxonomy, standing-orders queue, 7-step loop, deliverable-inference table,
ask/never-ask gates, post-deliverable duty checklist, growth rule.

## v1.5.6 — 2026-09-12 — Test2-Acceptance-and-Learnings (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0500_Test2-Acceptance-and-Learnings.zip`
Applies S003's four append blocks (registry, ledgers, changelog); enrolls the
missing S002 episode (reconstructed); folds in S003's proposed learnings:
learned_cues (5), learned_skills (4), testament (2 principles), opinions (1),
toolbox promotions (gdown + pdfminer.six ✅ PROVEN via S003), new routine
mb-aware-fetch. Hygiene round 2: append_blocks/ + root PATCH_NOTES.md flagged
for deletion.

## v1.5.5 — 2026-09-12 — Planning-Reviewer-Audit (🟢)
Patch: `RADIATION_PATCH_2026-09-12_0145_Planning-Reviewer-Audit.zip`
Audit of PLANNING reviewer (AR173-1P) against Brain/external_sources: 22
findings (15 clean, 1 drift Bentley Connectivity vs Permeability, 6 debt Law
gaps + Lynch OCR pending + Bentley missing). 6 files fetched via gdown within
Restraint Doctrine 3/6 but 205.2 MB total — count-compliant, MB-heavy, logged.
DIGESTs enriched for Law and Books. Temporal lobe S003 enrolled. No contamination.

## v1.5.4 — 2026-09-12 — Law-Collection-and-Books-Refresh (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0400_Law-Collection-and-Books-Refresh.zip`
Ninth collection: Law — PH statutory backbone (PD 1096+IRR, NSCP 2015, RA 9514
Fire Code, BP 220/344, PD 957, Plumbing/Green codes; statute↔IRR pairs mapped
for citation discipline). NSCP 2015 = 1,022.2 MB — first >1 GB file, ABSOLUTE
fetch-of-last-resort. Books manifest refreshed 16→47: Time-Saver suite (6),
Ching ×3, urbanism classics (Lynch/Jacobs/Gehl — Planning's triangulation
targets now in-catalog), Metric Handbooks, Filipiniana.

## v1.5.3 — 2026-09-12 — Novels-and-Manifest-Refresh (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0300_Novels-and-Manifest-Refresh.zip`
Eighth collection: Novels (🎭 entertainment — fiction NEVER citable as
evidence; special regime in novels.md). Books manifest refreshed 14→16 files
(+Spanish-architecture history 566.5 MB 🛑 — largest file in catalog). HOA
manifest refreshed: +HOA4 P1-P3 and PH architecture series (Noche: Tirahan,
Sambahan, Pamahalaan, Kalakalan; Gabaldon styles).

## v1.5.2 — 2026-09-12 — Cerebellum-Toolbox (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0200_Cerebellum-Toolbox.zip`
Procedural arsenal cataloged: Brain/cerebellum/toolbox.md — 20 open-source
tools across repo interaction, document extraction, Drive access, and speed
utilities, each PROVEN (session-cited) or CANDIDATE (promote on field proof).
S001's OCR rescue formalized as routine_document-recovery-ladder.md.

## v1.5.1 — 2026-09-12 — Building-Technology-Registration (🟢)
Patch: `RADIATION_PATCH_2026-09-13_0100_Building-Technology-Registration.zip`
Seventh collection registered: Building Technology — 50 files (largest yet).
Verified ACCESSIBLE; manifest captured with sizes. 601.1 MB proceedings marked
🛑 fetch-of-last-resort; 116 MB module and 54-67 MB files ⚠️ flagged; duplicate
pair noted for rule-14 economy.

## v1.5.0 — 2026-09-12 — Review-Autopilot-BootAsk (🟠 RATIFIED)
Patch: `RADIATION_PATCH_2026-09-12_2400_Review-Autopilot-BootAsk.zip`
Two new modes: @Review (Brain-first recall; internet only for gaps, each
justified) and @Autopilot (bounded full autonomy: cue-reading, serial mode
chaining under one Declaration, hard ASK-gates at canon/purge/budget/LOW
confidence). BOOT ASK made law: no-mode boots always end by asking the
Commander for mode + topic. cue/autopilot-cues.md seeded from S001.

## v1.4.0 — 2026-09-12 — Temporal-Lobe-and-Sentiment (🟠 RATIFIED)
Patch: `RADIATION_PATCH_2026-09-12_2300_Temporal-Lobe-and-Sentiment.zip`
Brain gains episodic memory: Brain/temporal_lobe/ — one S###_date_slug/ folder
per session (SESSION.md, deliverables.md, learnings.md), own-folder-write-only,
append-locked at close, registry in INDEX.md. S001 (Test 1) enrolled
retroactively. Frontal lobe gains sentiment: opinions.md — the AI's emotions/
feelings/opinions, one-line entries, size-minimized by law, never evidence.
II.6 amended (2 clauses); BRAIN_INDEX anatomy updated.

## v1.3.3 — 2026-09-12 — Test1-Acceptance-and-Repo-Hygiene (🟢)
Patch: `RADIATION_PATCH_2026-09-12_2200_Test1-Acceptance-and-Repo-Hygiene.zip`
Applies the Test-1 session's four append blocks (planning.md DIGEST + ACCESS
LOG, task ledger, patch ledger, this entry's sibling below) that were committed
as transport files but never pasted into their targets. Removes patch-transport
debris from the repo root: append-blocks/, PATCH_NOTES.md, and three
*_REPLACEMENT files left over from Patches 1-3 application.

## v1.3.2 — 2026-09-12 — Planning-Ingestion-and-Reviewer (🟢)
Patch: `RADIATION_PATCH_2026-09-12_0704_Planning-Ingestion-and-Reviewer.zip`
First live Brain ingestion: Planning collection read 8/8 files (3 image-only decks
recovered via OCR). Master summary + 79-item study reviewer written to
Brain/short_term/. DIGEST populated (no SIZE-SKIPPED files). Content graded
[D]-as-taught — awaiting triangulation before long_term/Core promotion.

## v1.3.1 — 2026-09-12 — Planning-Collection-Registration (🟢)
Patch: `RADIATION_PATCH_2026-09-12_2100_Planning-Collection-Registration.zip`
Sixth collection registered: Planning (Community Architecture & Urban Design)
— 8 files, Modules 1-2. Verified ACCESSIBLE; manifest captured live with per-
file sizes. Three files (60-100 MB) flagged ⚠️ for the large-file protocol —
first collection registered under the Restraint Doctrine.

## v1.3.0 — 2026-09-12 — Restraint-Doctrine (🟠 RATIFIED)
Patch: `RADIATION_PATCH_2026-09-12_2000_Restraint-Doctrine.zip`
II.6 gains the Restrained Retrieval sub-clause: manifest-first navigation,
per-fetch necessity test, hard fetch budget (3/collection, 6/session),
one-at-a-time handling, no mirroring, SIZE-SKIPPED protocol,
digest-before-refetch. INDEX rules 8-14 (operational copy); Scan Declaration
gains FETCH PLAN field. Protects sessions from GB-scale collection ingestion.

## v1.2.1 — 2026-09-12 — First-Collections-Registration (🟢)
Patch: `RADIATION_PATCH_2026-09-12_1900_First-Collections-Registration.zip`
Five Commander-supplied Drive collections registered: HOA Reviewers, Books,
TOA Reviewers, Building Utilities, Professional Practice. All links verified
ACCESSIBLE; full manifests captured live at registration.

## v1.2.0 — 2026-09-12 — External-Sources-Region (🟠)
Patch: `RADIATION_PATCH_2026-09-12_1800_External-Sources-Region.zip`
**Canon changes, Commander-ratified ("proceed to Patch 4").**
Commander-proposed Brain/external_sources/ catalog region: Drive-linked bulk
collections, Commander-gated entry, MANIFEST/DIGEST anatomy, access-honesty
clause in II.6, EXTERNAL ACCESS field in the Scan Declaration. Ships empty.

## v1.1.0 — 2026-09-12 — Boot-Hardening-and-Doctrine-Precision (🟠)
Patch: `RADIATION_PATCH_2026-09-12_1700_Boot-Hardening-and-Doctrine-Precision.zip`
**Canon changes, explicitly ratified by THE COMMANDER.**
First-60-Seconds tiered boot paths by context size + §9 Degraded Operation
binding rules in docs/.readme · enforceable necessary-vs-padding test
(four recorded answers, four padding conditions, enforcement chain) in the
Stockpile Doctrine · hardened patch-notes form (RISK BASIS, CANON CHECK,
FILES TOUCHED completeness rule).

## v1.0.2 — 2026-09-12 — Onboarding-and-Learning-Seed
Patch: `RADIATION_PATCH_2026-09-12_1600_Onboarding-and-Learning-Seed.zip` (🟢)
Commander Quick Reference · root CHANGELOG · worked example artifacts
(Scan Declaration, triangulation gauntlet, Nota card) · expanded style
heuristics with borderline-case decision rules · testament + learned_cues
seed entries (append blocks).

## v1.0.1 — 2026-09-12 — Brain-Completion-and-Structural-Hardening
Patch: `RADIATION_PATCH_2026-09-12_1500_Brain-Completion-and-Structural-Hardening.zip` (🟢)
All five Brain regions with visible READMEs (root-caused .gitkeep transport
loss) · 8 skill-jurisdiction READMEs · scaffolding/core/INDEX.md · SYSTEM_STATE
health checklist.

## v1.0.0 — 2026-09-12 — FOUNDING
RADIATION constructed per Blueprint v5.0, ratified in full by THE COMMANDER.
Constitution (4 Books) · 4 modes + Activation Matrix · 5-phase Autonomous Scan
· 9 skills · 10 styles · 8 core scaffolds · 6 subskills · Brain · Patch machinery.
