# PATCH NOTES — ICS Normalizer (the calendar finally reads)

**Patch:** `RADIATION_PATCH_2026-09-13_2800_ICS-Normalizer.zip`
**Base:** `c1ba3b6` (main) · **Prepared:** 2026-09-13 · **Type:** DELTA

1. **RISK LEVEL   : 🟢 ORDINARY — new tooling + content (PATCH component → v1.6.6)**
   **RISK BASIS   :** CANON CHECK resolves **NO** — no constitutional text, no core
   scaffold, no core style, no mode definition, no Scan rule, not `docs/.readme`.
   `scripts/` is tooling; `docs/CAPABILITIES.md` and `docs/SYSTEM_STATE.md` are
   registry/state files (the latter is the designated overwrite-permitted file).
   **RATIFICATION:** none requested, none needed.

2. **FILES TOUCHED:**
   1. `scripts/ics_normalize.py` — **ADD** — the one iCalendar parser (§4).
   2. `scripts/plan_term.py` — **REPLACE** — inline parser deleted; delegates instead.
   3. `docs/CAPABILITIES.md` — **REPLACE** — tool #8 documented; "NOT HERE YET" corrected.
   4. `scripts/README.md` — **REPLACE** — the new tool surfaced in the tool list.
   5. `.github/workflows/validate.yml` — **REPLACE** — runs the 19-assertion self-test.
   6. `docs/SYSTEM_STATE.md` — **REPLACE** — v1.6.6; situation section gains the calendar.
   7. `README.md` — **REPLACE** — version line only.
   8. `CHANGELOG.md` — **REPLACE (insertion-only)** — the v1.6.6 entry.
   9. `APPLY.sh` · `APPLY.ps1` — verification + reconciliation runner (§6).
  10. `PATCH_NOTES.md` — this file (transport; **deleted by the APPLY script**).

3. **AREAS TOUCHED:** [x] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
   [ ] cues [ ] modes/Scan [ ] other: **`scripts/`, `docs/`**

4. **RATIONALE — THE FINDING THIS PATCH ANSWERS.**
   The Commander asked about the calendar five times across this engagement. The honest
   answer was always a version of *"the parser drops `RRULE`, so a weekly class appears
   once instead of eleven times."* `docs/CAPABILITIES.md` said so plainly under
   *"WHAT IS NOT HERE YET: no ICS fetcher · no recurrence expansion."*

   `scripts/ics_normalize.py` closes both. It expands `RRULE` (FREQ / INTERVAL / BYDAY /
   COUNT / UNTIL), honours `RDATE` and `EXDATE`, resolves `RECURRENCE-ID` **overrides**
   (a rescheduled occurrence *replaces* the original rather than appearing beside it as a
   phantom second event), filters `STATUS:CANCELLED`, resolves `TZID` through `zoneinfo`
   and displays everything in `Asia/Manila`, decodes RFC 5545 escapes, handles quoted
   parameter values and folded lines, and honours `DTEND` so durations survive.

   **Diffing is series-aware**, which the old one could not be. The old diff keyed on
   `UID` alone — correct only because it never expanded anything. With expansion, several
   occurrences share a `UID`, so the key was changed to compare the *set of occurrence
   dates per series*. "Moved" now means the series moved, and a single cancelled date
   inside series is reported as precisely that:

   ```
   ⚠ MOVED  AR163-1P Lecture, Building Tech — lost 2026-06-18
   ```

   **One parser, deliberately.** `plan_term.py`'s inline parser was deleted in favour of
   delegation. This repository's own Marciale-OS review identified *"two parsers of
   different quality, the weaker one serving the more important input"* as a structural
   smell. Shipping a second parser here would have reproduced it in the very document
   that named it.

   **The credential rule holds.** The feed URL is read from `$RADIATION_ICS_URL` — never
   a file, never committed, never printed. Every summary and location is scrubbed of
   instructor names, room codes, sections, emails and URLs before it reaches any output,
   reusing the same `REDACT` list as validator check 2.5.

