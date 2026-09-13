# PATCH NOTES — Situation Layer + Capability Registry

**Patch:** `RADIATION_PATCH_2026-09-13_2700_Situation-Layer.zip`
**Base:** `e76ef8c` (main — patch 2600 **already applied**) · **Prepared:** 2026-09-13
**Type:** DELTA. This does **not** re-ship patch 2600's files (`SCHEDULE.md`,
`INDEX.md`, `.gitignore` are already in the tree).

1. **RISK LEVEL   : 🟢 ORDINARY — content growth + tooling (PATCH component → v1.6.5)**
   **RISK BASIS   :** CANON CHECK resolves **NO** — no constitutional text
   (`docs/AI_RULES.md`), no core scaffold, no core style, no mode definition, no Scan
   rule, and **not** `docs/.readme`. `docs/SYSTEM_STATE.md` is not canon: it is the file
   explicitly designated **the ONLY overwrite-permitted file (II.2 exception)**, which is
   exactly why the Situation Layer lives there and nowhere else. `docs/CAPABILITIES.md`
   is new; `scripts/` is tooling; the workflow file is CI.
   **CANON CHECK  : NO.**  **RATIFICATION:** none requested, none needed.

2. **FILES TOUCHED:**
   1. `docs/SYSTEM_STATE.md` — **REPLACE** — Tier 0 now opens with **THE SITUATION** (§4).
   2. `docs/CAPABILITIES.md` — **ADD** — all 7 scripts: invocation, inputs, exit codes,
      gotchas, and a plain "what is NOT here yet" section.
   3. `scripts/validate.py` — **REPLACE** — **check 21** added, running last so its
      count includes itself. Amendment A1 (from 2600) is untouched.
   4. `scripts/README.md` — **REPLACE** — 26 checks (was 14); all 7 tools surfaced.
   5. `.github/workflows/validate.yml` — **REPLACE** — CI label de-counted so it cannot
      drift again. CI still runs the same 2 of 7 scripts, deliberately.
   6. `README.md` — **REPLACE** — version line only.
   7. `CHANGELOG.md` — **REPLACE (insertion-only)** — the v1.6.5 entry. Verified
      insertions only; no existing entry touched.
   8. `APPLY.sh` · `APPLY.ps1` — payload check, CSV retirement, carrier + report untrack,
      Situation Layer verification, validator run.
   9. `PATCH_NOTES.md` — this file (transport; **deleted by the APPLY script**).

3. **AREAS TOUCHED:** [x] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
   [ ] cues [ ] modes/Scan [ ] other: **`docs/SYSTEM_STATE.md` (overwrite-permitted),
   `docs/CAPABILITIES.md` (new), tooling, CI**

4. **RATIONALE — THE FINDING THIS PATCH ANSWERS.**
   RADIATION's Tier 0–2 loaded the constitution, six mode charters, the Scan rules, four
   passive subskills, the scaffolds and the styles — **and never named a single asset the
   Commander actually owns.** Measured with fixed-string matching (a substring pass had
   already produced a false positive on `INDEX.md` inside `CORE_INDEX.md`):

   | Asset | Size | Boot-path references |
   |---|---|---|
   | `docs/KNOWLEDGE_REGISTRY.md` — what the Commander **knows** | 31,715 B | **0** |
   | `Brain/courses/INDEX.md` + `SCHEDULE.md` — what he's **studying** | 13,122 B | **0** |
   | `Brain/external_sources/INDEX.md` — his 12 **collections** | 5,754 B | **0** |
   | `scripts/` — the 7 **tools** he can run | 68 KB | **0** |

   A fresh AI given the link and the magic words therefore became **an AI that knew the
   rules of a system it had never seen the contents of.** It could explain the difference
   between `[D]` and `[O]`; it could not say which courses the Commander takes, what he
   knows, or that a term planner existed.

   The consequence was already visible in the repository's own instruments: check 16
   reports **15 canon patches against 3 content sessions — over budget by 42
   session-equivalents**; check 20.5 reports **no recorded attempt**; the mastery ledger
   holds **one row whose own text says "NOT a Commander attempt."** Those are not three
   problems. An AI booted into governance produces governance — every session opened on
   the constitution, so every session's natural output was a constitutional patch.

   **THE SITUATION adds no subsystem. It re-homes existing assets onto the path every
   session already walks**, and the budget was already there: the 1,193 B "Previously:"
   recital in Tier 0 was duplicated byte-for-byte in `CHANGELOG.md` (verified for five
   versions), so deleting it is lossless — and it funds the inline schedule.

   **Second finding, same file:** `SYSTEM_STATE.md` is Tier 0 *current ground truth* and
   it was **false**. Its CURRENT STATE section still read *"Brain CONTENT (ingestions,
   promotions, dossiers) | 🕳️ EMPTY — awaits first live sessions"* against 45 K-IDs, two
   completed ingestions (K-CUR-005/006) and a forged drill set. A boot-time falsehood is
   the worst instance of the class this repository exists to catch.

