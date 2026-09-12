# PROPOSAL P-09 — II.9 EVAL-FIRST + boot caps + meta-budget · ratify: "ratify P-09"
**Re-homed 2026-09-12 (Wave 1&2 closure): carriers moved from canonical dirs to lawful proposal homes per IV.2/IV.4/scaffolding-README §4. Text unchanged except path-reference hygiene. NOTHING below is applied until the Commander's ratification line.**


---
## ◈ Amendment rows + clause

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
> **Boot-byte budget:** Tier 0+1 ≤ 40 KB · Tier 0–2 ≤ 80 KB, measured by check 15 (task_ledger counted at its boot-effective size: header + last 3 rows, per BOOT_SEQUENCE Tier 0). **Remove-to-add:** a patch increasing either figure must remove at least as many bytes from the set, or carry an explicit Commander waiver recorded in docs/BOOT_BUDGET_WAIVERS.md (row marked ACTIVE) and the patch notes. Adding any file to the boot set is a 🟠 act by definition. New material defaults to REFERENCE (consulted on demand), never to BOOT.
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


---
## ◈ PROMPT_PLAYBOOK template

# STAGED — `docs/PROMPT_PLAYBOOK.md` addition (P-09, apply on "ratify P-09")
## Template: filing a canon proposal under EVAL-FIRST (II.9)

```markdown
### CANON PROPOSAL — <name>
1. INSTANCE     : <failure in THIS repo — path + date. No hypotheticals.>
2. COST         : <files touched; net lines; net Tier-0/1 boot bytes per check 15 — MEASURED>
3. DISPLACEMENT : <what this replaces, or proof it cannot live in an existing file>
4. CHECK        : <the validator/register check that fails without it — or "unassertable" (presumption: REJECT)>
```

**Worked COMPLIANT example (P-09 itself):**
1. INSTANCE     : 18 patch rows filed 2026-09-12 (docs/PATCH_LEDGER.md); 0 Core cards in 09-nota/; 4/4 sessions on system upkeep.
2. COST         : 0 boot files added; +0 boot bytes (clause enters AI_RULES: +~1.9 KB Tier-1, paid under the 40 KB cap with 7.3 KB headroom measured by check 15).
3. DISPLACEMENT : lives inside AI_RULES (new II.9) + existing validator — no new mandatory file.
4. CHECK        : checks 15 (cap breach) and 16 (ratio) fail/warn when violated; rejection record 08-overhaul/proposals/REJECTED_2026-09-12_* proves teeth.
```


---
## ◈ Original patch notes

# PATCH NOTES — RADIATION_PATCH_2026-09-13_1100_P09-EvalFirst-Clause-STAGED.zip
**Risk class:** 🟠 CANON-AFFECTING — ENTIRE PATCH STAGED, NOTHING APPLIED. Ratify: **"ratify P-09"**.
## CONTENTS
1. docs/AMENDMENT_ROWS_STAGED_P09.md — II.9 EVAL-FIRST full text + II.7.4 cross-ref + IV.3 rows (signature blanks)
2. docs/PLAYBOOK_EVALFIRST_TEMPLATE_STAGED.md — compliant-proposal template + worked example
## ON RATIFICATION
Insert II.9 + amend II.7.4 in AI_RULES.md · move amendment rows to the Log ·
append template to PROMPT_PLAYBOOK.md · check 15 auto-escalates WARN→FAIL-class
(it keys on "EVAL-FIRST" appearing in AI_RULES.md) · delete carriers · re-run
validator · bump version · AUTO-PATCH.
## EVAL-FIRST SELF-APPLICATION (this patch answers its own four questions)
INSTANCE: 18 rows/day, 0 Core cards, 4/4 system sessions (ledger + 09-nota/, 2026-09-12).
COST: +0 boot files; ratification adds ~1.9 KB to Tier-1 (headroom: 7.3 KB measured).
DISPLACEMENT: no new mandatory file — text lives in AI_RULES + existing validator.
CHECK: checks 15/16; rejection record proves the clause rejects.
## SPLIT (no-mix)
🟢 measurement machinery + register shipped separately: _1200_P09-AntiPatterns-and-Measurement.zip.
## STATED DEVIATIONS (none swallowed)
- Check 15 runs WARN-class until ratification: enforcing an un-ratified cap as
  FAIL would apply law before Commander signature (IV.3). It self-escalates on ratification.
- task_ledger counted at boot-effective size (header + last 3 rows) because
  BOOT_SEQUENCE Tier 0 mandates only "last 3 entries" — full-file counting would
  punish II.3's append-only duty. Raw full-ledger figure was 39,018 B at delivery.
- Directive's "~36 KB Tier 0+1" evidence line not fully reproduced: measured
  raw = 39.0 KB, boot-effective = 32.7 KB (ledger grew during this campaign).
  Both real numbers reported instead.
- Check 16 counts STAGED 🟠 rows too (11 not 9): a staged canon patch is still
  a canon patch filed. Ratio honestly OVER budget — grandfathered as the
  clause's motivating instance, not hidden.

