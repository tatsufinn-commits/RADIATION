#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3700 "The Curation Gate" (requires 3600/v2.2.0)
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
# Gates on 3600 artifacts this zip does NOT carry (extract-at-root overwrites carried ones)
[ -f docs/WAYFINDING.md ] || die "patch 3600 not applied — apply RADIATION_PATCH_2026-09-13_3600_Autopilot-Pipeline-and-Wayfinding.zip FIRST"
[ -f scaffolding/neurons/README.md ] || die "patch 3600 not applied (neuron relay missing)"
say "☢️  RADIATION patch 3700 — The Curation Gate (gate: 3600 ✓)"
for f in scaffolding/core/proc_self-directive.md scaffolding/core/INDEX.md cue/standing-directives.json \
         cue/autopilot-doctrine.md .gitignore Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md \
         docs/PATCH_LEDGER.md CHANGELOG.md README.md docs/SYSTEM_STATE.md docs/ROADMAP.md \
         scaffolding/neurons/sensoryneurons/TID-2026-09-13-b_intake.md \
         scaffolding/neurons/interneurons/TID-2026-09-13-b_reasoning.md \
         scaffolding/neurons/motorneurons/TID-2026-09-13-b_orders.md; do [ -f "$f" ] || die "payload missing: $f"; done
say "     ✓ 15 payload files"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rm -r --cached --ignore-unmatch --quiet \
    "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
    "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf" \
    "APPLY.sh" "APPLY.ps1" "PATCH_NOTES.md" || true
  say "     ✓ untracked vehicles + transport — NOW COMMIT to seal the loop permanently"
fi
moved=0
for f in "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"; do
  if [ -f "$f" ]; then d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1)); fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved vehicle(s) re-homed → _local_backup/" || say "     – vehicles already reconciled"
rm -f PATCH_NOTES.md
grep -q "v2.3.0" README.md || die "version not v2.3.0"
grep -q "CURATION GATE" scaffolding/core/proc_self-directive.md || die "scaffold not v1.1"
python3 -c "import json;d=json.load(open('cue/standing-directives.json'));ids=[x['id'] for x in d['directives']];assert len(ids)==12 and 'SD-GOV-012' in ids" || die "registry not at 12"
grep -qi "compression ladder" cue/autopilot-doctrine.md || die "doctrine ladder note missing"
grep -q "Brain/courses/SCHEDULE.csv" .gitignore || die "gitignore seal missing"
python3 scripts/status.py | head -5
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 31 checks · 30 pass · 1 warn · 0 FAIL. Now COMMIT (seals the untrack), push."