5. **CANON DIFFS:** none (🟢).

6. **APPLICATION:**
   - **Drop-in files:** items 1–7 (all in this zip).
   - `brain/courses/SCHEDULE.csv` retired to `_local_backup/` by the APPLY script.
   - `validation_report.json` untracked; `PATCH_NOTES.md` deleted — both by the script.
   - **Version:** v1.6.4 → **v1.6.5** (PATCH component; three sources ship together).

7. **VERSION BUMP :** **PATCH** → v1.6.5. Not MAJOR (no law, mode or Scan text); not
   MINOR (no core scaffold/style/subskill or structural folder change).

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session, 2026-09-13"

---

## VERIFICATION PERFORMED BEFORE DELIVERY

- **All 7 tool invocations executed and confirmed working** — not read from docstrings.
  `export_anki.py` → 10 cards · `grade_exam.py` → 2 mistake-bank candidates ·
  `decay_compute.py --fixed` → 0 expired · `plan_term.py --self-check` → exit 0 ·
  `validate.py` → exit 1 (FAILs present, correct) · `knowledge_regression.py` → exit 0 ·
  `ingest_collection.py --help` → 4 subcommands.
- **Check 21 negative-tested both ways:** an undocumented script → ❌ FAIL
  (*"undocumented script: scripts/decay_compute.py"*); a false count → ❌ FAIL
  (*"scripts/README.md claims 14 checks, actually 26"*) — the historical bug, reproduced
  on demand and now impossible to merge.
- **Own violation caught and fixed:** the first draft of `CAPABILITIES.md` used literal
  `/tmp/scratch` paths, which **check 14 fails**. Replaced with `<scratch-dir>`.
- **Acceptance on a clean clone of the live tree**, simulating the APPLY script:
  **26 checks · 23 pass · 2 warn · 1 fail** — the single fail being check 2.5 (the
  vehicles + `desktop.ini` the Commander deletes himself).
- **Version coherence:** SYSTEM_STATE = CHANGELOG = README = v1.6.5.
- **Boot budget measured after:** Tier0+1 **37,081 B (36.2 KB / cap 40)** · Tier0-2
  **60,207 B (58.8 KB / cap 80)**. Net +1.7 KB for a Tier 0 that now states the situation.
  **Headroom is down to 3.9 KB (9.5 %)** — worth watching; the next Tier 0 addition
  should displace rather than append.

## KILL-LIST HONESTY

This Patch does **not** clear the last FAIL:

- **check 2.5** — the 5 vehicles + `desktop.ini` under `Brain/courses/`. Extraction is
  verified complete (MEC30-7's record even carries the calendar's full week-by-week scope
  and a meeting pattern that matches `SCHEDULE.csv` exactly), and the course records
  already *claim* them deleted — so the files being present is the false statement.
  **You delete them; that makes the records true and takes the tree to 0 FAIL.**

## STILL OUTSTANDING, AND NOT FIXABLE BY ANY PATCH

**The LMS feed URL committed in `4a98e59` is live, in public history.** Rotate the feed
at source: disable the external-calendar feed, re-enable it to mint a new URL, and place
the new one in an Actions secret and a local env var — never in a file. Record the date
in the `INDEX.md` rotation table.
