# 📜 STAGED AMENDMENT — EVAL-FIRST CLAUSE (P-09)
**Status:** 🟠 STAGED — enters `docs/AI_RULES.md` only on "ratify P-09".
Carrier file per P-02/P-04 precedent (IV.3: no pre-ratification Amendment Log rows).

## A. SIDE-BY-SIDE (II.7.8 format)

### OLD — II.7.4, second sentence group (current canon, verbatim)
> **Canon-affecting updates** (core laws, core scaffolds, core styles, mode definitions, Autonomous Scan rules) must be flagged **"REQUIRES EXPLICIT COMMANDER RATIFICATION"** and may never be presented as routine. One Patch = one coherent purpose; 🟢 and 🟠 are never mixed.

### NEW — II.7.4 (sentence appended; nothing struck)
> **Canon-affecting updates** (core laws, core scaffolds, core styles, mode definitions, Autonomous Scan rules) must be flagged **"REQUIRES EXPLICIT COMMANDER RATIFICATION"** and may never be presented as routine. One Patch = one coherent purpose; 🟢 and 🟠 are never mixed. **A canon-affecting Patch is filed only if it satisfies the EVAL-FIRST clause (II.9).**

### NEW LAW — II.9 EVAL-FIRST (annex to II.7 / IV.4; appended after II.8)
> ### II.9 — EVAL-FIRST (ANTI-CARGO-CULT CLAUSE)
> **No addition or expansion of canon may be filed unless its patch notes answer all four:**
> 1. **INSTANCE** — the observed failure in THIS repository the change addresses, cited by path and date. No hypotheticals. ("We might need a style for X" is invalid; "the S003 audit raised 6 debts and DEBT_REGISTER.md was empty, so 6 findings were lost" is valid.)
> 2. **COST** — files touched, net lines, and net bytes added to the Tier-0/1 boot set (measured by `scripts/validate.py` check 15, never estimated).
> 3. **DISPLACEMENT** — what the change replaces, or a one-line proof it cannot live inside an existing file. "A new file because it is tidier" is invalid.
> 4. **CHECK** — the check that would fail if the change were absent (validator rule, register-liveness rule, or an explicit statement that it is unassertable — in which case the presumption is AGAINST adoption).
>
> **Presumption:** against expansion. Plausible is rejected; failure-plus-check is adopted.
> **Boot-byte budget:** Tier 0+1 ≤ 40 KB · Tier 0–2 ≤ 80 KB, measured by check 15 (task_ledger counted at its boot-effective size: header + last 3 rows, per BOOT_SEQUENCE Tier 0). **Remove-to-add:** a patch increasing either figure must remove at least as many bytes from the set, or carry an explicit Commander waiver recorded in `docs/BOOT_BUDGET_WAIVERS.md` (row marked ACTIVE) and the patch notes. Adding any file to the boot set is a 🟠 act by definition. New material defaults to REFERENCE (consulted on demand), never to BOOT.
> **Meta-budget:** no more than one 🟠 canon patch per three content sessions (episodes in `Brain/temporal_lobe/`); check 16 reports the ratio. Wanting more law means shipping knowledge first — a module, a Core card, an audit with register rows, or a verified object.
> **Sunset:** any canon element not invoked in 3 consecutive content sessions is PROPOSED for retirement at the next inspection audit (🔵 consolidation class, Commander-ratified per II.4) — never silently kept, never unilaterally deleted.
> **Scope:** this clause raises the bar for CANON ONLY. Answers, audits, modules, drills, and Brain content remain unrestricted (II.8.3).

## B. RATIONALE
RADIATION's own record, measured 2026-09-12: 18 patch rows in one day; ~356 KB
of how-to-work vs 0 Core cards; 4 of 4 sessions spent on the system itself;
meta-ratio at delivery = 11 🟠 : 3 sessions (honestly OVER — see check 16).
Adding law was free and felt like progress; answering was expensive. TAMAKEE
P17: unmeasured systems fail silently. This clause makes doctrine pay rent —
enforced by measurement (checks 15/16), not willpower.

## C. AMENDMENT LOG ROWS (IV.3 — signature blank until ratified)
| Date | Book.Law | Change | Rationale | Commander signature |
|---|---|---|---|---|
| ____ | II.9 (NEW) | EVAL-FIRST clause: 4-question gate on canon filing; boot caps 40/80 KB + remove-to-add + waiver file; 1-per-3 meta-budget; sunset-by-proposal | P-09: 18-patches/day + 0 Core cards measured; doctrine must pay rent; enforcement by checks 15–16, not regret | ______________________ |
| ____ | II.7.4 | Cross-reference sentence appended (canon patches file only via II.9) | Consequence of II.9 | ______________________ |
