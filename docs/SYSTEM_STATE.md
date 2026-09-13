# 📡 SYSTEM STATE (`docs/SYSTEM_STATE.md`)
## Current Ground-Truth Snapshot — the ONLY overwrite-permitted file (II.2 exception)
**Last updated:** 2026-09-14 · **Version:** v2.9.0
**Updated by:** Protocol Architect (Patch proposal; effective at the Commander's push)

---

## 🎯 THE SITUATION

Boot files carry state, not narrative (II.10). History: `CHANGELOG.md` + the ledgers.

**Who:** the Commander — Mapúa University, BS Architecture, ALE-bound.
**Purpose:** a public, copy-pasteable assistant. Link + magic words → an AI that knows
the Commander's schedule, knowledge, sources and tools.
**Term 1, AY 2026-2027: 6 courses · 18 units.**

### Schedule — 36.0 contact-hours/week · **Wednesday and Sunday FREE**
*(rooms and sections: `Brain/courses/SCHEDULE.md`)*

```text
Mon  07:30–12:00 AR163-1P            · 16:30–21:00 AR153P
Tue  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10 · 18:00–21:00 AR173-1P
Thu  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10
Fri  09:00–12:00 AR163-1P (online)   · 15:00–16:30 MEC30-7 (online)
                                     · 16:30–19:30 AR153P (online)
Sat  07:30–09:00 GED103 (online)     · 09:00–10:30 DSS10 (online)
                                     · 12:00–16:30 AR173-1P · 18:00–21:00 MEC30-7
```

**Heaviest:** Mon and Sat (9.0 h each). **Longest block 4.5 h.** **50 % online** (18.0 h).
**Anchor:** `week1_start` = **2026-08-24** (inferred from the LMS feed's Coursera
Week-1 report; one Commander word ratifies it).

### What the Commander KNOWS
`docs/KNOWLEDGE_REGISTRY.md` — K-ID count GENERATED in the machine-facts block below.
Highest-yield courses:
**AR173-1P (9) · AR163-1P (8) · AR153P (8)** — the three carrying the licensure yield.

### What can be REACHED
`Brain/external_sources/INDEX.md` — **12 collections** · open-source bank:
`docs/OPEN_SOURCES.md` (50 categories, @Fetch's library) · per-course readings and
graded items: `Brain/courses/INDEX.md`.

### What can be RUN
`docs/CAPABILITIES.md` — script inventory GENERATED there. `docs/SKILLS.md` says how to think; that file says what can be executed.

---

## REPOSITORY VERSION
**RADIATION v2.9.0** — binding (patch 4600): every bundle object is schema- and
identity-bound (recursive execution, foreign plans hard-fail, verification
attests succeeded outcomes — 11 negative vectors in CI), planner/CI facts are
generated from data, and APPLY commits the sealed tree itself. Prior: 4500
last mile · 4400 reconciliation · 4300 compression law · 4200 the Commander's
expansion (@Fetch/@Overule/OPEN_SOURCES bank). Machine facts: GENERATED here.
Full version history: `CHANGELOG.md` (single source of record — not recited here, II.10.3).

## CURRENT STATE *(truth-up 2026-09-14)*
- **Machine Enforcement:** `scripts/validate.py` (check count GENERATED below;
  check 28 pins the
  activation matrix · check 15 gauges boot budget, II.10 gauge ACTIVE) +
  `knowledge_regression.py` (**11 locked · 5 pending**) + CI on every push.
- **Core (09-nota/): 2 admitted cards** — CARD_001 (BP 344 accessibility) · CARD_002
  (RA 10587 repeals PD 1308; K-LAW-009 REPEALED-GENERATION; exam answer-of-record
  pending Commander ruling — reviewer ⚑).
- **Registry:** 13 standing directives (SD-GOV-013 = the @Overule boundary).
  **Subskills:** 4 passive + 5 active (scout · colony · selfdirectives · fetch · overule).
- **Brain content:** K-IDs GENERATED below; 2 collection ingestions (K-CUR-005/006);
  6 course records; term plan in `Brain/short_term/plan/`.
- **Registers live:** TASK · PATCH · MASTERY · MISTAKE · DECAY · CONFLICT · KNOWLEDGE · DEBT.
- **Transport hygiene:** course vehicles + APPLY runners untrack/re-home at apply
  (idempotent); audit with `python3 scripts/verify_apply.py --strict`.

## OPEN ITEMS (the short list)
① LMS feed URL (committed `4a98e59`) is live — **rotate at source** (no patch can
revoke it) · ② `week1_start` INFERRED — one confirm ratifies · ③ 5 knowledge
assertions PENDING on raw primaries (PD 1096 IRR, RA 9514 IRR) · ④ 11 feed items
unattributed · ⑤ check 15 stays WARN-class until P-09 ratifies (frozen by order —
listed, not lost).

## 🩺 COMPONENT HEALTH (abridged, II.10)
| Component | Status |
|---|---|
| Constitution (AI_RULES, 4 Books + II.10) | ✅ CURRENT |
| Entry gate (docs/.readme) + BOOT_SEQUENCE | ✅ CURRENT |
| Modes + Activation Matrix (check-28-pinned) | ✅ CURRENT |
| CUE_SYSTEM + cue/ lexicon + inference log | ✅ CURRENT · 🌱 grows via II.5 |
| Subskills (4 passive + 5 active) | ✅ CURRENT — @Fetch/@Overule per 4200 |
| Core (09-nota/) | ✅ 2 cards · nota.py-guarded |
| Brain content | ✅ GENERATED facts · 2 ingestions · 1 drill set |
| Machine layer | ✅ GENERATED facts · CI |
| Shrine + session outputs contract | ✅ LIVE (checks 24/23) |
| Calendar mirror | ⏳ BUILT, UNARMED — rotate feed, then arm |

## HANDOVER NOTE
Boot per `docs/.readme`, read the last 3 `task_ledger` entries, then THE
SITUATION above. If the task touches the system itself, read the newest testament
in `docs/shrine/members/` first (CHARTER §3). Standing orders:
`docs/COMMANDER_QUICKREF.md` §5. Await the Commander.

<!-- GENERATED:machine-facts:START -->
**Machine facts (GENERATED — hand edits here are a CI failure; source: render_docs.py):** 34 validator checks · knowledge locks 11/16 (5 pending) · 46 K-IDs · Core 2/2 cards canonical · registry 13 directives · subskills 4 passive + 5 active · scripts 14 (8 exercised in CI)
<!-- GENERATED:machine-facts:END -->
