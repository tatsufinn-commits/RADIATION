# 📚 REVIEWER — STATICS OF RIGID BODIES (MEC30-7 / CE)
**Course:** MEC30-7 Statics of Rigid Bodies (Mapúa, W1–W10) · cross-checked vs PUP/UP/UST-style statics syllabi + held MEC30-7 lectures
**Sources:** held lectures (Force Vectors, Force-System Resultants) `[D]-as-taught`; calendar scope `[D]`; standard mechanics (Hibbeler-consistent) = mathematics, timeless `[D]`; method-choice & numeric-integration citations `[R]` (varsitytutors/scienceinsights, learnaboutstructures, Wikipedia/cuemath).
**Built for ONE goal:** *teach you how to decide WHICH formula a word problem needs, then solve it.*

> **How to use:** Read PART 0 until the decision table is automatic. Then PART A sheets for the toolbox. Then PART Q: cover the solutions, classify each problem FIRST, then check your work against the full solutions.

---

# PART 0 — HOW TO CHOOSE THE FORMULA (the decision method)

## The universal 5-step routine (every problem)
1. **DRAW the Free-Body Diagram (FBD).** Never skip. Unknowns live here.
2. **CLASSIFY the system.** Ask: Is it a *particle/concurrent forces*? A *rigid body* (rotation matters)? A *truss/frame*? Is *friction* mentioned? Or is it *pure geometry* (centroid / inertia / area)?
3. **LIST knowns vs unknowns.** Count unknowns.
4. **MATCH a tool** whose available equations ≥ unknowns (see table).
5. **SOLVE, then CHECK** with an unused equation (e.g., a second moment point).

## THE DECISION TABLE — "if the problem says… use…"
| Signal in the problem | System | Tool | Governing equations |
|---|---|---|---|
| "resultant of forces" at a point; forces meet at one point | concurrent | components | FRx=ΣFx, FRy=ΣFy, FR=√(ΣFx²+ΣFy²), θ=tan⁻¹(ΣFy/ΣFx) |
| two forces at an angle, "find resultant/direction" | 2-force | parallelogram | FR=√(F1²+F2²+2F1F2cosθ); law of sines for direction |
| "moment about O", "tendency to rotate", wrench, couple | rotation | moment | Mo=F·d ; (Mr)o=ΣF·d ; couple M=F·d |
| "replace by equivalent force & couple at O" | reduction | force-couple | FR=ΣF ; MRo=ΣMo(+Σcouples) |
| "find reactions/supports", body at rest, beam/bracket | rigid body | 2D equilibrium | ΣFx=0, ΣFy=0, ΣM=0 |
| "force in EVERY member" | truss | method of joints | 2 eq/joint (ΣFx,ΣFy), ≤2 unknowns/joint |
| "force in ONE/a few members" | truss | method of sections | 3 eq (ΣFx,ΣFy,ΣM), ≤3 cut members |
| "slipping/impending motion/coefficient μ" | friction | Coulomb | F≤μsN ; impending F=μsN ; moving F=μkN |
| "centroid / center of area / composite shape" | geometry | composite centroid | x̄=Σx̃A/ΣA, ȳ=ΣỹA/ΣA |
| "irregular area / table of ordinates / integrate numerically" | geometry | numeric integration | Trapezoidal or Simpson 1/3 |
| "moment of inertia / radius of gyration" | geometry | composite + parallel-axis | I=Ī+Ad² ; k=√(I/A) |
| "distributed load w(x)" | loading | load resultant | W=area under w; acts at load centroid |

## Counting-equations sanity check
- 2D particle/concurrent: 2 eq (ΣFx,ΣFy).
- 2D rigid body: 3 eq (ΣFx,ΣFy,ΣM). → at most 3 unknowns per FBD.
- Truss joint: 2 eq. Truss section: 3 eq.
If unknowns > equations → you need another FBD (break the body / take a section) or a constraint (friction at impending, symmetry).

---

# PART A — THE TOOLBOX (per-topic sheets: formulas + when + worked ex. + trap)

## A1 · Force vectors & concurrent resultants (W1–W2) `[D]`
**Formulas:** Fx=F·cosθ, Fy=F·sinθ · FRx=ΣFx, FRy=ΣFy · FR=√(FRx²+FRy²) · θ=tan⁻¹(FRy/FRx) · parallelogram FR=√(F1²+F2²+2F1F2cosθ).
**When:** forces all pass through one point; "resultant", "components", "resolve along axes".
**Worked:** F1=300N@0°, F2=400N@90°. FRx=300, FRy=400 → FR=500N, θ=tan⁻¹(400/300)=53.1°.
**Trap:** measure θ from the correct axis; keep sign of each component (a leftward force = negative Fx).

