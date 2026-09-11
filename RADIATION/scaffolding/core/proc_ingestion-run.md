# 📥 INGESTION RUN (`proc_ingestion-run.md`)
**Subskill:** curator | **Mandatory for:** every ingestion (passive under @Radiation; invoked under @Gather/@Decode)

```text
For EACH source consumed:
□ 1. PROVENANCE HEADER — origin: <url/file> | type: slide/pdf/document/paper/
     forum/social/comment/site | date consumed: <…> | consuming mode: @<…>
□ 2. AUTHORITY TIER    — official / credentialed / community / anonymous
     (unsure → tier DOWN)
□ 3. EXTRACTION        — claims, data, quotes pulled; noise stripped;
     claims numbered: C1…Cn
□ 4. GRADE CEILING     — I.2 applied: forum/social/comment matter enters at
     [O]/[N] MAX. Grades: C1[…] C2[…] …
□ 5. STORE             — file: Brain/short_term/ingest/YYYY-MM-DD_<slug>.md
□ 6. DUPLICATE CHECK   — Brain already holds this? → LINK to <path>, don't
     re-store (II.1). New matter only: <confirmed>
```
FADE: this sheet accompanies the ingestion file in short_term. Promotion out
of short_term is NOT curator's power — triangulation gates the vault (II.6).
