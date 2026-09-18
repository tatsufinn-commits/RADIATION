# INGEST — DSS10 Lesson 6: Linear Regression (+ statistics refresher, R)
origin: Brain/external_sources/intro-data-science.md (Drive, "Lesson 6 Linear Regression.pdf", id 1OH9qs9oxuNryisyymS9zrRhdfgHhEyMw) | type: slide deck (21 pp, text-layer present) | authority: curriculum as-taught | consumed: 2026-09-17 | mode: @Autopilot[@Gather] | rung: 1 (text)
Grade: [D]-as-taught (standard stats — most items would triangulate to [R] against any stats text; here held as-taught)

## Claims
1. **Two areas of statistics** — DESCRIPTIVE (collection, organization, presentation) vs INFERENTIAL (draw conclusions for a larger group, determine relationships, make predictions). Inferential branches: Probability, Estimation (point/interval), Hypothesis Testing. [D]-as-taught
2. **Process of statistics** — POPULATION → (sampling theory) → SAMPLE → (descriptive) → STATISTIC; PARAMETER ← inferential. Statistic describes sample; parameter describes population. [D]-as-taught
3. **Regression analysis (def.)** — statistical technique most frequently used to analyze relationship between two or more variables; needs ≥2 continuous variables; studies how one variable changes as others change. [D]-as-taught
4. **When used** — describe relationship between single response Y and one/more predictors X1..Xp; p=1 simple regression; p>1 multivariate/multiple regression. Examples: sales vs ad spend; quantity demanded vs price; profit vs R&D. [D]-as-taught
5. **Variables** — response Y must be continuous; predictors X may be continuous, discrete, or categorical. [D]-as-taught
6. **Initial EDA checklist (before regression)** — data-entry errors, missing values, outliers, unusual/asymmetric distributions, changes in variability, clustering, non-linear bivariate relationships, unexpected patterns. [D]-as-taught
7. **SLR model** — Y_i = β0 + β1·X_i + ε_i; ε_i ~ N(0,σ²) iid (random error); β0+β1·X_i = E(Y|X=X_i). β0 = intercept (y-axis crossing); β1 = slope (increase in Y per unit X). [D]-as-taught
8. **Residual** — e_i = y_i − ŷ_i (observed minus fitted). [D]-as-taught
9. **Least squares** — choose b0,b1 to minimize RSS = Σ(y_i − b0 − b1·x_i)² (residual sum of squares). [D]-as-taught
10. **SLR vs MLR** — dependent variable rarely explained by one variable; MLR predicts Y using >1 independent variable; MLR used for explanation, prediction, inference; can be linear or nonlinear. [D]-as-taught
11. **Practical** — SLR/MLR performed in Excel and in R with visual output (scatter plot + trend line); module objectives include performing both in both tools. [D]-as-taught

## Notes for reviewer
- CO2 core (Weeks 5-8; Long Quiz 2 + CO2 Examination + Final).
- Formulas as extracted; ε~N(0,σ²) iid assumption is a classic exam item.
- Logistic regression NOT in this file (Lesson 7 per syllabus) — web-triangulate at [O]/[R] if included.