## A2 · Moments, couples, reduction (W2–W3) `[D]`
**Formulas:** Mo=F·d (CCW+) · (Mr)o=ΣF·d · couple M=F·d (independent of point) · 3D M=r×F · reduction FR=ΣF, MRo=ΣMo+ΣM_couple.
**When:** "moment about O", "couple", "replace by equivalent system".
**Worked:** 50N force, ⊥ arm 0.4m → Mo=20N·m. A couple of 100N forces 0.3m apart → M=30N·m (same about ANY point).
**Trap:** use the ⊥ distance, not the slant length; Varignon: you may split F into components and sum their moments (often easier).

## A3 · Distributed loads (W3) `[D]`
**Formulas:** W=area under load curve; location = centroid of that area. Uniform w over L: W=wL @ L/2. Triangle (peak w at one end): W=½wL @ 2/3·L from the zero end.
**When:** "distributed loading", w in N/m.
**Worked:** uniform 2kN/m over 3m → W=6kN at 1.5m from either end.
**Trap:** replace the load by its resultant BEFORE writing equilibrium; don't forget its location.

## A4 · Equilibrium of rigid bodies (W4) `[D]`
**Formulas:** ΣFx=0, ΣFy=0, ΣM=0. Supports: roller=1(⊥), pin/hinge=2(x,y), fixed=2+moment.
**When:** "reactions", "support", body at rest.
**Strategy:** take ΣM about a support so its reaction drops out → solve the other directly.
**Worked:** beam L=6m, pin A, roller B, point load 12kN at 2m from A. ΣM_A: B·6−12·2=0→B=4kN. ΣFy: A+4−12=0→A=8kN.
**Trap:** include the resultant of distributed loads and any applied couple in ΣM; couple enters ΣM unchanged regardless of position.

## A5 · Internal forces at connections / frames (W5) `[D]`
**Tool:** dismember the frame; each member is a rigid body (3 eq); connect with Newton's 3rd law (equal-opposite at pins). Two-force members carry axial force only.
**When:** "force at pin/connection", "frame/machine".
**Trap:** identify two-force members first — they collapse unknowns to one (magnitude along the member).

## A6 · Friction (W6) `[D]`
**Formulas:** F≤μsN · impending/slipping F=μsN · moving F=μkN · angle of friction tanφ=μ.
**When:** words "slip", "impending", "hold", "coefficient of friction", wedge/ladder/box on incline.
**Strategy:** assume impending (F=μsN) to find the limiting case; check the assumption.
**Worked:** 100N block on floor μs=0.4 → max friction F=0.4·100=40N. A 30N push does NOT move it (F_needed=30<40; actual F=30).
**Trap:** N is the ⊥ contact force (NOT always the weight — inclines/extra loads change N). Static friction is ≤μsN (it self-adjusts); only at impending is it =μsN.

## A7 · Numerical integration (W7) `[R]` — for irregular areas/centroids
**Trapezoidal:** ∫≈(h/2)[y0+2(y1+…+y_{n−1})+yn].
**Simpson 1/3 (n even):** ∫≈(h/3)[y0+4(y1+y3+…)+2(y2+y4+…)+yn].
**When:** given a table of ordinates or a curve with no clean antiderivative; "approximate the area/centroid".
**Worked (Simpson, h=1, y=[0,3,8]): ∫≈(1/3)[0+4·3+8]=(1/3)(20)=6.67.
**Trap:** Simpson needs an EVEN number of intervals (odd number of ordinates). Trapezoidal works for any n.

## A8 · Trusses (W8) `[D]+[R]`
**Determinacy:** m+r=2j. **Joints:** 2 eq, ≤2 unknowns, start at a joint with ≤2; assume tension (+). **Sections:** cut ≤3 members, 3 eq; take ΣM about the intersection of two unknowns to isolate the third. **Zero-force members:** (a) two non-collinear members at a joint with no load → both zero; (b) three members, two collinear, no load → the third is zero.
**When-to-use:** all members → joints; one/few members → sections.
**Worked (sections):** to get a mid-span member, cut it + two others that intersect; ΣM about that intersection → one equation, one unknown.
**Trap:** tension-positive convention; a negative answer = compression. Never cut >3 members in 2D.

## A9 · Centroids (W9) `[D]`
**Composite:** x̄=Σx̃A/ΣA, ȳ=ΣỹA/ΣA. Shapes: rectangle center (b/2,h/2); triangle ȳ=h/3 from base; semicircle 4r/3π from flat side; quarter circle 4r/3π. Holes = NEGATIVE area.
**When:** "centroid/center of area", composite shape.
**Worked:** rectangle 2×4 (A=8, ȳ=2) + triangle on top (A=4, ȳ=4+4/3). ȳ=ΣỹA/ΣA.
**Trap:** use consistent reference axis; subtract holes; a composite with a hole can have x̄/ȳ outside material.

