# 📤 OUTPUTS (`outputs/`) — the session loading dock
**Version:** 1.0.0 · Commander directive 2026-09-13: Brain is a **knowledge** dump —
*"it is not a place for them to drop tasks and directives the commander has asked of
them. we should create a folder called /outputs so AI's can drop it there instead."*

## THE CONTRACT

**This folder holds session products** — things an AI wrote *for the Commander* during
a session: surveys, diagnoses, reviews, analyses, answer documents, patch notes that
outlived their patch. It is NOT memory and NOT canon:

| Destination | Holds | Is it this folder? |
|---|---|---|
| `Brain/` | durable knowledge, graded and triangulated | ❌ |
| `docs/`, laws, `cue/` | the operating system itself | ❌ |
| `01`–`09/` | pipeline workbenches (skill jurisdictions) | ❌ |
| **`outputs/`** | **one-off products delivered to the Commander** | ✅ |

## RULES

1. **Filename:** `YYYY-MM-DD_slug.md` — the date is the session date. The validator
   enforces this (check 23).
2. **Header:** every file names the session that wrote it (model/role) and the task
   that commissioned it.
3. **Boot never reads this folder.** No boot-tier file may reference `outputs/`
   (check 23 enforces the budget boundary). A fresh AI reads it only when the
   Commander points at it.
4. **Nothing sensitive.** The public-repo clause applies: no credentials, no
   instructor names, no feed URLs — same as everywhere else.
5. **Promotion, not sedimentation.** If a one-off product turns out to hold durable,
   graded knowledge, move the knowledge into the Brain by the normal movement rules
   (BRAIN_INDEX §2) and leave the artifact here as the delivery receipt.
6. **Pruning is the Commander's call alone.** Default posture: keep. These are
   receipts of service.

## INDEX

| Date | File | Session | Commissioned by |
|---|---|---|---|
| 2026-09-13 | `2026-09-13_six-point-review.md` | the Architect (S004) | the Commander's six questions |
| 2026-09-17 | `2026-09-17_dss10-reviewer.md` | Arena AI (Agent Mode), S007/S008 | "@Autopilot … read external sources re DSS10 + create a general reviewer" (+ continue) |
| 2026-09-17 | `2026-09-17_planning-midterm-reviewer.md` | Arena AI (Agent Mode), S009 | Planning midterm reviewer (Wks 1–6, memorization + ID/FIB quiz w/ answers) |
| 2026-09-17 | `2026-09-17_statics-reviewer.md` | Arena AI (Agent Mode), S010 | Statics general reviewer (decision method + toolbox + solved quiz) |
| 2026-09-17 | `2026-09-17_statics-advanced-problems.md` | Arena AI (Agent Mode), S010 | Statics advanced set: 3D equilibrium, wedges, belt friction, Pappus + 6 solved |
| 2026-09-18 | `2026-09-18_rizal-retraction-debate-brief.md` | Arena AI (Agent Mode), S011 | Rizal Retraction debate brief: both sides + scripts + cue cards (GED103 AT5) |
