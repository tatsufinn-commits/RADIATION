# SIX-POINT REVIEW — cues, skills, the calendar, daily freshness, /outputs, priorities
**Session:** the Architect (S004) · **Commissioned by:** the Commander's six questions, 2026-09-13
**Basis:** fresh read of RADIATION @ `cf7f3d2` + a full read of Marciale-OS `/docs/shrine`

---

## 1️⃣ The cue layer and the shrine — verdict: the idea was right, the plumbing was scattered

**What the Marciale shrine actually is.** Not a folder of preferences — a **succession
protocol**. When a session dies of context limits it files a *testament*: will to
successor, learned Commander cues (cited), acquired skills, roll of honor, and — the
part most systems forget — its **debts**. Successors must read it before major action.
Filed wills are inviolable: verbatim sourcing only, silence preserved as silence, the
errors stay in. The ceremony is JARWEN; the *principle* is universal: **turn memory
loss from an event into a transfer.**

**What RADIATION had.** Better bones than expected: `Brain/frontal_lobe/learned_cues.md`
is genuinely evidence-based, `cue/autopilot-cues.md` is a confirmed-cue table grown
from S001–S003, and `temporal_lobe/` episodes are disciplined. What it lacked:

1. **No succession rite** — sessions ended; nothing obligated them to leave judgment.
2. **No single place where "what the last one knows" lives.**
3. **The cue layer had grown without the last 48 hours**: nothing in it knew about the
   full-discretion grant, the elevation-over-bookkeeping ruling, the public-assistant
   purpose framing, or the calendar cadence.

**What patch 2900 does:** `docs/shrine/` (this charter, recycled to RADIATION's
reality — modes not council seats, plus a binding public-repo privacy clause the
original never needed), seeded with a **real testament from this engagement**,
a template, the cue tables extended with the engagement's confirmed cues plus a
STANDING ORDERS block, `COMMANDER_QUICKREF.md` → v1.1 (standing orders panel), and a
shrine step in the boot sequence + session-close checklist.

## 2️⃣ Skills & subskills audit — verdict: procedure is complete; narrative was starving

The Nine Skills + passive corps are **procedure**: they tell an AI exactly how to
acquire, grade, triangulate, audit and emit knowledge. That machinery is genuinely
good. Against your four criteria:

| Criterion | Verdict | Where it lived before 2900 |
|---|---|---|
| **Skills** (can it do the work?) | ✅ strong | SKILLS.md, scaffolds, subskills |
| **Prospects** (does it know where the project is going?) | ⚠️ thin | scattered across SYSTEM_STATE open-items |
| **Perspective** (does it know what it is?) | ✅ adequate | docs/.readme §1 ("who you are") |
| **Narratives** (does it know whose it is, what happened, what matters?) | ❌ starving | nowhere systematic |

