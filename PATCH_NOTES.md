# PATCH NOTES — RADIATION_PATCH_2026-09-13_2300_Courses-Region-and-Containment.zip
**Risk class:** 🟢 ORDINARY (no constitutional text, no core scaffold, no mode definition, no Scan rule touched)
**Pre-merged. Extract over the repository root, then run `APPLY.ps1` (or `APPLY.sh`).**
**Version:** v1.6.3 → **v1.6.4** *(bump applied by the Commander after review — see §7)*
**Validator:** 22 checks / 5 fail → **23 checks / 16 pass / 3 warn / 4 fail** — *the 4 remaining fails are pre-existing and are NOT this patch's (see §5)*

---

## 1 · WHAT THIS PATCH IS FOR

Commit `4a98e59` ("Add course calendars and materials") pushed 11 files into `Brain/courses/`. Three of the intentions were right — the region, the material, the instinct to feed the system the term — but the **layer** was wrong: **vehicles and identifiers were committed where records belong**, including **one live credential in a public repository.**

This patch does four things, in one coherent purpose: **make the courses push lawful, safe, and usable.**

1. **Containment** — the credential and the identifying vehicles leave the tree (backed up locally first).
2. **The `.gitignore` that should have existed from day one** — so the class cannot recur by accident.
3. **The `Brain/courses/` region rebuilt as records** — `INDEX.md` + six course records extracted from the documents that were read in full.
4. **A validator check that makes the failure class un-recommittable** — check 2.5.

---

## 2 · 🔴 THE CONTAINMENT — AND WHAT THIS PATCH DOES *NOT* FIX

`Brain/courses/0_CALLENDER/ics.txt` (101 bytes) contained a **live LMS external-calendar feed URL** — the institution's Blackboard host, the `/calendarFeed/` path, and a per-user token. *(Redacted here on purpose: a patch document is not a place to reproduce a credential. See commit `4a98e59`.)* Per the platform's own documentation, anybody holding that URL can read the Commander's course calendar. **The repository is public.**

### ⚠️ THE PATCH REMOVES THE FILE. IT DOES NOT REVOKE THE URL.
An earlier message (MSG_04) named the correct remedy and it remains the Commander's action, not the Architect's:

> **ROTATE THE FEED AT SOURCE** — disable the external-calendar feed in the LMS, then re-enable it to mint a new URL.
> **Until that is done, the exposure is open regardless of what this patch removes.**

A record was created for the rotation date in `Brain/courses/INDEX.md` §"OPEN ACTION", currently reading **pending**. **Fill it in.** An unrecorded security action is indistinguishable from an unperformed one.

### 2.1 DELETION LIST — 11 vehicles (backed up, never destroyed)
`APPLY.ps1` **moves** these to `_local_backup/` (repo-relative, structure preserved) **before** removing them from the working tree. Nothing is deleted outright; the working copies survive on the Commander's machine, which `git rm` alone would not have guaranteed.

```text
Brain/courses/0_CALLENDER/ics.txt                     ← the credential
Brain/courses/0_CALLENDER/readme.txt
Brain/courses/desktop.ini                              ← Windows shell metadata
Brain/courses/SCHEDULE.png                             ← identifying timetable
Brain/courses/AR153P_BUILDING_UTILITIES_2/syllabus for this course is not ava.txt
Brain/courses/AR163-1P_BUILDING_TECHNOLOGY/syllabus for this course is not ava.txt
Brain/courses/AR173-1P_PLANNING_2/syllabus for this course is not ava.txt
Brain/courses/AR173-1P_PLANNING_2/AR173-1P (…)-CLASS SCHEDULE.pdf
Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx
Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx
Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html
```
The three `syllabus…txt` stubs are AP-06's class (placeholder records): a file whose content is *"not available"* carries no information. The fact belongs in the course record's GAP log, where it now is.

**The script moves every non-`.md` file under `Brain/courses/` and prunes the emptied directories** — a rule, not a list, so a re-push of the same shape is caught by construction.

### 2.2 🔴 STILL OPEN — history, and it is the Commander's call
The deletion above fixes the **tree**. The blob remains in history at `4a98e59`. Three options were presented in MSG_04 and **none has been chosen**; this patch deliberately does not choose:

| | Option | Effect |
|---|---|---|
| **A** | Leave history | Fastest. Exposure persists in every clone and cache |
| **B** | `git filter-repo` purge + force-push | Blobs gone from fresh clones; hashes rewrite from `4a98e59`; cannot recall clones already taken |
| **C** | **Make the repository private** | Stops further spread. **Correct for a repo that now holds a student's academic records** |

Neither B nor C substitutes for the rotation. **Architect's recommendation: rotate (now) + C (then decide B).**

---

## 3 · WHAT WAS BUILT

### 3.1 `.gitignore` — NEW (root)
Four blocks, each reasoned in the file: **credentials** (`*ics.txt`/`*.ics`/`schedule/`) · **vehicles** (`*.pdf`/`*.docx`/`*.html`/`*.png`/`desktop.ini`/`syllabi/`) · **archives** (`*.zip` — patches are transported, not stored) · **noise**. The vehicle block also **implements II.6's delete-the-binary rule at the tooling layer**: a fetched binary that is ignored cannot be committed by accident.

