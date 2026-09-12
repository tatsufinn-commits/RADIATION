# PROPOSAL P-04 — Source Tiers, IP & Access (II.6 rules 8–9) · ratify: "ratify P-04"
**Re-homed 2026-09-12 (Wave 1&2 closure): carriers moved from canonical dirs to lawful proposal homes per IV.2/IV.4/scaffolding-README §4. Text unchanged except path-reference hygiene. NOTHING below is applied until the Commander's ratification line.**


---
## ◈ Amendment rows + II.6 side-by-side

# 📜 STAGED AMENDMENT — II.6 RULES 8 & 9 (P-04)
**Status:** 🟠 STAGED — enters `docs/AI_RULES.md` only on "ratify P-04".
Staged in a carrier file per the P-02 precedent: appending pre-ratification
rows to the live Amendment Log would violate IV.3 (see P-02 Challenge).

## A. SIDE-BY-SIDE (II.7.8 format)

### OLD — II.6 Restraint Doctrine, rule 4 (current canon, verbatim)
> 4. **One-at-a-time** — open, extract, write findings to the collection's DIGEST, release; never hold multiple large files simultaneously.

### NEW — rule 4 (amended; strike-through per IV.3)
> 4. **One-at-a-time** — open, extract, write findings to the collection's DIGEST, ~~release~~ **and delete the fetched binary (rule 8)**; never hold multiple large files simultaneously.

### NEW — rules 8 and 9 (appended after rule 7)
> 8. **DELETE-THE-BINARY.** After an extract is written to the DIGEST (or to `Brain/short_term/ingest/`), the fetched binary is deleted in the same step. Reason: workspace snapshots and session context are finite; a persisted PDF is a cost every future session pays for. Every ingestion logs bytes reclaimed. Retaining a binary requires a stated reason in the ACCESS LOG (e.g. "image-only; OCR pending — retained for next session").
> 9. **COPYRIGHT POSTURE.** Material is used, never appropriated. Government issuances may be stored in full. Paid or copyrighted standards are cited by clause and **never reproduced verbatim** beyond fair quotation; where a value must be stated, the governing equivalent standard may be cited alongside. Textbooks are links-only. Every collection carries a COPYRIGHT & ACCESS block, and a session that cannot determine a collection's posture records `unknown` and applies EXTRACT-ONLY behaviour.

## B. RATIONALE (including the II.4 interplay — stated, not swallowed)
- Rules 1–7 governed navigation and budget but stopped one step short of the
  bytes: rule 4 said "release," never "delete." S003 pulled 205.2 MB and the
  recorded lesson was about pricing the fetch, not disposing of it.
- **II.4 interplay (Non-Destructive Mandate):** II.4 protects raw sources and
  prior outputs *held by the system* — repo files, Brain holdings, collection
  originals. A fetched binary is a session-local transient COPY; the original
  remains in the Commander's collection, and the extract remains in the Brain.
  Rule 8 deletes the copy, never the source. This interpretation is recorded
  here so no future session reads rule 8 as licence to delete holdings — any
  such deletion stays 🔴 under the (separately staged) IV.6 classes.
- Rule 9 exists because the catalog lists ASEP-copyrighted NSCP 2015 (1,022 MB),
  Ching, Time-Saver, Banister Fletcher, Fajardo and lecturer decks — a legal
  posture, not a nicety. Demonstrated live 2026-09-12: BP 344 statute ingested
  from LawPhil, extract kept, binary deleted, 6,277 bytes reclaimed.

## C. AMENDMENT LOG ROWS (IV.3 format — signature blank until ratified)
| Date | Book.Law | Change | Rationale | Commander signature |
|---|---|---|---|---|
| ____ | II.6 | Restraint Doctrine rule 4 amended (delete-the-binary cross-ref); rules 8 (DELETE-THE-BINARY) and 9 (COPYRIGHT POSTURE) appended | P-04: sourcing posture made explicit, legal, and cheap in bytes; II.4 interplay recorded (transient copies ≠ held sources) | ______________________ |
| ____ | II.6 annex | Every external collection carries a COPYRIGHT & ACCESS block (form + nine retrofits); docs/SOURCE_TIERS.md enters canon; tier-down default and Tier-3/4 [O]-cap made law | P-04: "tier" defined; scout's vocabulary grounded; TAMAKEE §§16–21 posture ported | ______________________ |


