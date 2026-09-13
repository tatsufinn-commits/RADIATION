#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3900 "Reflex Arc" (requires 3800/v2.3.1)
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
grep -q "CARD_001" 09-nota/CORE_INDEX.md 2>/dev/null || die "patch 3800 not applied — apply RADIATION_PATCH_2026-09-13_3800_First-Light.zip FIRST"
grep -q "CURATION GATE" scaffolding/core/proc_self-directive.md 2>/dev/null || die "patch 3700 not applied"
say "☢️  RADIATION patch 3900 — Reflex Arc (gate: 3800 ✓)"
for f in scripts/validate.py scripts/status.py 07-inspect/TABLETOP_injection_2026-09-13.md \
         scaffolding/neurons/sensoryneurons/TID-2026-09-13-d_intake.md \
         scaffolding/neurons/interneurons/TID-2026-09-13-d_reasoning.md \
         scaffolding/neurons/motorneurons/TID-2026-09-13-d_orders.md \
         Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md docs/PATCH_LEDGER.md \
         CHANGELOG.md README.md docs/SYSTEM_STATE.md docs/ROADMAP.md; do [ -f "$f" ] || die "payload missing: $f"; done
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
grep -q "v2.4.0" README.md || die "version not v2.4.0"
grep -q "c27relay" scripts/validate.py || die "check 27 missing"
[ -f 07-inspect/TABLETOP_injection_2026-09-13.md ] || die "tabletop missing"
python3 scripts/status.py | head -4
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 32 checks · 31 pass · 1 warn · 0 FAIL. COMMIT (seal), push."
