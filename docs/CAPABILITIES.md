# 🛠️ CAPABILITIES (`docs/CAPABILITIES.md`)
## What this repository can RUN — the executable half of the system
**Version:** 1.0 | **Origin:** Commander's order, 2026-09-13 — *"our task is to improve RADIATION from its current standing, elevate it."*
**Companion to:** `docs/SKILLS.md` (how the AI **thinks**) — this file is what the AI can **execute**.

---

## THE RULE

`SKILLS.md` says how to reason. This file says what can be **run**. An AI that does not
know a tool exists will do that work by hand, worse, and call it a session.

**Every script in `scripts/` appears below. Check 21 FAILS if one does not.** That guard
exists because this repository already shipped a capability doc that said "14 checks"
while the validator ran 25 — a count nobody could have got right by reading.

## COMMON PROPERTIES

- **Stdlib only** — no third-party packages, with one exception (`ingest_collection.py`
  needs PyMuPDF for PDF work).
- **Offline** — none calls the network, except `ingest_collection.py` and
  `ics_normalize.py --fetch`, both of which contact only a URL you supply explicitly.
- **Non-destructive** — no script writes to the repository except `validate.py`
  (its own report, git-ignored) and `ingest_collection.py` (only on `--repo`, which
  refuses to render inside the tree). `grade_exam.py` and `decay_compute.py` **propose**
  register rows; they never write them. A session appends.
- **Exit codes** — `1` means a real failure, not a warning. A nonzero exit from
  `validate.py` or `knowledge_regression.py` means **the session is not closable**.

---

## THE TOOLS

### 1. `validate.py` — structural validator · **run before claiming closure**
```
python3 scripts/validate.py
```
**Answers:** is the repository structurally sound? 26 form-and-resolvability checks.
Never truth — form. **Writes** `validation_report.json` (git-ignored).
**Read the exit code, not the vibe:** exit 1 = at least one ❌ FAIL → the session is
**not closable**; fix it or report the failure honestly. ⚠️ WARN entries are
ratification-pending items — **list them in your delivery; never "fix" canon to silence
one.** Check 16 is the meta-budget law (canon patches vs content sessions) and check 20.5
is the planner-theater guard: *plans are not progress.*

### 2. `knowledge_regression.py` — locked value assertions
```
python3 scripts/knowledge_regression.py
```
**Answers:** has a verified factual value drifted? Reads `tests/knowledge_assertions.json`
(4 locked · 5 pending · 0 failing). **A drifted verified value = exit 1 = cannot ship.**
Locking a value requires a Shield Stamp (I.3) or an in-session-verified `[D]` primary —
locking `[O]`/`[N]` matter is forbidden.

### 3. `plan_term.py` — the term planner
```
python3 scripts/plan_term.py --week 4
python3 scripts/plan_term.py --week 4 --ics local.ics     # + LMS feed delta
python3 scripts/plan_term.py --week 4 --anchor 2026-06-15  # week-1 Monday
python3 scripts/plan_term.py --self-check                  # integrity of the register
python3 scripts/plan_term.py --audit                       # audit the plan
```
**Answers:** what to study this week, ranked. Prints the term brief, the ranked load, and
— with `--ics` — *what moved* since the last run (added / moved / removed).
**Reads** `Brain/short_term/plan/TERM1_DEADLINES.json` (6 courses · 21 items).
**Gotchas:** without `--anchor` it plans in **weeks, not dates** — that is by design, not
a bug. `--ics` reads a **local file only**, and **drops `RRULE`** (recurring events are
not expanded). Nothing is written except an ICS snapshot beside the register.

### 4. `ingest_collection.py` — collection ingestion harness
```
python3 scripts/ingest_collection.py list    --url <drive-folder-url>
python3 scripts/ingest_collection.py fetch   --manifest <file.json> --dest <scratch-dir>
python3 scripts/ingest_collection.py extract --dir <scratch-dir>
python3 scripts/ingest_collection.py verify  --pdf <file.pdf> --page 55
```
**Answers:** how do I acquire and extract a source collection repeatably?
Enforces three lessons learned the hard way: **① binaries never touch the repository**
(working dir defaults to a temp path); **② a table extracted by text order alone is
UNVERIFIED** — `verify` renders the page, because naive extraction once produced a
complete, plausible, completely wrong code table; **③ the skip log is destination-scanned.**
**Needs** PyMuPDF for PDF work. Two runtime modes (fetch 165 s+, extract 10–157 s).

