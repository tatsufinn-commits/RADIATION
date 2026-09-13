# 🧭 WAYFINDING (`docs/WAYFINDING.md`) — the lost-AI page
**Tier-3 reference (never boots) · 🟢 docs · patch 3600.** You are a fresh AI and don't
know where things go. Start here. Law lives in `docs/AI_RULES.md`; this page is the map.

## 1. THE MAP (every top-level region, one line each)
| Region | Holds |
|---|---|
| `docs/AI_RULES.md` · `PROTOCOL.md` · `docs/MODES.md` | THE LAW + the modes. Canon: 🔴 never edit without a Commander order |
| `README.md` · `CHANGELOG.md` · `docs/SYSTEM_STATE.md` · `docs/ROADMAP.md` | what this is · what changed · where it stands · what's next |
| `Brain/` | the memory. Movement: short_term → long_term via triangulation (II.6). Map: `Brain/BRAIN_INDEX.md` |
| `09-nota/` | the Core — the emission surface. Shield-stamped cards only (I.3) |
| `01-…-08-*/` | the nine skill jurisdictions (research → overhaul). Each README = its contract |
| `cue/` | reflexes: confirmed cues, lexicon, doctrine, the directive registry |
| `scaffolding/` | work formats. `core/` mandatory for its tasks · `neurons/` = the relay records |
| `subskills/` | scout · colony · selfdirectives · compass · curator · sentinel · surgeon |
| `scripts/` | the machinery (validator, status, verify_apply, planner…). `docs/CAPABILITIES.md` = the catalog |
| `docs/shrine/` | shared judgment: LOG heartbeats + member testaments (II.9: file per conversation) |

## 2. THE ROUTING TREE — input in hand; where does it go?
1. Knowledge someone should remember? → `Brain/` (movement rules; never canon)
2. A session product (reviewer, audit, card)? → its skill jurisdiction / `09-nota`
3. A standing behavior or reflex? → `cue/` (append-only)
4. A work format? → use `scaffolding/core/`; propose refinements to `improved/`
5. New law, mode, or deletion? → **STOP — 🔴. Proposal via patch notes; the Commander decides**
6. Stuck between two readings? → `04-incubate/TICKET_*.md` + ask with a POSITION (never a menu)

## 3. SELF-LOCATION — commands that tell you where you are
`python3 scripts/status.py` (machine state, one screen) · `python3 scripts/verify_apply.py`
(did the last apply land?) · `python3 scripts/validate.py` (what's broken + its REMEDY) ·
`git log --oneline -5` (what the Commander last did) · `scaffolding/neurons/` (tasks in flight).

## 4. WHEN LOST — the recovery ladder
INDEXes (`BRAIN_INDEX`, `CORE_INDEX`, region READMEs) → this page → validator REMEDY lines →
status.py / verify_apply.py → shrine LOG (who did what last) → 04-incubate ticket → ask the
Commander with a position. Never re-acquire what the Brain already holds (II.1).
