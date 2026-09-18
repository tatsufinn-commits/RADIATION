# COLLECTION — Introduction to Data Science

## 1. IDENTITY
- LINK           : https://drive.google.com/drive/folders/1wDPfXnQrbWpZiUZkkt2lYYwvKRYbbk3S?usp=sharing
- OWNER          : THE COMMANDER
- PERMISSIONS    : anyone-with-link (verified working without auth)
- APPROVED       : 2026-09-13 — RADIATION_PATCH_2026-09-13_2300_Three-Collections-Registration.zip
- LAST VERIFIED  : 2026-09-13 (re-verify by 2026-12-12)

## 2. CONTENTS DESCRIPTION
Introductory data science course: lesson sequence 0–6 (data science overview,
big data overview & ecosystem, data life cycle parts 1–3, linear regression),
an R introduction, R notebook HTML exports (simple linear regression + SLR
example), and a data-preparation supplement. 11 files. **First collection
OUTSIDE the architecture domain** — consistent with RADIATION's universal
scope (ratified). **Registered on Commander's order 2026-09-13; NOT yet
ingested — Commander holds a larger plan.**

## 3. EVIDENCE-GRADE EXPECTATIONS
Lesson PDFs → [D]-as-taught for curriculum matter · statistical/ML claims →
[D] against a named published text when triangulated (lesson slides alone
carry no publisher — never [R]) · R notebook HTML outputs → [I]-adjacent
(executed code with visible results) but graded at ingest, not presumed.

## 4. MANIFEST (captured 2026-09-13, live embedded-folder read)
| File | Type | Topic | Noted |
|---|---|---|---|
| Lesson 0 Overview of Data Science (1).pdf | PDF | DS overview | 2026-09-13 |
| Lesson 1 Big Data Overview (1).pdf | PDF | Big data | 2026-09-13 |
| Lesson 2 Big Data Ecosystem.html | HTML | Big data ecosystem | 2026-09-13 |
| Lesson 3 Data Life Cycle Part 1.pdf | PDF | Data life cycle 1 | 2026-09-13 |
| Lesson 4 Data Life Cycle Part 2.pdf | PDF | Data life cycle 2 | 2026-09-13 |
| Lesson 5 Data Life Cycle Part 3.pdf | PDF | Data life cycle 3 | 2026-09-13 |
| Lesson 6 Linear Regression.pdf | PDF | Linear regression | 2026-09-13 |
| Lesson 6.1 Simple Linear Regression_new.html | HTML | SLR (R notebook export) | 2026-09-13 |
| SLR_example.html | HTML | SLR worked example (R) | 2026-09-13 |
| INTRO TO R - Tagged (1).pdf | PDF | R language intro | 2026-09-13 |
| Supplementary Discussion 1 Data Preparation.pdf | PDF | Data preparation | 2026-09-13 |

## 5. ACCESS LOG
| Date | Result | Note |
|---|---|---|
| 2026-09-13 | ✅ ACCESSIBLE | HTTP 200 no-auth; 11 entries listed via embedded folder view |
| 2026-09-17 | ✅ ACCESSIBLE | S007 @Autopilot re-verify (HTTP 200 no-auth); 11 rows via `<tr data-id>` parse; IDs mapped; fetches: Lesson 0, Lesson 3, Lesson 6 (3/3 cap). Restraint Doctrine honored (one-at-a-time, extracts only). |
| 2026-09-17 | ✅ ACCESSIBLE | S008 continuation (HTTP 200 no-auth); fetches: Lesson 1 (PDF, text + p18 vision), Lesson 2 (HTML text). 2/3 of S008's own 3-file cap. One-at-a-time, extracts only. |

## 6. DIGEST
**S007 (2026-09-17) — first ingestion. Three files fetched (cap 3): Lesson 0, Lesson 3, Lesson 6. Grade [D]-as-taught throughout; vision-recovery used (image-heavy decks).** Full graded extracts in `Brain/short_term/ingest/2026-09-17_ds10-*.md`.

- **Lesson 0 Overview of Data Science (12 pp, image-heavy):** big-data definitions (traditional-apps limit; Gartner high-volume/velocity/variety) · **Ten V's** = Volume, Velocity, Variety, Veracity, Value (L) + Validity, Variability, Venue, Vocabulary, Vagueness (R) · common types (Web/Social, M2M, Big Transaction, Biometrics, Human-Generated with exemplar lists) · data science = cleansing+prep+analysis; stats+math+programming+problem-solving · DS process = Ask→Get→Explore→Model→Communicate/visualize (iterative) · data analytics = inference from raw data · **Analytics value chain** = Data Management→Reporting→Descriptive→Predictive→Optimization & ML (value & difficulty ascend).
- **Lesson 3 Data Life Cycle Part 1 (25 pp, text-layer OK; EMC-quoted):** SIX PHASES = Discovery, Data Preparation, Model Planning, Model Building, Communicate Results, Operationalize (iterative; several at once) · 7 KEY ROLES = Business User, Project Sponsor, Project Manager, BI Analyst, DBA, Data Engineer, Data Scientist · Phase 1 deep-dive: learn domain, assess resources (people/tech/time/data), frame problem (success+failure criteria), stakeholders, sponsor interview, initial hypotheses (IHs), 5 data-source activities, exit = draft analytics plan · Phase 2 analytic sandbox + ELT/ETL(ETLT) · common mistake = rushing to collection before framing.
- **Lesson 6 Linear Regression (21 pp, text-layer OK):** descriptive vs inferential statistics (inferential = probability, estimation point/interval, hypothesis testing) · population/parameter vs sample/statistic · regression = relationship Y vs X1..Xp (p=1 SLR, p>1 MLR) · Y continuous, X any · EDA checklist (8) · SLR Y_i=β0+β1X_i+ε_i, ε~N(0,σ²) iid · β0 intercept / β1 slope · residual e_i=y_i−ŷ_i · least squares min RSS=Σ(y_i−b0−b1x_i)² · MLR = >1 predictor, explanation/prediction/inference · SLR/MLR in Excel + R.

- **Lesson 1 Big Data Overview (30 pp, text-layer OK; p18 via vision):** 3 attributes (volume/complexity/speed) · McKinsey 2011 def (scale/distribution/diversity/timeliness → new architectures) · 4 data structures (structured/semi/quasi/unstructured; 80-90% growth non-structured; MPP) · 3 repositories (spreadmarts / data warehouses / analytic sandbox) · BI vs DS (hindsight when/where vs foresight how/why) · traditional-architecture problems (EDW bottlenecks, in-memory limits, isolated DS).
- **Lesson 2 Big Data Ecosystem (HTML, text OK):** drivers (TB→PB→EB; genomic/video/surveillance/mobile/smart/RFID) · 4 player groups (devices/collectors/aggregators/users-buyers) · 3 role categories (Deep Analytical Talent 140-190k gap; Data Savvy 1.5M gap=10×; Tech & Data Enablers) · DS 3 activities + 5 skills · Hadoop cited once (NLP on social text).

**Still UNFETCHED (S007 budget; S008 used 2/3 of its own cap):** Lesson 4 Life Cycle Part 2 · Lesson 5 Life Cycle Part 3 · Lesson 6.1 SLR notebook · SLR_example · INTRO TO R · Supp. Discussion 1 Data Prep. CO3 topics (association rules, decision trees, clustering) exist in **no** collection file — web-triangulate at [O]/[R] only.
