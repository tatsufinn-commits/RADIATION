# START HERE — Newcomer One-Pass (G6)

**Purpose:** The last fail-cell G6 — no newcomer one-pass existed. This file is the ≤10 step newcomer tour. Virtual lanes only — links, never moves.

## One-Pass (≤10 numbered steps)

1. **Clone** the repo: `git clone https://github.com/tatsufinn-commits/RADIATION.git` — you are now at root. See [README.md](README.md) for magic words.

2. **Validate green:** run `python3 scripts/validate.py` — expect `42·39·3·0` 0 FAIL. See [docs/WARN_LEDGER.md](docs/WARN_LEDGER.md) for accepted WARNs.

3. **Skim protocol:** read [PROTOCOL.md](PROTOCOL.md) — mission, name, chain of activation. Then [docs/AI_RULES.md](docs/AI_RULES.md) constitution.

4. **Walk boot sequence:** read [BOOT_SEQUENCE.md](BOOT_SEQUENCE.md) — mandatory tiered load order TIER 0→3. Declare boot tier per [AGENTS.md](AGENTS.md).

5. **Layer tour via lanes:** open [docs/INDEX.md](docs/INDEX.md) — four Diátaxis lanes (Tutorial/How-to/Reference/Explanation) + Generated sub-lane. Every `docs/*.md` assigned exactly once.

6. **Tutorial lane first:** start [docs/WAYFINDING.md](docs/WAYFINDING.md) → [docs/COMMANDER_QUICKREF.md](docs/COMMANDER_QUICKREF.md) → [docs/SKILLS.md](docs/SKILLS.md) → [docs/MODES.md](docs/MODES.md) — newcomer learning path.

7. **Run PASS activation:** follow [docs/ACTIVATION_PASS_EXERCISE_5830.md](docs/ACTIVATION_PASS_EXERCISE_5830.md) — `python3 agents/_common/radiation_pass.py --host "<your host>"` — zero-write state machine.

8. **Health-check trio (one-command each):**
   - `python3 scripts/validate.py` — structural validator
   - `python3 scripts/brain_retrieve.py --cases evals/brain/retrieval_cases.json` — corpus behavior 15-match
   - `python3 scripts/docs_index_check.py` — docs lanes + link harness

9. **Next:** read [docs/ROADMAP.md](docs/ROADMAP.md) for what's next, [docs/SYSTEM_STATE.md](docs/SYSTEM_STATE.md) for ground-truth snapshot, [docs/CAPABILITIES.md](docs/CAPABILITIES.md) for executable inventory. File heartbeat per [docs/shrine/LOG.md](docs/shrine/LOG.md) II.9.

---

**Links only — no moves/renames.** All relative markdown links in this file resolve. See [docs/INDEX.md](docs/INDEX.md) for full lane assignments.
