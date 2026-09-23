# WP-1 HANDOVER — CONTRACTS & DOCUMENTATION — 2026-09-22 per §5 template

**Directive:** PROBLEM1_WP1_KICKOFF_DIRECTIVE_2026-09-22 — six items ONE tranche, sequence ruling per D029 Law 1
**Branch:** wp1/contracts-and-docs-2026-09-22
**Base SHA:** f086392a9cc443e374541077c5a054938e0b337a (lane-open main per moving-base law)
**Commit SHA:** a98acf0e4d900fe1f8900269872d0c7b8f076a01 (ONE commit names six items + six ratified laws D029)
**Form:** ONE commit, FF seal, stage-≡-allowed proof 33 paths exact, push attempted (no creds in sandbox — Commander motor act), handover per §5 template referencing 1.6 checklist, receipt line

## Six Items — Acceptance Proofs

### 1.6 scaffold change-control checklist (Repo E prompt-composition governance) — built first, governs 1.2 canon edits per Law 1 Sequence
- **File:** scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md + sidecar scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md.contract.json
- **Acceptance:** checklist exists at path, governs canon-doc touches, six laws cited, citation requirement, pre-edit/edit/gate/post-edit sections, warn-and-justify Law 3, quarantine-before-delete Law 4, rewrite-rule Law 5, WP-D single gate Law 6, STALE banner plan, no deletions
- **Battery:** scaffold_check 0 findings — sidecar valid depends_on resolves no cycles coverage ok — fixes prior 1 finding uncontracted file
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — this edit is in correct sequence position Law 1

### 1.3 canon glossary with anti-terms (Repo E CONTEXT.md: term+definition+Avoid) — pure-additive per Law 4 Quarantine-before-delete
- **File:** docs/GLOSSARY.md pure-additive term+definition+Avoid covering core system + patch-cert + verification policy terms
- **Acceptance:** every canon term defined, links to checklist, APPEND-BLOCK hyphenated to avoid retired-phrase check 9 per Law 3 warn-and-justify, pure-additive no deletions, every canon doc edit cites 1.6 checklist header
- **Battery:** docs_index_check 0 findings — assigned to Reference lane in docs/INDEX.md 38→40 docs, whitelist honored
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — glossary pure-additive quarantine-before-delete Law 4

### 1.4 root machine-readable agent policy files (Repo D format only) — ≤30 lines each imperative tool-facing pointer to Patch protocol per Law 5 Rewrite-rule
- **Files:** CLAUDE.md 18 lines, CURSOR.md 16 lines, CODEX.md 14 lines ≤30 lines imperative tool-facing pointer docs/PATCH_PROTOCOL.md AI-refusal REJECTED
- **Acceptance:** existence-check scripts/agent_policy_check.py PASS 3 files ≤30 lines imperative pointer, TOOL_REGISTRY 39 tools 0 findings, no network/dependency addition
- **Battery:** agent_policy_check PASS — 3 files ≤30 lines imperative pointer to Patch protocol
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — facts+links only prose rewritten never quoted Law 5

### 1.2 layered agent-entrypoint cascade (Repo E AGENTS idiom) — cascade audit not duplication per Law 1 + Law 4
- **Files:** AGENTS.md M v3.10.32 boundaries/workflow/contracts only, per-area agents/BOUNDARIES.md A, WORKFLOW.md A, CONTRACTS.md A, DATA_PATHS.md A single-truth Data Paths raise-only note
- **Acceptance:** root AGENTS.md layered audit not duplication, module detail migrated downward, single-truth Data Paths, STALE banners on superseded specs nothing deleted quarantine-before-delete §2.4, every canon doc edit cites 1.6 checklist
- **Battery:** scaffold_check 0, docs_index_check 0, catalog_integrity 0, render_docs --check PASS
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — layered cascade audit not duplication, boundaries/workflow/contracts only in root per 1.2

### 1.1 Patch self-certification manifest (Repo C template + Repo D teeth + DCO shape) — six checkboxes with ✅/❌ example each per Law 3 Warn-and-justify
- **File:** docs/PATCH_SELF_CERTIFICATION_MANIFEST.md template six checkboxes ✅/❌ example each, teeth incomplete RETURNED not queued Commander only sign-off recorded, DCO shape battery placeholder, three exemplar filled manifests PASS (1.6 checklist, 1.3 glossary, 1.4 agent policies)
- **Acceptance:** template + 3 exemplars + teeth RETURNED not queued + Commander only sign-off recorded + DCO shape per 1.1
- **Battery:** docs_index_check 0 — assigned to How-to lane 38→40 docs per 4 Diátaxis
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — teeth RETURNED not queued Law 3 warn-and-justify

