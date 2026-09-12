# 🔁 ROUTINE — Term Briefing
**Serves:** @Review · @Data · @Autopilot · (upgrade path: @Drill on P-05 ratification)
**Armed by:** the Commander's ask — *"plan my week" · "what's due" · "what's coming"*
**Reachability:** Tier 3 ("as needed") — `docs/.readme` §3 already lists *cerebellum routines*. **Zero boot bytes, no tier amendment.**
**Proof status:** ⏳ **STAGED — write-after-proof pending.** Runs as a 🟢 proposal routine until its first successful execution; promotes to permanent on the first accepted brief (II.6 cerebellum rule).

---

## 0 · SCOPE LIMIT — READ FIRST

**This routine does NOT self-initiate.** It runs when the Commander asks for it.
The standing-orders queue (`cue/autopilot-doctrine.md` §2) is a **closed list of seven**; adding an eighth item that fires on session-open would extend that list and is a **🟠 canon act** (P-10 §8.2). Until the grant is earned — three logged runs, then the doctrine's own §7 growth rule — a booting session may **name** an approaching assessment in its Scan Declaration, and may **propose** the drill. It may not open the leg unprompted.

## 1 · THE RUN, IN ORDER

```text
1. READ   Brain/short_term/plan/TERM1_DEADLINES.json
          → if absent: say so plainly and stop. Never invent a term.
          → if present: note blind_courses — the courses with no data are the finding.
2. READ   Brain/frontal_lobe/mastery_ledger.md            (the MASTERY clock)
3. OPTIONAL  the local ICS via --ics <path>               (the DELTA layer)
          → parse, scrub identifiers, diff against ICS_SNAPSHOT.local.json
          → REPORT MOVEMENT FIRST. "the exam moved" is the single most
            actionable line this routine can produce.
4. RANK   priority = yield × proximity × deficit
              yield      : the course record's ALE yield (1..9)
              proximity  : same week 3.0 · next week 2.0
              deficit    : no mastery row 1.5 · last score <70 1.5 · else 1.0
          → emit TOP 3 WITH THE ARITHMETIC SHOWN. Never a bare list: six courses,
            one student, ~6 usable hours — the output is a TRIAGE.
5. RECONCILE the two clocks
          → for each ranked item with a knowledge object, compare the ledger's
            next_review against the assessment week.
          → ledger review falls AFTER the assessment  ⟹ PULL FORWARD to D-2 and
            log the pull with its reason.
          → no knowledge object exists  ⟹ emit BUILD-REQUIRED. Do NOT emit a
            review date for material that cannot be reviewed.
6. DELIVER the brief:
          · ranked top 3 with reasons
          · any pulled review dates (with the pull amount)
          · any BUILD-REQUIRED
          · ONE line of what is NOT being prepared, and why
          · the honest degradation notice (weeks-only if the anchor is absent)
7. ACT    if the Commander says drill → hand off.
          → LAWFUL NOW: @Review (Brain-first recall/refresh — ratified).
          → ON P-05 RATIFICATION: @Drill (Socratic / distractor / recall-first).
            The drill set SET-PD1096-VIII-001 and its grader already exist; what
            P-05 supplies is the mode charter, not the machinery.
          → declare the chain per III.2 if more than one leg runs.
8. RECORD cue/inference-log.md + the session episode.
          → THREE logged runs are the evidence that earns the Tier B grant.
```

## 2 · WHAT IT MAY NEVER DO

- **Invent a date, a weight, or a deadline.** If it is not in the register or the feed, it does not exist. `null` is a legitimate answer; a guess is not.
- **Write to `Brain/courses/`.** This routine reads records; it does not edit them.
- **Put an identifier in a brief.** Instructor, section, room, email, URL → scrubbed by `plan_term.py`, and check 20 fails a register that carries one.
- **Promise overnight preparation.** The GitHub Action (P-10 Phase 4) computes and flags; it has no model. Preparation happens in-session.
- **Report a plan as progress.** Attempts are the metric.

## 3 · THE DEGRADATION LADDER (use the highest rung available)

| Rung | Have | Brief quality |
|:--:|---|---|
| 4 | anchor + ICS + records | dated, delta-aware, ranked |
| 3 | anchor + records | dated, ranked |
| 2 | **records only** ← *today* | **week-based, ranked, blind-courses flagged** |
| 1 | records only, and even those partial | week-based, ranked from weights where known |
| 0 | no register | **say so and stop** — do not improvise a term |

**Rung 2 is the current state.** That is a working planner, not a stub: it knows a Q1 lands in week 4, a Q2 in week 7, a Q3 and the Coursera certificate in week 10, finals in week 11 — and it knows the three highest-yield courses are invisible.

## 4 · WHY THIS ROUTINE EXISTS (the instance it cures)

AP-07, evidenced: **0 Core cards after 4 sessions; 15 🟠 patches against 3 content sessions.** The system had excellent law and no mechanism that converted an academic deadline into a study session. This routine is that mechanism — small, 🟢, and reached without touching the boot set or the standing-orders queue.

---
*First proven: ⏳ pending. On first accepted brief: replace this line with the session ID and promote the routine from STAGED to permanent (II.6 cerebellum rule — write-after-proof).*
