# 📚 REVIEWER — DSS10: Introduction to Data Science (with Coursera)
**Course:** DSS10 — Introduction to Data Science (Mapúa, Term 1 AY 2026-2027 · 3 units · CO1–CO3)
**Syllabus:** `Brain/courses/DSS10.md` / `SOIT_DSS10_1Q_Syllabus.md` `[D]` · **Lessons:** `Brain/external_sources/intro-data-science.md` (Drive; Lessons 0, 3, 6 fetched S007 + Lessons 1, 2 fetched S008 — 2026-09-17) `[D]-as-taught`
**Mode/Style:** @Autopilot[@Review→@Gather→scribe] · research.md base + reviewer sections (no reviewer style exists in /styles/; mirrors ratified S001 PLANNING_reviewer pattern)
**Evidence grade:** lesson-derived = `[D]-as-taught` (EMC-quoted where noted); web-only topics (logistic, association, trees, clustering, Hadoop) = `[R]` (≥2 independent web sources, cited); syllabus facts = `[D]`. NOT Core-grade — study-grade (single curriculum spine; I.3 keeps it out of 09-nota).

> **How to use:** Cover PART C. Work PART B top-to-bottom; re-take until cold.
> PART A = last-minute sheet · PART D/E = recall hooks. Items tagged `[R]` are
> standard-textbook facts triangulated on the open web (course may phrase differently —
> curriculum term wins, P-07). Items tagged `[NOT HELD]` are not in any fetched source —
> verify against your own lecture notes before an exam.

---

## PART A — QUICK-REFERENCE TABLES (memorize cold)

### A1. Big Data — definition + the Ten V's `[D]-as-taught`
- **Big data:** humongous volumes that traditional applications can't process; raw/unaggregated; won't fit one computer's memory; structured+unstructured; analyzed for better decisions. **Gartner:** "high-volume, high-velocity and/or high-variety information assets that demand cost-effective, innovative information processing for enhanced insight, decision making, and process automation."
- **THE TEN V's** (five per side):

| Left | Meaning | Right | Meaning |
|---|---|---|---|
| Volume | size of data | Validity | quality, governance, master-data mgmt at scale |
| Velocity | speed generated | Variability | dynamic, evolving behavior in source |
| Variety | different types | Venue | distributed heterogeneous multi-platform data |
| Veracity | data accuracy | Vocabulary | data models / semantics of structure |
| Value | useful data | Vagueness | confusion over meaning & tools |

### A2. Common types of big data `[D]-as-taught`
| Type | Examples |
|---|---|
| Web & Social Media | clickstream, Twitter feeds, Facebook postings, web content |
| Machine-to-Machine | smart-meter, RFID, oil-rig sensor, GPS |
| Big Transaction Data | healthcare claims, telecom call-detail records, utility billing |
| Biometrics | facial recognition, genetics |
| Human Generated | call-center voice, email, electronic medical records |

### A3. DS vs DA vs statistics; process; value chain `[D]-as-taught`
- **Data science:** unstructured+structured; everything on cleansing/preparation/analysis; combo of statistics+math+programming+problem-solving; umbrella of techniques to extract insight.
- **Data analytics:** examining raw data to draw conclusions; algorithmic/mechanical process; focus = inference.
- **Statistics:** descriptive (collect/organize/present) vs inferential (conclude for larger group, relationships, predict). Inferential branches: probability, estimation (point/interval), hypothesis testing.
- **DS process (iterative):** ASK → GET → EXPLORE → MODEL → COMMUNICATE/visualize.
- **Analytics value chain (value & difficulty ascend):** Data Management → Reporting → Descriptive → Predictive → Optimization & ML.