5. **CANON DIFFS:** none (🟢).

6. **APPLICATION — and a reconciliation you should read.**
   The APPLY script runs the parser's self-test **first** and aborts if it fails, before
   touching anything else. Then it does three things beyond dropping files:

   - **Retires `SCHEDULE.csv`** to `_local_backup/` (superseded; data is in `SCHEDULE.md`).
   - **Re-homes the vehicles** — see below.
   - Removes `PATCH_NOTES.md` and untracks `validation_report.json`.

   **RECONCILIATION.** You reported that groups A–E had been deleted. Verified on
   `c1ba3b6`: A, B, C and E are gone, but **group D never ran** — the credential, the
   PDF, both syllabi, the course-calendar HTML and `desktop.ini` were all still tracked.

   That mattered because **five course records already state they were deleted**
   (*"binary deleted (II.6 r.8)"*, *"vehicle removed from tree"*). The files being
   present made those records **false**, and a fresh AI reading them would conclude the
   region was clean.

   I verified extraction is genuinely complete for all of them — MEC30-7's record even
   carries the calendar's full week-by-week scope and a meeting pattern that matches
   `SCHEDULE.csv` exactly. **They are MOVED, not deleted:** `_local_backup/` is
   git-ignored, so they remain on your disk and recoverable. This makes the records true
   and clears the last FAIL.

7. **VERSION BUMP :** **PATCH** → v1.6.6 (content growth + tooling; not MAJOR, not MINOR).

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session, 2026-09-13"

---

## VERIFICATION PERFORMED BEFORE DELIVERY

- **Self-test: 19 assertions, all passing.** It caught four defects on the way —
  including three that were my own expectations being wrong, which is the more
  interesting half:
  1. an unpack bug on multi-date events;
  2. the fixture was wrong, not the code — RFC 5545 unfolding removes CRLF + **exactly
     one** whitespace, so a fold written `\n across` yields `foldedacross`, not
     `folded across`;
  3. three early `return` paths inside the weekly expander skipped timezone
     reattachment, leaking naive datetimes into a mixed sort;
  4. `COUNT=6` with one `EXDATE` and one override yields **five** live occurrences —
     the engine was right and my test was wrong. Likewise a shift-test that targeted the
     very date the override had moved.
  A weaker escape assertion also passed *while the backslash was still present*; it now
  matches exactly. **A test that cannot tell decoding from a leftover backslash is not
  testing decoding.**
- **UTC conversion fixed after a real display bug:** `DTSTART:…235900Z` was staying in
  UTC, so the renderer would have printed 23:59 for an event at 07:59 Manila time.
  Every timestamp is now converted to the display zone at parse time.
- **`plan_term.py` delegation tested both ways** — without `--ics` the baseline output is
  unchanged; with `--ics` it now reports *9 occurrences from 5 series* where the old
  parser reported 5 events with `RRULE` dropped. `--self-check` still passes.
- **Check 21 exercised for real** — the registry guard would have failed the build had
  the new script not been documented. It is documented.
- **Acceptance on a clean clone of the live tree**, running the frozen zip's APPLY.sh.

## KILL-LIST HONESTY

After this patch the tree should reach **0 FAIL** for the first time. If check 2.5 still
reports anything, the APPLY script will have printed which path it could not move.

## STILL OUTSTANDING, AND NOT FIXABLE BY ANY PATCH

**The LMS feed URL committed in `4a98e59` is live, in a public repository.** Moving
`ics.txt` does **not** revoke it — git history keeps it. Rotate the feed at source
(disable the external calendar feed, re-enable it to mint a new URL), then place the new
URL in an Actions secret and a local env var. Record the date in the `INDEX.md` rotation
table. Until that is done, anyone holding the old URL retains read access.

**No scheduled fetch.** `--fetch` works, but nothing runs it automatically. Wiring an
Actions job is a small, separate follow-up — and it is only worth doing *after* rotation.
