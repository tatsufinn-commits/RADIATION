# PATCH NOTES — RADIATION_PATCH_2026-09-13_2500_BT-Ingestion-AR163P.zip
**Risk class:** 🟢 ORDINARY — no constitutional text, no core scaffold, no mode definition, no Scan rule.
**⚠️ This patch modifies two validator checks (`scripts/validate.py`).** Both are precision fixes, both carry regression tests in both directions, and **neither loosens a guard** — §6 states exactly what changed and why.
**This patch is a SUPERSET of `…_2400_BU-Ingestion-AR153P.zip`.** If the 2400 patch was never applied, this one alone brings the tree to the same state; if it was applied, extracting this over it is idempotent. Nothing is removed from the tree either way.
**Validator (clean mirror):** 25 checks · **22 pass · 2 warn · 1 fail — identical before and after.** It adds no failure and clears none. The one fail is check 2.5's six pre-existing course vehicles (pending the authorised Phase-0 removal); the warns are check 16 (meta-budget, standing) and check 20.5 (AP-08 — *correctly still on; see §6*).

---

## 1 · WHAT THIS IS

**Ingestion run #2 — K-CUR-006, Building Technology (AR163-1P, K-CUR-011).** The last high-yield course of the term that had never been processed.

| | |
|---|---|
| **Accounted for** | **50 / 50 files** — 49 fetched (1,177.9 MB, **0 failures**) · **1 SIZE-SKIPPED** (601.1 MB, lawful and logged) |
| **Inventoried** | 45 PDFs / **8,797 pages** · 4 non-PDF objects extracted · 2,038 pp image-only |
| **Produced** | DIGEST populated (§5) · 6 registry objects · 4 decay rows · 1 ingestion record · the harness hardened |
| **Deleted** | every binary — **no vehicle entered the repository** (II.6 r.8) |

**Live manifest vs registered manifest: no drift.** 50 files both times, 1,177.9 MB live vs 1,178.2 MB registered — two titles are merely abridged in the registration. *Checked rather than assumed; the first version of that check was wrong and said the opposite (§8).*

---

## 2 · ⭐ THE FINDING THAT MATTERS MOST — the core course texts are TEXT-BLIND

**Every book this course is actually taught from is a scan with no text layer.**

| File | pp |
|---|--:|
| **Barry**, *The Construction of Buildings* **vols 1–5** | 984 |
| **the course's own module** (`Module - Building Technology`) | 248 |
| *Visual Handbook of Building and Remodeling* (US) · *Architectural Surfaces* · *Essential Guide to Framing* · *STAIRS DESIGN* | 806 |
| **Total** | **2,038 = 23.2 % of the collection** |

**Building Utilities, ingested the day before, was 8.5 % image-only — and its text-blind files were peripheral. Here it is 23.2 %, and it is the spine.**

**So this patch's own headline sentence needs a second half.** "K-CUR-006 ingested" is true and incomplete: the ingestion read the *periphery*, and is blind to the *core*. Any future session that repeats the first half alone is reporting a half-truth, which is why the caveat is written into the DIGEST, the course record, the ingest record and the ledger rather than buried in one of them.

**Measured, not assumed:** the scans are legible — rendering *The Construction of Buildings 1* p. 50 at 110 dpi returns clean body text and legible captions. The recovery ladder is **viable** (≈ a page per render-and-read). **None of it has been done, and none of it is claimed.**

**Grade consequence:** no page of those 2,038 carries `[D]` — *including the volumes whose editions were settled*, because an edition is a fact and the content behind it is still unread.

---

## 3 · ⭐ THE METHOD FINDING — a 200 with the wrong bytes is a FAILED fetch

**The first fetch of this collection downloaded Google's "virus scan warning" HTML page as `Module - Building Technology.pdf`, and my harness counted it OK** — because the interstitial *is text*, and the harness's check accepted text.

**116 MB of the course's own module was silently absent from a run that printed "48 fetched, 0 failures".**

Nothing about that output looked wrong. **This is the PEC-table failure in a different costume:** the right shape, the wrong contents, passing a check that only asked for something plausible.

> **THE RULE THIS ESTABLISHES — a fetch is successful only if the bytes match the declared type.**
> HTTP 200, a non-zero size and a plausible-looking file are **not** evidence. Validate the magic bytes against the extension; on mismatch, run the >100 MB confirm flow; if it still fails, **fail loudly**. *A document fetch that silently yields a web page is a missing document, not a downloaded one.*

