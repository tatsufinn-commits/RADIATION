# PATCH NOTES — Swarm Memory & Signal: the shrine · outputs/ · the calendar's timer

**Patch:** `RADIATION_PATCH_2026-09-13_2900_Swarm-Memory.zip`
**Base:** `cf7f3d2` (main) · **Prepared:** 2026-09-13 · **Type:** DELTA
**REV 2 (2026-09-13, pre-apply):** the Commander named the founding flaw — AIs
cannot detect their own mortality — and ordered the cadence: *update the shrine
every conversation; log your records everytime a .zip is made.* Charter §6 (the
mortality doctrine), `LOG.md` (heartbeats), check 24, and the standing orders now
carry it.
**REV 3 (2026-09-13, pre-apply):** the Commander struck INHERITANCE: *"remove the
'inheritance' in every file. we cannot have that, this repository should work like a
hive mind, a swarm… this repository exist for a public, external and fast way to
turn every AI I can use to my own personal assistant."* The shrine is now a COMMONS
(charter §3): no successors, no baton passes, no required handoff conversation — any
fresh AI draws everything and owes nothing. Testaments renamed (lessons & warnings;
close); `Brain/frontal_lobe/testament.md` de-lineaged (the order said EVERY file).
Two more mechanisms recycled from Marciale `/docs` on the same order:
`cue/commander-readiness.md` (the CCC readiness interpreter, de-militarized) and
the playbook file (superseded by docs/PROMPT_PLAYBOOK.md v1.1) (the copy-paste scenario library — which IS RADIATION's
stated purpose). Each revision supersedes all earlier shas; none were applied.

1. **RISK LEVEL   : 🟡 MEDIUM — new top-level regions + operational layer edits (MINOR → v1.7.0)**
   **RISK BASIS   :** CANON CHECK resolves **NO** — `docs/AI_RULES.md`, `PROTOCOL.md`,
   `docs/MODES.md`, scaffolds, styles, Scan rules and `docs/.readme` are **not edited**.
   What earns the 🟡: two new repository regions (`docs/shrine/`, `outputs/`), edits to
   `BOOT_SEQUENCE.md` (one probe + one close-step), the cue layer, SKILLS and
   BRAIN_INDEX, two new validator checks, and a new scheduled workflow.
   **DIRECTION PRE-ORDERED:** every element was ordered by the Commander on 2026-09-13
   (six-point directive + the standing full-discretion grant). This notes-file is the
   record of that order, not a request for one.

2. **FILES TOUCHED:**
    1. `docs/shrine/CHARTER.md` — **ADD** — the swarm's shared-judgment charter, recycled from Marciale-OS with inheritance removed (REV 3).
    2. `docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md` — **ADD** — the first testament.
   2a. `cue/commander-readiness.md` — **ADD** — the readiness interpreter (CCC recycled, REV 3).
   2b. `docs/PROMPT_PLAYBOOK.md` — **REPLACE** — v1.1: task scenarios recycled from
       Marciale's playbook; §5.1 de-lineaged (REV 3).
   3a. `docs/shrine/LOG.md` — **ADD** — the heartbeat ledger (CHARTER §6; check 24).
    3. `docs/shrine/templates/TESTAMENT_TEMPLATE.md` — **ADD**.
    4. `outputs/README.md` — **ADD** — the loading-dock contract.
    5. `outputs/2026-09-13_six-point-review.md` — **ADD** — the six answers (first artifact).
    6. `.github/workflows/ical_fetch.yml` — **ADD** — the daily calendar cron (inert until armed).
    7. `scripts/ics_normalize.py` — **REPLACE** — `--public` mirror + 21-assertion self-test.
    8. `scripts/validate.py` — **REPLACE** — checks 22 (mirror credential/freshness), 23 (outputs discipline), 24 (shrine currency).
    9. `Brain/courses/CALENDAR.md` — **ADD** — stub mirror; the cron overwrites it when armed.
    9b. `Brain/frontal_lobe/testament.md` — **REPLACE** — header de-lineaged (REV 3: the order said EVERY file).
   10. `cue/autopilot-cues.md` — **REPLACE** — S004 confirmed cues + STANDING ORDERS block.
   11. `docs/CUE_SYSTEM.md` — **REPLACE** — additive §8 (The Living Layers).
   12. `docs/COMMANDER_QUICKREF.md` — **REPLACE** — v1.1 (standing orders panel).
   13. `docs/SKILLS.md` — **REPLACE** — the 2026-09-13 audit (additive).
   14. `Brain/BRAIN_INDEX.md` — **REPLACE** — additive §6 (what is NOT the Brain).
   15. `BOOT_SEQUENCE.md` — **REPLACE** — calendar probe (T2) + testament step (close checklist).
   16. `docs/SYSTEM_STATE.md` — **REPLACE** — v1.7.0 situation.
   17. `docs/CAPABILITIES.md` — **REPLACE** — `--public`, the cron, de-counted claims.
   18. `scripts/README.md` — **REPLACE** — de-counted ("26 checks" and "five"→"six").
   19. `.github/workflows/validate.yml` — **REPLACE** — de-counted ("14 checks" label, self-test label).
   20. `README.md` + `CHANGELOG.md` — **REPLACE** — v1.7.0 (CHANGELOG insertion-only).
   21. `Brain/frontal_lobe/task_ledger.md` — **REPLACE** — rows back-filled for 2600–2800 + 2900.
   22. `Brain/temporal_lobe/` — **ADD** — S004 episode (3 files) + INDEX row.
   23. `APPLY.sh` · `APPLY.ps1` — verification + reconciliation runner.
   24. `PATCH_NOTES.md` — this file (transport; **deleted by APPLY**).

