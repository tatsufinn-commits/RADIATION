# 📅 TERM PLAN (`Brain/short_term/plan/README.md`)
## Derived, regenerable, and partly un-committable by design
**Version:** 1.0 | **Basis:** P-10 Phase 1–3 | II.6 (short_term = working memory)

---

## WHAT LIVES HERE

| File | Committed? | Why |
|---|:--:|---|
| `TERM1_DEADLINES.json` | ✅ **yes** | Machine view of what the course records state — week numbers, assessment types, weights. **Contains no personnel, no section, no room, no URL** (enforced by validator check 20). |
| `README.md` | ✅ yes | this file |
| `*.local.md` (generated briefs) | ❌ no — git-ignored | May carry coursework detail; regenerable at will |
| `ICS_SNAPSHOT.local.json` | ❌ no — git-ignored | The feed fingerprint used for delta detection |
| the `.ics` itself, and its URL | ❌ **never** | The URL is a credential. A local copy is fine; a committed one is not. |

---

## THE RULES

1. **This region is derived, not canonical.** `TERM1_DEADLINES.json` is a *parseable projection* of `Brain/courses/*.md` — it exists so the planner does not have to parse markdown. **The course records are the authority.** If the two disagree, the record wins and the JSON is wrong. Regenerate it when a record changes.

2. **Nothing here is citable evidence.** It is schedule data. It appears in no deliverable, carries no grade, and proves nothing.

3. **Two clocks, never merged.**
   - **Deadline clock** — course records → `TERM1_DEADLINES.json` (+ the ICS once rotated).
   - **Mastery clock** — `Brain/frontal_lobe/mastery_ledger.md`, which computes its own `next_review` dates from error categories.
   The planner **reconciles** them: it places review so the last one lands **D-3 … D-1** before a deadline, and pulls a ledger date forward when it would otherwise fall *after* the assessment. **It never overwrites the ledger's schedule.**

4. **No module ⇒ BUILD-REQUIRED, never a review date.** A course with no knowledge object cannot be drilled. The planner emits `BUILD-REQUIRED` and routes it to the inter-term build window (P-10 §2) instead of nagging.

5. **Week numbers, not dates — until the anchor arrives.** No syllabus in the Term-1 capture prints a calendar date; they print *"W4"*. So the planner works in weeks and says so. **One datum (`week1_start`) converts the whole term to dates.** Either supply it (`--anchor YYYY-MM-DD`) or let the LMS ICS supply it.

6. **The ICS is a change-detector, not a source of truth.** It carries only items a professor attached a due date to; syllabus-only deadlines never appear, and the refresh lags ~a day. Its real job is to tell you **something moved** — `moved 1: PD 1096 midterm W6 → W5`.

7. **Measure attempts, never plans.** A brief that is read and not acted on is planner theater (AP-08). `plan_term.py --audit` reports it, and validator check 20.5 WARNs. **The metric is drills executed, not plans generated.**

---

## USAGE

```bash
python3 scripts/plan_term.py --week 4                    # the brief, as of week 4
python3 scripts/plan_term.py --week 4 --ics ~/schedule/bb.ics
python3 scripts/plan_term.py --self-check                # register integrity
python3 scripts/plan_term.py --audit                     # plan-vs-attempt ratio
```

---

## 🚩 WHAT THIS REGION IS WAITING FOR

| Datum | Effect once supplied |
|---|---|
| **`week1_start`** (one date) | every week number becomes a calendar date |
| **the LMS ICS** (local, git-ignored) | delta detection: moved/added/cancelled assessments |
| **the three missing AR syllabi** | restores deadline-awareness to the three highest-yield courses — **currently the planner is blind exactly where the yield is highest** |
| **MEC30-7 weights** | lets its quizzes be ranked against each other rather than merely dated |

**None of these is a build task.** The machinery is finished; it is waiting on data.
