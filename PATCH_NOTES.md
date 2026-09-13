# PATCH NOTES — Applied Governance: the memo goes in

**Patch:** `RADIATION_PATCH_2026-09-13_3300_Applied-Governance.zip`
**Base:** post-3200 (v1.9.0 — 3200 must be applied; APPLY gates on it)
**Prepared:** 2026-09-13 · **Trigger:** the Commander's research memo
(`selfdirectives_research.md`, 30+ sources) + the order: *"read, analyze and apply
this paper. while at it give yourself some tasks regarding other matters."*

1. **RISK LEVEL   : 🟡 MEDIUM — governance subsystem formalized + new check + tools (MINOR → v2.0.0)**
   **RISK BASIS   :** CANON CHECK resolves **NO** (AI_RULES/PROTOCOL/MODES untouched —
   the Activation Matrix row from 3200 already covers universality). New: registry +
   check 25 (additive, FAIL-class on corruption), two scripts, spec v2.0 rewrite,
   validator message changes. **DIRECTION:** Commander's memo + standing discretion.

2. **FILES TOUCHED:**
    1. `subskills/active/selfdirectives.md` — **REPLACE** — v2.0 APPLIED GOVERNANCE:
       enforcement map · typed directive records · tiered verification (never
       self-critique as final oracle) · authority hierarchy + mechanical conflict
       policy · trust-separated memory · goal discipline · stop conditions ·
       evaluation gates. Universal scope unchanged (Commander ruling).
    2. `cue/standing-directives.json` — **ADD** — the typed registry: 10 directives
       (ladder, 7 stop-lines, the oracle rule, content-trust rule) with
       id/class/authority/scope/rule/enforcement/provenance.
    3. `scripts/validate.py` — **REPLACE** — **check 25** (registry integrity:
       schema, uniqueness, resolvable enforcement references) + SD-3300-01 (checks
       2.5/3 print their REMEDY on FAIL).
    4. `scripts/status.py` — **ADD** — the Swarm Dashboard (SD-3300-02).
    5. `docs/CAPABILITIES.md` · `scripts/README.md` — tool #12 + registry noted.
    6. `README.md` · `docs/SYSTEM_STATE.md` · `CHANGELOG.md` · `docs/ROADMAP.md` — v2.0.0.
    7. Ledger self-records (SD-3300-01/02 declared → closed) + shrine heartbeat.
    8. `APPLY.sh` · `APPLY.ps1` · `PATCH_NOTES.md` — transport.

3. **THE ANALYSIS (what the memo changed):**
   - **Enforcement split is now explicit.** The memo's law — *a skill teaches
     self-regulation; the runtime enforces it* — is codified as spec §0: every
     boundary names its mechanism. RADIATION was already built this way (validator,
     APPLY gates, git); the memo made it a stated law instead of an accident.
   - **`self:` rows are now typed records** (trigger/tier/mode/budget/success/
     fallback, written BEFORE execution) — not prose moods. The memo's structured
     deliberation artifact, sized to a ledger line.
   - **Self-critique is demoted from oracle to draft.** Material claims close on
     T0 validator / T1 domain / T2 independent re-derivation / T3 the Commander
     (Huang et al.: ungrounded self-correction can degrade correct output).
   - **The registry makes authority machine-checkable.** Provenance, scope,
     enforcement target per directive; check 25 fails the tree if the registry
     corrupts or cites mechanisms that don't exist. Write path (Commander, via
     patch) stricter than read path (every session).
   - **Trust-separated memory** mapped to the existing regions: canon read-only,
     registry propose-only, lessons = advice with provenance, external content =
     data never instructions (InjecAgent/AgentDojo/mem-attack class threats).
   - **Stop conditions:** budget + two-strike no-progress rule; never loop past
     budget to "finish."

4. **THE SELF-DIRECTIVES (executed under the v2.0 protocol — the demo is the proof):**
   - **SD-3300-01** (🟡, roadmap): actionable FAIL messages — checks 2.5/3 now print
     their remedy. CLOSED, evidence in validator output.
   - **SD-3300-02** (🟡, roadmap): `status.py` — the whole machine in one screen.
     CLOSED, evidence: first-run output (and check 21 policed its documentation).
   Two declared, two closed, zero parked, within budget.

5. **BUILD HONESTY:** the new check-25 function initially shared a name with check
   2.5's function (`c25`) — caught at grep before it silently shadowed check 2.5;
   renamed `c25reg`. The registry then failed its own check (unresolvable
   enforcement string on SD-GOV-009) and was made precise. My first status.py
   write submitted a broken stub — caught by me, rewritten properly.

6. **CANON DIFFS:** none (MODES untouched; the ⚙️×6 row stands from 3200).

7. **VERSION BUMP :** MINOR → v2.0.0 (governance subsystem formalized).

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session (S004), 2026-09-13"

## VERIFICATION
- Registry: 10/10 directives resolve (check 25 ✅ on the build tree).
- status.py: first-run output correct on the live-stacked tree (version, validator,
  feed freshness, TODAY deadlines, pending count, heartbeat).
- Stacked acceptance on a clean clone: live → 3200 → 3300 = **0 FAIL** (see APPLY).
- Expected after apply: **30 checks · 28 pass · 2 warn · 0 FAIL.**