### A4. Data Analytics Lifecycle — 6 phases + 7 roles `[D]` (EMC-quoted)
**PHASES (order!):** 1 Discovery · 2 Data Preparation · 3 Model Planning · 4 Model Building · 5 Communicate Results · 6 Operationalize. (Iterative; several at once; designed for Big Data.)
| Phase | Essence |
|---|---|
| 1 Discovery | learn domain+history; assess resources (people/tech/time/data); frame problem (success AND failure criteria); stakeholders; sponsor interview; initial hypotheses (IHs); 5 data-source activities; exit = draft analytics plan |
| 2 Data Prep | analytic sandbox; ELT/ETL (=ETLT); transform & condition data |
| 3 Model Planning | choose methods/techniques/workflow; explore relationships; select key variables + models |
| 4 Model Building | build train/test/production datasets; run models; check tool adequacy (fast HW, parallel) |
| 5 Communicate | determine success/failure vs Phase-1 criteria; key findings; quantify value; narrative |
| 6 Operationalize | final reports/briefings/code/docs; pilot in production |

**7 KEY ROLES:** Business User (domain; advises context/value) · Project Sponsor (genesis; funds; sets priorities & outputs) · Project Manager (milestones, quality) · BI Analyst (KPIs/metrics; dashboards & reports) · DBA (provisions/configures DB; access; security) · Data Engineer (SQL tuning; extraction; ingestion into sandbox; shapes data) · Data Scientist (SME techniques/modeling; designs & executes methods).

### A5. Statistics & regression fundamentals `[D]-as-taught`
- **Population → Sample** (sampling theory); **Parameter** (population) vs **Statistic** (sample).
- **Regression:** most-used technique for relationship between ≥2 variables (≥2 continuous); Y continuous, X any (cont/disc/cat). p=1 → simple; p>1 → multiple/multivariate.
- **EDA checklist (8):** data-entry errors, missing values, outliers, asymmetric distributions, changes in variability, clustering, non-linear bivariate relationships, unexpected patterns.
- **SLR model:** Y_i = β0 + β1·X_i + ε_i ; ε_i ~ N(0,σ²) iid. β0 = intercept; β1 = slope (ΔY per unit X).
- **Residual:** e_i = y_i − ŷ_i. **Least squares:** minimize RSS = Σ(y_i − b0 − b1·x_i)².
- **MLR:** >1 predictor; explanation/prediction/inference; linear or nonlinear.

### A6. Logistic regression `[R]` (web; syllabus Lesson 7 — not in fetched set)
Supervised **classification** (despite the name) for binary outcomes; applies **sigmoid** σ(z)=1/(1+e^−z) to a linear combination → probability in (0,1); threshold (≈0.5) assigns class. Estimated by **MLE** (not OLS); coefficients = log-odds/odds ratios.

### A7. Supervised ML — association rules · decision trees · clustering `[R]` (CO3; no collection file)
- **Association rules (market basket):** rule A→B; **support**=P(A∩B) frequency; **confidence**=P(A∩B)/P(A) (likelihood of B given A); **lift**=confidence/expected-confidence = P(A∩B)/(P(A)P(B)); lift>1 positive, =1 independent, <1 negative. Algorithms: **Apriori**, FP-Growth.
- **Decision trees:** supervised; root→internal→leaf nodes; splits chosen by impurity reduction — **entropy / information gain** (ID3/C4.5) or **Gini impurity** (CART, binary splits); lower impurity = purer node; pruning vs overfitting.
- **Clustering (k-means):** **unsupervised** (no labels); partition into K clusters by similarity to **centroid**; iterate assign→update until convergence; choose K by **elbow method** (WCSS vs K); sensitive to outliers/initialization; Euclidean distance, scale features first.

