# 📦 THE STOCKPILE DOCTRINE (`docs/STOCKPILE_DOCTRINE.md`)
## Source Intake Quotas & Dossier Reference Limits — Ratified Figures
**Version:** 1.1 | Constitutional basis: III.5 (Stockpile Quotas), III.8 (Scout's Gate)

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

## 4. NECESSARY vs PADDING — THE ENFORCEABLE TEST (v1.1 clarification)
A source is **NECESSARY** if it passes ALL FOUR of scout's tests, with the
answers RECORDED in the Acquisition Plan:
1. **RELEVANCE** — names the specific need-profile gap (G-n) it fills. "General
   background" is not a gap.
2. **AUTHORITY** — its tier is stated; a lower-tier source is necessary only
   when no higher-tier source covers the same gap, and that absence is noted.
3. **NOVELTY** — states what it adds that no already-acquired source and no
   Brain holding provides. "Confirms S-03" is only valid as EXPLICIT
   triangulation duty (and is then marked `role: triangulation`).
4. **NECESSITY** — one line: what weakens in the deliverable if this source
   is dropped?

A source is **PADDING** if any of these is true — and padding is a III.8
violation surgeon must flag:
- It repeats another source's contribution without a declared triangulation role.
- Its Acquisition Plan entry cannot name its gap (G-n).
- It was added AFTER the quota gap became visible, without a new need-profile
  entry justifying it.
- Its per-source entry (proc_research-sortie §4) extracts zero claims used
  anywhere downstream.

**Enforcement chain:** scout records the four answers → prospector acquires
only planned sources → sentinel spot-checks that per-source entries produced
downstream-used claims → surgeon blocks closure on padding findings.

**@Gather/@Radiation specific rule:** the quota is a FLOOR for genuine
coverage, not a TARGET to hit. If the need-profile is fully served below
quota: acquire the remaining count ONLY as declared triangulation-role or
tier-upgrade sources; if none exist, log `[STOCKPILE SHORTFALL]` with the
coverage argument. A shortfall with full coverage is lawful; padding never is.

## 5. SHORTFALL PROTOCOL
If quotas are genuinely unreachable (niche topic), log `[STOCKPILE SHORTFALL]`
with count achieved + reason; surgeon-passive adjudicates whether the session
may close. Secondary-source claims remain [O]/[N]-capped until triangulated (I.2).

## 6. STOPPING PHILOSOPHY (Gap-9 — named per S-2-LINK v3.10.25)

Stopping philosophy = necessity test + floor-not-target + shortfall protocol — necessity test (four answers per source, §4), floor-not-target (quota is FLOOR for genuine coverage, not TARGET, §4 @Gather/@Radiation rule), shortfall protocol (§5); philosophy already enforced, line names it per Gap-Report Domain-9; see `docs/SOURCE_QUALIFICATION.md` §VI for qualification ≠ verification cross-ref.