## A10 · Moment of inertia (W10) `[D]`
**Definitions:** Ix=∫y²dA, Iy=∫x²dA. Shapes (centroidal): rectangle Ix=bh³/12; triangle Ix=bh³/36; circle Ix=πr⁴/4. **Parallel-axis:** I=Ī+Ad². **Radius of gyration:** k=√(I/A). Composite: Σ(Ī+Ad²).
**When:** "moment of inertia", "I", "radius of gyration".
**Worked:** rectangle b=2,h=6 about centroid: Ī=2·216/12=36. About base 3 below: I=36+12·3²=144.
**Trap:** parallel-axis ONLY between a centroidal axis and a parallel axis (d = distance between axes); never add Ī of parts about different axes without transferring each.

---

# PART Q — WORD-PROBLEM QUIZ (classify first, then solve) · FULL SOLUTIONS

**Q1 (concurrent).** A bolt is pulled by F1=600N at 30° above +x and F2=400N along −y. Find the resultant magnitude and direction.
*Classify:* forces at one point → components.
*Solution:* FRx=600cos30=519.6; FRy=600sin30−400=300−400=−100. FR=√(519.6²+100²)=529.1N. θ=tan⁻¹(−100/519.6)=−10.9° (i.e., 10.9° below +x).

**Q2 (moment).** A 200N force acts perpendicular to a wrench 0.5m from the bolt O. Find the moment.
*Classify:* rotation about a point → Mo=F·d.
*Solution:* Mo=200·0.5=100N·m (CCW or CW per figure; magnitude 100).

**Q3 (equilibrium).** Simply-supported beam, span 8m; uniform load 3kN/m over the whole span. Find reactions.
*Classify:* rigid body at rest → 3 eq; first reduce distributed load.
*Solution:* W=3·8=24kN @ 4m. ΣM_A: B·8−24·4=0→B=12kN. ΣFy: A=24−12=12kN.

**Q4 (friction).** A 50kg crate rests on the floor, μs=0.3. (a) Max push before slipping? (b) If pushed with 100N, does it move?
*Classify:* friction, impending check.
*Solution:* N=mg=50·9.81=490.5N. F_max=μsN=0.3·490.5=147.2N. (a) 147.2N. (b) 100<147.2 → does NOT move; friction=100N (self-adjusts).

**Q5 (truss/sections).** In a simply-supported truss, you need ONLY the force in one diagonal near mid-span. Which method and why?
*Classify:* few members → method of sections (3 eq, cut ≤3).
*Solution:* Cut the diagonal + two members whose lines meet at one point; ΣM about that point isolates the diagonal in ONE equation. (Joints would force solving many joints first.)

**Q6 (centroid).** Composite: 4×2 rectangle with a 1×1 hole at its center. Find ȳ about the base.
*Classify:* composite centroid, hole = negative area.
*Solution:* A_rect=8, ȳ=1; A_hole=−1, ȳ=1. ȳ=(8·1+(−1)·1)/(8−1)=7/7=1.0. (Symmetric, so unchanged — the check.)

**Q7 (numerical).** Ordinates y=[1,3,5,3,1] at h=1. Approximate ∫ by Simpson 1/3.
*Classify:* table of ordinates, n=4 (even) → Simpson.
*Solution:* ∫≈(1/3)[1+4·3+2·5+4·3+1]=(1/3)[1+12+10+12+1]=(1/3)(36)=12.

**Q8 (inertia).** Find I about the base of a rectangle b=3, h=4 using parallel-axis.
*Classify:* moment of inertia, non-centroidal axis.
*Solution:* Ī=bh³/12=3·64/12=16. A=12, d=h/2=2. I=16+12·4=64. (Check: bh³/3=3·64/3=64 ✓.)

**Q9 (equilibrium + couple).** A beam carries a 60N·m couple and a 10kN… (keep simple) — a 2m beam, pin A, roller B, applied couple 60N·m. Find reactions.
*Classify:* equilibrium with a couple (couple enters ΣM unchanged).
*Solution:* ΣM_A: B·2−60=0→B=30N (direction per sense). ΣFy: A=−B → A=30N opposite → forms a couple balancing 60N·m.

**Q10 (truss/zero-force).** A joint connects two non-collinear members and carries no load. What are the member forces?
*Classify:* zero-force member rule.
*Solution:* Both = 0 (rule a). Recognizing these shrinks the truss before you solve.

## ANSWER KEY (quick)
Q1 529.1N @10.9° below +x · Q2 100N·m · Q3 A=B=12kN · Q4 (a)147.2N (b)no, F=100N · Q5 method of sections · Q6 ȳ=1.0 · Q7 12 · Q8 64 · Q9 30N each (couple balance) · Q10 both 0.

## LIMITS LINE (honesty, I.1)
Held lectures [D]-as-taught; formulas = standard mechanics (timeless math, Hibbeler-consistent) [D]; method-choice & numeric-integration guidance [R] from cited web. Single-lecture spine not independently triangulated → study-grade, not Core. Where your lecturer's sign/axis convention differs, it wins.
