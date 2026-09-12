# PATCH NOTES — RADIATION_PATCH_2026-09-13_2340_Term-Planner.zip
**Risk class:** 🟢 ORDINARY — no constitutional text, no core scaffold, no mode definition, no Scan rule
**Pre-merged. Extract over the repository root.**
**Applies on top of** `RADIATION_PATCH_2026-09-13_2300_Courses-Region-and-Containment.zip` (this patch ships the same `.gitignore` and the same `validate.py` with both patches' checks — **either apply order works; the later patch wins on shared files**).
**Validator:** 23 → **25 checks · 17 pass · 4 warn · 4 fail** — *all four remaining FAILs are pre-existing carriers, not this patch's (see §5)*

---

## 1 · WHAT THIS IS

**P-10 Phase 1–3: the term planner.** The mechanism that converts an academic deadline into a study session — which the system has never had, and whose absence is AP-07 (*"0 Core cards after 4 sessions; 15 🟠 patches against 3 content sessions"*).

It is **not** a new mode, a new scaffold, or a boot-set member. It is a script, a register, a routine, and five cue rows.

| # | Artifact | Purpose |
|---|---|---|
| 1 | `scripts/plan_term.py` | the planner — stdlib only, no network |
| 2 | `Brain/short_term/plan/TERM1_DEADLINES.json` | the term register (K-REF-003), derived from the course records |
| 3 | `Brain/short_term/plan/README.md` | region doc — the rules and the wait-list |
| 4 | `Brain/cerebellum/routines/routine_term-briefing.md` | the procedure (STAGED, write-after-proof pending) |
| 5 | `cue/autopilot-cues.md` | **append** — 5 term cues, into the existing registry |
| 6 | `scripts/validate.py` | **+check 20** (plan integrity + privacy) · **+check 20.5** (AP-08 guard) |
| 7 | `docs/KNOWLEDGE_REGISTRY.md` | **+K-REF-003** |
| 8 | `.gitignore` | `*.local.*` + `_local_backup/` (see §4 — this closed a hole in the previous patch) |

---

## 2 · WHAT IT DOES

```bash
python3 scripts/plan_term.py --week 4                  # the brief
python3 scripts/plan_term.py --week 4 --ics <local.ics> # + feed delta
python3 scripts/plan_term.py --self-check              # register integrity
python3 scripts/plan_term.py --audit                   # plan-vs-attempt ratio
```

**Real output, week 10, in the current state:**
```text
  TERM BRIEF — Term 1, AY 2026-2027 · week 10 of 11
  dates    : ANCHOR ABSENT — planning in WEEKS (no syllabus prints a date).
  ─ RANKED LOAD (this week + next) ─ top 3 of N ─
   1. [ 22.5] MEC30-7 — Q3            THIS WEEK · weight UNKNOWN
        why: yield 5 x proximity 3.0 x deficit 1.5 (no mastery row)
   2. [ 22.5] MEC30-7 — Coursera PR5 + certificate
   3. [ 15.0] MEC30-7 — Final exam + course portfolio   NEXT WEEK
  ─ MASTERY CLOCK ─ (reconciliation against Brain/frontal_lobe/mastery_ledger.md)
  ─ UNPREPARABLE / BUILD-REQUIRED ─
    AR173-1P (yield 9): HIGHEST-YIELD COURSE OF THE TERM IS DEADLINE-BLIND
  ─ NOT BEING PREPARED, AND WHY ─
```

**The core algorithm** — `priority = yield × proximity × deficit`, and the arithmetic is printed with every row. Six courses, one student, ~6 usable hours: **a full list is not a triage, so it shows top 3.**

**Two clocks, reconciled — never merged:**
- **deadline clock** → the register + the ICS
- **mastery clock** → `mastery_ledger.md`, which computes its own `next_review` from error categories

The reconciliation rule: place review so the last one lands **D-3…D-1** before an assessment; **pull the ledger's date forward** if it would fall after one; and when **no knowledge object exists**, emit **`BUILD-REQUIRED`** rather than a review date. *An unsatisfiable reminder is a defect, not a plan.*

**The ICS layer works and is proven.** It parses the feed, **scrubs every identifier before anything touches disk**, and reports **movement** — the one genuinely actionable line a schedule system can produce:
```text
  ─ LMS FEED ─ 3 event(s) parsed, summaries scrubbed of identifiers
    added 0 · moved 1 · removed 0
    ⚠ MOVED  MEC30-7 Q1 Quiz: 2026-09-23 → 2026-09-18
```
Proof of scrubbing, read back off the snapshot file on disk:
```text
"summary": "AR153P Deadline [SECTION REDACTED]"
"summary": "Consultation w/ Instructor [INSTRUCTOR REDACTED] at room [ROOM REDACTED]"
```

---

## 3 · THE HONEST LIMIT — RUNG 2 OF 4

The routine defines a four-rung degradation ladder. **This patch delivers a working rung 2, and says so:**

| Rung | Have | State |
|:--:|---|---|
| 4 | anchor + ICS + records | — |
| 3 | anchor + records | — |
| **2** | **records only** | ⬅ **shipped, working** |
| 1 | partial records | — |
| 0 | no register | — |

**What that means concretely:** it knows a Q1 lands in week 4, a Q2 in week 7, a Q3 and the Coursera certificate in week 10, finals in week 11 — **and it knows the three highest-yield courses are invisible.**

> **⚠ THE FINDING THAT MATTERS MOST: the planner is blind exactly where the yield is highest.**
> AR173-1P (yield 9), AR163-1P (8), AR153P (8) — no syllabus, so no graded items, so no triage. The three courses that carry the ALE are the three the planner cannot see.
>
> **That is a data gap, not a build gap.** The machinery is finished. One missing datum (*the week-1 anchor*) converts the whole term from weeks to dates; three missing syllabi restore deadline-awareness where it counts.

**Waiting on, and all four are data not code:** `week1_start` · the LMS ICS (local, git-ignored) · the three AR syllabi · MEC30-7's weights.

---

## 4 · TWO HOLES THIS PATCH CLOSED IN ITS OWN PREDECESSOR

**4.1 `.gitignore` missed the planner's own output.** The Phase-0 ignore file covered `*.local.md` but **not** `*.local.json` — and the ICS snapshot is a `.json`. Fixed: `*.local.md`, `*.local.json`, and `Brain/short_term/plan/*` variants are all ignored. **Verified:** `git check-ignore -v` resolves `Brain/short_term/plan/ICS_SNAPSHOT.local.json` to `.gitignore:40`.

**4.2 The validator was scanning `_local_backup/`.** The Phase-0 apply script re-homes 11 vehicles into `_local_backup/`. But `validate.py` walked the whole tree, so **the local scratch folder was being linted** — check 1 failed on a path inside the PATCH_NOTES the script had just archived there. A local, git-ignored folder must never fail CI. Fixed in **both** patches: every `os.walk` now skips `_local_backup`, and it is added to `.gitignore`. *(Found by running the patches together, not by reading them.)*

**4.3 The example above is the point.** Neither hole was visible in either patch alone. **Both surfaced only when the two were applied in sequence and validated** — which is the standard this campaign exists to enforce, applied to its own output.

---

## 5 · VALIDATOR STATE — HONEST REPORT

```text
baseline  (4a98e59):                22 checks · 14 pass · 3 warn · 5 fail
after Courses-Region-and-Containment: 23 checks · 16 pass · 3 warn · 4 fail
after THIS patch:                   25 checks · 17 pass · 4 warn · 4 fail
```

| Check | State | Owner |
|---|:--:|---|
| 2 required files | ✅ PASS | previous patch |
| 2.5 records-only + identifiers | ✅ PASS | previous patch |
| **20 term plan integrity** | ✅ **PASS** | **this patch** |
| **20.5 planner-theater guard** | ⚠️ WARN | **this patch — and it is CORRECT** |
| 1 · 3 · 3.5 · 8 | ❌ | **pre-existing carriers** — untouched, awaiting the Commander's purge authorization |

**On check 20.5 firing on day one — that is the check working, not failing.** It warns that a plan exists and the last three ledger rows record no attempt. It is right. **The metric is drills executed, never plans generated.** It clears the moment a genuine attempt is logged.

**Boot bytes:** 34,138 B Tier0+1 (cap 40 KB) · 57,264 B Tier0–2 (cap 80 KB). **+196 B** — one ledger row. The routine is reached at **Tier 3** (`docs/.readme` §3 already lists *cerebellum routines*), so **no tier amendment and no boot-set member were added.**
**🟠 count: 15 → 15. This patch adds ZERO canon.**

### 5.1 Deliberate-break proof for check 20 (pasted)
```text
PROOF 1 — clean:                         ✅ PASS [check 20] term plan integrity
PROOF 2 — URL in the register:           ❌ FAIL … URL in term register; URL/credential in term register
PROOF 3 — "Instructor: Maria Santos":    ❌ FAIL … instructor name in term register
PROOF 4 — week 99:                       ❌ FAIL … week out of range MEC30-7 W99
PROOF 5 — k_id K-CUR-999 (unregistered): ❌ FAIL … unknown k_id K-CUR-007
PROOF 6 — restore:                       ✅ PASS [check 20] term plan integrity
```

### 5.2 🔴 AND THE VALIDATOR CAUGHT ME AGAIN
The first draft of this register used **`K-REF-001`** — which is **already taken** (UAP Documents 200–208; `K-REF-002` is the Bentley annotation). **Check 17 failed the duplicate**, and the frozen-domain rule required renumbering to **`K-REF-003`**.

That is the **second ID collision the validator has caught in my work** in two patches (`K-CUR-001…006` were the first). The rule was corrected; the content was not excused. Recorded here rather than quietly renumbered.

---

## 6 · DELIBERATELY NOT INCLUDED

| Not included | Why |
|---|---|
| **Tier B autonomy** (self-initiating at session-open) | Extends `autopilot-doctrine.md` §2's **closed list of seven** → 🟠. Arrives instead as a 🟢 doctrine refinement **after three logged runs**, per the doctrine's own §7 growth rule |
| **`@Drill` handoff** | P-05 not ratified. The routine hands off to **`@Review`** — ratified 2026-09-12 — and upgrades on ratification. *The drill set and grader already exist; P-05 supplies the charter, not the machinery* |
| **The GitHub Action (Phase 4)** | Needs the Commander's ICS secret, and Phase 4 follows a proven Phase 1–3 |
| **The 18-carrier purge** | Separate patch, separate authorization, separate purpose (II.7.4) |
| **A new cue file** | Would require editing `docs/CUE_SYSTEM.md` §5 — which is law. Cues append to the existing registry instead |
| **A new scaffold** | `scaffolding/core/INDEX.md`: additions arrive only via `improved/` → 🟠. The scaffolds this needs already exist as staged proposals |

---

## 7 · FILES

```text
NEW       scripts/plan_term.py
NEW       Brain/short_term/plan/TERM1_DEADLINES.json
NEW       Brain/short_term/plan/README.md
NEW       Brain/cerebellum/routines/routine_term-briefing.md
CHANGED   cue/autopilot-cues.md                       +5 term cues (append)
CHANGED   scripts/validate.py                         +check 20, +check 20.5, +_local_backup exclusions
CHANGED   docs/KNOWLEDGE_REGISTRY.md                  +K-REF-003
CHANGED   .gitignore                                  +*.local.* and +_local_backup/
CHANGED   Brain/frontal_lobe/task_ledger.md           +1 row (real filename)
CHANGED   docs/PATCH_LEDGER.md                        +1 row
CARRIED   PATCH_NOTES.md                              zip-only (archived out of the tree on apply)
```

---

## 8 · NEXT

1. **Rotate the LMS feed** — still open from the previous patch, still Commander-only.
2. **Purge the 18 carriers** — one word, and CI goes green.
3. **Supply `week1_start`** — one date, and the whole term becomes dated.
4. **Drill something.** Check 20.5 is warning for a reason; the register is finished and the first genuine `mastery_ledger` row is the only thing that turns a plan into progress.

---

## 9 · EVAL-FIRST (the clause, applied)
| | |
|---|---|
| **INSTANCE** | AP-07: 0 Core cards after 4 sessions; 15 🟠 vs 3 content sessions; no mechanism converted a deadline into a session |
| **COST** | +4 files, +196 boot bytes, +2 checks, **0 canon, 0 new modes, 0 boot-set members, 0 new scaffolds** |
| **DISPLACEMENT** | Removes nothing; **depends entirely on existing machinery** — P-06's yield rubric, P-05's drill set and grader, P-03's registry, the cerebellum routine folder. *If it could not be built on those four, it should not have been built* |
| **CHECK** | **check 20, proven by five deliberate breaks** (pasted §5.1). Check 20.5 measures the failure mode (AP-08) rather than assuming it away |
