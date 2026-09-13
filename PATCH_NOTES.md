# PATCH NOTES — @SELFDIRECTIVES: the swarm self-governs

**Patch:** `RADIATION_PATCH_2026-09-13_3200_Self-Directives.zip`
**Base:** post-3100 (v1.8.1 — 3100 must be applied; APPLY gates on it)
**Prepared:** 2026-09-13 · **Type:** DELTA

1. **RISK LEVEL   : 🟠 ELEVATED — canon addition (new subskill → MINOR v1.9.0)**
   **RISK BASIS   :** a new ACTIVE subskill is a canon addition (IV.4 travels as 🟠).
   **RATIFICATION IS INHERENT:** the subskill was PROPOSED BY THE COMMANDER ("I
   propose a subskill called @selfdirectives… you may expand on this one") and built
   under the standing discretion. The proposer is the ratifier; this notes-file is
   the record, not a request. The honest 🟠 stands because the system is granting
   itself bounded initiative — the stop-lines (§4 of the spec) are the
   constitutional grant, and they are severable: delete the file and the autonomy
   ends without touching anything else.

2. **FILES TOUCHED:**
    1. `subskills/active/selfdirectives.md` — **ADD** — the spec (six mandatory blocks).
    2. `subskills/SUBSKILL_INDEX.md` — **REPLACE** — actives table 2→3.
    3. `cue/autopilot-cues.md` — **REPLACE** — standing order 6: the AUTONOMY LADDER
       + reversibility-weighted asking + stop-lines.
    4. `docs/COMMANDER_QUICKREF.md` — **REPLACE** — the "work on stuff" contract.
    5. `docs/SYSTEM_STATE.md` · `README.md` · `CHANGELOG.md` — v1.9.0.
    6. Shrine heartbeat (LOG + testament) — §6 doctrine.
    7. `APPLY.sh` · `APPLY.ps1` · `PATCH_NOTES.md` — transport.

3. **WHAT WAS RECYCLED vs REJECTED (the Commander asked for the harvest):**
   RECYCLED: the Letters-of-Last-Resort discipline (preserve reversibility · never
   manufacture completion · repository truth over model memory), the severity
   classifier (→ the 🟢/🟡/🔴 autonomy ladder), the Zero-Paralysis intake (→
   reversibility-weighted asking: act with declared assumptions when cheap).
   REJECTED: the persona squad — roles must be staffed; skills need no staffing.
   RADIATION is a swarm by order.

4. **THE MECHANISM (one screen):** trigger (grant / roadmap / environmental cue /
   close) → SOURCE it verbatim → GRADE the tier → DECLARE (`self:` ledger row) →
   EXECUTE bounded (one patch per directive) → CLOSE with evidence. 🔴 tier work
   (canon, credentials, deletions, new powers) STOPS and proposes. Seven absolute
   stop-lines. One directive at a time. Everything auditable.

5. **CANON DIFFS:** the subskill itself (IV.4 — Commander-authored; see §1).

6. **VERSION BUMP :** MINOR → v1.9.0.

7. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session (S004), 2026-09-13"

## VERIFICATION
- Build tree: 29 checks · 25 pass · 2 warn · 2 fail (the known vehicles — cleared at APPLY).
- Stacked acceptance on a clean clone: 0 FAIL after apply (3100's reconciliation included here too).
- The spec satisfies the six-block subskill standard (MISSION · TRIGGERS · ACTIONS ·
  FORBIDDEN · FAILURE MODES · OUTPUTS) — the index's own spec rule.
