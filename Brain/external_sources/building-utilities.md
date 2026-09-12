# COLLECTION — Building Utilities

## 1. IDENTITY
- LINK           : https://drive.google.com/drive/folders/1NDwAt57pRNbvRCuK40xKBGd1PAldfmOb?usp=sharing
- OWNER          : THE COMMANDER
- PERMISSIONS    : anyone-with-link (verified working without auth; owner hidden)
- APPROVED       : 2026-09-12 — RADIATION_PATCH_2026-09-12_1900_First-Collections-Registration.zip
- LAST VERIFIED  : 2026-09-12 (re-verify by 2026-12-11)

## 2. CONTENTS DESCRIPTION
Building utilities (MEPFS) reference set: electrical systems (Fajardo
Electrical Layout & Estimate, Philippine Electrical Code, electrical modules),
plumbing/sanitary (Fajardo Plumbing, sanitary system texts, pipe color codes,
fireground hydraulics), mechanical systems module, and architectural
acoustics (Ginn; two recording-studio design texts). 14 PDFs, up to 77.6 MB.

## 3. EVIDENCE-GRADE EXPECTATIONS
Philippine Electrical Code → [D] — cite article/section exactly · Fajardo
handbooks → [D] for published formulas/standards · modules/presentations →
[D] as-taught · acoustics texts → [R]/[D].

## 4. MANIFEST (captured 2026-09-12, live read)
| File | Type | Topic | Noted |
|---|---|---|---|
| Architectural Acoustics 2nd Ed. (K.B. Ginn) | PDF 23.2 MB | Acoustics | 2026-09-12 |
| ELECTRICAL Bu2.pdf | PDF 77.6 MB | Electrical systems | 2026-09-12 |
| Electrical Layout and Estimate 2nd Ed. (Fajardo & Fajardo) | PDF 33.1 MB | Electrical | 2026-09-12 |
| Module — Mechanical and Electrical Systems | PDF 47.2 MB | M&E systems | 2026-09-12 |
| Module — Plumbing and Sanitary Systems | PDF 21.9 MB | Plumbing/sanitary | 2026-09-12 |
| Philippine Electrical Code.pdf | PDF 6.8 MB | PEC law text | 2026-09-12 |
| Pipe Color Code.pdf | PDF | Standards | 2026-09-12 |
| Plumbing_Sanitary_System_Flea_2012.pdf | PDF 5 MB | Plumbing/sanitary | 2026-09-12 |
| Plumbing–Max Fajardo.pdf | PDF 12.5 MB | Plumbing handbook | 2026-09-12 |
| Plumbing-System.pdf | PDF | Plumbing | 2026-09-12 |
| presentationplumbing.pdf | PDF 5.2 MB | Plumbing lecture | 2026-09-12 |
| QS_3FiregroundHydraulics_edited.pdf | PDF | Fire hydraulics | 2026-09-12 |
| Recording Studio Design (+ duplicate copy) | PDF 24.9 MB ×2 | Acoustics/studio design | 2026-09-12 |

## 5. DIGEST
*(populated 2026-09-13 — first ingestion session. Method: manifest → fetch to a scratch
volume outside the repository → text-layer extraction with table verification → record.
Binaries deleted after extraction, per II.6 rule 8. **Nothing in this section is citable
until its grade is stated.**)*

### 5.1 INGESTION VERDICT — 14 files, 283.4 MB, all fetched (0 failures)

| # | File | Pages | Text layer | Grade | Anchors |
|:--:|---|:--:|---|---|---|
| 01 | Pipe Color Code | 1 | ✅ | **[D]** | PD 1096 Rule XII/XIII |
| 02 | Plumbing-System | 17 | thin (43 w/p) | [D]-as-taught | plumbing fundamentals |
| 03 | QS_3 Fireground Hydraulics | 20 | ✅ | **[R]** (US manual) | fire hydraulics principles |
| 04 | Plumbing_Sanitary_System_Flea_2012 | 166 | ✅ | [D]-as-taught | sanitary systems |
| 05 | presentationplumbing | 100 | ✅ | [D]-as-taught | water supply · sanitary · storm drainage |
| 06 | **Philippine Electrical Code** | **856** | ✅ | **[D] primary law** | **K-STD-004** |
| 07 | Plumbing — Max Fajardo | 175 | ❌ **image-only** | ⏳ **RECOVERY NEEDED** | plumbing design tables |
| 08 | Module — Plumbing and Sanitary Systems | 57 | ❌ **image-only** | ⏳ **RECOVERY NEEDED** | course module |
| 09 | Architectural Acoustics 2nd Ed (Ginn) | 172 | ✅ | **[D]/[R]** | **K-BK-004** |
| 10 | Recording Studio Design (1) | 737 | ✅ | [D]/[R] | acoustics (duplicate) |
| 11 | Recording Studio Design | 737 | ✅ | [D]/[R] | acoustics |
| 12 | Electrical Layout and Estimate 2nd Ed (Fajardo ×2) | 349 | ✅ | [D] published handbook | **K-BK-005** |
| 13 | Module — Mechanical and Electrical Systems | 102 | ❌ **image-only** | ⏳ **RECOVERY NEEDED** | course module |
| 14 | **ELECTRICAL Bu2** | **434** | ✅ | [D]-as-taught | electrical systems |

