# 🌐 THE ECOSYSTEM (`docs/ECOSYSTEM.md`)
## Four Repos, One Checked System — Contracts, Boundary Laws, Interfaces
**Tier-3 REFERENCE (never boot). 🟢 documentation — no law text touched.**
**P-08 Part A (2026-09-12). Part B (§5 handoff demo) DEFERRED — blocked on P-05 + P-07 ratification (docs/PENDING_RATIFICATIONS.md). Every TAMAKEE claim below was verified live at write time; unverifiable claims are marked, not asserted.**

## 1. THE REPOS (URLs verified 2026-09-12, HTTP status shown)
| Repo | URL | Status at write |
|---|---|---|
| RADIATION | https://github.com/tatsufinn-commits/RADIATION | 200 ✅ |
| TAMAKEE | https://github.com/tatsufinn-commits/TAMAKEE | 200 ✅ |
| sources | https://github.com/tatsufinn-commits/sources | 200 ✅ ("a branch of tamakee based on current courses" — repo description, verified) |
| Marciale-OS | https://github.com/tatsufinn-commits/Marciale-OS | 200 ✅ (+ Marciale-OS-copy, 200) |
| ~~TAMAintegration~~ | github.com/tatsufinn-commits/TAMAintegration | **301 → TAMAKEE** — a GitHub RENAME redirect, not a dead link: clones still resolve, but the name is stale and one rename away from breaking. TAMAKEE README line 55 + AGENTS templates still use it (fix list item 1). |
| TheHUB (as a separate repo) | — | **404** — TheHUB exists only as a pillar/folder inside the Marciale-OS plan, not as a repo. Do not link it as one. |

## 2. THE CONTRACTS
| Repo | Owns | Must never do | Consumes | Produces |
|---|---|---|---|---|
| **RADIATION** | The epistemology: constitution, modes, skills, Brain, registers, Core, validator, Patch discipline | Store binaries · host bulk collections · assert grades for material it has not seen | TAMAKEE modules & registry rows · Drive collections · sources staging | Verified K-ID objects · Core cards · canonical modules (P-06) · drill sets (P-05) · validator output |
| **TAMAKEE** | The study product: vault/ spine, courses/ curriculum graph, reviewers/ (mock exams, flashcards, Anki), CLI tools, STUDY_LOGBOOK | Assert verification RADIATION has not done · publish unverified keys as exam answers · duplicate a RADIATION canonical module | RADIATION Core cards & modules · sources course material | Modules, reviewers, decks, exam sims, mastery data, source-registry rows |
| **sources** | Staging one term's course material by current coursework | Become a second vault (it is a branch, not a home) | — | Raw material for promotion into TAMAKEE vault/ and registration as RADIATION collections |
| **Marciale-OS / TheHUB pillar** | Local runtime, UI, calendar/XP/brain-profile shell (verified: FUTURE_BRAIN_UPGRADE_SPEC defines query_building_code / generate_mock_exam / log_study_xp and a +200 XP bridge) | Re-implement knowledge logic | RADIATION + TAMAKEE JSON exports (§3 schemas) | Session UX, XP dispatch, study scheduling |

**The asymmetry, stated (both sides verified):** TAMAKEE's DEFINITIVE_MASTERPLAN names four pillars — TheHUB · Companion RPG · TAMA engine · (Local AI) — none of them RADIATION; RADIATION's README calls itself the third pillar of an ecosystem with TAMAKEE and Marciale-OS. Both true from their side, contradictory together. This file and the TAMAKEE fix list (docs/DIRECTIVE_TAMAKEE_FIXES.md item 9) are the reconciliation: **RADIATION is the verification authority the masterplan's pillars consume; it does not need to be a pillar.**

## 3. BOUNDARY LAWS (five, enforceable)
1. **One canonical path per knowledge object, across all repos.** Both repos holding a module = one canonical + one pointer README.
2. **A grade never crosses a boundary untranslated.** Cross-repo use requires docs/TAXONOMY_MAPPING.md + the K-ID.
3. **Binaries live in exactly one place: nowhere in git.** Extract, write the extract in-repo, delete the binary (P-04 rule 8, staged; already demonstrated twice).
4. **The Core is the only emission surface.** Study artifacts consume cards; they do not mint claims.
5. **The Commander's push remains legal effect in every repo.** No cross-repo automation bypasses it (IV.5.1).

