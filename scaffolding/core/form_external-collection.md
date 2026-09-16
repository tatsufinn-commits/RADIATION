# 🔗 EXTERNAL COLLECTION TEMPLATE (`form_external-collection.md`)
**Use:** mandatory format for every file in `Brain/external_sources/` (one file per approved collection). Entries reach the live repo only via Commander-approved Patch.

```markdown
# COLLECTION — <official collection name>

## 1. IDENTITY
- LINK           : <Google Drive / other permanent link>
- OWNER          : <who controls it>
- PERMISSIONS    : <public / anyone-with-link / restricted — expected access mode>
- APPROVED       : <date + Patch filename that registered it>
- LAST VERIFIED  : <YYYY-MM-DD — re-verify if older than 90 days (I.4)>

## 2. CONTENTS DESCRIPTION
<What this collection holds, in 3–6 lines: subject areas, document types,
approximate volume, why it was approved.>

## 3. EVIDENCE-GRADE EXPECTATIONS
<Default grades for this collection's material, e.g. "official lecture slides
→ [D] for course content" / "collected forum exports → [O]/[N] cap applies".
Individual claims are still graded at ingestion (I.2) — this sets expectations,
not verdicts.>

## 4. MANIFEST (file inventory)
Written/updated by any Drive-capable session; dated.
| File/folder | Type | Topic | Noted |
|---|---|---|---|
| … | … | … | YYYY-MM-DD |

## 5. DIGEST (verified extractions — optional but valuable)
Claims already extracted, graded, and carried IN-REPO so Drive-blind sessions
retain partial use. Each entry: claim [GRADE] (file, location) {decay}.
Digest claims still pass triangulation before long_term (II.6 — no bypass).

## 6. ACCESS LOG (append-only, II.2)
| Date | Session/model | Result: ACCESSIBLE / DEAD / AUTH-BLOCKED / SOFT-404 / PAYWALL / REDIRECT-LOGGED | Note |
|---|---|---|---|
| … | … | … | … |
```

**Access-honesty rule:** a session that could not open the link works from
§§4–5 only and says so. Claiming to have read the underlying documents without
access is contamination (I.1).

**Gap-4 extension (S-2-LINK v3.10.25):** Result states extend from `ACCESSIBLE / DEAD / AUTH-BLOCKED` to `ACCESSIBLE / DEAD / AUTH-BLOCKED / SOFT-404 / PAYWALL / REDIRECT-LOGGED` per Gap-Report Domain-4 fold.

**JS-only honesty line (LAW-2 mirror, no headless ambition):** dynamically-rendered sources that cannot be read are recorded as `INACCESSIBLE-UNKNOWN` with a note — never claimed read, never claimed dead (UNKNOWN grammar; no headless-browser ambition).

**Gap-2 same-source re-fetch supersession note (II.4):** when a source is re-fetched and its content has changed, the ACCESS LOG row must carry a supersession note (prior state → new state hash/short-diff + supersession remark); prior acquisition records stay (II.4).
