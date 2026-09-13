# PATCH NOTES — 4400 Reconciliation (due-diligence remediation, Milestones A–C)
**Patch:** `RADIATION_PATCH_2026-09-14_4400_Reconciliation.zip` · 🟠 · v2.7.0
**SUPERSET of 4200 + 4300.** Base: your current main (`c9592bba`, validator RED ×3) — this apply IS the fix.

## ⚠️ THE SEAL — do all three steps (this is what 4300 was missing)
Your main is red because the 4300 payload was committed BEFORE its runner reconciled the tree.
4400's APPLY is built as the completion of that transaction:
```bash
unzip -o RADIATION_PATCH_2026-09-14_4400_Reconciliation.zip -d /path/to/RADIATION
cd /path/to/RADIATION && bash APPLY.sh          # (or .\APPLY.ps1)
git add -A && git commit -m "Seal 4400 reconciliation patch" && git push
```
After push, a FRESH clone must show: `34 checks · 33 pass · 1 warn · 0 FAIL`. That is the exit criterion.

## What this patch does
1. **F-01/F-02 — release hygiene, mechanically:** APPLY cross-removes BOTH runners (+ notes); check 3
   now FAILs on any committed runner; vehicles untracked/re-homed; duplicate active TIDs faded.
2. **F-03 — the Core gate finally guards the Core:** `nota.py` speaks the canonical contract
   (`09-nota/CARD_###` + `core-card/v1` front matter + exact index parity). Both real cards migrated
   (content untouched — envelope + 2 structural headers added). **check 29** pins it; CI already runs it.
3. **F-04 — the relay judges content, not filenames:** `radiation_core.relay` validates task bundles
   (envelope/plan/commands/outcomes/events): digest-verified evidence, state-machine transitions,
   Markdown projection fidelity. Pre-runtime TIDs a–g = `legacy_trace` (never fabricated); **TID-h
   (this build) is the first canonical bundle**. Negative vectors: 3/3 — garbage motor records now FAIL.
4. **F-06 — facts are generated, not remembered:** `scripts/render_docs.py` computes counts/inventories
   from reality (checks, locks, K-IDs, cards, subskills incl. fetch/overule, scripts, CI coverage);
   `--check` fails CI on drift. Stale prose (26 checks / 4+2 subskills / 45 K-IDs) corrected at source.
5. **F-07/F-08 — time tells the truth:** validator exposes `--json` + importable `run_all()`;
   status/verify_apply consume structure, not scraped text; activity = first table column only (the
   "LAGS 2027" false alert is gone); `grade_exam.py --attempted-at` (default: today).
6. **F-05 — honest labels:** passives declared protocol checks (in-context, advisory unless machine-
   backed) in .readme, the 4 passive specs, and the generated roster. Mode-inference contradiction
   resolved per the ratified BOOT ASK law — README aligned to it, law untouched.
7. **Milestone D — STAGED, not built:** a policy-gateway/executor runtime (auditor §5.2) is the
   Product-2 fork and needs your explicit scope ratification. Say "ratify Product-2 scope" if you
   ever want it; until then the honest hybrid stands (their §5.1 option 1, with teeth).
8. **Expected after apply:** 34 checks · 33 pass · 1 warn (meta-budget, standing) · 0 FAIL ·
   regression 11 locked / 0 failed · nota 2/2 cards · relay 0 findings.

**DECLARATION:** "This Patch is a proposal. It has no effect until the Commander applies it.
— S005, relay TID-2026-09-14-h (the first canonical bundle)"
