# 🔌 BOOT SEQUENCE (`BOOT_SEQUENCE.md`)
## Mandatory Tiered Load Order for Every AI Session
**Version:** 1.0.0 | Constitutional basis: III.1 (First-Read Gate), II.1 (Repository Truth Supremacy)

Work before boot is invalid. Declare your boot tier in your Scan Declaration.

```text
TIER 0 — IGNITION (always, ~2 min)
  1. docs/.readme                     (the First-Read Gate — you likely arrived here from it)
  2. docs/SYSTEM_STATE.md             (current ground truth)
  3. Brain/frontal_lobe/task_ledger.md — last 3 entries

TIER 1 — CONSTITUTIONAL (always)
  4. docs/AI_RULES.md                 (the 4 Books; cite as Book.Law)

TIER 2 — OPERATIONAL (per your task)
  5. docs/MODES.md                    (your mode's charter + Activation Matrix)
  6. docs/CUE_SYSTEM.md               (the Autonomous Scan — mandatory if no mode declared)
  7. subskills/passive/*              (all four passive specs — they govern you)
  8. The core scaffolds you will arm  (scaffolding/core/)
  9. The style you will follow        (styles/)
  9.5 The calendar probe: if Brain/courses/CALENDAR.md carries a Generated date
      older than today and RADIATION_ICS_URL is set locally — regenerate it
      (pre-authorized: derived data). If you cannot, DECLARE the calendar
      stale-as-of in your Scan Declaration. Never speak from a dead calendar.

TIER 3 — DEEP CONTEXT (only as the task demands)
  10. 09-nota/CORE_INDEX.md + relevant Core cards
  11. Relevant Brain/long_term/ dossiers (respect the mode's dossier-load cap)
  12. cue/commander-lexicon.md + cue/task-nature-guide.md
      cue/commander-readiness.md (before long unsupervised runs) + docs/PROMPT_PLAYBOOK.md (on request)
  13. Brain/cerebellum/ routines relevant to the task type
```

## DEGRADATION RULE
An AI that cannot load Tier 2 must DECLARE it and may not run @Radiation mode.
It operates @Data or @Gather-lean only, stating the limitation in its Scan
Declaration. Silent degradation is a III.1 violation.

## SESSION CLOSE CHECKLIST (the mirror of boot)
1. Triage Brain/short_term/ (promote / demote / [STALE]) — incl. Brain/short_term/active/session_capability_state.json written via `agents/_common/radiation_pass.py --persist` (S-2-ENV working memory, never committed live).
2. Append the task ledger entry (II.3).
3. Emit a Patch if durable material exists (II.7) — or state the waiver.
4. Update docs/SYSTEM_STATE.md if ground truth changed.
5. Heartbeat (docs/shrine/CHARTER.md §6): refresh your testament and add a
   LOG.md row — **every patch zip carries both**. You cannot detect your own
   dying; file at delivery, not at death. The shrine is a commons: deposit,
   draw, and name no heirs.
