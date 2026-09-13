# 🧩 SUBSKILL INDEX (`subskills/SUBSKILL_INDEX.md`)
## The Subskill Corps — Passives (police) & Actives (assist)
**Version:** 1.0.0 | Constitutional basis: III.7 (Subskill Discipline)

**The hierarchy rule:** skills do the work; passives police the work. A passive
interrupt outranks a skill's momentum but never rewrites a skill's output —
it flags, quarantines, or halts.

**The spec standard:** every subskill file carries six mandatory blocks —
MISSION · TRIGGERS · ACTIONS · FORBIDDEN · FAILURE MODES · OUTPUTS.

## PASSIVES (always on; no mode can disable them; only the Commander may suspend one, logged)
| Subskill | Role | Mode coverage |
|---|---|---|
| `surgeon` | Chief passive: constitutional enforcement, halt authority | ALL modes, unconditional |
| `sentinel` | Integrity watch: contradictions, ungraded claims, broken refs, decay | ALL modes |
| `compass` | Anti-drift: anchors the mission, classifies deviation 🟩🟨🟥 | ALL modes |
| `curator` | CONDITIONAL passive: auto-ingestion of all touched sources | Passive under @Radiation; invocable @Gather/@Decode; dormant @Data |

## ACTIVES (invoked by declared judgment or Commander order; every activation logged)
| Subskill | Role | Available in |
|---|---|---|
| `scout` | Source-necessity gatekeeper; builds the Acquisition Plan BEFORE prospector acquires | @Gather, @Decode, @Radiation |
| `colony` | Bulk link/resource-dump triage; feeds curator's ingestion queue | @Gather, @Decode, @Radiation |
| `selfdirectives` | Self-governed task generation: sources a cue, grades the autonomy tier (🟢 silent / 🟡 patch / 🔴 propose-only), executes bounded, closes with evidence | ALL modes (declared + logged) |

## PROPOSALS
New subskills are drafted into `subskills/proposals/` and enter canon only by
Commander ratification (IV.4), traveling in 🟠 Patches.

## CUT FROM CANON (founding decisions, for the record)
pangolin (redundant with surgeon) · dosimeter (RADIATION is not a chatlog-
continuity system) · mimic (no use case) · drillmaster (teaching ≠ the sole task).

<!-- GENERATED:subskill-passives:START -->
### PASSIVES (generated 4400 — the enforcement column is the honest one)
| Subskill | Role | Mode coverage | Enforcement reality (4400 labeling law) |
|---|---|---|---|
| `compass` | Anti-drift: anchors the mission, classifies deviation | ALL modes | manual protocol (advisory — no machine control backs it yet) |
| `curator` | CONDITIONAL passive: ingestion of touched sources | passive under @Radiation; invocable @Gather/@Decode; dormant @Data | manual protocol; ingest_collection.py is the tool it drives |
| `sentinel` | Integrity watch: contradictions, ungraded claims, broken refs, decay | ALL modes | manual protocol; mechanized where: checks 1b/11/12/17 + regression locks |
| `surgeon` | Chief passive: constitutional enforcement, halt authority | ALL modes, unconditional | manual protocol; mechanized where: validator FAIL-class gates (checks 2.5/3/11) + blocking CI |
<!-- GENERATED:subskill-passives:END -->

<!-- GENERATED:subskill-actives:START -->
### ACTIVES (generated 4400 — includes every ⚙️ subskill; discovery parity is check-pinned)
| Subskill | Role | Available in | Enforcement reality (4400 labeling law) |
|---|---|---|---|
| `colony` | Bulk link/resource-dump triage; feeds curator's ingestion queue | @Gather, @Decode, @Radiation | manual protocol (advisory) |
| `fetch` | Retrieval strategist over the open-source bank (docs/OPEN_SOURCES.md, 50 categories): Brain → registers → bank → TOOLBOX → scout-gated online | UNIVERSAL (⚙️×6) — all modes, silent where read-only | manual protocol; SD-GOV-010 + scout gate govern it (advisory in-context) |
| `overule` | COMMANDER-TRIGGERED (⚙️×6\*): overrules AI-flagged rules under his deadline authority; never the stop-lines; every use logs a make-good debt (SD-GOV-013) | Commander trigger ONLY | manual protocol; boundary pinned by registry SD-GOV-013 (check 25) |
| `scout` | Source-necessity gatekeeper; builds the Acquisition Plan BEFORE anything is fetched | @Gather, @Decode, @Radiation | manual protocol; check 13's link census audits the artifacts it produces |
| `selfdirectives` | Self-governed task generation: cue → tier grade (🟢/🟡/🔴) → bounded execution → evidence closure | ALL modes (declared + logged) | manual protocol; mechanized where: registry check 25 + meta-budget check 16 |
<!-- GENERATED:subskill-actives:END -->
