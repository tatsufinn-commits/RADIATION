# INGEST — DSS10 Lesson 3: Data Analytics Life Cycle Part 1
origin: Brain/external_sources/intro-data-science.md (Drive, "Lesson 3 Data Life Cycle Part 1.pdf", id 1IDWNi7RlgczfEyeEVL7b0Aw9KL2_uUP_) | type: slide deck (text-layer present, 25 pp) | authority: curriculum, quoted from *Data Science and Big Data Analytics* (EMC Education Services — prescribed e-book) | consumed: 2026-09-17 | mode: @Autopilot[@Gather] | rung: 1 (text)
Grade: [D]-as-taught; lifecycle/roles claims traceable to EMC text → may read [D] vs named published text for those specific items (triangulation to Core still requires independence check, I.3).

## Claims
1. **DS projects vs traditional BI** — data science projects are more exploratory; large problems broken into actionable phases; good process = comprehensive, repeatable method; focus early on grasping the business problem. [D] (EMC-quoted)
2. **Common mistake** — rushing into data collection/analysis before planning/scoping/framing the business problem → mid-stream mismatch with sponsor objective → revert to Phase 1 or cancel. [D] (EMC)
3. **Lifecycle overview** — designed for Big Data / data science; SIX phases; work can occur in several phases at once; iterative (circular arrows) until sufficient info to advance. [D] (EMC)
4. **THE SIX PHASES (names, in order)** — 1 Discovery · 2 Data Preparation · 3 Model Planning · 4 Model Building · 5 Communicate Results · 6 Operationalize. [D] (EMC)
5. **Phase 1 Discovery** — learn business domain + relevant history; assess resources (people, technology, time, data); frame business problem as analytics challenge; formulate initial hypotheses (IHs). Activities: learning domain, resources, framing the problem (success AND failure criteria), identifying key stakeholders, interviewing sponsor (what problem/outcome/data sources/industry issues/timelines), developing IHs, identifying potential data sources (5 activities: identify sources, capture aggregate data, review raw data, evaluate data structures & tools, scope data infrastructure). Exit when able to draft an analytics plan for peer review. [D] (EMC)
6. **Phase 2 Data Preparation** — requires an analytic sandbox; execute ELT / ETL (sometimes ETLT) to load data; transform & condition data; familiarize thoroughly with data. [D] (EMC)
7. **Phase 3 Model Planning** — determine methods, techniques, workflow for model building; explore data to learn relationships between variables; select key variables + most suitable models. [D] (EMC)
8. **Phase 4 Model Building** — develop datasets for testing/training/production; build & execute models; assess whether existing tools suffice or need robust environment (fast hardware, parallel processing). [D] (EMC)
9. **Phase 5 Communicate Results** — with stakeholders, determine success/failure vs Phase-1 criteria; identify key findings, quantify business value, develop narrative for stakeholders. [D] (EMC)
10. **Phase 6 Operationalize** — deliver final reports, briefings, code, technical documents; may run a pilot to implement models in production. [D] (EMC)
11. **KEY ROLES (7 listed)** — Business User (domain expert; benefits from results; advises context/value/operationalization) · Project Sponsor (genesis; defines core problem; funds; sets priorities & desired outputs; gauges value) · Project Manager (milestones/objectives on time & quality) · Business Intelligence Analyst (domain expertise via data/KPIs/metrics; dashboards & reports; knows data feeds) · Database Administrator (provisions/configures DB environment; access; security) · Data Engineer (tunes SQL; data extraction; ingestion into sandbox; shapes data for analysis) · Data Scientist (SME for analytical techniques & modeling; designs/executes methods; ensures objectives met). [D] (EMC)
12. **Framing the problem** — write problem statement, share with stakeholders; identify objectives (business terms), success criteria AND failure criteria (failure criteria tell when to stop/settle). [D] (EMC)

## Notes for reviewer
- CO1 Examination core (Weeks 3-5). Phases 1-2 deep-dive here; Phases 3-6 summaries here (Parts 2-3 unfetched) but phase names+essence all present.
- "ETLT" = ELT + ETL combined abbreviation.
- Roles enumeration is a classic exam list (7).