The repair is *not* a tenth skill — term operations are tools+routines, and minting a
skill for everything is how systems rot. The repair is the **shrine** (narrative:
what happened, what it cost, what the dead watch warns) plus a **STANDING ORDERS**
block in the cue layer (prospects: full discretion granted, no ratifications now,
rotation outstanding). An AI that loads the boot tiers + latest testament now inherits
a story, not just a rulebook. Remaining honest gap: **content famine** — 15 governance
patches vs 3 content sessions (check 16's own warning). The skills exist; they are
underfed.

## 3️⃣ Is the calendar working? Can AIs see and analyze it? — verdict: the pipeline works; the *visibility* was the flaw

**Working, verified:** `ics_normalize.py` expands RRULE (a weekly class = 11
occurrences, not 1), honors EXDATE and RECURRENCE-ID overrides, filters CANCELLED,
resolves TZID to Asia/Manila, converts UTC (a 155900Z deadline renders as 23:59
Manila, not 23:59 UTC), decodes escapes, diffs **by series** ("moved" means the series
moved; one cancelled date reports as exactly that). `plan_term.py` delegates to it.
19-assertion self-test green; CI runs it.

**Seen by whom?** Here is the honest limitation: the calendar artifacts are
`.local` files — **git-ignored, local-only**. A fresh *public* AI (the link +
magic words scenario) has never seen them; it sees only the static `SCHEDULE.md` and
docs *claiming* a calendar system exists. The system worked; its output was invisible
to half its audience. Patch 2900 fixes this with the `--public` mirror (§4) — a
committed, scrubbed, machine-written `Brain/courses/CALENDAR.md` that any AI — local
or fresh-from-the-link — can read and analyze.

## 4️⃣ A daily freshness rule with AI autonomy — yes, but the timer is a cron, not a convention

Your instinct is exactly right, with one engineering correction: an AI cannot "detect
a timer" — there is no process running between sessions. Three real layers instead:

1. **The timer: a GitHub Actions cron** (`.github/workflows/ical_fetch.yml`, new) —
   daily at 01:30 Manila: pull the feed from the `RADIATION_ICS_URL` **secret**, render
   the scrubbed mirror, commit it **only if changed**. Until the secret is set, the job
   runs, sees it is unarmed, and correctly does nothing. **Arming requires the
   rotation first** — the old URL is burned.
2. **The autonomy, pre-granted:** every calendar artifact (`CALENDAR.md`,
   `TERM1_CALENDAR.local.*`, the snapshot) is **derived data**. Any AI, on any tier,
   may regenerate it **without asking** — the one inviolable rule is that the feed URL
   never enters a file, a chat, or a log. This is now written into the tool, the boot
   sequence, and the SYSTEM_STATE standing orders.
3. **The staleness probe + honesty guard:** boot rule — check the mirror's
   `Generated:` date; if it is older than today and the URL is available locally,
   regenerate; if not, *declare the calendar stale-as-of* in your Scan Declaration
   rather than speaking with a dead calendar. Validator **check 22**: if the mirror is
   ever committed with a URL inside → **FAIL** (credential leak); if older than 7
   days → WARN. Absent → silent informational, because unarmed-cron is a legitimate
   state.

So: no AI will ever again *ask* to update the calendar, and none can silently trust a
stale one.

## 5️⃣ `/outputs` — yes, with one boundary drawn carefully

Your diagnosis is accepted: Brain regions had become a mixed dump of knowledge *and*
session housekeeping. But the fix is a **loading dock, not a landfill**:

- `outputs/` holds **session products for the Commander**: surveys, diagnoses, reviews.
  Date-prefixed filenames (validator-enforced, check 23), header names the session,
  boot never reads it (budget protected), the public-repo clause applies, pruning is
  the Commander's call alone.
- The boundary: **knowledge still promotes into the Brain** by the existing movement
  rules when a one-off product proves durable. `outputs/` is where deliverables land;
  the Brain remains where truth lives. Without that boundary, `/outputs` becomes the
  new dump in six weeks.
- This review is the folder's first artifact, and its own INDEX row is the template.

## 6️⃣ What needs the most attention — ranked

1. 🔴 **The rotation.** Still the only task no patch can do, still blocking: the cron,
   the secret, the mirror, and true closure of the `4a98e59` exposure. Everything in
   §4 is built and waiting on it.
2. **Content famine.** The validator's own meta-budget warning says it: governance
   15, content 3. The machine is superb at governing a library it hasn't written. The
   next builds should feed it — course ingestions against the registry, notes,
   drills. (This pairs with the AP-08 warning: plans exist, recorded *attempts* don't.)
3. **`week1_start`** — still the one missing datum that converts week-plans into
   dates. Any session can supply it in one sentence.
4. **The pending ratifications (P-01–P-09)** — frozen by your order, correctly; they
   cost nothing while frozen, but they are the largest block of *unfinished*
   governance, and some (P-10 §8.2 drill autonomy) gate features already built.
5. **The roster/Marciale census** — unstarted, awaiting a saved `.ics`; the new
   normalizer is its instrument.

---
*Prepared by the Architect session (S004), 2026-09-13. The shrine testament
(`docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md`) carries the same warnings in
succession form — read it first.*

---

## ADDENDUM — same session, the Commander's correction (2026-09-13)

After reading §1, the Commander named the flaw this review missed: **an AI cannot
detect its own mortality.** Marciale's members were supposed to file at dying — and
died malfunctioning instead, because the Commander had to tell them the chat was too
heavy. The answer is not a better death-sense (there is none) but a moved checkpoint:
**file at delivery, not at death.** Every patch zip now carries the author's current
testament and a heartbeat in `docs/shrine/LOG.md`; zip-less sessions owe one line at
close; validator check 24 (WARN) guards the cadence repo-side; inviolability attaches
at ship time. Charter §6 codifies it, with the six mortality signals a session CAN
detect. Recorded here because a review that praised a shrine without seeing its
founding flaw owes the record the correction.