---
## ◈ SOURCE_TIERS (becomes docs/SOURCE_TIERS.md)

# 🪜 SOURCE TIERS (docs/SOURCE_TIERS.md)
## The Authority Ladder, Evaluation Axes & Tier-Down Default
**Status:** 🟠 STAGED — becomes canon only on Commander ratification of P-04
**Constitutional basis:** I.2 (taxonomy), II.6 (Restraint Doctrine), III.8 (Scout's Gate)
**Origin:** TAMAKEE Master Directive §§16–20, ported per Commander directive P-04
**Referenced from:** `subskills/active/scout.md` §3/§5 · `docs/STOCKPILE_DOCTRINE.md` §3–4

## 1. THE TIER LADDER
"Tier" was undefined vocabulary in scout and the Stockpile Doctrine until this
file. Tier = **provenance**, never usefulness (a Tier-3 lecture deck can be
exam-decisive — see the curriculum-authority principle, P-07 territory).

| Tier | Definition | RADIATION examples | Grade ceiling (I.2) |
|---|---|---|---|
| **TIER-1 — Official** | Government/regulator text; the code's own words; the curriculum's own document | PD 1096 IRR (DPWH), RA 9514 RIRR (BFP), BP 344 IRR, RA 9266, CHED CMO 61 s.2017, DHSUD issuances | `[D]` |
| **TIER-2 — Credentialed** | Peer-reviewed papers; textbooks by recognised publishers/authorities; professional-body documents | UAP Docs 200–208 / SPP, NSCP (ASEP), Ching, Time-Saver, Banister Fletcher | `[R]` / `[D]` for what it itself states |
| **TIER-3 — Institutional secondary** | Reviews, lecture material, study guides, recognised encyclopaedias | Mapúa lecture decks (exam-authoritative — P-07), Pritzker profiles, Britannica | `[O]` → elevatable to `[D]`-as-taught |
| **TIER-4 — Community** | Forums, social media, student-uploaded material, blogs, Q&A sites | Studocu/CourseHero uploads, Reddit, YouTube tutorials | `[O]`/`[N]` cap (I.2) |
| **TIER-X — Unverifiable** | No traceable publisher or author | content farms, grokipedia | `[N]` max; never cited as support |

## 2. EVALUATION AXES (seven — recorded in the Acquisition Plan)
Next to scout's four-part necessity test, each candidate records:
**authority · accuracy · relevance · depth · currency · uniqueness · educational value.**

## 3. SOURCE SCORE
Every candidate gets an explicit short score — 0–10 per axis, or a one-line
composite — recorded in the Acquisition Plan. **Rejected sources keep their
tier and score in the rejection log**: the rejection record is training data.

## 4. DEFAULTS (binding once ratified)
1. **Unsure → tier DOWN.** Never guess upward. (Already scout/curator practice;
   now law.)
2. **Tier-3/4-only coverage → `[O]` cap** until triangulated (I.2), and the
   shortfall is logged (`[STOCKPILE SHORTFALL]` mechanics, III.5).
3. **No tier padding.** Inflating a tier to make a source look stronger is an
   I.1-class falsification of provenance.
4. **Tier is recorded even for rejected candidates** (§3).

## 5. INTERPLAY
- I.2 grade ceilings and tier ceilings are the same wall seen from two sides:
  tier constrains what grade a claim may ENTER at; triangulation (I.3) is
  still the only elevator.
- The Mapúa-deck elevation (`[D]`-as-taught) applies ONLY to claims about
  what the curriculum teaches — not to claims about the world.


---
## ◈ COPYRIGHT & ACCESS blocks ×10

# ©️ STAGED — COPYRIGHT & ACCESS BLOCKS (P-04)
**Status:** 🟠 STAGED. On "ratify P-04": block 0 is appended to
`scaffolding/core/form_external-collection.md` (new template section between
DIGEST and ACCESS LOG); blocks 1–9 are appended to the nine collection files
in `Brain/external_sources/`. Nothing below is applied yet.
No guessed legal claims: unknowns read `unknown`. All `Last reviewed` dates are
real (collection identities reviewed this session, 2026-09-12).

## BLOCK 0 — template addition to `form_external-collection.md`
```markdown
## COPYRIGHT & ACCESS
- Copyright status : public-domain (govt issuance) | licensed | copyrighted-not-held | unknown
- Access mode       : official-portal | Drive-link-only | links-only | recorded-not-held
- Reproduction rule : full-text storage allowed | EXTRACT-ONLY (no verbatim reproduction)
                      | quotes-only (fair use, cite page) | links-only (never store the file)
- Rationale         : <one line>
- Last reviewed     : YYYY-MM-DD
```

## BLOCK 1 → `law.md`
- Copyright status : public-domain (govt issuances) — **EXCEPTION: NSCP 2015 = copyrighted-not-held (ASEP)**
- Access mode       : Drive-link-only
- Reproduction rule : full-text storage allowed for statutes/IRRs (cite rule/section/table) · **NSCP 2015: EXTRACT-ONLY — no verbatim tables; cite clause; where a value must be stated, cite the governing ACI/ASTM equivalent alongside**
- Rationale         : PD 1096/RA 9514/BP 344/PD 957/RA 9266 and their IRRs are government issuances; NSCP is a paid ASEP standard (1,022 MB, catalogued 🛑🛑, never fetched)
- Last reviewed     : 2026-09-12

## BLOCK 2 → `books.md`
- Copyright status : licensed (commercial textbooks: Ching, Time-Saver, Banister Fletcher, Gehl, Jacobs, Lynch)
- Access mode       : Drive-link-only
- Reproduction rule : links-only / EXTRACT-ONLY — quotes + page cites, never the file
- Rationale         : commercial publishers; catalog presence is not a licence
- Last reviewed     : 2026-09-12

## BLOCK 3 → `hoa-reviewers.md`
- Copyright status : unknown (lecturer-authored course material)
- Access mode       : Drive-link-only
- Reproduction rule : EXTRACT-ONLY — no redistribution; page/slide cites
- Rationale         : lecturer decks; ownership not established → unknown + EXTRACT-ONLY per rule 9 default
- Last reviewed     : 2026-09-12

## BLOCK 4 → `toa-reviewers.md`
- Copyright status : unknown (lecturer-authored course material)
- Access mode       : Drive-link-only
- Reproduction rule : EXTRACT-ONLY — no redistribution; page/slide cites
- Rationale         : same class as HOA reviewers
- Last reviewed     : 2026-09-12

## BLOCK 5 → `building-utilities.md`
- Copyright status : unknown/licensed mixed (Fajardo textbooks = licensed; PEC = professional-body; modules = lecturer)
- Access mode       : Drive-link-only
- Reproduction rule : EXTRACT-ONLY — quotes + cites only
- Rationale         : mixed corpus; strictest applicable rule governs the collection
- Last reviewed     : 2026-09-12

## BLOCK 6 → `professional-practice.md`
- Copyright status : mixed — RA 9266 public-domain; UAP Docs 200–208/SPP = professional-body (licensed)
- Access mode       : Drive-link-only
- Reproduction rule : statutes full-text allowed; UAP/SPP documents EXTRACT-ONLY with doc-number cites
- Rationale         : professional-body documents are not government issuances
- Last reviewed     : 2026-09-12

## BLOCK 7 → `planning.md`
- Copyright status : unknown (lecturer-authored modules, AR173-1P)
- Access mode       : Drive-link-only
- Reproduction rule : EXTRACT-ONLY — no redistribution; module/page cites
- Rationale         : lecturer material; ownership not established
- Last reviewed     : 2026-09-12

## BLOCK 8 → `building-technology.md`
- Copyright status : unknown/licensed mixed (proceedings volume 601 MB 🛑; lecturer decks; misc references)
- Access mode       : Drive-link-only
- Reproduction rule : EXTRACT-ONLY
- Rationale         : mixed corpus, strictest rule governs; 601 MB file remains SIZE-SKIPPED territory
- Last reviewed     : 2026-09-12

## BLOCK 9 → `novels.md`
- Copyright status : copyrighted (commercial fiction)
- Access mode       : Drive-link-only
- Reproduction rule : links-only — never store; already governed by fiction-never-evidence (🎭)
- Rationale         : entertainment library; no evidentiary use, no reproduction
- Last reviewed     : 2026-09-12


---
## ◈ STOCKPILE_DOCTRINE line

# STAGED DIFF — `docs/STOCKPILE_DOCTRINE.md` (P-04)
**Status:** 🟠 STAGED — apply on "ratify P-04".

## §3 DEFINITIONS — line appended
NEW: `- **Tier:** provenance rank per docs/SOURCE_TIERS.md (TIER-1 Official … TIER-X Unverifiable). §4's AUTHORITY test states the tier from that ladder; Tier-3/4-only coverage caps claims at [O] until triangulated (I.2).`


---
## ◈ Original patch notes

# PATCH NOTES — RADIATION_PATCH_2026-09-13_0900_P04-Source-Tiers-IP-STAGED.zip
**Risk class:** 🟠 CANON-AFFECTING — ENTIRE PATCH STAGED, NOTHING APPLIED.
Ratify with: **"ratify P-04"**. Directive of record: uploads/P-04_SOURCE_TIERS_AND_IP.md.

## CONTENTS (staged carriers)
1. docs/SOURCE_TIERS_STAGED.md → becomes docs/SOURCE_TIERS.md
2. docs/AMENDMENT_ROWS_STAGED_P04.md → II.6 rule-4 strike + rules 8–9 + IV.3 rows (signature blanks)
3. docs/COPYRIGHT_ACCESS_BLOCKS_STAGED.md → form addition + 9 collection retrofits (unknowns honest)
4. scaffolding/core/proc_ingestion-run_STAGED_DIFF.md → DELETE + LOG step 7
5. subskills/active/scout_STAGED_DIFF.md + docs/STOCKPILE_DOCTRINE_STAGED_DIFF.md → tier-vocabulary wiring

## ON RATIFICATION
Apply 1–5 to live files · move amendment rows into AI_RULES.md Amendment Log ·
delete the *_STAGED* carriers · re-run scripts/validate.py (must stay 15/15) ·
bump version · emit AUTO-PATCH.

## SPLIT DECISION (no-mix rule)
🟢 demonstration evidence (BP 344 demo ingest, CONFLICT_REGISTER first row,
SRC-015, ledger rows) was applied live under II.8.3 (Brain/append-only
registers) and ships as a SEPARATE 🟢 patch:
RADIATION_PATCH_2026-09-13_1000_P04-Demo-Ingestion-Evidence.zip.

## STATED CONFLICTS / DEVIATIONS (none swallowed)
- II.4 vs rule 8: resolved by interpretation (transient session copy ≠ held
  source) — recorded in the amendment rationale, kept visible for ratification.
- Amendment rows staged in a carrier, not appended live: P-02 precedent (IV.3).
- Collection blocks COULD be 🟢 under II.8.3 (Brain is free ground), but they
  implement rule 9 which is not yet law — staged with the canon for coherence,
  per the directive's own classification of items 1–4 as 🟠.
- Demo binary was session-local (LawPhil HTML, 6,277 B): small by design —
  the demonstration proves the STEP, not a stress test. Official Gazette
  returned HTTP 403 this session; LawPhil mirror used, tier-downed to
  TIER-2/credentialed honestly in the ingest sheet.
- Rule 8/9 text is the directive's verbatim; the only addition is the
  cross-reference wording in rule 4's strike-through.

