#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 4100 "Recalibration" (requires 4000/v2.4.1) — self-removing
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
grep -q "CARD_002" 09-nota/CORE_INDEX.md 2>/dev/null || die "patch 4000 not applied — extract RADIATION_PATCH_2026-09-13_4000_Stale-Generation.zip (and 3900 first) then re-run"
say "☢️  RADIATION patch 4100 — Recalibration (gate: 4000 ✓)"
for f in cue/autopilot-cues.md cue/commander-lexicon.md cue/inference-log.md \
         cue/autopilot-doctrine.md 04-incubate/TICKET_001_skill-renovation.md \
         tests/knowledge_assertions.json Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md \
         docs/PATCH_LEDGER.md CHANGELOG.md README.md docs/SYSTEM_STATE.md docs/ROADMAP.md; do [ -f "$f" ] || die "payload missing: $f"; done
say "     ✓ 13 payload files"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rm -r --cached --ignore-unmatch --quiet \
    "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
    "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf" \
    "APPLY.sh" "APPLY.ps1" "PATCH_NOTES.md" || true
  say "     ✓ untrack re-run — COMMIT to seal the loop permanently"
fi
moved=0
for f in "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"; do
  if [ -f "$f" ]; then d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1)); fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved vehicle(s) re-homed" || say "     – vehicles already reconciled"
rm -f PATCH_NOTES.md
grep -q "v2.4.2" README.md || die "version not v2.4.2"
python3 scripts/knowledge_regression.py 2>&1 | tail -1
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 32 checks · 31 pass · 1 warn · 0 FAIL · 11 locked. COMMIT (seal), push. Runners self-remove now."
rm -f "$0"
