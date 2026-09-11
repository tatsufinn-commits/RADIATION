# 🔬 THE EVIDENCE TAXONOMY (`docs/EVIDENCE_TAXONOMY.md`)
## Grading, Half-Life & Decay — Operational Standard
**Version:** 1.0.0 | Constitutional basis: I.2, I.3, I.4

## 1. THE SIX GRADES
| Grade | Definition | Example |
|---|---|---|
| `[D]` **Documented** | Stated by the authoritative primary source itself | The law's own text; official API docs; the repo's actual code |
| `[O]` **Observed** | Seen directly but not authoritatively published | Forum consensus; a behavior tested once; social media reports |
| `[I]` **Implemented** | Proven by a working artifact in this repository | A cerebellum routine that has run successfully |
| `[R]` **Research-supported** | Peer-reviewed or formally studied finding | Published paper results; third-party benchmarks |
| `[N]` **Inferred** | Logical derivation from graded claims — premises cited | "X deprecated + Y forked it → Y is the active lineage [from D-claim №3 + O-claim №7]" |
| `[S]` **Speculative** | Hypothesis. Belongs in 04-incubate/, nowhere else | "This pattern would likely scale to…" |

**Rules:** one grade per claim · ungraded = invalid · secondary sources (forums,
social, comments, website statements) enter at `[O]`/`[N]` cap until
triangulated · `[S]` never rises above `[N]` without new external sources ·
triangulation is the ONLY elevator · even `[D]` needs an independence check for
Core admission — a single authority can be wrong.

## 2. HALF-LIFE CLASSES (decay: dates, I.4)
| Class | Decay period | Examples |
|---|:---:|---|
| Volatile | 90 days | prices, versions, leadership, active development status |
| Stable-domain | 1 year | established practices, mature APIs, institutional facts |
| Timeless | none | mathematics, historical record, ratified law texts (cite version) |

## 3. DECAY & DOWNGRADE MECHANICS
- **On expiry:** sentinel flags → claim auto-downgrades ONE grade + gains
  `[DECAYED]` → listed in `docs/DECAY_REGISTER.md` → re-verification restores
  grade and resets the date.
- **Source retracted:** immediate quarantine review (I.1 procedure).
- **Contradiction registered:** both sides frozen at current grade until
  triangulated (I.5).

## 4. CLAIM FORMAT (canonical)
`<claim text> [GRADE] (source: <id/citation>) {decay: YYYY-MM-DD | none}`