## 4. THE INTERFACE SCHEMAS (schema_version mandatory; consumer REJECTS unknown fields loudly; every crossing object carries a K-ID; nothing crosses without a citation locator)
### 4.1 rad.knowledge_object/v1 — RADIATION → TAMAKEE (real example: this repo's K-MOD-001)
```json
{ "schema": "rad.knowledge_object/v1", "k_id": "K-MOD-001",
  "title": "PD 1096 Rule VII–VIII: PSO · TOSL · Setbacks · AMBF/AMVB",
  "canonical_path": "03-dossier/MODULE_WORKSHOP_pd1096-rule7-8-setbacks-pso.md",
  "status": "VERIFIED", "grade_basis": "D", "last_verified": "2026-09-12",
  "verification_frequency": "1yr",
  "citations": ["PD 1096 (2005 Revised IRR), Rule VIII, Table VIII.1", "PD 1096 (2005 Revised IRR), Rule VIII, Table VIII.2"],
  "yield_rank": 9, "depth_level": 4, "drill_set": "SET-PD1096-VIII-001" }
```
### 4.2 rad.drill_set/v1 — RADIATION → drill engine (real example: first 1 of the 10 live items)
```json
{ "schema": "rad.drill_set/v1", "set_id": "SET-PD1096-VIII-001", "target": "K-MOD-001",
  "context": "ALE-UD / departmental",
  "items": [ { "id": "Q07",
    "brief": "BP 344 (amended IRR): the general gradient limit for an accessible ramp is:",
    "options": { "A": "1:12", "B": "1:10", "C": "1:20", "D": "1:15" }, "key": "C",
    "rationale": "Appendix A p.17: gradient not steeper than 1:20; steeper only in special cases by length.",
    "distractors": { "A": { "mb_id": "MB-006", "mistake": "pre-amendment value — RADIATION's own disproven seed", "category": "B" } },
    "citations": ["BP 344 IRR Amendments, Appendix A, p.17 / Table A.1.1"],
    "k_id": "K-LAW-003", "yield_rank": 9, "difficulty": "foundation" } ] }
```
(Full 10-item instance lives at Brain/short_term/drills/SET-PD1096-VIII-001.json — the P-05 companion's real artifact.)
### 4.3 tama.vault_object/v1 — TAMAKEE → RADIATION (example built from TAMAKEE's verified Law-I citation style)
```json
{ "schema": "tama.vault_object/v1",
  "title": "RA 9514 Canonical Fire Code Egress Compendium",
  "path": "vault/00-CORE-BUILDING-LAWS/RA-9514-CANONICAL-FIRE-CODE-EGRESS-COMPENDIUM.md",
  "claimed_tags": ["[RA 9514 Sec. 10.2.5.2]", "[STATUS: UNCONFIRMED CITATION]"],
  "claimed_grades_note": "TAMAKEE-side grade letters marked UNVERIFIED pending its own legend (TAXONOMY_MAPPING §3)",
  "requested_k_id": true }
```
### 4.4 rad.mastery_event/v1 — either → Marciale-OS (real example: the P-05 fixture run, provenance carried)
```json
{ "schema": "rad.mastery_event/v1", "topic_k_id": "K-MOD-001", "score": "7/10",
  "error_cats": { "A": 1, "B": 2 }, "next_review": "2026-09-15",
  "provenance": "FIXTURE — not a Commander attempt", "xp": 200,
  "xp_note": "+200 bridge per TAMAKEE FUTURE_BRAIN_UPGRADE_SPEC (verified); XP is Marciale's economy — never evidence in either knowledge repo (III.9.4-staged)" }
```

## 5. THE SHARED VALIDATOR (one instrument, two repos — note, not code)
`scripts/validate.py` (22 checks) is the shared reference implementation; TAMAKEE's audit.js + knowledge-regression.js are the predecessor. **Port requirement (B8 fix): path lists live in DATA (a manifest/JSON the checks read), never in code literals** — TAMAKEE's regression paths broke on consolidation precisely because they were literals. Check-number impact on RADIATION: **none — zero changes to validate.py in this delivery** (the reviewer's split rule therefore not triggered). Cross-repo link freshness (this file §1, TAMAKEE's counterpart) is check-13 territory: offline-skip by design in-session, run manually/CI where network exists. TAMAKEE-side adoption travels via the fix list, never by edits from here.

## 6. SHARED ID CONVENTION (P-03 carries the RADIATION side)
K-IDs are minted where verification happens: **RADIATION mints; TAMAKEE adopts and never re-uses the K- prefix for anything else** (fix list item 7). Format: `K-<DOMAIN>-<NNN>` per docs/KNOWLEDGE_REGISTRY.md frozen domains. **Grade-name binding: the curriculum modifier is `[D]-as-taught` — P-07's staged text keeps that name; the [D-c] rename option is dead; this mapping binds to the kept name.**
**⚠️ VERIFIED COLLISION — K-EXT-GDRIVE-001 names two different objects today:** TAMAKEE's registry row = one Drive folder (1q5iXLUJ...7d6P, "TAMA Google Drive Resource Hub", verified in its KNOWLEDGE_GOVERNANCE_REGISTRY §2); RADIATION's row = the nine-collection catalog hub (Brain/external_sources/INDEX.md). Same ID, different referents — exactly what the convention forbids. Resolution: RADIATION's row is annotated (registry append, this date); TAMAKEE re-scopes on adoption (fix list item 7a): its folder takes a fresh -002 suffix (a NEW ID it mints on adoption — deliberately not written in K-ID form here: it does not exist yet) or becomes a sub-entry, RADIATION's hub row stays 001, OR the Commander rules the reverse. Until ruled: **cross-repo references must use repo-qualified form** — `RAD:K-EXT-GDRIVE-001` / `TAMA:K-EXT-GDRIVE-001`.