**3,923 pages extracted or inventoried** — the §5.1 column sums to exactly this. 11 files carry a
usable text layer (10 full, 1 thin); **3 files (334 pages) are image-only** and need the recovery ladder.

### 5.2 ⭐ THE FINDING THAT MATTERS MOST — naive text extraction silently corrupts legal tables

**PEC Table 2.20.2.3 was extracted WRONG by line-order text parsing, and the error was invisible.**

Naive extraction produced: `Armories 33 · Banks 11 · Churches 22 · Dwellings 22 · Schools 3` — a
plausible-looking table with **every value shifted**. The correct table (verified by rendering
the page and reading it, i.e. the recovery ladder's vision rung) is:

| Occupancy | VA/m² | | Occupancy | VA/m² |
|---|:--:|---|---|:--:|
| Armories and auditoriums | **11** | | Industrial commercial (loft) | 22 |
| Banks | **39**ᵇ | | Office buildings | **39**ᵇ |
| Barber shops and beauty parlors | **33** | | Restaurants | 22 |
| Churches | **11** | | Schools | 33 |
| Clubs | 22 | | Stores | 33 |
| Court rooms | 22 | | Warehouses (storage) | **3** |
| Dwelling unitsᵃ | **33** | | Assembly halls and auditoriums | 11 |
| Garages — commercial (storage) | **6** | | Halls, corridors, closets, stairways | 6 |
| Hospitals · Hotels and motels | 22 | | Storage spaces | 3 |

*Footnotes: ᵃ see 2.20.2.5(j) · ᵇ see 2.20.2.5(k). Source: PEC 2009, Table 2.20.2.3 (print p.55).*

**RULE ESTABLISHED (proposed for `proc_ingestion-run`, P-04 ratification):**
> **A legal or numeric table extracted by text order alone is UNVERIFIED.** Two-column tables,
> multi-line row labels, and merged cells **mis-bind silently** — the output looks like a table
> and reads like one. Any table carrying a code value **must be verified by coordinate-based
> extraction or by rendering the page and reading it.** A number that cannot be traced to a
> verified table read is not `[D]`.

This is the same defect class as AP-03 (grade inflation through convenience) — a value wearing a
grade it has not earned. It was caught here **only because the table was checked against a render.**

### 5.3 PRIMARY-LAW CONTENT RECOVERED — PD 1096 Rule XII/XIII (pipe colour coding)
File 01 is **not a utilities handout — it is a PD 1096 table**, and it enters as `[D]` primary law,
citable to Rule and section, not to the handout. Recovered verbatim (Rule XIII Electrical and
Mechanical Regulations / Rule X Mechanical Regulations):

**Division codes** — Steam: HP **WHITE** · Exhaust **BUFF** · Water HP & LP fresh **BLUE**, salt **GREEN**
· Oil delivery **BRASS-BRONZE**, discharge **YELLOW** · Pneumatic all **GRAY** · Gas all **BLACK**

**Pipe-identification colour key** — **RED**: carbon dioxide, fire-service water · **ORANGE**:
acetylene, blast-furnace gas, gasoline, grease, hydrogen, oxygen, oil, tar, producer gas, LPG,
oil-and-water, high vacuum · **YELLOW**: acid, HP air, ammonia, HP steam, LP steam, boiler-feed
water, hot water, HP water · **GREEN**: LP air, LP argon, LP helium *(list continues in the source)*.

**Anchors K-LAW-001 (PD 1096, already held).** This is the first **mechanical/electrical** content
extracted for PD 1096 — until now the held module (K-MOD-001) covered only Rules VII–VIII.

### 5.4 PEC 2009 — structure and a currency question
**856 pages, 399 bookmarks.** Structure verified by TOC: Chapter 1 General (definitions, permits,
Art. 110) · Chapter 2 Wiring and Protection (branch circuits, grounding, load calculations Art.
2.20) · Chapter 3 Wiring Methods and Materials (Art. 3.14–3.74) · Chapter 4 Equipment (Art. 4.9–4.70)
· Chapter 5 Special Occupancies (hazardous locations, health care, assembly) · Chapter 6 Special
Equipment (manufactured wiring, cranes, EVs, solar PV Art. 6.90, fire pumps Art. 6.95) · Chapter 7
Emergency Systems (Art. 7.0–7.70) · Chapter 8 Communications (Art. 8.0).

**Voltages for load calculation (2.20.1.5(a), verbatim):** 115 · 115/230 · 208Y/120 · 230 · 347 ·
400Y/230 · 460Y/265 · 460 · 600Y/347 · 600.

> ⚠️ **EDITION CURRENCY — UNRESOLVED.** This is the **2009** edition. The PEC has been revised since
> (2017 is the edition commonly cited in current PH practice). **Nothing from this file may be
> taught as current until the edition question is settled** — see the decay-register row.
> *Recorded as a currency flag, not as a defect in the file.*

### 5.5 🎯 PRECISION FINDING — file 03 is a US fire-service manual, not a Philippine source
`QS_3FiregroundHydraulics_edited.pdf` is the **Tennessee Fire Academy Driver Operator Manual,
Chapter 3, revised 04/2014** — its own text says the data comes from tests on TFACA equipment
("flow, force, and/or pressure ... safe and practical to what we use here in Tennessee"). Units are
**psi, feet, FPS, gallons**.
**Grade: `[R]` for hydraulics principles** (friction loss, elevation pressure ≈ 0.5 psi/ft, water
hammer) · **NEVER citable for any Philippine code value.** Its presence in a "Building Utilities"
collection is a **categorisation hazard** — a future session could mistake it for a PH standard.
Flagged here so it cannot.

### 5.6 STRUCTURAL FINDINGS
- **Byte-identical duplicate.** Files 10 and 11 share MD5 `d7c0b5cf…` — the same document twice, as
  the manifest's "duplicate copy" note suspected. **This is AP-05 (mirror duplication) present in
  a live collection**, and the first instance found *in RADIATION's own holdings* rather than in
  TAMAKEE. One file is redundant; nothing is lost by treating 10 and 11 as ONE object.
- **334 pages are image-only and unrecovered** (files 07, 08, 13 — 175 + 57 + 102 pages). The
  recovery ladder applies; a text-layer pass simply returns 0 words. **These are course modules for
  AR153P — the highest code-density course of the term** — so their recovery is not optional.
- **File 07 renders at 2200 × 1700 pt** (a large-format scan) while 08 and 13 are A4 — likely three
  different originals, not one family.
- **Overlap:** files 02, 04, 05, 07, 08 all cover plumbing/sanitary. The collection is **redundant in
  its plumbing half and thin in its mechanical half**.

### 5.7 WHAT THE COLLECTION DOES **NOT** CONTAIN
- **The Revised National Plumbing Code** — the governing instrument for the sanitary half. Still not
  held. *(Confirmed: the collection has handbooks and handouts about plumbing, but not the Code.)*
- **NSCP 2015** — governs the structural/mechanical interface; held elsewhere (Law collection) but
  **still has no registry row**.
- **No fire-code text** (RA 9514) despite fireground hydraulics being present.

## 6. ACCESS LOG (append-only, II.2)
| Date | Session/model | Result | Note |
|---|---|---|---|
| 2026-09-12 | Protocol Architect (registration session) | ACCESSIBLE | Full listing read; manifest captured |
| 2026-09-13 | Architect (ingestion session, P-10 follow-on) | ACCESSIBLE | **14/14 files fetched, 283.4 MB, 0 failures.** 3,923 pages inventoried. Text layer usable on 11 (10 full + 1 thin), image-only on 3 (334 pp). Digest populated §5. Binaries deleted per II.6 r.8. Found: PEC edition = 2009 (currency flag); byte-identical dup (10≡11); file 03 is a US/ Tennessee manual, not PH |