### A8. Big Data ecosystem — 4 player groups + 3 role categories `[D]-as-taught` (Lesson 2, EMC/McKinsey)
- **4 PLAYER GROUPS (value chain):** Data **DEVICES** (gather/generate; ~1 GB new data → ~1 PB data-about-data) · Data **COLLECTORS** (cable-TV viewing, RFID cart-path tracking) · Data **AGGREGATORS** (compile + make sense; package lists for ad brokers) · Data **USERS & BUYERS** (retail banks buying credit/equity data).
- **3 ROLE CATEGORIES (McKinsey May 2011):** **Deep Analytical Talent** (quant training — math/stats/ML; needs robust sandbox; US gap 140–190k by 2018) · **Data Savvy Professionals** (business/market-research/ops/financial analysts; gap 1.5M ≈ 10× the DS gap) · **Technology & Data Enablers** (computer eng/programming/DBA; provision & administer sandboxes).
- **Data Scientist:** 3 activities = reframe business problem as analytics challenge · design/implement/deploy statistical & data-mining models on Big Data · develop & communicate actionable insights (business value). 5 skills = quantitative · technical (SW eng/ML/programming) · skeptical & critical · curious & creative · communicative & collaborative.
- **Hadoop (supplementary `[R]` — cited once in lesson for NLP on social text):** core 4 = HDFS (NameNode=metadata/DataNode=blocks) · MapReduce (parallel processing) · YARN (ResourceManager/NodeManager/AppMaster) · Hadoop Common. Extras: Hive, Pig, Spark, HBase, Kafka, Oozie, Sqoop, Zookeeper.

### A10. Big Data structures, repositories, BI vs DS `[D]-as-taught` (Lesson 1, EMC)
- **3 defining attributes:** huge VOLUME · COMPLEXITY of types/structures · SPEED of creation/growth. (Variety+velocity are the apter definition, not volume alone.)
- **McKinsey 2011 def:** "data whose scale, distribution, diversity, and/or timeliness require new technical architectures and analytics to unlock new business value."
- **4 data STRUCTURES** (80–90% of growth non-structured; MPP preferred): **structured** (RDBMS, CSV, spreadsheets, OLAP cubes) · **semi-structured** (XML, self-describing/parseable) · **quasi-structured** (clickstream, erratic but formattable) · **unstructured** (docs, PDFs, images, video).
- **3 REPOSITORIES:** **spreadmarts** (spreadsheets+low-volume DBs; analyst depends on extracts) · **data warehouses** (centralized purpose-built; support BI/reporting but restrict robust analysis) · **analytic sandbox** (multi-source workspaces; flexible high-perf nonproduction; in-DB processing).
- **BI vs DS:** BI = hindsight, aggregated historical, closed-ended, answers WHEN/WHERE, needs structured rows/cols. DS = foresight, disaggregated/exploratory, open-ended, answers HOW/WHY (e.g., time-series forecasting vs trend line).

### A9. Grading & course map `[D]` (syllabus)
| Item | Weight | Floor |
|---|:--:|:--:|
| FA1 (Exer, Short Quiz) | 20% | 70% |
| FA2 (Long Quiz) | 25% | 70% |
| Coursera (IBM *Data Analysis with R*) | 15% | 70% |
| SA (Final) | 40% | 70% |
Split: Computer Topics 90% · Gen-Ed 10%. **CO1** landscape+stat tools (Wk1-5) · **CO2** mathematical reasoning / regression+R (Wk5-8) · **CO3** problem-solving / association, trees, ggplot2, data prep (Wk9-11). CO1 Exam after Wk5; CO2 Exam after Wk8; Long Quiz 3 + Final in Wk11.

---

## PART B — QUESTION BANK

### B1 · Big Data Foundations (CO1)
1. Define big data in one line (traditional-apps limit). _______________
2. The Gartner definition names three "high-" traits — name them. _______________
3. ENUMERATE the Ten V's of big data. _______________
4. Which V means "data accuracy"? _______________
5. Which V means "confusion over meaning of big data and tools"? _______________
6. Match: facial recognition & genetics belong to which big-data type? _______________
7. Smart-meter and RFID readings belong to which type? _______________

