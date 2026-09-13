#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3600 "Autopilot Pipeline & Wayfinding" (requires 3500/v2.1.1)
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
# Gates on 3500 artifacts this zip does NOT carry (extract-at-root would overwrite carried ones)
grep -q "BUILD CUES" cue/autopilot-cues.md 2>/dev/null || die "patch 3500 not applied — apply RADIATION_PATCH_2026-09-13_3500_Cue-Renewal.zip FIRST"
[ -f 04-incubate/TICKET_001_skill-renovation.md ] || die "patch 3500 not applied (TICKET_001 missing)"
say "☢️  RADIATION patch 3600 — Autopilot Pipeline & Wayfinding (gate: 3500 ✓)"
for f in scaffolding/neurons/README.md scaffolding/neurons/sensoryneurons/TEMPLATE_intake.md \
         scaffolding/neurons/sensoryneurons/TID-2026-09-13-a_intake.md \
         scaffolding/neurons/interneurons/TEMPLATE_reasoning.md \
         scaffolding/neurons/interneurons/TID-2026-09-13-a_reasoning.md \
         scaffolding/neurons/motorneurons/TEMPLATE_orders.md \
         scaffolding/neurons/motorneurons/TID-2026-09-13-a_orders.md \
         scaffolding/core/proc_self-directive.md scaffolding/core/INDEX.md \
         docs/WAYFINDING.md docs/TOOLBOX.md docs/ROADMAP.md .gitignore scripts/status.py \
         cue/autopilot-doctrine.md Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md \
         README.md docs/SYSTEM_STATE.md CHANGELOG.md; do [ -f "$f" ] || die "payload missing: $f"; done
say "     ✓ 20 payload files"
# ── THE UNTRACK FIX (3400-F3 root cause): tracked vehicles die here, permanently ──
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rm -r --cached --ignore-unmatch --quiet \
    "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" \
    "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
    "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf" \
    "APPLY.sh" "APPLY.ps1" "PATCH_NOTES.md" || true
  say "     ✓ untracked vehicles + transport (git rm --cached) — commit to seal it; merges can never resurrect them"
fi
# vehicles on disk → _local_backup (idempotent)
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
grep -q "v2.2.0" README.md || die "version not v2.2.0"
grep -q "proc_self-directive" scaffolding/core/INDEX.md || die "scaffold not INDEX-registered"
grep -q "FORBIDDEN EDGES" scaffolding/neurons/README.md || grep -q "forbidden edges" scaffolding/neurons/README.md || die "relay law missing"
[ -f docs/WAYFINDING.md ] && [ -f docs/TOOLBOX.md ] || die "wayfinding/toolbox missing"
grep -q "APPLY.sh" .gitignore || die "transport not gitignored"
python3 scripts/status.py | head -7
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 31 checks · 30 pass · 1 warn · 0 FAIL (warn = check 16, your doctrine call)."
say "Now: commit (the untrack seals here), push. Then 3500's and 3600's SDs are yours to steer."
