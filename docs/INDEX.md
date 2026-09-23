# 📚 Docs Index — Diátaxis Lanes (G6)

**Purpose:** The last fail-cell G6 — newcomer one-pass, task-first lanes, link-check harness. Virtual lanes only — links, never moves. Every `docs/*.md` assigned to exactly one lane. Generated files in honest sub-lane.

**Four Diátaxis lanes:** Tutorial (learning-oriented) / How-to (task-oriented) / Reference (information-oriented) / Explanation (understanding-oriented). Plus Generated sub-lane (machine-generated, do not edit manually).

**Usage:** Newcomer starts at `START_HERE.md` → this file → lane tour.

**Register status (v3.10.33, WP-2.3):** verify cassette seeds CONSUMED (J1) · runner `scripts/verify_cassette_runner.py` live-advisory (via `verify_apply.py`, WARN-only) · cassette + seeds under `evals/verify_policies/` (outside docs/, so no lane row) · WP-2.3 row IN-FLIGHT → DELIVERED on seal (see ROADMAP.md).

---

## Tutorial (learning-oriented) — newcomer one-pass, safe environment

| Doc | Task | Audience |
|-----|------|----------|
| [WAYFINDING.md](WAYFINDING.md) | Learn repo map + routing tree where things go | Fresh AI newcomer lost |
| [COMMANDER_QUICKREF.md](COMMANDER_QUICKREF.md) | Learn magic words to boot any AI + control panel | Commander + newcomer AI |
| [SKILLS.md](SKILLS.md) | Understand nine skills (how AI thinks, not personas) | Newcomer AI learning to think |
| [MODES.md](MODES.md) | Learn six Commander-declared modes + activation matrix | Newcomer AI |
| [PROMPT_PLAYBOOK.md](PROMPT_PLAYBOOK.md) | Learn copy-paste prompt patterns by mode/task scenario | Commander learning to prompt |
| [ACTIVATION_PASS_EXERCISE_5830.md](ACTIVATION_PASS_EXERCISE_5830.md) | Run PASS handoff exercise 5830 to verify activation | Newcomer verifying host posture |
| [DEPTH_LADDER.md](DEPTH_LADDER.md) | Learn levels 1-5 objective completion criteria | Newcomer AI earning depth |

## How-to (task-oriented) — goal-driven, steps to solve specific problem

| Doc | Task | Audience |
|-----|------|----------|
| [PATCH_PROTOCOL.md](PATCH_PROTOCOL.md) | Emit a Patch correctly per II.7 workflow | Architect AI evolving system |
| [TOOLBOX.md](TOOLBOX.md) | Find OSS rescue tool to unblock stuck task (ocrmypdf, ics_normalize) | AI with image-only PDFs/tables/calendar |
| [CUE_SYSTEM.md](CUE_SYSTEM.md) | Run five-phase autonomous intent-reading scan before any work | AI on every Commander prompt |
| [CONTROL_PLANE.md](CONTROL_PLANE.md) | Route work through control plane with strict task-ID grammar + receipts | AI executing tasks needing policy flow |
| [COURSE_CORPUS_POLICY.md](COURSE_CORPUS_POLICY.md) | Declare new course corpus asset via hash-bound manifest (5300 E1) | AI adding Brain/courses assets |
| [OPEN_SOURCES.md](OPEN_SOURCES.md) | Find external source catalog entry to pull via @Fetch | AI doing research |
| [PENDING_RATIFICATIONS.md](PENDING_RATIFICATIONS.md) | Track unratified 🟠 items awaiting Commander ratification line | Architect + Commander |
| [KNOWLEDGE_REGISTRY.md](KNOWLEDGE_REGISTRY.md) | Register knowledge object provenance lifecycle conflicts consumers | AI tracking knowledge |
| [PATCH_SELF_CERTIFICATION_MANIFEST.md](PATCH_SELF_CERTIFICATION_MANIFEST.md) | Self-certify Patch via six checkboxes ✅/❌ + teeth RETURNED not queued per 1.1 | Architect + Commander |

## Reference (information-oriented) — technical descriptions, facts, registers