**Fixed in this patch, three ways:**
1. **declared-type gate** — `.pdf→pdf`, `.xlsx/.pptx/.docx→zip`, `.ppt/.xls/.doc→ole`; a mismatch is a **FAIL** and is logged, never a pass;
2. **the >100 MB confirm-token flow** — parses the interstitial's `id/export/confirm/uuid` form and re-requests from `drive.usercontent.google.com`. Verified: 116.08 MB, `%PDF-1.6`;
3. **cache validity** — a cached file is re-fetched unless its bytes match the declared type (the first run's 2,449-byte "PDF" sat in the cache and would have been counted as present).

*The log said OK. The file was a web page. It was caught by reading the bytes instead of the log.*

---

## 4 · 🎯 THE QUESTION BANK — 3,036 items, and what it is NOT

`Building Tech, Utilities, Structural (1).xlsx` → sheet **"Ultimate Reviewer"**, **3,036 items**, options inline `[A]`–`[D]`. It is the single highest-value-looking object in the collection.

**It looks like an answer bank. It is not one.**

| Column | Holds | Coverage |
|---|---|---|
| question text | the question | 3,036 |
| **answer letter** | **the key** | **24 items — 0.8 %** |
| the attempt's answer | what someone chose | all items |
| verdict / score | 16 Correct · 2,906 Wrong · score **16** | |

**The correct answer is recoverable for 16 items out of 3,036.** Filed `K-REF-004` as **[R] — a question corpus, not an answer source.**

**Building drills from it as if it were keyed would be the PEC-table failure at a scale of three thousand** — a plausible, unverified letter, memorised until it feels like knowledge. **Its honest value is the reverse one: it is a coverage map** of what this course examines (concrete 348 · doors & hardware 190 · roofing 170 · PEC 144 · steel 137 · wind 118 · NSCP 80 · foundation 62 · masonry 58 · timber 43 · plumbing 26).

*The 2,906 "Wrong" marks are unexplained — possibly a bulk-marked or stale attempt. Recorded as unexplained, not interpreted.*

---

## 5 · WHAT WAS RECOVERED

- **The Philippine material** — `K-BK-006` **Salvan**, *Architectural Building Materials* ("The New Ladder Type Curriculum", UAP) — the PH text, and the only object here that speaks to PH practice rather than a foreign code. **Edition unresolved** (interior years 1963/69/87); no dated claim until settled.
- **`K-BK-008` FLEA 2013 UAP-Dubai review chapters** — steel · doors & hardware · roofing · concrete · site preparation · formworks. **Philippine licensure review**, each with "Refresher Questions". `[R]`: *a review deck is not an authority; it points at authorities.*
- **`K-REF-005`** a 1,066-row glossary · **`K-REF-006`** a **210-item identification list** ("Short metal 'T' beam in suspended ceilings" → *Cross Tee*) — **drill-shaped, the same shape as the PD 1096 drill already in use.**
- **`K-BK-007` Barry vols 1–5 — editions settled by render, not by filename:** vol 1 **7th** · vol 2 **5th** · vol 3 **4th** · vol 4 **4th** · vol 5 **NOT SETTLED** (recorded as unknown rather than guessed). **The set is mixed editions: "cites Barry" is not a citable act — a claim must name the volume *and* the edition.** Decay row filed.
- **Hazards flagged:** most of the collection is foreign-code (US ASD/NDS · UK/BS · EU/EC5 · India/IS) and **none of it is a source for a Philippine code value**; one file is a **marketing SAMPLE** sold into the folder as a book (`25`, Walshaw — 37 pp of a title that runs to hundreds); one is a **1988** Elsevier energy text; one is a **2002 Carbon Trust UK wind-turbine report**.

---

## 6 · TWO VALIDATOR CHECKS MADE PRECISE — and the guard my own patch broke

**This patch modifies `scripts/validate.py`. Here is exactly what changed.**

### 6.1 check 2.5 — a denied code is a token, not a substring
The check denies a list of literal room/section codes (`S308`, `NW408`, **`C5`**, `E01`, …) with `if w in text`. **My new course record contains "EU/EC5" (Eurocode 5) — which contains "C5" — so the patch introduced a check-2.5 failure on legitimate domain content.**

`CV_DENY` codes are now matched with **word boundaries**; distinctive strings (`calendarFeed`, `@mapua.edu`) keep substring matching.
**Regression-tested in both directions:** a **standalone `C5` still FAILS** (verified), and `EC5` no longer does. *This fixes the rule's precision; it does not exempt the content.*

### 6.2 ⚠️ check 20.5 — the AP-08 guard my ingestion rows switched off
When I first ran the validator, **pass went up by one: check 20.5 went from WARN to PASS.** That looked like good news. It was not.

The check cleared if any of the last three task-ledger rows merely **contained the substring "drill"** — and my ingestion rows say *"**not a drill source**"*. **The AP-08 guard — the one that exists to say "plans are not progress" — switched itself off on a sentence about the opposite of practising.**

**A guard that a passing mention can silence is not a guard.** The check now requires an **explicit marker** (`attempt:` · `mastery:` · `drilled` · `@Review`), documented in `Brain/short_term/plan/README.md` with the reason written next to it. **Consequence: the AP-08 warning is correctly still ON** — the plan exists and no attempt has been logged. *That warning is true, and this patch deliberately leaves it true.*

**Net effect of both fixes: the check count is unchanged (22 · 2 · 1 before and after).** Nothing was loosened; one false positive was removed and one false clear was removed.

---

## 7 · CORRECTIONS TO PRIOR RECORDS — the 4th registry cross-check

**K-CUR-006 was mis-described at registration, in two ways:**

| Registered | Reality |
|---|---|
| *"Building Technology **deck set**"* | **predominantly textbooks** — Barry ×5, Salvan, Duggal, EC5/BS/IS texts; only ~8 of 50 files are decks |
| *"50 files; **601 MB**"* | live total **1,177.9 MB** — 601.1 MB is **one file inside it** |

**The mis-description would have under-specified this ingestion by half:** a session trusting it would have budgeted 601 MB and met 1,178 MB, and would have gone looking for slide decks and found two core textbooks. Corrected in the row, with the correction recorded rather than silently edited.

**Four build sessions, four registry corrections** (K-CUR ID collisions · the K-REF-001 collision · two false "not held" gaps · a mis-sized material set). The mechanism is doing what P-03 built it for. *Also fixed in passing: a typo in `K-BK-005`'s notes ("bookbook").*

**Registry rows:** K-CUR-005 and K-CUR-006 status → `INGESTED 2026-09-13`; **+K-BK-006, +K-BK-007, +K-BK-008, +K-REF-004, +K-REF-005, +K-REF-006** (every prefix grepped free across the whole tree first — 0 hits each). Total **45 K-IDs**, no duplicates (check 17 PASS).

---

## 8 · WHAT WAS BUILT

```text
CHANGED   Brain/external_sources/building-technology.md   §5 DIGEST populated (was: "empty") + ACCESS LOG row
NEW       Brain/short_term/ingest/BT_INGEST_2026-09-13.md  the ingestion record (8 sections, incl. the method rule)
CHANGED   docs/KNOWLEDGE_REGISTRY.md                       K-CUR-005/006 → INGESTED; +6 objects; 1 typo fixed
CHANGED   docs/DECAY_REGISTER.md                           +4 rows (Barry mixed editions · 1988 energy text · Salvan edition · FLEA 2013 currency)
CHANGED   scripts/ingest_collection.py                     declared-type gate · >100 MB confirm flow · --max-size + skip log · cache validation · OOXML extraction
CHANGED   scripts/validate.py                              check 2.5 token-aware · check 20.5 requires an explicit attempt marker
CHANGED   Brain/courses/AR163-1P.md                        material → INGESTED + the caveat; what the run produced; 3 findings
CHANGED   Brain/courses/INDEX.md                           both register tables updated
CHANGED   Brain/short_term/plan/README.md                  the attempt-marker convention (why, not just what)
CHANGED   Brain/frontal_lobe/task_ledger.md                +1 row
CHANGED   docs/PATCH_LEDGER.md                             +1 row
CARRIED   (from the superseded 2400 patch)                 building-utilities.md §5 · BU_INGEST record · AR153P.md · APPLY scripts
NEW       APPLY.sh · APPLY.ps1                             updated for this patch
CARRIED   PATCH_NOTES.md                                   zip-only (archived out of the tree on apply)
```

**The harness now carries the restraint doctrine in code:** `--max-size` makes a large file a **logged skip** instead of a silent omission, and the skip log is **built by scanning the destination** rather than from the run's control flow — *the first version lost an entry on a second run because the file was cached, and an accountability log that depends on cache state is not a log.*

---

## 9 · VALIDATOR STATE — HONEST REPORT

```text
clean mirror, before this patch:  25 checks · 22 pass · 2 warn · 1 fail
clean mirror, after  this patch:  25 checks · 22 pass · 2 warn · 1 fail   ← identical
```

| measure | before | after |
|---|---|---|
| checks · pass · warn · fail | 25 · 22 · 2 · 1 | **identical** |
| boot budget Tier0+1 | 34,138 B | **35,161 B** (+1,023 B — two ledger rows) — **86 % of the 40 KB cap, PASS** |
| registry K-IDs (check 17) | 36 | **45** |
| 🟠 canon count (check 16) | 15 | **15 — zero canon added** |

*Measured on a mirror that includes the repo's own `PATCH_NOTES.md` / `*_STAGED*` files, the same run reads 15 pass / 4 warn / 6 fail — those extra failures are the carriers themselves, they appear identically with and without this patch, and they are reported here only so the next session does not mistake the delta for progress.*

**Defects caught in my own work before this patch left the workspace:** the type-gate bug (§3, the most serious) · a **broken drift check that reported phantom drift** and was re-run robustly · the cache-dependent skip log · the AP-08 false clear (§6.2) · `validate.py` missing from the patch tree while this patch modifies it · and **an invalid acceptance test of my own making** — the tree comparison used unquoted `$(find …)`, which word-split on the spaced course filenames, so md5sum silently skipped most of them and the "identical" result was meaningless. Redone NUL-safe: **221 files compared, zero differences.** *A test that silently skips what it cannot name is the same failure class as everything else in this patch — and it was the second time that trap has caught me.*

---

## 10 · WHAT THIS DOES NOT DO

| Not done | Why |
|---|---|
| **Recovering the 2,038 image-only pages** | The real constraint, and it is a project: ≈ a page per render-and-read. Flagged, quantified, **not started** |
| **Building any module or drill** | Ingestion is evidence-in. The drill-shaped corpora are *identified*; keys must be resolved against governing sources first |
| **Verifying the 3,036-item corpus** | Same reason — and it must not be trusted as a key in the meantime |
| **Verifying the PEC 2.10.3 citation** in the outlet/switch deck | Cheap, and it is the first action if that file is used |
| **Touching the `structural` collection** | Standing instruction: it stays `NOT ingested — Commander holds a larger plan`. **13 structural titles inside K-CUR-006 were processed as members of that collection; the collection on hold was never opened.** §5.8 of the digest states this so nobody conflates the two |
| **The 18-carrier purge** | Separate patch, separate authorisation (II.4) |

---

## 11 · NEXT — ranked

1. **🔴 Rotate the LMS feed** — still open, still yours alone.
2. **🟠 Authorise the 18-carrier purge** — one word, and check 2.5's remaining fail and the CI noise both clear.
3. **The 2,038 image-only pages of K-CUR-006** — now the single largest evidence gap in the system, and it sits under the course with the second-highest ALE yield. Barry vols 1–5 (984 pp) and the course module (248 pp) are the priority subset.
4. **`K-REF-006` — the 210-item identification list → a drill set.** Drill-shaped already, answers are the terms themselves, no key needed. **This is the cheapest real yield in the collection.**
5. **A Building Technology module** — Salvan (PH) + the FLEA chapters are enough for a first pass; NSCP remains `RECORDED-NOT-HELD`, so any structural value would be a pointer, not `[D]`.
6. **Supply `week1_start`** — one date and the planner's whole term becomes dated.
7. **`attempt:` something.** Check 20.5 is warning, and it is right.

---

## 12 · EVAL-FIRST (the clause, applied)
| | |
|---|---|
| **INSTANCE** | AP-03 (grade inflation through convenience) reached a *third* form here: not a wrong value, but a **fetch that returns the wrong kind of bytes**, and an **attempt guard switched off by a word**. Both were caught by reading the artifact instead of the log |
| **COST** | +2 files, +1,023 boot bytes, 0 canon, 0 new modes. All binaries deleted — net repository growth is documentation plus two hardened scripts |
| **DISPLACEMENT** | Discharges a standing order (the empty-DIGEST cue) for the second collection. Reuses the existing machinery — `external_sources/` pattern, II.6 restraint doctrine, the existing drill format |
| **CHECK** | Two checks were made **more precise, not weaker**, each with a two-direction regression test. **The honest gap: nothing yet enforces "the bytes match the declared type" inside CI** — it lives in the harness. Flagged rather than papered over |