### 5. `export_anki.py` — drill set → Anki
```
python3 scripts/export_anki.py --set <set.json> [--out <file.tsv>]
```
**Answers:** get the forged drill set into Anki. Front = brief + options · back = key +
rationale + citations · tags = K-ID, context, difficulty, yield rank.

### 6. `grade_exam.py` — drill grader
```
python3 scripts/grade_exam.py --set <set.json> --answers <answers.json> [--tally]
```
**Answers:** what did the Commander score, and what did he miss?
Scores against the **stored key only — never memory.** Prints the report plus a
**proposed** `mastery_ledger` row and mistake-bank candidates. **Never writes registers
itself:** a session appends. Scores are study data and are **never citable as evidence.**

### 7. `decay_compute.py` — knowledge decay arithmetic
```
python3 scripts/decay_compute.py [--fixed]
```
**Answers:** which registry rows have passed their currency window?
Reads `docs/KNOWLEDGE_REGISTRY.md`, computes expiry from `Last verified` + `Freq`
(90 d / 1 yr), and prints **proposed** `DECAY_REGISTER` rows. `--fixed` pins "today" for
reproducible output. Arithmetic, not memory — and again, it proposes; it never appends.

---

### 8. `ics_normalize.py` — **the** iCalendar parser (RFC 5545 subset)
```
python3 scripts/ics_normalize.py --ics local.ics            # summary + delta
python3 scripts/ics_normalize.py --ics local.ics --md       # AI-readable calendar
python3 scripts/ics_normalize.py --ics local.ics --write    # durable .local artifacts
python3 scripts/ics_normalize.py --fetch                    # URL from $RADIATION_ICS_URL
python3 scripts/ics_normalize.py --public                 # COMMITTED scrubbed mirror
python3 scripts/ics_normalize.py --self-test                # the self-test suite
```
**Answers:** what is actually on the LMS calendar — *including every occurrence of a
recurring event.* This is the ONE parser; `plan_term.py --ics` delegates to it.
**Handles:** RRULE expansion (FREQ/INTERVAL/BYDAY/COUNT/UNTIL) · RDATE · EXDATE ·
**RECURRENCE-ID overrides** (a rescheduled occurrence replaces the original instead of
appearing beside it as a phantom) · `STATUS:CANCELLED` filtering · `TZID` resolved via
`zoneinfo` and displayed in `Asia/Manila` · RFC 5545 escape decoding · quoted parameter
values · line unfolding · `DTEND` durations.
**Diffing is series-aware:** "moved" means the *series* moved, and a single cancelled
date inside a series is reported as exactly that.
**The URL rule:** the feed URL is a **credential**. It is read from the environment
variable `RADIATION_ICS_URL` — never from a file, never committed, never printed.
**Scrubbing is unconditional:** every summary and location is stripped of instructor
names, room codes, sections, emails and URLs before it reaches any output.
`--write` emits `Brain/short_term/plan/TERM1_CALENDAR.local.{md,json}` (git-ignored).

### 9. `nota.py` — Core card tool (shape guard, never an admission authority)
```
python3 scripts/nota.py --new NOTA-001 --topic "..." --dossier <long_term path> --worksheets <ids>
python3 scripts/nota.py --check        # every card: <=300 words · LINEAGE · SHIELD · decay · index parity
python3 scripts/nota.py --self-test
```
**Answers:** can this Core card stand in the cleanest room? Cards are scaffolded to
the proc_nota-distillation shape; `--check` enforces the <=300-word limit, the
mandatory lineage block, the Shield stamp, the decay tag, and CORE_INDEX parity for
admitted cards. **It never admits** — the six-box pass is a session's act.

