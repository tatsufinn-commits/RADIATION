# 📦 THE STOCKPILE DOCTRINE (`docs/STOCKPILE_DOCTRINE.md`)
## Source Intake Quotas & Dossier Reference Limits — Ratified Figures
**Version:** 1.0.0 | Constitutional basis: III.5 (Stockpile Quotas), III.8 (Scout's Gate)

## 1. SOURCE INTAKE QUOTAS PER MODE
| Mode | Primary (min) | Secondary (min) | Triangulation floor | Sources listed? |
|---|:---:|:---:|:---:|:---:|
| @Data | 2 | 3 | 2 independent | ❌ used, never listed |
| @Gather | **10** (Commander-fixed) | **18** (Commander-fixed) | 2 independent | ✅ full list |
| @Decode | repo tree(s) in full | 8 | 2 independent | ✅ full list |
| @Radiation | 12 | 20 | 3 independent (Core-bound) | ✅ full list + grades |

## 2. DOSSIER REFERENCE LOAD (existing knowledge consulted per task)
| Mode | Dossiers from Brain/long_term/dossiers/ | Nota cards from the Core |
|---|:---:|:---:|
| @Data | up to 2 (most relevant) | up to 5 |
| @Gather | up to 5 | up to 10 |
| @Decode | up to 5 | up to 10 |
| @Radiation | unlimited (relevance-ranked via CORE_INDEX) | unlimited |

## 3. DEFINITIONS (so no AI can weasel)
- **Primary source:** the original artifact — official docs, the actual
  repo/code, the law text, the paper itself, first-party announcements, raw data.
- **Secondary source:** analysis/derivative — reviews, tutorials, journalism,
  third-party benchmarks, forum consensus.
- **Independent:** different author/organization AND different publication channel.

## 4. RULES
1. **Scout's Gate (III.8):** every source passes the necessity test (relevance ·
   authority · novelty · necessity) BEFORE acquisition. The Brain is checked
   first — never re-acquire held knowledge.
2. **Zero padding:** quotas are met with necessary sources. Stuffing filler to
   hit a number is a III.8 violation.
3. **Shortfall protocol:** if quotas are genuinely unreachable (niche topic),
   log `[STOCKPILE SHORTFALL]` with count achieved + reason; surgeon-passive
   adjudicates whether the session may close.
4. Secondary-source claims enter at `[O]`/`[N]` grade maximum until
   triangulation elevates them (I.2).