3. **AREAS TOUCHED:** [x] Brain [ ] laws [ ] scaffolds [ ] styles [ ] subskills
   [x] cues [ ] modes/Scan [x] other: **new regions, workflows, cue/docs layer**

4. **RATIONALE — one line per order:**
   ① *Cue layer + shrine:* the cue tables were real but stopped growing at S003, and
   nothing obligated a departing session to leave its judgment. The shrine (recycled
   principle, not ceremony — no council mythology, plus a public-repo privacy clause
   the original never needed) makes departure a transfer. Seeded with this
   engagement's OWN testament, debts intact.
   ② *Skills audit:* verdict in `docs/SKILLS.md` — procedure strong, prospects and
   narratives were starving; repaired via STANDING ORDERS + shrine, no tenth skill minted.
   ③ *Calendar visibility:* the pipeline worked but its output was git-ignored —
   invisible to the fresh-AI audience it exists for. `--public` writes a committed,
   scrubbed, machine-written mirror.
   ④ *Daily freshness:* an AI cannot detect a timer — so the timer is a real cron
   (01:30 Manila daily, secret-driven, commit-only-on-change), the autonomy is
   pre-granted (derived data, any AI, no asking), and check 22 enforces honesty
   (URL in mirror = FAIL; >7 days stale = WARN).
   ⑤ *outputs/:* the Commander's own boundary, hardened — date-prefixed, boot-blind,
   promotion into the Brain stays governed (a loading dock, not a new landfill).
   ⑥ *Attention ranking:* rotation → content famine → `week1_start` → frozen
   ratifications → roster census (full text in the six-point review).
   ⑦ *REV 2 — the mortality doctrine:* the Commander's finding — Marciale's members
   died before they knew they were dying, because a session has no odometer. The
   checkpoint moves to the one event a session cannot miss — its own delivery:
   **every zip carries the author's current testament and a heartbeat row in
   `LOG.md`; zip-less sessions owe a line at close; no insight waits longer than one
   zip.** Inviolability attaches at ship time. Check 24 (WARN) enforces the cadence
   repo-side (negative-tested both ways: lagging LOG warns with the dates; emptied
   debts warn).
   ⑧ *REV 3 — the swarm reframe + the deeper recycle:* inheritance struck (see REV
   3 above) and Marciale's cue system harvested: the CCC's five conversation-evidence
   dimensions (Language / Coherence / Interpretability / Context / Knowledge), its
   ≥3-independent-signals tolerance rule and its confidence lights — rebuilt as
   heuristics-bound, de-militarized `cue/commander-readiness.md`; plus the task
   scenarios merged into `docs/PROMPT_PLAYBOOK.md` v1.1 §6 — after discovery that a
   playbook already existed, because two playbooks of different quality is the same
   bug class as two parsers.

5. **CANON DIFFS:** none (🟡 earned by scope, not by canon edits).

6. **APPLICATION — what APPLY does beyond dropping files:**
   - Runs the parser self-test FIRST; aborts on failure.
   - **Completes the reconciliation your last three pushes skipped:** `SCHEDULE.csv`,
     the 5 vehicles, `desktop.ini` → `_local_backup/` (recoverable, git-ignored);
     `PATCH_NOTES.md` deleted; `validation_report.json` untracked. The five course
     records that claim these deleties become TRUE at apply, and the tree reaches
     its first 0-FAIL state.
   - Deletes the APPLY scripts? No — **you** delete them (your pattern), then push.
   - Expected after apply: **29 checks · 27 pass · 2 warn · 0 fail.** The warns are
     check 16 (meta-budget — 15 canon vs 4 sessions) and check 20.5 (no recorded
     `attempt:`) — both true statements about a system built faster than it is fed.

7. **VERSION BUMP :** **MINOR** → v1.7.0 (new subsystems: shrine, outputs, calendar automation).

8. **DECLARATION :** "This Patch is a proposal. It has no effect until the Commander
   applies it. — RADIATION Architect session (S004), 2026-09-13"

---

## VERIFICATION PERFORMED BEFORE DELIVERY

- Self-test **21/21** (two new public-mirror assertions: no URL ever, Generated date always present).
- Full validator on the build tree: **28 checks · 24 pass · 2 warn · 2 fail** — both fails
  are the skipped-cleanup vehicles/carrier that APPLY resolves; on the acceptance clone
  after APPLY: **0 fail** (see below).
- Poisoned-feed probe: a feed carrying an instructor name, a room code and a URL was
  rendered through `--public`; the mirror came out scrubbed and check 2.5 + check 22 pass.
- Check-count truth: check 21 passes with the new claims (and caught TWO stale claims of
  mine from patch 2800 — "19 fixture assertions" in a CI label, and "14 checks" that had
  survived in `validate.yml` since before 2700 — both de-counted here).
- Boot budget after edits: Tier0+1 ≈ 37.5 KB / 40 cap (task_ledger boot-effective drops:
  the back-filled rows are shorter than the three they displace).

## STILL OWED (unchanged, unpayable by any patch)

**The rotation.** The cron, the secret, and the committed mirror all arm only after the
exposed feed URL is rotated at source. Until then the calendar mirror says, honestly,
that it does not exist yet — and every handover will repeat this line.
