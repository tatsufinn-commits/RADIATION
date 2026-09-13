# PATCH NOTES — The Deadline Engine

**Patch:** `RADIATION_PATCH_2026-09-13_3100_Deadline-Engine.zip`
**Base:** post-3000 (v1.8.0 — 3000 must be applied; APPLY gates on it)
**Prepared:** 2026-09-13 · **Type:** DELTA · **Trigger:** the Commander landed the
LMS feed himself (`cb5ec95`) — the hivemind now owns the schedule data.

1. **RISK LEVEL   : 🟢 ORDINARY — content + tooling (PATCH → v1.8.1)**
   **RISK BASIS   :** CANON CHECK **NO** — no constitutional/core/mode/Scan edits.
   New script, feed-driven register data, CI mirror workflow, check 22 upgrade
   (WARN-class). The register data change is the patch's payload.
   **DIRECTION:** the Commander's feed drop + standing build discretion.

2. **FILES TOUCHED:**
    1. `scripts/deadline_feed.py` — **ADD** — the engine (11-assertion self-test).
    2. `Brain/short_term/plan/TERM1_DEADLINES.json` — **REPLACE** — 21→26 items (+5
       attributed MEC30-7 with k_ids from the course map), 3 Coursera records
       anchored to real dates, `week1_start = 2026-08-24 (inferred)`, and a new
       `feed_pending[]` queue: 11 unattributed items with sibling hints — the
       **Commander's decisions**, listed in §6.
    3. `scripts/ics_normalize.py` — **REPLACE** — auto-detects the committed feed.
    4. `scripts/plan_term.py` — **REPLACE** — `--week N` needs zero arguments;
       plans now print real dates.
    5. `scripts/validate.py` — **REPLACE** — check 22 v3: feed-staleness guard.
    6. `.github/workflows/ical_fetch.yml` — **REPLACE** — `calendar-mirror`:
       regenerates `CALENDAR.md` from the committed feed on push. **No secret, no
       cron — the Commander's re-export-and-push cadence IS the timer.**
    7. `docs/CAPABILITIES.md` · `scripts/README.md` — tool #11 registered.
    8. `README.md` · `docs/SYSTEM_STATE.md` · `CHANGELOG.md` — v1.8.1.
    9. Shrine heartbeat: LOG row + testament refresh (§6 doctrine — every zip carries one).
   10. `APPLY.sh` · `APPLY.ps1` · `PATCH_NOTES.md` — transport.

3. **THE CENSUS VERDICT (recorded):** the feed is a DEADLINE/ACTIVITY feed, not a
   meeting schedule — 47 items, zero RRULEs; the LMS publishes no meeting grid except
   AR173's (Tue 18:00 / Sat 12:00), which **confirms** SCHEDULE.md. The 36-hour grid
   remains the Commander's record alone.

4. **RATIONALE:** the planner was built blind — the three highest-yield courses had
   no dates. The Commander's own feed fixes exactly that, and the merge is built
   conservative: attribution ladder (code → existing-item anchor → citable keywords
   → pending-with-hint), meeting-series filter, stale filter, idempotent re-runs.
   Three engine defects were caught by probes/dry-runs before ship (PR-token
   normalization, case-sensitive type patterns, meeting-series pollution) — each fix
   carries a test that remembers it.

5. **CANON DIFFS:** none. **AMENDMENT A2 (in-code):** `TERM1_FEED.txt` joins the
   check-2.5 allowlist as the one permitted data file in the records region — the
   Commander ordered the feed into `Brain/courses/` (the hivemind needs it; GitHub
   rejects .ics uploads). Identifier scans still apply to it; everything else stays
   records-only.

6. **THE COMMANDER'S 11 DECISIONS** (`feed_pending[]`, with hints — answer in one
   line, any AI applies them): Assessment 2 · Assessment 3 · SQ1* · CW3* · CW4* ·
   Activity 1 · Activity 2 · Assignment 1 · Collaborative Work 1 (GW) · Online
   Activity 1 · LQ1(1Q2627). Hints: the Assessment series is likely DSS10 (siblings
   registered); the rest need your one-word course assignments.

7. **VERSION BUMP :** PATCH → v1.8.1.

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session (S004), 2026-09-13"

## VERIFICATION
- Self-tests: deadline_feed 11/11 · ics_normalize 21/21 · register integrity (check 20)
  passes WITH the merged data — pending items live outside `items[]` by design.
- `plan_term.py --week 3` with zero arguments: `W3 = 2026-09-07 .. 2026-09-13` + feed-driven ranked load.
- Idempotency: second `--write` run = 0 added, 0 anchored, all dups skipped.
- Expected after apply: **29 checks · 27 pass · 2 warn · 0 FAIL** (the 2 vehicle FAILs
  clear at APPLY step 3 — the reconciliation your pushes kept skipping, now part of
  every apply).
