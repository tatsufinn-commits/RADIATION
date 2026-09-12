# 🎖️ COMMANDER QUICK REFERENCE (`docs/COMMANDER_QUICKREF.md`)
## Your one-page control panel. For the Commander's eyes — AIs read it to understand how they will be commanded.
**Version:** 1.0

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

| **@Review** | "answer from what we KNOW; fetch only gaps" | in refresh report | yes |
| **@Autopilot** | "handle it end-to-end; read my cues" | per leg | per leg |

**Full invocation:** `@[MODE] | STYLE: [name or AUTO] | TOPIC: [task]`
**Minimal:** just give the task — the AI runs the Autonomous Scan and infers (asking when unsure).

## 3. FORCING & OVERRIDING
- **Force a mode:** declare it explicitly — declaration outranks all inference (III.2).
- **Override a Scan mid-flight:** say what was misread ("this was meant as @Gather") — triggers Misread Recovery (III.9): halt, re-scan, salvage triage, lexicon entry.
- **Veto at the Declaration:** the Scan Declaration always precedes work. Your silence = proceed; any correction = immediate override.
- **Emergency override of anything:** you outrank the Constitution (IV.1). Say the word.

## 4. PATCH VERDICTS (how the system evolves)
After a session hands you a Patch zip:
1. Read PATCH_NOTES.md — 🟠 flag = your ratification is being requested.
2. Extract at repo root → follow application steps → commit → push. **Your push is legal effect.**
3. Next session, say: `Patch verdict for [filename]: APPLIED` (or `PARTIAL — kept: …` / `REJECTED — reason: …`). The AI updates the Patch Ledger before any new task.

## 5. CORRECTION PHRASES THAT TEACH THE SYSTEM (enter the lexicon via II.5)
- "That should have been @[mode]" — mode misread correction
- "Wrong style — use [style]" — style correction
- "Too deep / too shallow" — DEPTH tuple correction
- "This is for the record" / "just for now" — PERMANENCE correction
- "Don't chase that — stay on task" — compass reinforcement (tangent gets parked)
- "When I say [phrase], I mean [meaning]" — direct lexicon dictation (strongest form)

## 6. QUICK PLAYBOOK POINTERS
Boot: Playbook 0.1 · Self-audit: 1.3 · Quiz answers: 2.1 · Research sweep: 3.1 ·
Repo decode: 4.1 · Rate-limit handover: 5.1 · Damaged repo recovery: 5.2 · Verdict: 5.3