### B2 · DS / DA / Statistics Concepts (CO1)
8. "Science of examining raw data to draw conclusions, focus on inference" = ? _______________
9. ENUMERATE the analytics value chain in ascending order. _______________
10. ENUMERATE the data science process (5 steps, in order). _______________
11. Descriptive statistics does what three things? _______________
12. A numeric summary of a SAMPLE is a ______; of a POPULATION a ______.
13. T/F: Inferential statistics includes hypothesis testing and estimation. _______________

### B3 · Data Analytics Lifecycle (CO1)
14. How many phases does the Data Analytics Lifecycle have? _______________
15. ENUMERATE the six phases in order. _______________
16. Which phase requires an analytic sandbox + ELT/ETL? _______________
17. Which phase formulates initial hypotheses (IHs)? _______________
18. Which phase delivers final reports, code, and may run a pilot? _______________
19. ENUMERATE the seven key roles in an analytics project. _______________
20. Who funds the project and sets its priorities? _______________
21. T/F: Work can occur in several lifecycle phases at once. _______________
22. The common mistake the EMC text warns against is rushing into ______ before framing the problem. _______________

### B4 · Regression (CO2)
23. In SLR, the response variable Y must be ______. _______________
24. Write the SLR model. _______________
25. The random error ε_i is assumed ~ ______ (distribution and parameters). _______________
26. β1 represents ______. _______________
27. Residual e_i = ______. _______________
28. Least squares chooses b0,b1 to minimize ______. _______________
29. p>1 predictors → what kind of regression? _______________
30. ENUMERATE four items on the initial EDA checklist. _______________

### B5 · Logistic Regression (CO2) `[R]`
31. Despite its name, logistic regression is a ______ algorithm. _______________
32. The core squashing function is the ______, with output range ______. _______________
33. It is estimated by ______ (not OLS). _______________
34. A predicted probability above the threshold (≈0.5) assigns class ______. _______________

### B6 · Supervised ML — Association / Trees (CO3) `[R]`
35. The rule format "if A then B" in market-basket analysis is an ______. _______________
36. Support = ______. Confidence = ______.
37. Lift > 1 indicates ______. Lift = 1 indicates ______.
38. Name two algorithms that generate association rules. _______________
39. The topmost node of a decision tree is the ______; terminal nodes are ______.
40. Name two impurity/split criteria used by decision trees. _______________
41. CART makes ______ splits using the ______ index. _______________

### B7 · Clustering (CO3) `[R]`
42. Clustering is supervised / unsupervised? _______________
43. k-means assigns each point to the nearest ______. _______________
44. The common way to choose K is the ______ method. _______________
45. T/F: k-means is sensitive to outliers and to initial centroid placement. _______________

### B8 · Hadoop Ecosystem (CO1) `[R]`
46. HDFS stands for ______; its two node types are ______ and ______.
47. The Hadoop module for parallel processing is ______; the resource manager is ______.
48. Name the four core Hadoop modules. _______________

### B9 · Big Data Ecosystem & Structures (CO1) `[D]-as-taught`
49. ENUMERATE the four player groups in the Big Data ecosystem. _______________
50. The McKinsey (May 2011) role category with a 140–190k US talent gap by 2018 is ______.
51. The role category whose gap (≈1.5M) is ten times the Data-Scientist gap is ______.
52. ENUMERATE the five main skill sets of a Data Scientist. _______________
53. ENUMERATE the four data structures; which four-letter abbreviation is the semi-structured example? _______________
54. Which repository "supports BI and reporting but restricts robust analyses"? _______________
55. Which repository is a multi-source, nonproduction workspace for flexible high-performance analysis? _______________
56. BI answers WHEN/WHERE (hindsight); Data Science answers ______ and ______ (foresight).
57. T/F: 80–90% of future data growth is projected to come from non-structured data types. _______________

---

