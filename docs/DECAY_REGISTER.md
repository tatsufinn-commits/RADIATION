# ⏳ THE DECAY REGISTER (`docs/DECAY_REGISTER.md`)
## Claims past their verification half-life, awaiting re-verification (I.4)
**⚠️ APPEND-ONLY (II.2).** Entries move OUT only by re-verification (restore) or Commander purge.

Format: `| date flagged | claim (verbatim) | location | old grade → decayed grade | decay class | status |`

| Date flagged | Claim | Location | Grade change | Class | Status |
|---|---|---|---|---|---|
| — | *(register empty — system founding)* | — | — | — | — |
| 2026-09-12 | "PD-1096 collection file (retrieved 2025-01-09) reflects current amended state" | Brain/external_sources/law.md DIGEST | [D] → [D][DECAYED] (currency aspect only; statute text itself timeless) | stable-domain 1yr, expired 2026-01-09 | AWAITING RE-VERIFICATION |

| 2026-09-12 | "BP-344 IRR-amendments file (2024 ed., retrieved 2025-01-09) reflects current amended state" — COMPUTED from KNOWLEDGE_REGISTRY K-LAW-003 (last_verified 2025-01-09 + 1yr = expired 2026-01-09) via scripts/decay_compute.py | Brain/external_sources/law.md + docs/KNOWLEDGE_REGISTRY.md K-LAW-003 | [D] → [D][DECAYED] (currency aspect only) | stable-domain 1yr, expired 2026-01-09 | AWAITING RE-VERIFICATION |
| 2026-09-13 | "the PEC file held reflects the current Philippine Electrical Code" | Brain/external_sources/building-utilities.md §5.4 + K-STD-004 | [D] → [D][DECAYED] (currency aspect only; extracted text is sound) | volatile (code editions), file edition = **2009** | AWAITING RE-VERIFICATION — Commander to supply or confirm the current edition |

| 2026-09-13 | "The Construction of Buildings (Barry) is a citable source" — the held set is **MIXED EDITIONS** (v1 7th · v2 5th · v3 4th · v4 4th · v5 unsettled) | Brain/external_sources/building-technology.md §5.3 + K-BK-007 | [D] → **[D] only with volume + edition named** (the bare name "Barry" is not citable) | edition-currency · mixed set | OPEN — action: always cite volume + edition |
| 2026-09-13 | "Architecture: Comfort and Energy (Gallo/Sala/Sayigh, Elsevier **1988**) supports current comfort/energy guidance" | Brain/external_sources/building-technology.md §5.6 + K-BK-006 K-CUR-006 | [D] → **[D][DECAYED]** for currency of practice (the physics is timeless; the guidance is not) | stable-domain 1yr, expired long ago | AWAITING RE-VERIFICATION |
| 2026-09-13 | "Salvan, Architectural Building Materials — edition/year known" — **UNRESOLVED** (interior years 1963/69/87 appear; no edition statement settled) | K-BK-006 | [D] → **[D] provisional** — dated claims blocked until the edition is settled | edition-currency · unresolved | OPEN — action: settle the edition before dating any claim from it |
| 2026-09-13 | "UAP-Dubai FLEA 2013 review chapters reflect current licensure content" — **13 years old** | K-BK-008 | [R] → **[R][DECAYED]** for currency (rules revise; the *shape* of the questions ages better than the answers) | ALE-content 1yr, expired | AWAITING RE-VERIFICATION |
