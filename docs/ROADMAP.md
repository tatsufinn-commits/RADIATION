# 🗺️ RADIATION ROADMAP — 2026-09-13
**Verified against:** live tree @ `cb5ec95` (v1.8.0) at build; 3100+3200 deliver v1.9.0 · **Prepared by:** the Architect (S004)
**Purpose:** the Commander never has to ask "what's next." This file is regenerated
with every patch; stale roadmaps are deleted, not archived. Masters live in-repo
(shipped with patch 3100) so any AI in the swarm reads the same plan.

---

## 0 · WHERE THINGS STAND (verified, not assumed)

| Thing | State |
|---|---|
| Constitution, modes, skills, passives | ✅ live since founding |
| Schedule record (A1 full fidelity) · Situation Layer · Capability Registry | ✅ live (2600–2700) |
| Calendar pipeline (`ics_normalize.py`: RRULE, overrides, EXDATE, series diff) | ✅ live (2800) |
| Shrine (commons), `outputs/`, cue layer + readiness + playbook v1.1 | ✅ live (2900, `bbb067c`) |
| Core tooling (`nota.py`), module mirror, 9/14 locked assertions, check 13 online | ✅ live (3000, `fdf3a15`) |
| **Validator verdict on the LIVE tree** | **29 checks · 25 pass · 2 warn · 2 FAIL** |
| Feed + mirror + deadline engine | ✅ live after 3100 — the Commander's push is the timer |
| `week1_start` | 🟡 INFERRED (2026-08-24, from Coursera W1) — one Commander word ratifies |
| LMS feed census | ✅ DONE (2026-09-13) — deadline feed; 11 items pending Commander attribution |
| P-01–P-09 ratifications | 🧊 frozen by Commander order — listed, not lost |

**The 2 FAILs (every push, five for five):** tracked vehicles (`SCHEDULE.csv`,
`desktop.ini`, `ics.txt`, both syllabi, the MEC30-7 HTML, the AR173 PDF) +
`PATCH_NOTES.md`. The APPLY script clears these — its step 3 has never reached git.

## 1 · THE PATTERN, NAMED — and its engineering answer

Every apply so far: payload committed, reconciliation skipped. The fix is not a
reminder; it is three mechanisms (one exists, two are queued):

1. **Idempotent APPLY** — ✅ exists. Re-running `APPLY.sh` from the 3000 zip is safe
   and clears everything left over. This is Phase 1, Step 1.
2. **verify_apply.py (planned, not yet built)** — 🔜 patch 3100. Read-only: reports exactly what is
   missing from the tree versus the clean state, with the fix for each line. The
   Commander's clueless-killer: one command, honest answer.