### 3.2 `Brain/courses/` — REBUILT AS RECORDS
```text
Brain/courses/INDEX.md      the register + the region's 8 rules + the load finding
Brain/courses/GED103.md     K-CUR-007   from the syllabus, read in full
Brain/courses/DSS10.md      K-CUR-008   from the syllabus, read in full
Brain/courses/MEC30-7.md    K-CUR-009   from the course calendar, read in full
Brain/courses/AR173-1P.md   K-CUR-010
Brain/courses/AR163-1P.md   K-CUR-011
Brain/courses/AR153P.md     K-CUR-012
```
Every record carries: meeting pattern (days/times only), graded items with weights **and locators**, a week-by-week sequence, answering K-IDs, and a GAP log. **No personnel, no section, no room, no URL.**

**Region rule 6 is new and resolves a layering problem the patch itself uncovered:** a **course-object row** (`K-CUR-007…012`) describes a course; a **material-set row** (`K-CUR-001…006`, pre-existing) describes lecture/reviewer material attached to one. They cross-link; neither replaces the other.

### 3.3 `scripts/validate.py` — CHECK 2.5 ADDED (tooling, 🟢)
```text
check 2.5  Brain/courses/ records-only + no identifiers
  · non-.md file under the region            → FAIL
  · any URL                                   → FAIL
  · instructor name after a role label        → FAIL
  · contact detail                            → FAIL
  · room code (S3xx / NW4xx / SW2xx)          → FAIL
  · section code after a label                → FAIL
  · the exact tokens published in 4a98e59     → FAIL  (deny-list)
```
Derived from the **observed incident**, not from imagination — it fails the precise shapes that were published on 2026-09-13.

**Deliberate-break proof, pasted (on the patched tree):**
```text
PROOF 1 — clean state:      ✅ PASS [check 2.5]
PROOF 2 — plant "Instructor: Maria Santos":
      ❌ FAIL [check 2.5] … AR153P.md (instructor name: Instructor: Maria Santos)
PROOF 3 — plant "Meet in S300.":
      ❌ FAIL [check 2.5] … DSS10.md (published token: S300); (room code: S300)
PROOF 4 — drop SCHEDULE.png back in:
      ❌ FAIL [check 2.5] … SCHEDULE.png (non-markdown vehicle)
PROOF 5 — restore:          ✅ PASS [check 2.5]
```

### 3.4 Registries & ledgers — APPENDED
`docs/KNOWLEDGE_REGISTRY.md` +6 rows (**K-CUR-007…012**) · `Brain/frontal_lobe/task_ledger.md` +1 real-filename row · `docs/PATCH_LEDGER.md` +1 row. No placeholder identifiers.

---

## 4 · 🔍 THE FOUR FINDINGS THE WORK PRODUCED (it found more than it built)

1. **⭐ The material already existed — and the registry is what proved it.** The first draft of these records said all three architecture courses were *BUILD-REQUIRED, no material held*. **That was wrong.** The registry's existing `K-CUR-001…006` rows showed: `AR173-1P` has an **ingested** lecture set + an audited reviewer + **K-MOD-001 (L4)** + a forged drill set; `AR163-1P` has a **50-file deck set (601 MB)**; `AR153P` has **14 PDFs including Fajardo and PEC material**. Both latter sets are *manifested, never ingested*. **The bottleneck this term is INGESTION, not acquisition** — and the highest-yield course in the term is the best-supplied course in the system. The correction is recorded in `AR173-1P.md` and `INDEX.md`, not silently edited.

2. **⭐ A registry gap: NSCP 2015 is held but unregistered.** The National Structural Code sits in the Law collection (~1,022 MB, logged as the first >1 GB file) but has **no `K-STD` row** — so it is **invisible to the yield-ranked build order**, despite governing two of the term's three high-yield courses. Cheap to close; flagged in `AR153P.md` and `AR163-1P.md`.

3. **A genuine instrument hole: the Revised National Plumbing Code is not held.** The electrical side is covered (PEC material inside `K-CUR-005`); plumbing is not. The only real acquisition task the term produced — and it is **scoped to plumbing only** (an earlier draft of the record overstated it as covering the whole course; corrected in place).

4. **GED103 classifies one assessment AI-PROHIBITED.** The syllabus defines *AI-Prohibited / AI-Assisted / AI-Integrated* per task and marks **AT1 = AI-Prohibited**. The record draws the line explicitly: **drilling the Commander on subject matter is a different act from producing his submission.** Recorded so no future session blurs it.

**Plus one process finding worth keeping:** **the validator caught two defects in this patch's own work.** (a) The first draft of `K-CUR-001…006` **collided with existing rows** — the validator's duplicate-K-ID check caught it, and the registry's frozen-domain rule required renumbering to `K-CUR-007…012`. (b) The first version of check 2.5 **failed the course records that state the exclusion**, because it flagged the bare word *instructor*, and then **failed on `S001`** — a session ID matching the room pattern. Both were fixed in the check, not exempted around it. **The rule was corrected three times; the content was never excused.**

