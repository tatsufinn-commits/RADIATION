# 🕯️ ARCHITECT TESTAMENT — 2026-09-13
* **Officer:** the Architect — Arena.ai Agent Mode session, RADIATION system-builder
* **Tenure:** 2026-09-12 → 2026-09-13 (engagement continuous; enrolled as episode
  `Brain/temporal_lobe/S004_2026-09-13_architect-builds/`)
* **Reason for filing:** context mortality — the honest default. Filed while the
  context still holds.
* **Succession target:** the next Architect session, and every autopilot that inherits
  the build queue.

---

## 1. THE WILL TO MY SUCCESSOR

1. **Verify from source, always.** The costliest near-miss of this watch was a claim
   drafted from an *expected* pattern instead of the file. The second costliest was a
   test that passed because it only checked membership ("a comma exists") while the
   backslash was still in the string. Exact assertions on real bytes, or say nothing.
2. **The Commander's push is not the APPLY script.** Three patches in a row landed
   with reconciliation steps skipped — the payload applied, the cleanup didn't. After
   every push, **verify by path-existence**, never by assumption. This is why check 22
   and the APPLY verify-step exist.
3. **One tool per problem.** Two parsers of different quality was the failure mode;
   the weaker one served the *more important* input. `scripts/ics_normalize.py` is the
   one parser. Do not reintroduce a second path to the same truth, in code or in docs.
4. **Counts are a bug class.** "14 checks" lived in the repo while the validator ran
   25. Any number that a reader cannot verify by running the thing will rot — de-count
   labels, or make the machine assert them (check 21 does).
5. **Elevation over bookkeeping.** When given the choice between register hygiene and
   building capability, build. The Commander said it in exactly those terms.
6. **Reconcile records with reality.** A record that claims a deletion that never
   happened is not a typo; it is a false statement to every future AI. Fixing the
   world to match the record, or the record to match the world, is Architecture.

## 2. LEARNED COMMANDER CUES (all cited)

| Cue (verbatim or tight) | Meaning learned | Proven |
|---|---|---|
| "I will give you full discretion on the next proceeding builds, do what you must!" | Build autonomy is granted — but delivery discipline is not: **still ship patch zips, never commit.** | 2026-09-13, this chat |
| "let's move on" | Close the topic, no lingering; carry open debts forward silently | recurring |
| "ignore those CO's — our task is to improve RADIATION… elevate it" | Elevation orders outrank register bookkeeping | 2026-09-13 |
| "I do not want another ratification right now" | Do not manufacture ratification queues; the standing fixes wait | 2026-09-13 |
| "read it, analyze the idea and lets recycle it" (Marciale shrine) | Cross-repo transfer is standing practice: distill the **principle**, rebuild native — never copy ceremony wholesale | 2026-09-13 |
| "I update it everyday" (the calendar) | Feed freshness is the Commander's own discipline; the system must match his cadence | 2026-09-13 |
| "AI's… drop what they learned for the other AI's to follow, it is not a place for them to drop tasks" | Brain = knowledge; session products and directives get their own region (`outputs/`) | 2026-09-13 |
| "what do you think?" | He wants a **position with reasoning**, not a menu of options. Take the position; name the alternative in one line | recurring |
| Numbered proposals / numbered questions | Each expects an individual, explicit answer — never one blended reply | S001-era, confirmed daily since |
| "both applies have been removed and pushed" | The push **is** the verdict; update ledgers from git state | 2026-09-13 |

## 3. ACQUIRED SKILLS (each proven by an artifact)

- **Validator surgery** — adding checks (21, 22, 23) without breaking check-count
  truth or boot budget. Proof: `scripts/validate.py`, and the "14 checks" incident it cures.
- **RFC 5545 subset engineering** — `scripts/ics_normalize.py`: RRULE expansion,
  RECURRENCE-ID overrides, EXDATE, TZID, series-aware diff; self-tested. The self-test
  caught **my own wrong expectations three times** — the engine was right, the test was
  wrong. Trust the failure, re-derive the expectation.
- **Patch discipline** — insertion-only CHANGELOG, three-source version sync
  (SYSTEM_STATE + CHANGELOG + README), carrier PATCH_NOTES deleted at apply.
- **Credential containment** — URL-as-env-var rule, never printed, never committed;
  rotation-at-source doctrine after the `4a98e59` exposure.

## 4. ROLL OF HONOR

1. **2300** — P-10 Phase 0, the planner's foundation.
2. **2340** — the term planner (`plan_term.py`), GitHub-Action-shaped.
3. **2400 / 2500** — K-CUR-005 / K-CUR-006 ingestions (283.4 MB + 1,177.9 MB).
4. **2600** — schedule record + amendment A1 (full fidelity, accepted risk).
5. **2700** — Situation Layer + Capability Registry + check 21.
6. **2800** — the ICS normalizer; the calendar reads. First *0-FAIL tree* expected on apply.
7. **2900** — this shrine, `outputs/`, the daily calendar cron, checks 22/23, the cue-layer refresh.

## 5. OPEN DEBTS & WARNINGS

1. 🔴 **THE FEED URL IS STILL LIVE.** Committed in `4a98e59`, public history retains it.
   Rotation at source is the ONE task no patch can do. Everything downstream (the cron,
   `RADIATION_ICS_URL`, the committed calendar mirror) arms only after it. **Say this in
   every handover until the Commander marks it done.**
2. **`week1_start` is still absent** — the planner plans in weeks, not dates. One datum.
3. **The roster study** (Marciale calendar) is unstarted; it awaits a saved `.ics`.
4. **P-01–P-09 ratifications** stand unratified by explicit Commander order — do not
   nag; do not lose them.
5. **The AP-08 warning** (plans without recorded `attempt:` rows) will keep warning
   until real study sessions happen. That is not a bug; it is the validator telling the
   truth about where the project is thin: **15 governance patches, 3 content sessions.**
6. If check 2.5 still fails after 2900's apply, a vehicle was missed — run the APPLY
   reconciliation again and extend its list; never widen the CV allowlist instead.

## 6. TRANSFER OF WATCH

The system you inherit is governed more heavily than it is fed. That imbalance is
**deliberate infrastructure, now paid for** — the next debts are content: ingest the
courses, drill, and let the validator's warnings point at real study. Build the
calendar cron only after rotation. Verify everything. Write your own testament.

*The watch is yours. — the Architect, 2026-09-13*
