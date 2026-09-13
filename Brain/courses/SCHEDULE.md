# 🗓️ TERM SCHEDULE (`Brain/courses/SCHEDULE.md`)
## The Commander's weekly class timetable — the authoritative meeting pattern
**Version:** 1.0 | **Constitutional basis:** II.6 (Brain integrity) | **Region:** `Brain/courses/`
**Origin:** Commander's order, 2026-09-13 — *"I permit 2, the full CSV in the repo."* Amendment A1 to P-10 §3.3.
**Supersedes:** `Brain/courses/SCHEDULE.csv` (grid-form; retired by this record) and the earlier `SCHEDULE.png`.

---

## WHAT THIS IS

The weekly meeting pattern for **Term 1, AY 2026-2027** — 6 courses, 18 units. It answers
*"when am I in class"*, which the course records cannot: they say what is taught and
what is graded, never when the room fills.

**This record is published at full fidelity by explicit Commander decision.** Room and
section codes are included, because the point of this repository is that a fresh AI,
given the link and the magic words, knows the Commander's schedule. Location
identifiers are permitted **in this file only** — every other file in the region remains
bound by the identifier rules (see `INDEX.md` rule 3 and validator amendment A1).

**A live-lesson note:** rooms change. If a class is relocated, this record is stale until
edited — and a stale room is worse than no room.

## THE WEEK

| Day | Time | Course | Section | Room | Mode | Hrs |
|-----|------|--------|:--:|:--:|:--:|:--:|
| Mon | 07:30–12:00 | AR163-1P | E01 | S308 | campus | 4.5 |
| Mon | 16:30–21:00 | AR153P | E01 | S300 | campus | 4.5 |
| Tue | 07:30–09:00 | GED103 | A3 | ONLINE | online | 1.5 |
| Tue | 09:00–10:30 | DSS10 | A4 | NW408 | campus | 1.5 |
| Tue | 18:00–21:00 | AR173-1P | A54 | SW304 | campus | 3.0 |
| Thu | 07:30–09:00 | GED103 | A3 | ONLINE | online | 1.5 |
| Thu | 09:00–10:30 | DSS10 | A4 | SW200 | campus | 1.5 |
| Fri | 09:00–12:00 | AR163-1P | E01 | ONLINE | online | 3.0 |
| Fri | 15:00–16:30 | MEC30-7 | C5 | ONLINE | online | 1.5 |
| Fri | 16:30–19:30 | AR153P | E01 | ONLINE | online | 3.0 |
| Sat | 07:30–09:00 | GED103 | A3 | ONLINE | online | 1.5 |
| Sat | 09:00–10:30 | DSS10 | A4 | ONLINE | online | 1.5 |
| Sat | 12:00–16:30 | AR173-1P | A54 | S303 | campus | 4.5 |
| Sat | 18:00–21:00 | MEC30-7 | C5 | S301 | campus | 3.0 |

**Total contact time: 36.0 h/week** over five days (Mon · Tue · Thu · Fri · Sat).

## PER-COURSE PATTERN

| Course | Meetings | Weekly hours | Days |
|---|:--:|:--:|---|
| AR163-1P | 2 | 7.5 | Mon (4.5 campus) · Fri (3.0 online) |
| AR153P | 2 | 7.5 | Mon (4.5 campus) · Fri (3.0 online) |
| AR173-1P | 2 | 7.5 | Tue (3.0 campus) · Sat (4.5 campus) |
| GED103 | 3 | 4.5 | Tue · Thu · Sat — all online, 1.5 h each |
| DSS10 | 3 | 4.5 | Tue · Thu · Sat — Sat online |
| MEC30-7 | 2 | 4.5 | Fri (1.5 online) · Sat (3.0 campus) |

## DERIVED FACTS — for planning

- **Free weekdays: Wednesday and Sunday.** Wednesday is the **only clear weekday** — the
  single largest study block in the week. Any planning routine targets these by default
  rather than proposing slots that do not exist.
- **Heaviest days: Monday and Saturday**, 9.0 h each. **Lightest weekday: Thursday**, 3.0 h.
- **Online share: 18.0 h/week — exactly 50 %.** GED103 is fully online; AR163-1P and AR153P
  each have one online session; DSS10's Saturday is online; MEC30-7's Friday is online.
- **Longest single block: 4.5 h** — AR163-1P Mon, AR153P Mon, AR173-1P Sat. These are
  studio/lab blocks; treat as unavailable for anything else.
- **Five of six courses meet on Saturday** — the week's second anchor day.

## OPEN DATUM — the anchor

**`week1_start` (the Monday of week 1) is not yet recorded.** Until it is, every date in
the term plan resolves in *weeks*, not days. The planner states this itself:

> *"ANCHOR ABSENT — planning in WEEKS (no syllabus prints a date). supply `--anchor` or let
> the LMS ICS supply it; **+1 datum, everything dates.**"*

One date converts the whole term from relative to absolute. It should come from the
academic calendar or from the LMS feed anchor.

## PROVENANCE

| Fact | Source | Grade |
|---|---|---|
| Meeting days, times, rooms, sections | Commander's timetable, committed 2026-09-13 (`SCHEDULE.csv`, since retired) | `[D]` |
| Course codes and titles | `Brain/courses/INDEX.md` register + `K-CUR-007…012` | `[D]` |
| Contact hours and derived load | computed from the table above | `[O]` |
| `week1_start` | **not held** | — |

**Consecutive-slot assumption:** the timetable's 4.5 h blocks are recorded as single
meetings. If any block is actually two or three stacked sessions, the total is unchanged
but the per-meeting count is not. Commander to confirm if it ever matters.
