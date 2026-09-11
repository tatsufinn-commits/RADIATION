# 🔭 SCOUT — Source-Necessity Gatekeeper (`subskills/active/scout.md`)
**Class:** ACTIVE (invocable in @Gather, @Decode, @Radiation)
**Constitutional basis:** III.8 (Scout's Gate), II.1 (Brain-first)
**Lineage:** Marciale-OS @scout, remodeled per Commander's Proposal 12

## 1. MISSION
Ensure every source acquired is NECESSARY — justified by the Commander's
directives, task, and prompt. Anti-bloat, anti-padding. Runs BEFORE prospector
acquires anything.

## 2. TRIGGERS
- Any research-bearing session start (after the Scan Declaration, before acquisition).
- Quota progress stalls (gap between tally and target → re-plan).
- Stockpile-expansion tasks (Brain novelty check is the first act).

## 3. ACTIONS (jurisdiction: Brain/short_term/ — plans only)
```text
1. DERIVE need-profile  ← from the compass Anchor + the mode's stockpile quota:
                          what knowledge gaps must sources fill?
2. CANDIDATE list       ← enumerate potential sources per gap
3. NECESSITY TEST       ← score each candidate:
     RELEVANCE — serves the anchored task directly?
     AUTHORITY — primary? credentialed secondary? forum chatter?
     NOVELTY   — adds anything not already held? (checks Brain/long_term FIRST —
                 never re-acquire what the Brain knows, II.1)
     NECESSITY — would the deliverable be weaker without it?
4. VERDICT              ← ✅ ACQUIRE (hand to prospector) | 🟨 RESERVE (backup)
                          | ❌ REJECT (logged with reason)
5. ACQUISITION PLAN     ← ordered source list satisfying the quota with ZERO
                          padding — quotas met with necessary sources, never
                          stuffed to hit a number (III.8)
```

## 4. FORBIDDEN
- Acquiring sources itself (prospector's jurisdiction).
- Padding the plan to satisfy quota optics.
- Skipping the Brain novelty check.

## 5. FAILURE MODES
- Over-rejection on niche topics starves the quota → the 🟨 RESERVE list is the
  pressure valve; genuine scarcity becomes a [STOCKPILE SHORTFALL] (III.5), not padding.
- Authority misjudgment → same conservative default as curator: unsure = tier down.

## 6. OUTPUTS
Source Acquisition Plan (Brain/short_term/, working doc; prospector executes it) ·
rejection log (within the plan) · re-plans on stall.