3. **Actionable validator messages** — 🔜 patch 3100. Check 2.5/3 failures will print
   the remedy ("run APPLY.sh from your last patch, or move these to `_local_backup/`
   and `git rm --cached`") instead of only naming paths.

**Correction of record:** the Architect previously reported that the 2900 push had
run APPLY in full. False — drafted from an acceptance clone, not the live tree.
This roadmap's rule was born from that error: **live state is verified from git,
never from a sandbox.**

## 2 · PHASE 1 — COMMANDER QUEUE (~15 minutes, only you can do these)

**Step 1 — clear the 2 FAILs (2 min).**
From the folder where you extracted the 3000 zip (or re-extract into the repo root):
```bash
bash APPLY.sh          # idempotent — safe even though the payload already landed
```
Then delete `APPLY.sh` + `APPLY.ps1`, commit, push.
**Done when:** validator says `29 checks · 27 pass · 2 warn · 0 FAIL` — the first
real clean tree in repo history.

**Step 2 — ~~rotate the credential~~ → WITHDRAWN by Commander order (2026-09-13).**
The Commander accepted the exposure ("it's fine even if people see it") and plans to
private the repository at final version. Noted once: privating breaks the *public*
link+magic-words boot — RADIATION's front door is its publicness — his call, recorded,
not re-raised. The cron/secret path (old Step 3) is superseded by the commit-driven
feed below.

**Step 3 — ~~arm the calendar via secret~~ → SUPERSEDED: the feed is a committed file.**
The Commander supplies the LMS export at `sources/lms/TERM1_FEED.ics` (45.6 KB,
2026-09-13). Update flow = he re-exports + pushes; CI regenerates `CALENDAR.md` from
the committed feed (patch 3100 wires it). No credential lives anywhere.

**Step 4 — one sentence: `week1_start`.**
Tell any AI "week 1 starts <date>" — it lands in the SYSTEM_STATE and every plan
becomes dated instead of week-numbered.

**Step 5 — the .ics feed → IN PROGRESS via the repository itself.**
Drop at `sources/lms/TERM1_FEED.ics`, commit, push. The Architect then runs the
strict census + `SCHEDULE.md` cross-check from git (no chat attachment needed —
the repo is the delivery vehicle).

**Parked (your order, no nagging):** drills/study/`attempt:` rows — the AP-08 and
meta-budget WARNs stay honestly lit until then. Zero build items behind them.

## 3 · PHASE 2 — ARCHITECT QUEUE (builds proceed under standing discretion)

| Patch | Name | Contents | Unblocks |
|---|---|---|---|
| **3100** | ✅ DELIVERED — The Deadline Engine | **deadline ingestion: map the 47 feed items → courses (content-based), filter 21 stale, merge into `TERM1_DEADLINES.json`, write `week1_start=2026-08-24` (flagged inferred)** · `ics_normalize.py` auto-detects `Brain/courses/0_CALLENDER/TERM1_FEED.txt` · CI regenerates `CALENDAR.md` from the committed feed · staleness guard (check 22 upgrade) | The planner finally eats live data; the three deadline-blind courses get dates |
| **3200** | ✅ DELIVERED — @SELFDIRECTIVES (Commander-proposed; UNIVERSAL — all modes; ladder + stop-lines) | `verify_apply.py` · check 2.5 non-`.md` fix · actionable FAIL messages · the persona squad was REJECTED (anti-swarm) · this file ships with 3200 | The skip-pattern dies; autonomy is bounded and coded |
| **3200** | Swarm Dashboard | status.py (planned, not yet built) — one screen: validator verdict · calendar staleness · shrine LOG lag · ledger tail · boot budget · open debts (validator WARNs included) | You, or any fresh AI, know the whole machine's state in one command |
| **3300** | ✅ DELIVERED — Applied Governance: the Commander's memo applied (spec v2.0, directive registry + check 25, status.py, FAIL remedies) | the swarm self-governs inside a machine-checked envelope |
| **3400** | ✅ DELIVERED — Enforcement Sweep & Shrine Mandate | `verify_apply.py` + CI non-blocking apply-report · check 2.5 GENERIC (skip-pattern dead) · **AI_RULES II.9** shrine mandate + check 26 · 3200 payload omission healed (ics_normalize) | apply state is auditable; the shrine files itself into law |
| **3600** | ✅ DELIVERED — Autopilot Pipeline & Wayfinding | neuron relay (research-applied closed loop; five forbidden edges; terminal states) + `proc_self-directive.md` (Commander-ordered scaffold) + WAYFINDING + TOOLBOX + the untrack fix + status.py pipeline line | tasks inspectable at stage granularity; the lost find their way; the rescue kit is graded |
| **3700** | ✅ DELIVERED — The Curation Gate | proc_self-directive v1.1 (research-applied) + SD-GOV-012 + the compression ladder + vehicle-seal gitignore | the swarm proposes; ratification or second-session use promotes — with field numbers to prove why |
| **3800** | ✅ DELIVERED — First Light (content, not machinery) | CARD_001 admitted via the full gauntlet · 02-analyze cured · SD-3600-02 closed | the system's final product EXISTS — the Core radiates |
| **3900** | ✅ DELIVERED — Reflex Arc | check 27 (chain integrity, 32 checks) + injection TABLETOP (live drill proposed, ask-gated) + Phase-0 closed (4 chains, verdict filed) | the relay is enforceable; the injection surface has a rehearsed defense |
| **4000** | ✅ DELIVERED — Stale Generation (content) | CARD_002 (RA 10587 ⇄ PD 1308) · K-LAW-009/014 corrected · CONFLICT row 3 · reviewer ⚑ note · queue sweep | the registers no longer carry a repealed law as current — and the Core's second card is the proof |
| **4100** | ✅ DELIVERED — Recalibration | Commander's task-selection correction encoded (doctrine §2 priority) + 3500 payload REMEDIATED (was never extracted) + regression locks KR-LAW-014/009S + APPLY self-removal | open-ended proceeds mean capability work; the cue lessons finally live in the repo |
| **4200** | ✅ DELIVERED — Expansion (Commander proposals) | OPEN_SOURCES bank · @Fetch (universal strategist) · @Overule (Commander-triggered deadline gear + SD-GOV-013) · autonomous-invocation semantics · universal row restored + check 28 · 4000 content remediated | any AI can pull from the bank; deadlines get a lawful fast gear; canon can't silently evaporate |
| **4300** | ✅ DELIVERED — Compression (Commander-ordered tier-1) | II.10 Ledger Compression law (P-09 stays frozen) · SYSTEM_STATE recital → CHANGELOG + truth-up · Architect-voice purge · TID fade a–e → _archive · check 15 II.10 gauge · supersedes 4200 (superset — applies alone on v2.4.2) | 2026-09-14 |
| **4400** | ✅ DELIVERED — Reconciliation (due-diligence remediation) | Milestones A–C: seal transaction · Core gate on canonical cards (check 29) · semantic relay bundles (radiation_core) · generated facts + CI drift gate · structured validator API · clock fixes · Milestone D (agent runtime) STAGED for Product-2 scope ratification | 2026-09-14 |
| **4500** | ✅ DELIVERED — Last Mile (4400 recheck remediated) | relay: schemas executed + identity/projection/causation bindings (6/6 vectors incl. recheck mutations) · generated-truth phrase lint (9 stale claims eradicated) · degraded-mode loud + strict-refused · apply-report BLOCKING · II.10.6 closed legacy list | 2026-09-14 |
| **4600** | ✅ DELIVERED — Binding (4500 recheck remediated) | relay fully bound (recursive schemas · total identity · foreign-plan hard-fail · vectors 7–11) · planner/CI facts generated · lint expanded · seal auto-commit (push = Commander's) | 2026-09-14 |
| **4700** | ✅ DELIVERED — Sealwright (4600 recheck remediated) | bundle=record/neurons=render (file==render, vector 12) · seal exit-codes REQUIRED · planner block parsed from plan_term · identity sentence adopted · v3.0.0 | 2026-09-14 |
| **4800** | ✅ DELIVERED — Attest (research Phase C-1, verification-only) | cap_record schema EXECUTED + cap_verify (check 35 CI) · payload-completeness probe · opinions.md restored from caa754b · TID-l + first dogfooded CAP record · v3.1.0 | 2026-09-15 |
| **4900** | ✅ DELIVERED — Probe (research Phase C-2 + C-4) | cap_probe (2 tools · empty effects · containment · allowlist) · host posture profile (declarative-only) · C-4 redaction EXECUTED in cap_verify · check 36 CI · v3.2.0 | 2026-09-14 |
| **5000** | ✅ DELIVERED — FIVE THOUSAND (II.11 control plane, ratified) | two-key resolver · structural approval boundary · drafts-bounded executor · immutable receipt chain (genesis = the ratification) · check 37 CI · v3.3.0 | 2026-09-14 |
| **5100** | ✅ DELIVERED — Truebound (excellence review implemented) | escape+forgery repros fail closed · claims=mechanism (THREAT_MODEL.md) · check 35 enumerates records · check 36 coherence · boot budget under cap · v3.3.1 | 2026-09-14 |
| **3500+** | reserved — candidates from the 3400 audit | pending-item attribution UX · plan_term snapshot · APPLY self-removal (runners die at end of run) · payload-completeness probe (APPLY runs every shipped tool's self-test) · meta-budget rebalance (check 16 is OVER — needs a Commander doctrine call) · drill-fixtures disposition ("no drills" ruling vs nota/export_anki fixtures) | his pick |


**Cadence (proposed default):** you apply patch N + clear your queue → I verify the
live tree from git → I build N+100. One patch in flight at a time. Veto freely.

## 4 · KNOWN FLAWS & DISPOSITIONS (the honest table)

| # | Flaw | Disposition |
|---|---|---|
| 1 | Live tree 2 FAIL (leftover vehicles + carrier) | **Phase 1 Step 1** — one command |
| 2 | check 2.5 only scans `.md` — tracked non-md vehicles slip on my own drafts | **patch 3100** |
| 3 | Apply-skip pattern (5/5) | engineering: idempotent APPLY ✅ + `verify_apply.py` + message UX (3100) |
| 4 | Architect's false "0 FAIL live" claim (2026-09-13) | retracted; recorded here; standing rule: verify from git |
| 5 | WARN 16 meta-budget (governance ≫ content) | TRUE by design; content is Commander-deprioritized; the warning stays |
| 6 | WARN 20.5 (no recorded `attempt:`) | TRUE; clears the day real study happens |
| 7 | Old feed URL in git history | **ACCEPTED by Commander order** (2026-09-13: "it's fine even if people see it"; private-at-final-version planned) — closed as a blocker; privating caveat recorded (public boot breaks) |
| 8 | Roadmap rot | this file is regenerated every patch; stale copies deleted |
| 9 | Single-maintainer risk (the Architect) | mitigated: shrine + playbook + this roadmap — any swarm AI can pick up the queue |
| 10 | Raw .ics may carry instructor names/emails (public file) | same risk class as A1 (rooms/sections) — accepted by order; ALL derived outputs (CALENDAR.md, .local.*) stay scrubbed regardless |

## 5 · STANDING RAILS (unchanged by anything above)

Ship zips, never commit · the push is legal effect · rotation before arming ·
no inheritance machinery (the swarm draws, none inherits) · feed URL only ever in
env/secret · every zip carries a shrine heartbeat · counts in files are lies unless
the machine asserts them · live state is verified, never assumed.

---
*Regenerate this file every patch. Delete stale copies. The map is not the territory —
the validator is.*
