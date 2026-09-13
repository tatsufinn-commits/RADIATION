# 🎖️ COMMANDER QUICK REFERENCE (`docs/COMMANDER_QUICKREF.md`)
## Your one-page control panel. For the Commander's eyes — AIs read it to learn how they will be commanded.
**Version:** 1.1 (2026-09-13 — standing orders panel added; verdict flow updated)

## 1. THE MAGIC WORDS (boot any AI)
```text
Read this repository, and act as per .readme
Repository: https://github.com/tatsufinn-commits/RADIATION.git
```

## 2. MODE SUMMARY
| Mode | Says to the AI | Sources listed? | Concludes? |
|---|---|:---:|:---:|
| `@Radiation` | "Full rigor, permanent record" | ✅ + grades | ✅ Core cards |
| `@Data` | "Quick answers, verified" | ❌ (verified silently) | ✅ answers only |
| `@Gather` | "Stockpile knowledge, 10+18 min" | ✅ full list | ❌ never |
| `@Decode` | "Understand this repository" | ✅ full list | ❌ never |
| `@Review` | "answer from what we KNOW; fetch only gaps" | in refresh report | yes |
| `@Autopilot` | "handle it end-to-end; read my cues" | per leg | per leg |

**Full invocation:** `@[MODE] | STYLE: [name or AUTO] | TOPIC: [task]`
**Minimal:** just give the task — the Autonomous Scan infers (asking when unsure).

## 3. FORCING & OVERRIDING
- **Force a mode:** declare it explicitly — declaration outranks all inference (III.2).
- **Override a Scan mid-flight:** say what was misread → Misread Recovery (III.9): halt, re-scan, salvage triage, lexicon entry.
- **Veto at the Declaration:** the Scan Declaration always precedes work. Silence = proceed; correction = immediate override.
- **Emergency override of anything:** you outrank the Constitution (IV.1). Say the word.

## 4. PATCHES — HOW THE SYSTEM EVOLVES
1. A session hands you a Patch zip with `PATCH_NOTES.md` inside (risk-flagged 🟢/🟡/🔴).
2. Extract at repo root → run `APPLY.sh` (or `.ps1`) → commit → push. **Your push is legal effect.**
3. A one-line verdict is welcome but optional: `Patch [N]: APPLIED` / `PARTIAL — kept: …` / `REJECTED — reason`. Sessions reconcile from git state either way — but if you skip APPLY steps, say so: patches have landed with cleanup skipped, and the validator only caught it late. The APPLY script's printed verification is the truth.

## 5. STANDING ORDERS (2026-09-13 — in force until you revoke them)
| Order | What every AI does with it |
|---|---|
| "Full discretion on the next proceeding builds — do what you must" | Build without per-step approval. Still deliver as patch zips; never commit directly. |
| "I do not want another ratification right now" | No new ratification queues; P-01–P-09 stay frozen and listed, unloved. |
| The calendar | Any AI may regenerate calendar artifacts at any time — derived data, pre-authorized. The feed URL never enters a file, chat, or log. Rotation before arming still stands. |
| "Elevate it" | Capability over bookkeeping. Don't propose register passes when something can be BUILT. |
| "Census first" | Reconnaissance before construction on any new domain. |
| "What do you think?" | A position with reasoning is wanted — not a menu of options. |
| Unstructured work time ("work on stuff") | The session self-directs per `subskills/active/selfdirectives.md`: 🟢 read-only runs silent · 🟡 reversible work ships as zips · 🔴 canon/credentials/deletions propose-only. Everything is ledger-logged with `self:` — fully auditable. |
| The shrine cadence | "Update your shrine every single conversation." Concretely: **every zip carries the session's current testament + a heartbeat in `docs/shrine/LOG.md`.** File at delivery, not at death — an AI cannot detect its own mortality (the Marciale flaw). |

## 6. CORRECTION PHRASES THAT TEACH THE SYSTEM (enter the lexicon via II.5)
- "That should have been @[mode]" — mode misread correction
- "Wrong style — use [style]" — style correction
- "Too deep / too shallow" — DEPTH tuple correction
- "This is for the record" / "just for now" — PERMANENCE correction
- "Don't chase that — stay on task" — compass reinforcement (tangent gets parked)
- "When I say [phrase], I mean [meaning]" — direct lexicon dictation (strongest form)

## 7. WHERE THINGS LIVE
Situation: `docs/SYSTEM_STATE.md` · Capabilities: `docs/CAPABILITIES.md` · Shared
judgment: `docs/shrine/` · Prompt library: `docs/PROMPT_PLAYBOOK.md` · Your session products: `outputs/` · Brain anatomy:
`Brain/BRAIN_INDEX.md` · This file: your control panel.
