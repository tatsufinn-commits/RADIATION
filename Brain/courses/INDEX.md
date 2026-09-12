# 🎓 COURSES (`Brain/courses/INDEX.md`)
## The Commander's enrolled courses — the join key between the curriculum and the drills
**Version:** 1.0 | **Constitutional basis:** II.6 (Brain integrity) | **Region pattern:** `Brain/external_sources/INDEX.md`
**Origin:** Commander's order, 2026-09-13 (term-planning directive P-10)

---

## WHAT THIS REGION IS

One record per enrolled course: what is taught, what is graded, when, and which knowledge objects answer it. It is the bridge between the Commander's academic calendar and the knowledge system — **no planner can rank a week without it.**

## THE RULES

1. **Records, not copies.** This region holds the extracted, `[D]`-graded graded-items table and the syllabus DIGEST. **The syllabus binary is a vehicle: read it, extract it, delete it** (II.6 rule 8, staged under P-04). Same rule as `Brain/external_sources/` — *the region holds records; it is never itself citable evidence.*
2. **Vehicles never enter.** Syllabus documents, course calendars, schedule PDFs, timetable screenshots, and ICS files live in git-ignored local folders (`syllabi/`, `schedule/`). Enforced by **check 2.5**.
3. **No personnel or location identifiers.** Names, section codes, room numbers, and student identifiers appear in **no** committed file. Not negotiable: the repository is public. Enforced by check 2.5.
4. **Every graded item carries a source locator** (module/section) — a bare date is not a citation (P-07 locator rule).
5. **Course codes are the join key** to `K-CUR` registry rows, to `K-MOD` modules, and to the instrument set in the Law collection.
6. **Distinguish the two registry layers.** A **course-object row** describes a course (this region). A **material-set row** describes lecture/reviewer material attached to a course (`K-CUR-001…006`, pre-existing). They cross-link; neither replaces the other.
7. **A syllabus is not a truth-source.** It tells you *which* parts of a subject are examinable; it does not tell you *what is true*. For architecture courses the truth-source is the instrument set (PD 1096, BP 344, RA 9514, RA 9266, NSCP 2015). **A missing syllabus delays prioritisation, not construction.**
8. **A course with no module is a BUILD-REQUIRED, not a plan.** State it; never schedule drilling for material that does not exist.

---

## THE REGISTER — Term 1, AY 2026-2027 · 6 courses · 18 units

| K-ID | Code | Title | Units | ALE yield | Syllabus | Material | Record |
|---|---|:--:|:--:|:--:|:--:|:--:|---|
| K-CUR-007 | GED103 | Readings in Philippine History | 3 | **1** | ✅ full | — | `Brain/courses/GED103.md` |
| K-CUR-008 | DSS10 | Introduction to Data Science (w/ Coursera) | 3 | **1** | ✅ full | (Coursera, external) | `Brain/courses/DSS10.md` |
| K-CUR-009 | MEC30-7 | Statics of Rigid Bodies for CE | 3 | **5** | ⚠️ calendar only | — | `Brain/courses/MEC30-7.md` |
| **K-CUR-010** | **AR173-1P** | **Planning 2 — Urban Design & Community Architecture** | 3 | **9** ⭐ | ❌ | ✅ **ingested + reviewer + module + drill** | `Brain/courses/AR173-1P.md` |
| K-CUR-011 | AR163-1P | Building Technology | 3 | **8** | ❌ | ✅ **INGESTED 2026-09-13** (K-CUR-006) — ⚠️ core texts image-only | `Brain/courses/AR163-1P.md` |
| K-CUR-012 | AR153P | Building Utilities 2 | 3 | **8** | ❌ | ✅ **INGESTED 2026-09-13** (K-CUR-005) | `Brain/courses/AR153P.md` |

**ALE yield** = the P-06 yield rubric's four factors applied to licensure relevance (frequency 40 / breadth 20 / error-proneness 25 / memorisation 15). Provisional at capture; replaced by the measured `yield_rank` in each `K-MOD` record as modules are built.

---

## ⭐ THE LOAD FINDING — corrected after registry cross-check (2026-09-13)

**UPDATE 2026-09-13 — AR153P has been ingested** (14/14 files, 3,923 pages, DIGEST populated). The finding below stands as written but is now **half-discharged**: one of the three high-yield courses has moved from *manifested* to *extracted*, and three registry objects were created (K-STD-004 PEC, K-BK-004 Ginn, K-BK-005 Fajardo Electrical). **Two ingestion runs remain: K-CUR-006 (AR163-1P) and the 334 image-only pages.**

**Six courses · 18 units · 31.5 contact-hours per week.** The two courses with complete primary documentation are **general education with no ALE component**. The three courses carrying the licensure yield have **no syllabus** — but they are **not empty**:

| Course | Yield | What is actually held | The real open work |
|:--:|:--:|---|---|
| AR173-1P | 9 | lecture set **ingested** · audited reviewer · **K-MOD-001 (L4)** · **drill set forged** | *nothing to acquire* — drill it |
| AR163-1P | 8 | 50 files / **1,177.9 MB** — ✅ **INGESTED 2026-09-13** · Salvan (PH) + Barry vols 1–5 + FLEA 2013 review + a 3,036-item corpus | **2,038 pp image-only = the core texts** (recovery ladder) |
| AR153P | 8 | 14 files / 283.4 MB — ✅ **INGESTED 2026-09-13** · PEC + Fajardo + PD 1096 pipe codes extracted | **334 pp image-only** (recovery ladder) + module build |

> **The bottleneck is INGESTION, not acquisition.** The material for the three highest-yield courses of the term is already in the Commander's collections — two sets have never been processed, and the third has been processed all the way to a working drill set.
>
> An earlier revision of this register described all three as "BUILD-REQUIRED, no material held." **That was wrong, and the registry's own `K-CUR-001…006` rows are what corrected it.** The correction is recorded here rather than silently edited, because a wrong workload statement is exactly the kind of claim this system exists to catch.

**Meeting pattern and the clear blocks:** Mon–Sat carries 31.5 hours, with 07:30 starts on five days and evening sessions to 21:00 on three (Mon/Wed… see each course record). **Wednesday and Sunday are the only clear blocks.** Any planning routine must target those by default rather than proposing slots that do not exist.

---

## 🚩 OPEN ACTION — feed rotation (time-critical)

A live LMS calendar-feed URL (a credential) was committed on 2026-09-13 in commit `4a98e59` and has been **removed from the tree by this patch**. **Removal does not revoke it** — anyone holding it retains read access to the Commander's course calendar. The Commander must rotate the feed at source (disable the external-calendar feed, then re-enable it to mint a new URL).

| Rotation | Date | Confirmed by |
|---|---|---|
| LMS external calendar feed | *(pending — Commander to record here)* | |

---

## WINDOW

`Brain/short_term/plan/` holds the derived term window (`*.local.md` — git-ignored). Populated by P-10 Phase 3; not yet built.
