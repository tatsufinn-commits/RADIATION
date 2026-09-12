# 📥 INGEST — BP 344 statute text (LawPhil mirror)
**Sheet:** proc_ingestion-run (steps 1–6 per current law; step 7 executed as P-04 DEMONSTRATION of the proposed DELETE + LOG rule — rule not yet canon)

```text
□ 1. PROVENANCE HEADER — origin: https://lawphil.net/statutes/bataspam/bp1983/bp_344_1983.html
     type: document (statute full text, HTML) | date consumed: 2026-09-12
     consuming mode: campaign build (P-04 demonstration)
□ 2. AUTHORITY TIER    — credentialed (LawPhil / Arellano Law Foundation:
     institutional mirror of official statute text — NOT the Official Gazette
     itself, which returned HTTP 403 this session → unsure = tier DOWN)
□ 3. EXTRACTION        — claims C1–C4:
     C1. BP 344 conditions construction/repair/renovation permits on installing
         architectural facilities for disabled persons — "sidewalks, ramps,
         railings and the like" (Sec. 1).
     C2. The statute text contains NO numeric ramp gradient. Sec. 3 delegates
         implementing rules to MPWH + MOTC in coordination with the National
         Commission Concerning Disabled Persons — gradient values live in the
         IRR, not the Act.
     C3. Approved: February 25, 1983.
     C4. Penalty (Sec. 4): imprisonment 1 month–1 year, or fine P2,000–P5,000,
         or both; responsible officers named for juridical entities.
□ 4. GRADE CEILING     — C1[D] C2[D] C3[D] C4[D] — [D] as mirrored statute text
     (C2 absence verified against the full fetched text); mirror caveat: re-confirm
     against the Official Gazette when accessible.
□ 5. STORE             — this file.
□ 6. DUPLICATE CHECK   — Brain holds the IRR-gradient CONFLICT (1:12 vs 1:20),
     not the statute text itself; new matter confirmed. C2 feeds the
     CONFLICT_REGISTER row appended 2026-09-12 — it does NOT resolve the
     conflict (statute silence is consistent with both positions).
□ 7. DELETE + LOG (P-04 DEMO) — fetched binary (bp344.html, session-local temp) DELETED
     after extraction | bytes reclaimed: 6277 B (0.006 MB) |
     kept: Brain/short_term/ingest/2026-09-12_bp344-statute-lawphil.md (extract only)
```
decay: 1 yr (stable-domain statute record) → 2027-09-12
