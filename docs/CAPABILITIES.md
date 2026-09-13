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
- **Offline** — none calls the network, except `ingest_collection.py`, which downloads
  only from a URL you pass it explicitly.
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

## WHAT IS NOT HERE YET

Stated plainly so a session does not assume capability it lacks:

- **No ICS fetcher.** `plan_term.py --ics` reads a local file only; the feed URL is a
  credential and lives in an env var / Actions secret, never in the repo.
- **No recurrence expansion.** `RRULE` is parsed to a frequency word and dropped.
  A weekly class therefore appears once, not eleven times.
- **No note-card generator** for the Core (09-nota/) — cards are authored by sessions.
- **CI runs 2 of the 7 scripts** (`validate.py` + `knowledge_regression.py`). The other
  five are session-invoked by hand. That is deliberate: they need arguments a runner
  cannot guess.
