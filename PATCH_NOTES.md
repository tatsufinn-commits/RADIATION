# PATCH NOTES — Schedule Record + Location Amendment (A1)

**Patch:** `RADIATION_PATCH_2026-09-13_2600_Schedule-Record-A1.zip`
**Base:** `f151e7c` (main, 2026-09-13) · **Prepared:** 2026-09-13

1. **RISK LEVEL   : 🟢 ORDINARY — content growth (PATCH component → v1.6.4)**
   **RISK BASIS   :** This Patch adds one Brain record and amends one *region* rule by
   explicit Commander decision. The CANON CHECK resolves **NO**: it touches no
   constitutional text (`docs/AI_RULES.md`), no core scaffold, no core style, no mode
   definition, no Scan rule, and **not** `docs/.readme`. `Brain/courses/INDEX.md` is a
   region document (P-10 §3.3), and `scripts/validate.py` is tooling — neither is canon.
   It is 🟢 **only** on that basis; the amendment it carries is substantive and is
   recorded verbatim below so the decision is auditable.
   **CANON CHECK  : NO.**
   **RATIFICATION :** none requested and none needed under the template's CANON CHECK.
   The Commander's authorization is already on record (2026-09-13):
   > *"I permit 2. the full CSV in the repo it doesnt matter if my public location is
   > unleashed, no body views my repositories anyway. the repository is a link copy paste
   > method + magic words to a fresh AI and that will turn the AI into somesort of an
   > assistant of mine that knows my schedule, calendar, and will have a full access of my
   > external links. that is the idea behind RADIATION."*
   That rationale is the reason this is not a privacy regression: the public repository
   **is** the delivery mechanism, so a record the assistant must know has to be legible
   inside it. It is also why the amendment is *narrow* — see §5.

2. **FILES TOUCHED:**
   1. `Brain/courses/SCHEDULE.md` — **ADD** — the authoritative weekly timetable (6
      courses, 14 meetings, 36.0 h/week) at full fidelity: days, times, **rooms,
      sections**, mode. Includes per-course pattern, derived planning facts, and the
      open `week1_start` anchor.
   2. `Brain/courses/INDEX.md` — **REPLACE** — rule 3 amended (location permitted in
      the schedule record only; personnel/student identifiers remain absolutely
      banned); term load corrected **31.5 → 36.0 contact-h/week** with the error
      recorded rather than silently edited; pointer to `SCHEDULE.md` added to the
      register.
   3. `scripts/validate.py` — **REPLACE** — amendment A1: room/section rules split out
      of the identifier rules into `CV_DENY_LOCATION` / `CV_LOCATION_PATTERNS`, with a
      single path-scoped allowance `CV_ALLOW_LOCATION = {"Brain/courses/SCHEDULE.md"}`.
      `CV_PATTERNS` keeps its old meaning for every other caller (check 20's term
      register is unaffected).
   4. `.gitignore` — **REPLACE** — adds `validation_report.json` (validator output,
      written on every run, previously tracked → every run produced a diff).
   5. `docs/SYSTEM_STATE.md` — **REPLACE** — version + ground-truth line (this is the
      one overwrite-permitted file, II.2 exception).
   6. `README.md` — **REPLACE** — version line only (v1.6.3 → v1.6.4).
   7. `CHANGELOG.md` — **REPLACE (insertion-only)** — the v1.6.4 entry inserted at the
      top of the entry list. **Verified: 0 lines removed, 7 added.** No existing entry
      is touched, so the II.2 append-only intent holds; the full file ships rather than a
      paste-block because a split version bump silently breaks check 7 (proven in test —
      SYSTEM_STATE=v1.6.4 / CHANGELOG=v1.6.3 / README=v1.6.4 → FAIL). The three version
      sources must move atomically.
   8. `APPLY.sh` · `APPLY.ps1` — convenience runners: payload check, CSV retirement,
      untrack of the generated report, amendment verification, validator run.
   9. `PATCH_NOTES.md` — this file (transport; deleted after application).

3. **AREAS TOUCHED:** [x] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
   [ ] cues [ ] modes/Scan [ ] other: **tooling (`scripts/validate.py`), `.gitignore`**

4. **RATIONALE:** RADIATION's stated purpose is a public, copy-pasteable assistant: repo
   link + magic words → a fresh AI that knows the Commander's schedule, calendar and
   external links. Until now the repo held course *records* (what is taught, what is
   graded) and **no meeting pattern at all** — the region rule forbade rooms and
   sections, and the only schedule artifact was an image. `Brain/courses/INDEX.md`
   compounded this with a **wrong** load figure (31.5 h) that no file could correct,
   because the authoritative timetable was not in the repository. This Patch puts the
   timetable in the repository, corrects the figure from it, and narrows the rule so
   that only this record is exempt.

5. **CANON DIFFS:** none (🟢). The region-rule change is an amendment, not a canon diff;
   its full text is in file 2 above and is quoted verbatim in `INDEX.md` rule 3.

6. **APPLICATION:**
   - **Drop-in files (paste/overwrite):** items 1–7 above — including `CHANGELOG.md`.
   - **Delete:** `Brain/courses/SCHEDULE.csv` — superseded by `SCHEDULE.md`; identical
     data, and the CSV form cannot pass check 2.5 (non-markdown vehicle). Keep a local
     copy if you want the grid form.
   - **Untrack (keep on disk):** `git rm --cached validation_report.json`
   - **CHANGELOG:** already carried in item 7 — **no manual paste needed.** If you want to
     confirm nothing was rewritten: `diff` the old and new file and check that the only
     change is an insertion of the v1.6.4 block (measured: 0 removed, 7 added).
   - **Version:** PATCH component — v1.6.3 → **v1.6.4** (all three version sources are in
     this zip and move together).

7. **VERSION BUMP :** **PATCH** → v1.6.4. Per `VERSIONING_GUIDE.md`: not MAJOR (no law
   text, no mode definitions, no Scan rules), not MINOR (no core scaffold/style/subskill
   and no structural folder change) — a Brain promotion + register growth.

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session, 2026-09-13"

---

## VERIFICATION PERFORMED BEFORE DELIVERY

- **Amendment A1 behaves:** `SCHEDULE.md` passes with rooms present; the same room
  tokens still FAIL in any other file in the region; the identifier rules (instructor /
  contact / email / URL) still apply **inside** `SCHEDULE.md`.
- **No collateral:** check 20's term-register scan uses `CV_PATTERNS` unchanged.
- **No regression:** full validator run on a clean mirror, before and after.
- **Kill-list honesty:** this Patch does **not** fix the two remaining FAILs —
  the 5 vehicles + `desktop.ini` (check 2.5) and
  `docs/PLAYBOOK_EVALFIRST_TEMPLATE_STAGED.md` (check 3). You delete those; the Patch
  only stops `SCHEDULE.csv` contributing to the first.

## STILL OUTSTANDING, AND NOT FIXABLE BY ANY PATCH

**The LMS feed URL committed in `4a98e59` is still live.** It was never deleted from
history, and history is public. **Rotate the feed at source**: disable the external
calendar feed, then re-enable it to mint a new URL; place the new one in an Actions
secret and a local env var — never in a file. Record the date in the `INDEX.md`
rotation table. Until then, anyone holding that URL can read the Commander's course
calendar.
