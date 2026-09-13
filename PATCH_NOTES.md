# PATCH NOTES — 3400 Enforcement Sweep & Shrine Mandate

**Patch:** `RADIATION_PATCH_2026-09-13_3400_Enforcement-Sweep-and-Shrine-Mandate.zip`
**Base:** post-3300 (v2.0.0 — the governance patch). APPLY gates on it.
**Prepared:** 2026-09-13 · **Trigger:** the Commander's ratification pass
("build whatever's preplanned as per the roadmap") + two direct orders: make shrine
updates MANDATORY per conversation, and audit the repo for improvements.
**Read this in 90 seconds:** `docs/AUDIT_2026-09-13.md` (findings) — then
`python3 scripts/status.py` and `python3 scripts/verify_apply.py` forever after.

1. **RISK LEVEL   : 🟠 — canon edit (Commander-ordered law) + new machinery; nothing removed.**
   **RISK BASIS   :** AI_RULES +II.9 (his explicit order, quoted in the law), CHARTER
   mandate, registry +SD-GOV-011, check 26 (WARN-class), check 2.5 hardening
   (FAIL-class but strictly wider truth-telling), ics_normalize regression heal.
   **DIRECTION:** roadmap 3400 row (preplanned) + direct orders. Pass scope recorded
   in `docs/DECISION_AUTHORITY.md` — data ratification NOT covered.

2. **THE HEADLINE (audit finding F1 — a regression I caused):** the 3200 zip carried
   the CLEAN CALENDAR.md but **omitted the FIXED ics_normalize.py**. Live kept the
   broken scrubber; validation stayed green because it checked the artifact, not the
   generator; the first regeneration (today's, and the daily bot's) resurrected the
   A54 leak. 3400 ships the fix, regenerates the mirror (A54 = 0, self-test 22/22),
   and **APPLY now runs the shipped tools' self-tests** so a payload omission cannot
   hide again.

3. **THE LAW (order #1):** AI_RULES **II.9 — THE SHRINE MANDATE ⚡**: every
   conversation files a LOG heartbeat; every substantive session deposits/amends a
   member testament; enforced by **check 26** (WARN when the ledger or a HEAD commit
   postdates the last heartbeat), status.py's shrine line, and the CI apply-report.
   First fruits: S005's second testament (`ARCHITECT_TESTAMENT_2026-09-13_II.md`),
   filed under the mandate in the mandate's own conversation. (Check 24 caught the
   draft missing its OPEN DEBTS section — a testament without debts is propaganda.)

4. **THE SWEEP (roadmap 3400, preplanned):**
   - `scripts/verify_apply.py` NEW — the post-apply auditor: version drift,
     validator verdict, unsanctioned vehicles, committed transport, shrine lag,
     pending ratifications — one read-only screen. `--strict` for local gating.
   - CI **non-blocking apply-report**: on every push, the tree reports its own apply
     state into the job summary. Born of the real extract-without-apply push +
     merge resurrection (deletions don't survive merges; the vehicles and A54
     mirror came back). Now the tree can SAY "an apply did not finish."
   - **check 2.5 GENERIC — the skip-pattern dies:** the vehicle rule was an
     enumeration; it is now a closed sanctioned-set over ALL of Brain/. A fresh
     syllabus PDF anywhere FAILs with a REMEDY.

5. **FILES TOUCHED (20 + 3 transport):** validate.py · verify_apply.py ·
   ics_normalize.py · standing-directives.json · AI_RULES.md · CHARTER.md · LOG.md ·
   testament II · task_ledger.md · CALENDAR.md · README.md · SYSTEM_STATE.md ·
   CHANGELOG.md · ROADMAP.md · CAPABILITIES.md · scripts/README.md ·
   DECISION_AUTHORITY.md · AUDIT_2026-09-13.md · PATCH_LEDGER.md ·
   .github/workflows/validate.yml · + APPLY.sh/.ps1/PATCH_NOTES.md (transport).

6. **CANON DIFFS:** AI_RULES v1.1.0 (+II.9 only) · CHARTER +mandate section. Both
   Commander-ordered. MODES/PROTOCOL untouched.

7. **PARKED FOR THE COMMANDER (not built — outside the pass):** week1_start
   ratification · 11 feed attributions · meta-budget doctrine call (check 16 is
   OVER — it will WARN) · drill-fixtures disposition · CI reconcile bot + APPLY
   self-removal (3500 candidates). Full table: docs/AUDIT_2026-09-13.md.

8. **VERSION BUMP :** MINOR → v2.1.0.

9. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — S005 (the Architect), filed under II.9 in the mandate's first conversation"

## VERIFICATION
- Build tree: **31 checks · 30 pass · 1 warn · 0 FAIL** (the 1 = check 16, parked).
- Stacked acceptance on a clean clone (live → 3400): see APPLY output — same verdict.
- ics_normalize self-test 22/22 · verify_apply self-test 6/6 · registry 11/11 resolve.