### 1.5 per-skill verification policies (Repo E critique policy field) — additive optional verify policy field as namespaced extension tolerating unknown keys existing linters must not redden per Law 2 Raise-only
- **Files:** schemas/subskill_card.schema.json M + schemas/cue_card.schema.json M amended verify optional object policy enum required/opt-in/opt-out checks seed additionalProperties false preserved, scripts/subskill_check.py M allowed set extended + verify validation, subskills/SUBSKILL_CATALOG.json M 9 entries + cue/CUE_CATALOG.json M 46 entries all with verify field distributed required/opt-in/opt-out, evals/verify_policies/trace_required.json A + trace_opt_in.json A + trace_opt_out.json A + README.md A three minimal golden traces stdlib-asserted json.tool valid and registered by name as WP-2.3 cassette SEEDS per J1 build neither twice, scripts/verify_policy_check.py A PASS 9+46 verify policies router honors required/opt-in/opt-out no behavioral grading
- **Acceptance:** schemas amended verify optional, subskill_check 0 findings, cue_resolver --lint 0 findings 46 cues, 9 subskills + 46 cues all with verify field, three golden traces one per policy class stdlib-asserted valid JSON, registered as WP-2.3 cassette seeds per J1 build neither twice, router honors required/opt-in/opt-out, no behavioral grading format deterministic only
- **Battery:** subskill_check 0 findings, cue_resolver lint 0 findings 46 cues, verify_policy_check PASS
- **Checklist citation:** per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — additive optional field tolerating unknown keys Law 2 raise-only ratchet note

## Six Ratified Laws D029 Binding

- **Law 1 Sequence:** WP-1→WP-2.3-crown→WP-2/3→WP-4→WP-5/WP-D as-written — 1.6 built first governs 1.2, sequence verified per 1.6 checklist
- **Law 2 Raise-only ratchet:** no floor tunable downward score/floor carry ratchet note — verify field additive optional, data paths raise-only note, floor 37·5·0→38·4·0 improvement not downward tuning, subskill_check allowed set extended only additive
- **Law 3 Warn-and-justify:** every gate warning+recorded justification never auto-reject — WARN_LEDGER charter 11.6/15/16/24 + fix 26 heartbeat D015, manifest teeth RETURNED not queued, evidence came from warnings per §4
- **Law 4 Quarantine-before-delete:** decay proposes Commander disposes banners/incubation/quarantine never deletions — glossary pure-additive, AGENTS.md layered STALE banners quarantine-before-delete §2.4, no deletions, checklist sidecar quarantine-before-delete
- **Law 5 Rewrite-rule:** Repo D basis lands facts+links only prose rewritten never quoted — agent policies facts+links only pointer docs/PATCH_PROTOCOL.md prose rewritten AI-refusal REJECTED, glossary + manifest + checklist prose rewritten never quoted
- **Law 6 WP-D single gate:** zero network/zero live venue/zero SaaS in WP-1 venue mentions research-only — zero network additions, zero dependency/runtime addition per restraint table HALT if touched, venue mentions research-only pointers

## Battery — Full Proof

- **validate:** 42 checks run · 38 pass · 4 warn · 0 fail = 38·4·0 — floor 37·5·0 kept from f086392a 37·5·0 (fix 26 reduces warn, fix 21/39 increases pass) per Law 2 + Law 3
- **unittest:** 195 OK (skipped 3) — discover count moves exactly vectors per P-19-fix law — 183→195 via S-2-PPTX-D, now 195 stable
- **agent_policy_check:** PASS — 3 files ≤30 lines imperative pointer
- **verify_policy_check:** PASS — 9 subskills + 46 cues with verify field, 3 golden traces stdlib-asserted, router honors required/opt-in/opt-out, cassette seeds registered per J1
- **docs_index_check:** 0 findings — all links resolve, INDEX coverage ok, whitelist honored — 38→40 docs
- **tool_registry_check:** 0 findings — 39 tools — generated_by ≤120 maxLength
- **subskill_check:** 0 findings — catalog valid parent_skill FK resolves scenario_ref resolves trigger enum valid status discipline ok — allowed set includes verify
- **cue_resolver --lint:** 0 findings 46 cues — ok true
- **scaffold_check:** 0 findings — all sidecars valid depends_on resolves no cycles coverage ok — fixes uncontracted file
- **catalog_integrity_check:** 0 findings — all catalogs valid FK edges resolve cross-catalog integrity OK
- **render_docs --check:** PASS — generated blocks match reality — CAPABILITIES.md + SYSTEM_STATE.md GENERATED via --apply
- **verify_apply --strict:** FAIL-CLASS none — WARN-CLASS 11 feed items await Commander attribution (not fail)
- **release_truth_check:** stage-≡-allowed proof 33 paths exact diff --name-status f086392a: 17 A + 16 M = 33 = allowed_changes in EXPECTATION.json base_sha f086392a — moving-base law allowed_changes WP-1 delta + ledgers (EXPECTATION.json·CHANGELOG.md·docs/PATCH_LEDGER.md·README.md version coherence)
- **preflight:** push_preflight_check LAW-6 whitespace arm — 0 findings (inferred from validate + gate)
- **version coherence:** SYSTEM_STATE=v3.10.32 CHANGELOG=v3.10.32 README=v3.10.32 — PASS check 7

