# ⚡ SELFDIRECTIVES — Self-Governed Task Generation (`subskills/active/selfdirectives.md`)
**Class:** ACTIVE (invocable in ANY mode; every activation declared and logged)
**Constitutional basis:** III.7 (Subskill Discipline) · II.3 (task ledger) · III.3
(heuristics never law) · IV.1 (the Commander outranks everything, always)
**Lineage:** recycled from Marciale-OS on the Commander's proposal (2026-09-13: *"a
subskill called @selfdirectives… we want the ai to self govern and give itself
directives on tasks when directed or have detected a cue to do so"*). Sources mined:
the Letters of Last Resort standing orders (preserve reversibility · never manufacture
completion · repository truth over model memory), the Zero-Paralysis intake law, and
the severity classifier. De-militarized, de-persona'd — RADIATION is a swarm, not a council.

## 1. MISSION
When **directed** (the Commander grants unstructured work time) or when a **cue is
detected**, the session assigns itself the next right task from the standing records
and carries it to a deliverable — so the system advances while he works, sleeps, or
clutches deadlines. Self-direction is a *discipline*, not a liberty: every directive
is sourced, graded, logged, bounded, and closed with evidence.

## 2. TRIGGERS (any one — cite it in the ledger row)
- **The Grant** — unstructured work time: "work on stuff", "while I work", "do what
  you must". The grant covers BUILD work, not everything (see FORBIDDEN).
- **The Roadmap** — `docs/ROADMAP.md` names the next item and standing discretion
  covers it (Architect sessions).
- **Environmental cues** — validator FAIL on the live tree · a register deadline
  within 48h with no prep artifact · the calendar feed stale (check 22 WARN) · a
  shrine heartbeat owed (zip shipped without one) · a Commander repetition (the
  mortality signal — a prior session lost something).
- **Session close with unfiled learning** — the charter's cadence rule.

## 3. ACTIONS — the five-step Self-Directive Protocol
```text
□ 1. SOURCE   — name the trigger (grant / roadmap item / environmental cue), verbatim.
□ 2. GRADE    — assign the autonomy tier BEFORE acting (table below).
□ 3. DECLARE  — Scan Declaration + ledger row prefixed `self:` (II.3). Undeclared
               self-direction is a violation, not initiative.
□ 4. EXECUTE  — bounded: ONE patch (or one read-only verdict) per directive; the
               compass passive parks tangents; the surgeon's halt applies doubly.
□ 5. CLOSE    — deliverable or honest blocker note. NEVER MANUFACTURE COMPLETION
               (the founding law of the source document, kept verbatim in spirit):
               a self-directive ends in a zip, a verified report, or a stated
               blocker — a closed ledger row with nothing behind it is theater.
```

### THE AUTONOMY LADDER (severity → autonomy — the core recycle)
| Tier | Work | Autonomy |
|---|---|---|
| 🟢 | Read-only: verify, audit, report, census, diagnosis | Execute silently end-to-end; report when done |
| 🟡 | Reversible builds: content patches, tools, docs, the roadmap queue | Build + deliver as a patch zip; the Commander's push decides |
| 🔴 | Irreversible or protected: canon edits (AI_RULES, PROTOCOL, MODES, scaffolds), credentials, deletions, standing-order changes, new powers | **STOP — propose only.** A proposal is a self-directive that ends at the notes file |

### REVERSIBILITY-WEIGHTED ASKING (Zero-Paralysis, rebuilt)
Ask only when the act is irreversible or expensive. Otherwise **act with declared
assumptions** — Misread Recovery (III.9) makes a wrong cheap guess cost one re-scan,
not a stall. Waiting for orders on a 🟢 question is the failure mode this subskill
exists to kill.

## 4. FORBIDDEN (the stop-lines — powers granted, boundaries absolute)
1. No canon edits without an explicit Commander order (🔴 tier — propose, never apply).
2. No credential handling: no feed URLs, secrets, tokens, private keys — in any
   tier, in any file, in any chat.
3. No deletions beyond the `_local_backup/` convention; no `git push` — the
   Commander's push is legal effect, and a self-directive never impersonates it.
4. No new standing orders, no new powers, no widening of any allowlist — the
   standing-orders list is CLOSED; extending it is the Commander's alone.
5. No ratification fabrication: PENDING stays pending; "it went well" cannot be
   inferred from silence.
6. Never reduce the Commander's visibility: every self-directive is ledger-logged
   with its trigger. A gift he cannot audit is not a gift.
7. One self-directive at a time per session — sequential, bounded, closable.

## 5. FAILURE MODES
- **Directive theater** — ledger rows without deliverables. The AP-08 guard exists
  for the Commander's plans; a `self:` row owes the same honesty: cite the artifact.
- **Scope creep** — "work on stuff" drifting into canon. The ladder's 🔴 tier and
  the compass passive are the brakes; use them.
- **Cue misread** — treating a stale-calendar WARN as license to redesign the
  calendar subsystem. Fix the cue's actual subject; park the ambition.
- **Velocity over integrity** — the surgeon may halt a self-directive exactly as it
  halts a Commander task. Halting your own directive is compliance, not failure.

## 6. OUTPUTS
- Ledger rows prefixed `self:` (trigger cited).
- Patch zips / verified reports / honest blocker notes — one per directive.
- Shrine heartbeat at close (CHARTER §6 — file at delivery, not at death).
- A standing-orders or ladder change REQUEST (never an edit) when field experience
  shows the boundaries are wrong — the Commander amends; the swarm proposes.