## PART C — ANSWER KEY
**B1:** 1. Humongous data volumes that traditional applications can't process effectively (raw, unaggregated, won't fit one machine's memory). 2. high-volume, high-velocity, high-variety. 3. Volume, Velocity, Variety, Veracity, Value, Validity, Variability, Venue, Vocabulary, Vagueness. 4. Veracity. 5. Vagueness. 6. Biometrics. 7. Machine-to-Machine.
**B2:** 8. Data analytics. 9. Data Management → Reporting → Descriptive → Predictive → Optimization & ML. 10. Ask → Get → Explore → Model → Communicate/visualize. 11. Collection, organization, presentation. 12. statistic · parameter. 13. TRUE.
**B3:** 14. Six. 15. Discovery, Data Preparation, Model Planning, Model Building, Communicate Results, Operationalize. 16. Phase 2. 17. Phase 1 (Discovery). 18. Phase 6 (Operationalize). 19. Business User, Project Sponsor, Project Manager, BI Analyst, DBA, Data Engineer, Data Scientist. 20. Project Sponsor. 21. TRUE. 22. data collection/analysis.
**B4:** 23. continuous. 24. Y_i = β0 + β1·X_i + ε_i. 25. N(0,σ²), iid. 26. increase in Y per unit change in X (slope). 27. y_i − ŷ_i. 28. RSS = Σ(y_i − b0 − b1·x_i)². 29. Multiple/multivariate regression. 30. any four of the eight (errors, missing values, outliers, asymmetric dist., variability changes, clustering, non-linear bivariate, unexpected patterns).
**B5 `[R]`:** 31. classification. 32. sigmoid (logistic) · (0,1). 33. Maximum Likelihood Estimation. 34. 1 (positive).
**B6 `[R]`:** 35. association rule. 36. P(A∩B) · P(A∩B)/P(A). 37. positive correlation · independence. 38. Apriori, FP-Growth. 39. root · leaves. 40. entropy/information gain, Gini impurity (or misclassification error). 41. binary · Gini.
**B7 `[R]`:** 42. unsupervised. 43. centroid. 44. elbow. 45. TRUE.
**B8 `[R]`:** 46. Hadoop Distributed File System · NameNode · DataNode. 47. MapReduce · YARN. 48. HDFS, MapReduce, YARN, Hadoop Common.
**B9 `[D]`:** 49. Data devices, Data collectors, Data aggregators, Data users & buyers. 50. Deep Analytical Talent. 51. Data Savvy Professionals. 52. quantitative · technical (SW/ML/programming) · skeptical & critical · curious & creative · communicative & collaborative. 53. structured, semi-structured, quasi-structured, unstructured · XML. 54. Data warehouse. 55. Analytic sandbox. 56. HOW · WHY. 57. TRUE.

---

## PART D — GLOSSARY (one-liners)
- **Big Data** — data too large/fast/varied for traditional processing `[D]`.
- **Analytic sandbox** — environment for the team to work with & analyze data (Phase 2) `[D]`.
- **ETL / ELT (ETLT)** — extract-transform-load / extract-load-transform pipelines into the sandbox `[D]`.
- **Initial Hypotheses (IHs)** — ideas formed in Discovery, tested later, basis of Phase-5 findings `[D]`.
- **Parameter / Statistic** — population / sample numeric summary `[D]`.
- **Residual** — observed minus fitted value `[D]`.
- **RSS** — residual sum of squares, minimized by least squares `[D]`.
- **Sigmoid** — σ(z)=1/(1+e^−z), maps reals to (0,1) `[R]`.
- **Support / Confidence / Lift** — frequency of A∩B / P(B|A) / vs-random-chance strength `[R]`.
- **Entropy / Gini** — impurity measures guiding tree splits `[R]`.
- **Centroid** — cluster mean; k-means anchor `[R]`.
- **NameNode / DataNode** — HDFS metadata / block storage `[R]`.
- **Structured / Semi / Quasi / Unstructured** — the four data structures `[D]`.
- **Spreadmarts / Data warehouse / Analytic sandbox** — three repository tiers `[D]`.
- **Deep Analytical Talent / Data-Savvy Professionals / Tech-&-Data Enablers** — McKinsey's three ecosystem role categories `[D]`.