| Doc | Task | Audience |
|-----|------|----------|
| [AI_RULES.md](AI_RULES.md) | Read supreme laws (constitution) Book.Law citation format | Every AI + Commander |
| [ANTI_PATTERNS.md](ANTI_PATTERNS.md) | Lookup documented failures + machine-checkable cures | Architect avoiding repeats |
| [ARCHIVE_NOTES.md](ARCHIVE_NOTES.md) | Lookup exempt historical paths for validator checks 1,8,9,14 | Validator + Architect |
| [BOOT_BUDGET_WAIVERS.md](BOOT_BUDGET_WAIVERS.md) | Check boot-byte waiver status (II.9 remove-to-add) | Architect checking cap breaches |
| [CAP_RECORD_POLICY.md](CAP_RECORD_POLICY.md) | Lookup CAP record content rules (C-4, 4900) executed by cap_verify | AI writing cap records |
| [DECISION_AUTHORITY.md](DECISION_AUTHORITY.md) | Lookup three decision classes + action map + challenge protocol | Commander + Architect |
| [EVIDENCE_TAXONOMY.md](EVIDENCE_TAXONOMY.md) | Lookup six evidence grades [D][O][I][R][N][S] + half-life | AI grading evidence |
| [PATCH_LEDGER.md](PATCH_LEDGER.md) | Lookup Patch history + verdicts append-only | Commander + Architect |
| [DECAY_REGISTER.md](DECAY_REGISTER.md) | Lookup claims past verification half-life awaiting re-verification | AI maintaining evidence |
| [STOCKPILE_DOCTRINE.md](STOCKPILE_DOCTRINE.md) | Lookup source intake quotas + dossier limits | AI scouting |
| [SOURCE_QUALIFICATION.md](SOURCE_QUALIFICATION.md) | Understand qualification ≠ verification doctrine — source can be authentic yet fail claim-fit; identity·integrity·authority·context·claim-fit vocabulary | AI qualifying sources |
| [DECKS.md](DECKS.md) | Understand deck is Nota answer format not product — outline is receipt, theme-lock doctrine, budgets-as-rules | AI building decks |
| [WARN_LEDGER.md](WARN_LEDGER.md) | Lookup accepted WARN census dispositions (11.6/15/16 chartered) | Validator + Architect |
| [GLOSSARY.md](GLOSSARY.md) | Lookup canon glossary term+definition+Avoid per 1.3 pure-additive | Every AI + Commander |

## Explanation (understanding-oriented) — deeper context, why

| Doc | Task | Audience |
|-----|------|----------|
| [AUDIT_2026-09-13.md](AUDIT_2026-09-13.md) | Understand 2026-09-13 audit findings + method + extension census | Architect + Commander reviewing history |
| [ECOSYSTEM.md](ECOSYSTEM.md) | Understand four repos contracts boundary laws interfaces | Architect understanding ecosystem |
| [PROVIDER_SURFACE_ANALYSIS_5830.md](PROVIDER_SURFACE_ANALYSIS_5830.md) | Understand five-provider decision-ready study (Capability/Safety/Operational/Activation) | Commander + Architect choosing provider |
| [REPLICA_DECISION.md](REPLICA_DECISION.md) | Understand 12-pair replica tranche open governed exception awaiting ruling | Commander reviewing replica decision |
| [ROADMAP.md](ROADMAP.md) | Understand what's next + shipped history (verified against live tree) | Commander never asking what's next |
| [TAXONOMY_MAPPING.md](TAXONOMY_MAPPING.md) | Understand RADIATION↔TAMAKEE evidence-vocabulary bridge (verified↔verified) | AI bridging vocabularies |
| [THREAT_MODEL.md](THREAT_MODEL.md) | Understand control plane + CAP layer threat model + cooperative limits | Architect + security reviewer |
| [YIELD_RANKING.md](YIELD_RANKING.md) | Understand four axes weighted exam-yield ranking (Frequency/Breadth/Error/Memorisation) | AI building modules by yield |
| [WP1_HANDOVER_2026-09-22.md](WP1_HANDOVER_2026-09-22.md) | Understand WP-1 handover six items + six laws D029 per §5 template referencing 1.6 checklist | Commander + Architect + Desk |

## Generated (machine-generated, honest label — do not edit manually, generated by render_docs.py)

| Doc | Task | Audience | Generator |
|-----|------|----------|-----------|
| [CAPABILITIES.md](CAPABILITIES.md) | Lookup what repo can RUN (executable half, companion to SKILLS.md) | AI + Commander | `python3 scripts/render_docs.py --apply` — GENERATED |
| [SYSTEM_STATE.md](SYSTEM_STATE.md) | Lookup current ground-truth snapshot (ONLY overwrite-permitted file II.2 exception) | AI + Commander | `python3 scripts/render_docs.py --apply` — GENERATED |

---

**Coverage:** 41 docs/*.md = 7 Tutorial + 9 How-to + 14 Reference + 9 Explanation + 2 Generated = 41. Every docs/*.md listed exactly once. No moves/renames — virtual lanes only (links, never moves). Lane assignments only, no prose rewrites of doctrine docs per G6 non-goals.
