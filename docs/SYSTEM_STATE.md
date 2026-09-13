# 📡 SYSTEM STATE (`docs/SYSTEM_STATE.md`)
## Current Ground-Truth Snapshot — the ONLY overwrite-permitted file (II.2 exception)
**Last updated:** 2026-09-13 · **Version:** v2.3.1
**Updated by:** Protocol Architect (Patch proposal; effective at the Commander's push)

---

## 🎯 THE SITUATION — read this before anything else

*This is what the session is standing **in**. The rest of the boot tells you how to
behave; this tells you **where you are**. Keep it current — it is the difference
between an AI that knows the rules and an AI that knows the situation.*

**Who:** the Commander — Mapúa University, BS Architecture, ALE-bound.
**Purpose of this repository:** a public, copy-pasteable assistant. Link + magic words
→ an AI that knows the Commander's schedule, knowledge, sources and tools.
**Term 1, AY 2026-2027: 6 courses · 18 units.**

### Schedule — 36.0 contact-hours/week · **Wednesday and Sunday FREE**
*(rooms and sections: `Brain/courses/SCHEDULE.md` — published at full fidelity)*

```text
Mon  07:30–12:00 AR163-1P            · 16:30–21:00 AR153P
Tue  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10 · 18:00–21:00 AR173-1P
Thu  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10
Fri  09:00–12:00 AR163-1P (online)   · 15:00–16:30 MEC30-7 (online)
                                     · 16:30–19:30 AR153P (online)
Sat  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10 (online)
                                     · 12:00–16:30 AR173-1P · 18:00–21:00 MEC30-7
```
**Heaviest:** Mon and Sat (9.0 h each). **Lightest weekday:** Thu (3.0 h).
**50 % online** (18.0 h). Longest block 4.5 h — treat as unavailable.
**Anchor:** `week1_start` = **2026-08-24** (inferred from the LMS feed's Coursera
Week-1 report; one Commander word ratifies it). Week numbers are now dates.

### What the Commander KNOWS
`docs/KNOWLEDGE_REGISTRY.md` — **45 K-IDs** (36 live). Highest-yield courses:
**AR173-1P (9) · AR163-1P (8) · AR153P (8)** — the three carrying the licensure yield.

### What can be REACHED
`Brain/external_sources/INDEX.md` — **12 collections** (Law, Books, HOA, TOA, Building
Utilities, Building Technology, Professional Practice, …) · per-course readings and
graded items: `Brain/courses/INDEX.md`.

### What can be RUN
`docs/CAPABILITIES.md` — **13 scripts** (validate · regression · plan_term ·
ingest · anki · grade · decay · ics_normalize · nota · module_scaffold). `docs/SKILLS.md` says how to think; that file says
what can be executed.

---

## REPOSITORY VERSION
**RADIATION v2.3.1** — the Core has radiated: CARD_001 (BP 344) admitted via 3 independent channels; 02-analyze exercised; the 1:12/1:20 generation trap locked to KR-LAW-005. Previously: v2.3.0 — self-directed work is now CURATED work: proc_self-directive v1.1 (default-deny + classifier triad, the curation gate, reflection triggers, rollback closure, draw quota) + SD-GOV-012 + the compression ladder (episode→cue→directive promotion + verified-slowest decay). Previously: v2.2.0 — the Autopilot pipeline is INSPECTABLE: the neuron relay (`scaffolding/neurons/`, research-applied closed-loop design) records every 🟡 build at stage granularity; `proc_self-directive.md` operationalizes @selfdirectives; WAYFINDING routes the lost; TOOLBOX grades the rescue kit; the vehicle-resurrection loop is dead (untrack). Previously: v2.1.0 — enforcement sweep complete: apply state is AUDITABLE (verify_apply.py + CI non-blocking apply-report), the vehicle rule is generic, the shrine mandate (AI_RULES II.9) is law with teeth (check 26), and a 3200 payload omission (the A54 scrubber fix) was caught by regenerating and HEALED. Previously: v2.0.0 — applied governance: the Commander's research memo is IN the
spec (typed directive records, enforcement map, tiered verification, authority
hierarchy, trust-separated memory, goal discipline, stop conditions), the registry
(`cue/standing-directives.json`) is machine-guarded by check 25, and `status.py`
gives the whole machine in one screen. Previously: v1.9.0 — the swarm can self-govern: `@selfdirectives` (Commander-proposed,
built on recycled Marciale standing-order laws) grades every autonomous act
🟢/🟡/🔴 and closes with evidence. Previously: v1.8.1 — the calendar is FED: the LMS feed is a committed file
(`Brain/courses/0_CALLENDER/TERM1_FEED.txt`), the Deadline Engine merged it into the
register (37 items · 19 dated · week1_start = 2026-08-24, inferred), and CI
regenerates the calendar mirror from it on every push — the Commander's own push
cadence is the timer. Previously: v1.8.0 — the emission layer: the Core and the modules are now
TOOL-GUARDED (`nota.py`, `module_scaffold.py` — born-valid output, shape enforced),
the regression net holds 9 locked assertions, and check 13's link census runs in CI.
Previously: v1.7.0 — swarm memory and signal: the shrine (`docs/shrine/`, recycled
from Marciale-OS as a COMMONS — the Commander struck inheritance), the session
loading dock (`outputs/`), the calendar's daily cron
(built, armed only after the feed URL is rotated), and a committed calendar mirror.
Previously: v1.6.6 — the calendar works (ICS normalizer). (Version history: `CHANGELOG.md` — the single source. It is not
recited here any more; the recital was duplicated byte-for-byte and cost the boot budget.)

## CURRENT STATE *(corrected 2026-09-13 — this section was stale by nine patches)*
- **Brain content is NOT empty.** 45 K-IDs registered (36 live); two full ingestions
  completed (K-CUR-005 Building Utilities · K-CUR-006 Building Technology, 50 files /
  1,177.9 MB); one drill set forged and graded; mastery ledger seeded.
- Six course records in `Brain/courses/` (K-CUR-007…012), the authoritative weekly
  timetable in `SCHEDULE.md`, term plan in `Brain/short_term/plan/`.
- Machine Enforcement Layer live: `scripts/validate.py` (31 checks) +
  `knowledge_regression.py` (9 locked · 5 pending) + CI on every push (now incl. the
  external-link census, `RADIATION_ONLINE=1`).
- Registers live: TASK · PATCH · MASTERY · MISTAKE · DECAY · CONFLICT · KNOWLEDGE (45).
- The Core (09-nota/) holds **no admitted cards yet** — genuine and still true.
- **Three open items:** ① the LMS feed URL committed in `4a98e59` is **live — rotate it
  at source** (no patch can revoke it); ② five vehicles still tracked under
  `Brain/courses/` (extraction verified complete — records already claim them deleted);
  ③ knowledge assertions: 9 of 14 locked (the BU/BT render-verified values are now pinned); 5 still pending on the PD 1096 IRR full-text.
  (②'s vehicles are re-homed by patch 2900's APPLY — the records become true at apply.)

## 🩺 COMPONENT HEALTH CHECKLIST
| Component | Status |
|---|---|
| Constitution (docs/AI_RULES.md, 4 Books) | ✅ FULLY POPULATED |
| Entry gate (docs/.readme) + BOOT_SEQUENCE | ✅ FULLY POPULATED |
| Modes + Activation Matrix (docs/MODES.md) | ✅ FULLY POPULATED |
| Autonomous Scan (docs/CUE_SYSTEM.md) | ✅ FULLY POPULATED |
| Styles (10 skeletons + index) | ✅ POPULATED (v1.0 drafts; refine via use) |
| Core scaffolds (8 + INDEX) | ✅ FULLY POPULATED |
| Subskills (4 passive + 3 active) | ✅ FULLY POPULATED — `selfdirectives` v2.0 APPLIED GOVERNANCE (memo-applied; registry check 25) |
| Patch machinery (protocol, ledger, form) | ✅ FULLY POPULATED |
| Brain STRUCTURE (5 regions + movement rules) | ✅ COMPLETE |
| Brain/external_sources catalog | ✅ OPERATIONAL — 12 collections |
| **Brain CONTENT** | ✅ **POPULATED** — 2 ingestions, 45 K-IDs, 1 drill set |
| **Schedule record** | ✅ **PUBLISHED** — `Brain/courses/SCHEDULE.md` (A1) |
| **Capability registry** | ✅ **POPULATED** — `docs/CAPABILITIES.md` (8 tools) |
| Skill jurisdictions 01–09 | ✅ STRUCTURAL / 🕳️ artifacts await sessions |
| cue/ lexicon + inference log | 🌱 SEEDED — grows via II.5 |
| The Core (09-nota/) | 🧰 TOOLING LIVE (`nota.py`) — shape guarded; no admitted card yet |
| **Shrine** (`docs/shrine/`) — the swarm's shared judgment | ✅ **SEEDED** — charter + living testament + heartbeat LOG (file-at-delivery doctrine, check 24) |
| **Session outputs** (`outputs/`) | ✅ **CONTRACT LIVE** — check 23 enforces it |
| **Calendar mirror** (`Brain/courses/CALENDAR.md`) | ⏳ BUILT, UNARMED — rotate, then arm |

## KNOWN GAPS / NEXT EXPECTED WORK
- **Study output is the bottleneck, not infrastructure.** 1 mastery row exists and it is
  a fixture, not a Commander attempt. check 20.5 asks for a real `attempt:` marker.
- Knowledge assertions: 5 of 9 PENDING on raw primaries (PD 1096 IRR, RA 9514 IRR).
- **Calendar FED and closed-loop** — the Commander pushes the LMS export (`TERM1_FEED.txt`); CI regenerates `CALENDAR.md`; `deadline_feed.py` merges it into the register; `plan_term.py` eats it with zero arguments. `week1_start` = 2026-08-24 (INFERRED from Coursera W1 — one Commander confirm ratifies it). 11 feed items remain UNATTRIBUTED for the Commander (sibling hints attached).
- `week1_start` unrecorded (see THE SITUATION).

## HANDOVER NOTE
Boot per `docs/.readme`, read the last 3 `task_ledger` entries, then **read THE
SITUATION above** before planning anything. If the task touches the system itself,
read the newest testament in `docs/shrine/members/` first (CHARTER §3). Standing
orders: `docs/COMMANDER_QUICKREF.md` §5. Await the Commander.