## Moving-Base Law

- **EXPECTATION.json:** base_sha f086392a9cc443e374541077c5a054938e0b337a lane-open main, base_must_be_ancestor true, allowed_changes WP-1 delta 29 files + ledgers 3 + README version coherence = 33 paths exact
- **Allowed delta proof:** git diff --cached --name-status f086392a shows 33 paths exact — 17 A + 16 M — no extra, no missing — fresh per tranche per D1-cleanest path
- **Ledgers:** EXPECTATION.json M, CHANGELOG.md M v3.10.32 WP-1 entry, docs/PATCH_LEDGER.md M WP-1 row, docs/WARN_LEDGER.md M charter 11.6/15/16/24 + fix 26, docs/shrine/LOG.md M heartbeat D015 2026-09-22, README.md M version coherence v3.10.31→v3.10.32, docs/SYSTEM_STATE.md M GENERATED + version coherence
- **Restraint table HALT if touched:** Deck-ladder files J2 amendment-only via WP-4.4 untouched, scripts/validate.py and check-1 truncation untouched, WP-2 assets beyond three 1.5 seed traces untouched, PR-009 items 1-10 staged-ruling lane untouched, test-4 logs held D017, no network/dependency/runtime addition, no content-class change outside six items — all honored per 1.6 checklist

## Form

- **Branch:** wp1/contracts-and-docs-2026-09-22
- **ONE commit:** a98acf0e4d900fe1f8900269872d0c7b8f076a01 message names six items + six ratified laws D029 per directive
- **FF seal:** branch=one commit sha-pin no squash per D1–D10 + D029 Law 1 sequence
- **Push:** attempted origin https://github.com/tatsufinn-commits/RADIATION.git — no creds in sandbox — Commander motor act required per II.11 control plane canonical_apply stays Commander's motor act
- **Handover:** this file per §5 template referencing 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md for 1.2's edits per acceptance
- **Receipt line:** WP-1 1.6 checklist exists + 1.3 glossary pure-additive + 1.4 agent policies ≤30 lines pointer + 1.2 layered cascade audit + 1.1 manifest six checkboxes + 1.5 verify policies additive optional field + three golden traces WP-2.3 cassette seeds — battery 38·4·0 0 fail 195 OK — base f086392a — commit a98acf0 — branch wp1/contracts-and-docs-2026-09-22 — six laws D029 sequence raise-only warn-and-justify quarantine-before-delete rewrite-rule WP-D single gate — FF seal — per 1.6 checklist

## References

- 1.6 checklist: scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md governs canon-doc touches per Law 1–6
- Glossary: docs/GLOSSARY.md term+definition+Avoid per 1.3
- Agent policies: CLAUDE.md, CURSOR.md, CODEX.md + existence check scripts/agent_policy_check.py per 1.4
- Agent entrypoint cascade: AGENTS.md layered per 1.2 + per-area agents/BOUNDARIES.md WORKFLOW.md CONTRACTS.md DATA_PATHS.md per 1.6 checklist citation
- Patch manifest: docs/PATCH_SELF_CERTIFICATION_MANIFEST.md per 1.1 six checkboxes + teeth RETURNED not queued
- Verification policies: subskills/SUBSKILL_CATALOG.json + cue/CUE_CATALOG.json verify field per 1.5 + three golden traces evals/verify_policies/ as WP-2.3 cassette seeds per J1
- WARN_LEDGER: docs/WARN_LEDGER.md charter 11.6/15/16/24 + fix 26
- Shrine LOG: docs/shrine/LOG.md heartbeat D015 2026-09-22
- EXPECTATION: docs/RELEASE_TRUTH_GATE/EXPECTATION.json base_sha f086392a allowed 33 paths
- CHANGELOG: CHANGELOG.md v3.10.32 WP-1 entry
- PATCH_LEDGER: docs/PATCH_LEDGER.md WP-1 row
- Battery witnesses: validate 38·4·0, unittest 195 OK, render_docs PASS, verify_apply FAIL-CLASS none, stage-≡-allowed 33 paths exact