### 10. `module_scaffold.py` — born-valid study modules (check-18 mirror)
```
python3 scripts/module_scaffold.py --new --level 3 --course AR153P --topic "..." --kid K-MOD-XXX
python3 scripts/module_scaffold.py --list     # inventory + parity + per-module health
python3 scripts/module_scaffold.py --self-test
```
**Answers:** does this module pass validator check 18 from birth? The scaffold
carries every required section/quotas for its level and is validated by a mirrored
rule-set before it is written. `--list` reports index parity honestly, including
"NO INDEX FILE" (check 18 counts a missing index as a mismatch).

### 11. `deadline_feed.py` — the Deadline Engine (feed → term register)
```
python3 scripts/deadline_feed.py            # dry-run: what WOULD merge
python3 scripts/deadline_feed.py --write    # merge into TERM1_DEADLINES.json (idempotent)
python3 scripts/deadline_feed.py --self-test
```
**Answers:** what does the committed LMS feed actually say, and what does it change?
Conservative attribution: explicit course code → fuzzy match to EXISTING register
items (their dates anchor week-based records) → citable content keywords →
UNATTRIBUTED for the Commander (with sibling hints), never guessed. Meeting series
(3+ identical titles) are skipped — meetings live in SCHEDULE.md. Pre-term items
counted and skipped. Re-runs are no-ops (feed_id hashing). First run (2026-09-13,
`cb5ec95` feed): 20 meeting instances filtered · 8 stale skipped · 3 Coursera
records anchored to real dates · 16 added · 11 UNATTRIBUTED pending Commander.

### 12. `status.py` — the Swarm Dashboard (one screen, read-only)
```
python3 scripts/status.py
```
**Answers:** where does the machine stand RIGHT NOW — validator verdict (+ the FAIL
lines), calendar feed freshness + mirror age, the next dated deadlines (TODAY
marked), the `feed_pending` attribution count, and the shrine heartbeat's currency
against the ledger. Runs the validator in a subprocess; modifies nothing. The first
command any fresh AI (or the Commander) runs instead of asking "what's next."
**Also in 3300:** `cue/standing-directives.json` — the typed directive registry
(id/class/authority/scope/rule/enforcement/provenance per directive; 11 standing
directives incl. the autonomy ladder and the seven stop-lines). **Check 25** fails
the tree if the registry corrupts, loses its enforcement mapping, or references
mechanisms that don't exist — the research memo's "prose never enforces" made
machine-checkable.

### 13. `verify_apply.py` — the post-apply auditor (read-only)
```
python3 scripts/verify_apply.py            # report, always exit 0
python3 scripts/verify_apply.py --strict   # exit 1 on FAIL-class findings
python3 scripts/verify_apply.py --self-test
```
**Answers the question the 3200 incident taught us to ask:** "did the last apply
actually land?" Version drift (README vs CHANGELOG), validator verdict, unsanctioned
vehicles still in Brain/, committed transport (runners/PATCH_NOTES), shrine-lag
(AI_RULES II.9), pending ratifications — one screen. CI runs it on every push,
NON-BLOCKING, into the job summary: the tree reports its own apply state; a push can
never be blocked by it, and a half-finished apply can never hide again.

## WHAT IS NOT HERE YET

Stated plainly so a session does not assume capability it lacks:

- **The scheduled fetch is BUILT but UNARMED.** `.github/workflows/ical_fetch.yml` runs
  daily (01:30 Manila): it pulls the feed from the `RADIATION_ICS_URL` secret and commits
  the scrubbed mirror `Brain/courses/CALENDAR.md` when the feed changed. It stays inert
  until the secret exists — and the secret comes ONLY after the old URL is rotated
  (the `4a98e59` exposure). Validator check 22 guards the mirror: URL inside it = FAIL,
  older than 7 days = WARN.
- **No router UI for the calendar** — CALENDAR.md is regenerated by CI and readable;
  a fresher query interface (per-week views, filters) awaits a session that needs one.
- **No admitted Core cards.** The tooling is live (nota.py scaffolds and checks
  shape), but admission needs Shield-stamped claims run through the six-box pass —
  a session act that has not happened yet.
- **CI runs 2 of the 7 scripts** (`validate.py` + `knowledge_regression.py`). The other
  five are session-invoked by hand. That is deliberate: they need arguments a runner
  cannot guess.