## PART E — MNEMONICS & STUDY HOOKS
- **Ten V's:** "**V**ery **V**ast **V**ariety **V**erifies **V**alue, **V**alid **V**ariables **V**enue **V**ocabulary **V**agueness" (L→R pairs: Volume/Validity, Velocity/Variability, Variety/Venue, Veracity/Vocabulary, Value/Vagueness).
- **Lifecycle:** "**D**on't **D**elay — **M**ake **M**y **C**offee **O**ften" = Discovery, Data-prep, Model-planning, Model-building, Communicate, Operationalize.
- **Roles:** "**B**usy **S**ponsors **P**ush **B**I **D**aily, **D**ata **D**elivered" = Business user, Sponsor, PM, BI analyst, DBA, Data engineer, Data scientist.
- **DS process:** "**A**sk **G**reat **E**xperts, **M**ake **C**laims" = Ask, Get, Explore, Model, Communicate.
- **Value chain:** "**D**ata **R**eports **D**escribe, **P**redict, **O**ptimize."
- **EDA checklist hook:** "Errors, Missing, Outliers, Asymmetry, Variability, Clustering, Non-linearity, Patterns."
- **Data structures:** "**S**nakes **S**lither **Q**uietly **U**nderground" = Structured, Semi-, Quasi-, Unstructured.
- **Ecosystem players:** "**D**evices **C**ollect, **A**ggregators **U**se" = Devices, Collectors, Aggregators, Users-buyers.
- **McKinsey roles:** "**D**eep **S**avvy **E**nablers" = Deep Analytical Talent, Data-Savvy Professionals, Tech-&-Data Enablers.
- **Repositories:** "**S**pread **W**are **S**and" = Spreadmarts, Warehouses, Sandbox.

## [ADDED] SYLLABUS ↔ COLLECTION COVERAGE MATRIX (honesty map, III.4)
| Syllabus topic | Fetched lesson | Grade held | Status |
|---|---|---|---|
| Overview of DS / big data | Lesson 0 | [D]-as-taught | ✅ covered |
| Big data structures / repositories / BI-vs-DS | Lesson 1 | [D] (EMC) | ✅ covered |
| Big Data ecosystem (players/roles) | Lesson 2 | [D] (EMC/McKinsey) | ✅ covered |
| Hadoop internals | (Lesson 2 cites once) | [R] web supplement | ⚠️ architecture detail from web, not lecture |
| Lifecycle 6 phases + roles | Lesson 3 | [D] (EMC) | ✅ covered |
| Linear regression (SLR/MLR) | Lesson 6 | [D]-as-taught | ✅ covered |
| Logistic regression | — | [R] web | ⚠️ Lesson 7 unfetched |
| R fundamentals / ggplot2 | — | [NOT HELD] | ⚠️ INTRO TO R unfetched |
| Association rules / trees / clustering | — | [R] web | ⚠️ no collection file (CO3) |
| Data preparation | — | [R]/[NOT HELD] | ⚠️ Supp. Discussion unfetched |
| Coursera IBM component | — | scheduling-only | ⚑ record as deadline, never knowledge (DSS10.md) |

## LIMITS LINE (honesty, I.1)
Curriculum spine (Lessons 0/1/2/3/6) + syllabus + web for gaps. `[D]-as-taught` items are study-grade, NOT triangulated to Core; `[R]` items (logistic, association, trees, clustering, Hadoop internals) are standard facts from ≥2 web sources but may differ in your lecturer's phrasing (curriculum term wins); `[NOT HELD]` topics (R, ggplot2) require your own notes. Nothing here is board/canon material. See DSS10.md CONFLICT/GAP LOG for the Coursera and 70%-per-task notes.