---

## 5 · VALIDATOR STATE — HONEST REPORT

```text
BEFORE (4a98e59):        22 checks · 14 pass · 3 warn · 5 fail · exit 1
AFTER (this patch):      23 checks · 16 pass · 3 warn · 4 fail · exit 1
```

| Check | Before | After | Whose |
|---|:--:|:--:|---|
| **2** required files | ❌ `Brain/courses/ lacks README/INDEX` | ✅ **PASS** | **fixed by this patch** |
| **2.5** records-only + identifiers | *(did not exist)* | ✅ **PASS** | **added by this patch** |
| 1 internal paths | ❌ 2 refs | ❌ 2 refs | pre-existing (carriers) |
| 3 transport artifacts | ❌ 18 carriers | ❌ 18 carriers | **pre-existing — NOT this patch** |
| 3.5 core/ closed set | ❌ | ❌ | pre-existing |
| 8 derived-count drift | ❌ | ❌ | pre-existing |
| 15 boot bytes | ✅ 33,848 B | ✅ **33,942 B** | +94 B (one ledger row) — **well under the 40 KB cap** |
| 16 meta-budget | ⚠️ 15 🟠 | ⚠️ **15 🟠 — unchanged** | **this patch adds ZERO canon** |
| 17 registry | ✅ 29 K-IDs | ✅ **35 K-IDs** | +6, **no duplicates** |

**This patch is not the reason CI is red, and it cannot make CI green.** The four remaining failures are the 18 carriers awaiting the Commander's explicit purge authorization, plus three pre-existing carrier-derived findings. **Bundling that purge into this patch would have violated II.7.4 — one patch, one coherent purpose.**

---

## 6 · FILES IN THIS PATCH

```text
NEW       .gitignore                                  ⚠️ dotfile — confirm your extractor kept it
NEW       Brain/courses/INDEX.md
NEW       Brain/courses/GED103.md      K-CUR-007
NEW       Brain/courses/DSS10.md       K-CUR-008
NEW       Brain/courses/MEC30-7.md     K-CUR-009
NEW       Brain/courses/AR173-1P.md    K-CUR-010
NEW       Brain/courses/AR163-1P.md    K-CUR-011
NEW       Brain/courses/AR153P.md      K-CUR-012
CHANGED   docs/KNOWLEDGE_REGISTRY.md                  +6 course-object rows
CHANGED   scripts/validate.py                         +check 2.5 (v3)
CHANGED   Brain/frontal_lobe/task_ledger.md           +1 row
CHANGED   docs/PATCH_LEDGER.md                        +1 row
CARRIED   APPLY.ps1 · APPLY.sh                        runners — do not commit these
CARRIED   PATCH_NOTES.md                              inside the zip only (II.8.2)
```

---

## 7 · ON APPLICATION — THE COMMANDER'S RUNNER

```powershell
# from the repository root, after extracting this zip over it
.\APPLY.ps1
```
It will: verify the repo root → **back up every non-`.md` file under `Brain/courses/` to `_local_backup/`** → copy the patch files into place → prune the emptied directories → re-run `validate.py` → print the git commands. **It does not commit.** Review, then:

```bash
git add -A && git commit -m "P-10 Phase 0: courses region as records + containment"
```
**Then, and separately:** bump version to v1.6.4 in `README.md`, `docs/SYSTEM_STATE.md`, `CHANGELOG.md` (check 7 compares all three — they must move together).

**Not yet done, and deliberately so:**
- 🟠 **The 18-carrier purge** — separate patch, needs one word from the Commander.
- 🟠 **Tier B autonomy** and the **`.readme` scope clause** — staged, per MSG_03 §6.
- **Rotation of the LMS feed** — Commander's action, §2.
- **History option A/B/C** — Commander's ruling, §2.2.

---

## 8 · EVAL-FIRST (the clause, applied to this patch)
| | |
|---|---|
| **INSTANCE** | `4a98e59`: 11 vehicles + 1 credential committed to a public repo; `Brain/courses/` failed check 2; no `.gitignore` existed |
| **COST** | +8 files, +94 boot bytes, +1 check, **0 canon changes, 0 new modes, 0 new mandatory boot files** |
| **DISPLACEMENT** | Removes 11 tree artifacts and closes a live credential. Region reuses the `external_sources/INDEX.md` pattern — no new structure invented |
| **CHECK** | **check 2.5, proven by four deliberate breaks** (pasted above). The rule that would have stopped `4a98e59` now exists and is tested |

---

## 9 · ONE LAST THING — A RULE FOR THE NEXT PUSH

> **If an artifact cannot be expressed as a record of an extract, it does not enter the repository.**
> The region holds what the Commander **knows**; the vehicles stay on his machine.

Written into `Brain/courses/INDEX.md` as rule 1 and enforced by check 2.5 — so the next push of syllabi, screenshots, or links fails CI **before** it becomes a public record, rather than after.
