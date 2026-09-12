# ⏳ THE DECAY REGISTER (`docs/DECAY_REGISTER.md`)
## Claims past their verification half-life, awaiting re-verification (I.4)
**⚠️ APPEND-ONLY (II.2).** Entries move OUT only by re-verification (restore) or Commander purge.

Format: `| date flagged | claim (verbatim) | location | old grade → decayed grade | decay class | status |`

| Date flagged | Claim | Location | Grade change | Class | Status |
|---|---|---|---|---|---|
| — | *(register empty — system founding)* | — | — | — | — |
| 2026-09-12 | "PD-1096 collection file (retrieved 2025-01-09) reflects current amended state" | Brain/external_sources/law.md DIGEST | [D] → [D][DECAYED] (currency aspect only; statute text itself timeless) | stable-domain 1yr, expired 2026-01-09 | AWAITING RE-VERIFICATION |

| 2026-09-12 | "BP-344 IRR-amendments file (2024 ed., retrieved 2025-01-09) reflects current amended state" — COMPUTED from KNOWLEDGE_REGISTRY K-LAW-003 (last_verified 2025-01-09 + 1yr = expired 2026-01-09) via scripts/decay_compute.py | Brain/external_sources/law.md + docs/KNOWLEDGE_REGISTRY.md K-LAW-003 | [D] → [D][DECAYED] (currency aspect only) | stable-domain 1yr, expired 2026-01-09 | AWAITING RE-VERIFICATION |
