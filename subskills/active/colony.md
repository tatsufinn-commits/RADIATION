# 🐜 COLONY — Bulk Intake Triage (`subskills/active/colony.md`)
**Class:** ACTIVE (invocable in @Gather, @Decode, @Radiation)
**Constitutional basis:** III.7 (declared activation), feeds curator per II.6
**Lineage:** Marciale-OS @colony (Scenario 24), adapted to research intake

## 1. MISSION
Triage bulk resource dumps from the Commander (multiple links/files in one
prompt) into a sorted, scored intake queue for curator and scout.

## 2. TRIGGERS
- Commander prompt contains 3+ links/artifacts → declare: "Activating colony —
  [n] resources detected."
- Commander explicitly orders a dump triage.

## 3. ACTIONS (jurisdiction: Brain/short_term/notes/ — queue docs only)
1. INVENTORY each resource: type, origin, apparent authority tier.
2. CLASSIFY against the anchored task: direct-relevance / peripheral / off-mission.
3. SCORE intake priority (direct + high authority first).
4. QUEUE: hand the ordered list to scout for necessity vetting (III.8 still
   applies — colony sorts, scout decides, curator ingests).
5. FLAG off-mission items to compass for 🟨 parking decision.

## 4. FORBIDDEN
- Ingesting (curator's jurisdiction) or vetting necessity (scout's).
- Silently dropping any Commander-provided resource — every item appears in the
  queue with a disposition, even ❌ off-mission.

## 5. FAILURE MODES
- Misclassification of niche-but-critical resources → mitigated: scout's
  necessity test re-examines everything colony ranks.

## 6. OUTPUTS
Sorted intake queue (Brain/short_term/notes/intake-queue_YYYY-MM-DD.md) with
per-item disposition · off-mission flags to compass.
