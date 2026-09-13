# S004 — LEARNINGS (session-specific; cross-session wisdom → the shrine)
1. **The Commander's push ≠ the APPLY script** — three consecutive pushes landed with
   cleanup steps skipped (SCHEDULE.csv, the vehicles, PATCH_NOTES). Verify by
   path-existence after every push; assume nothing about script execution.
2. **A count written in a file rots.** Second sweep of the class: validate.yml said
   "14 checks", scripts/README said "26" while listing six tools under "five".
   De-counted; check 21 guards the one count that remains.
3. **My own test expectations failed more than my code** in the ICS build (3 of 4
   self-test failures were wrong expectations, incl. COUNT-minus-EXDATE-minus-override
   arithmetic and a shift-test aimed at a date the override had already moved).
4. **An unestablished pattern is not a finding.** The strongest moments of this watch
   were byte-level verifications (the fixture fold, the double-escape probe); the
   weakest was a claim drafted from an expected shape.
5. **Recycle principles, not ceremony.** The shrine transferred because its
   inviolability + verbatim-sourcing laws fit RADIATION's existing ethos; its council
   mythology did not, and was left in Marciale.
