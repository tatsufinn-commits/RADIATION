# PATCH NOTES — Core Emission & The Net

**Patch:** `RADIATION_PATCH_2026-09-13_3000_Core-Emission.zip`
**Base:** post-2900 tree (v1.7.0 — **2900 must be applied FIRST**; APPLY.sh gates on it)
**Prepared:** 2026-09-13 · **Type:** DELTA · **Build order:** 3000 = the "prioritize
building RADIATION" patch (Commander directive: no drills, no study modules — build the system)

1. **RISK LEVEL   : 🟡 MEDIUM — new subsystems + one validator behavior change (MINOR → v1.8.0)**
   **RISK BASIS   :** CANON CHECK resolves **NO** — no constitutional text, no core
   scaffold, no mode definition, no Scan rule. Validator changes are additive and
   offline-safe: check 13 gains an OPT-IN online mode (sessions stay offline by law),
   and check 18's drill rule is hardened (word-bounded heading). Two new `scripts/`
   tools, five newly locked knowledge assertions, registry/docs refresh.
   **DIRECTION PRE-ORDERED:** "we prioritize building RADIATION" under the standing
   full-discretion grant.

2. **FILES TOUCHED:**
    1. `scripts/nota.py` — **ADD** — Core card tool: scaffolds to the proc-shape,
       `--check` enforces ≤300 words / LINEAGE / SHIELD / decay / index parity.
       Guards the door; never admits.
    2. `scripts/module_scaffold.py` — **ADD** — born-valid module scaffolds; mirrors
       check 18 BEFORE writing; `--list` reports parity honestly.
    3. `scripts/validate.py` — **REPLACE** — check 13 implemented (opt-in online
       census; offline default unchanged) + check 18 drill rule hardened (v2).
    4. `tests/knowledge_assertions.json` — **REPLACE** — 9 locked / 5 pending (was 4/9).
    5. `docs/CAPABILITIES.md` — **REPLACE** — tools #9 and #10; "no note-card
       generator" removed from NOT-HERE (now false).
    6. `scripts/README.md` — **REPLACE** — eight other tools; offline-default note.
    7. `.github/workflows/validate.yml` — **REPLACE** — +nota check, +scaffold
       self-test, +online link census step.
    8. `docs/SYSTEM_STATE.md` · `README.md` · `CHANGELOG.md` — **REPLACE** — v1.8.0.
    9. `APPLY.sh` · `APPLY.ps1` — verification + reconciliation runner (transport).
   10. `PATCH_NOTES.md` — this file (transport; deleted by APPLY).

3. **AREAS TOUCHED:** [x] Brain (tests/) [ ] laws [ ] scaffolds [ ] styles
   [ ] subskills [ ] cues [ ] modes/Scan [x] other: **scripts/, CI, docs**

4. **RATIONALE — build the system, feed it later:**
   - **The Core was the last convention-only surface.** Every other standard in this
     repo is machine-guarded; a Core card was enforced by prose. Now: `nota.py` makes
     the shape impossible to violate silently. The 300-word limit, lineage, stamp,
     decay and index parity are all checkable — admission stays a session act.
   - **Modules were unbuildable in practice.** Check 18 demands 13+ structural
     features per module; hand-authoring one without error is unlikely. The scaffold
     emits them born-valid. In building it, the mirror **caught check 18 itself
     napping**: bare `"DRILL"` accepted a "## DRILLS" heading with zero drill items.
     Both hardened together (they are designed to move in lockstep).
   - **The regression net now pins the render-verified past.** 9 of 14 locked: PEC
     856 pp [D] primary; Barry vols 1/2/3 = 7th/5th/4th editions (vol 5 stays
     unlocked BY DESIGN — the digest says render inconclusive); the K-CUR-006 census
     (8,797 pp · 2,038 image-only · 23.2 %). The first lock attempt FAILED the net —
     `appears_in` is enforced, not informational. The net works; the trail is kept
     in each assertion's `lock_note`.
   - **check 13 finally exists.** Since founding it was a permanent SKIP — a guard
     that never guarded. Now opt-in online (`RADIATION_ONLINE=1`, CI-only by law):
     HEAD-with-GET-retry census of every external URL in non-exempt files, WARN on
     dead. Its first live run caught its own extraction bugs (a `<FILE_ID>`
     placeholder and backtick-contaminated URLs) — fixed before it could cry wolf.
     Final census: **20 URLs, all reachable.**

5. **CANON DIFFS:** none (🟡 earned by scope: validator behavior + new subsystems).

6. **APPLICATION:**
   - **Dependency gate:** refuses to run unless v1.7.0 is present (apply 2900 first).
   - Idempotent reconciliation (leftover vehicles → `_local_backup/`) — a no-op if
     2900's APPLY ran fully.
   - Self-tests run BEFORE any file is touched; abort on failure.
   - Expected after apply: **29 checks · 27 pass · 2 warn · 0 FAIL · 9 locked / 5
     pending.** Warns unchanged: check 16 (meta-budget) + check 20.5 (no recorded
     attempts — the validator telling the truth).

7. **VERSION BUMP :** **MINOR** → v1.8.0 (new subsystems: emission tooling, online census).

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session (S004), 2026-09-13"

---

## VERIFICATION PERFORMED BEFORE DELIVERY

- Self-tests: nota 6/6 · module_scaffold 7/7 · ics_normalize 21/21 · regression
  9 locked / 5 pending / 0 failed.
- Real probes (then removed): an L3 module scaffolded → validated against the REAL
  check-18 rules; a NOTA-001 card scaffolded → `--check` clean at 48 words.
- Negative tests: over-limit card caught; missing lineage caught; "## DRILLS" now
  caught by BOTH the mirror and check 18; 3000's APPLY on a pre-2900 tree refuses
  at the gate.
- The sabotage test that exposed check 18's weakness is itself kept green in the
  self-test — the mirror remembers the flaw it found.
- Online census verified live in this sandbox: 20/20 reachable (and the offline
  default verified untouched).

## STILL OWED (unchanged)

**The rotation** (`4a98e59`) → then the `RADIATION_ICS_URL` secret → then the
calendar cron arms itself. Everything else is built.
