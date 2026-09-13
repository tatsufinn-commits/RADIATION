#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3200 "@SELFDIRECTIVES"
# DEPENDENCY: requires patch 3100 (v1.8.1). Apply from repo ROOT, then delete apply scripts, push.
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
[ -f scripts/deadline_feed.py ] || die "patch 3100 (v1.8.1) not applied — apply RADIATION_PATCH_2026-09-13_3100_Deadline-Engine.zip FIRST"
say "☢️  RADIATION patch 3200 — @SELFDIRECTIVES (gate: 3100 ✓)"
for f in subskills/active/selfdirectives.md subskills/SUBSKILL_INDEX.md cue/autopilot-cues.md \
         docs/COMMANDER_QUICKREF.md docs/SYSTEM_STATE.md README.md CHANGELOG.md \
         docs/shrine/LOG.md docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md docs/ROADMAP.md; do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 9 files"
moved=0
for f in "Brain/courses/SCHEDULE.csv" "Brain/courses/0_CALLENDER/ics.txt" "Brain/courses/0_CALLENDER/readme.txt" \
  "Brain/courses/desktop.ini" "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"; do
  if [ -f "$f" ]; then d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1)); fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved leftover(s) → _local_backup/" || say "     – already reconciled"
rm -f PATCH_NOTES.md
grep -q "AUTONOMY LADDER" cue/autopilot-cues.md || die "ladder missing from standing orders"
grep -qi "selfdirectives" subskills/SUBSKILL_INDEX.md || die "subskill not indexed"
grep -q "v1.9.0" README.md || die "version not v1.9.0"
grep -q "3300" docs/ROADMAP.md || die "roadmap missing"
python3 scripts/validate.py 2>&1 | tail -2
say "Done. Expected: 29 checks · 27 pass · 2 warn · 0 FAIL. Now delete apply scripts, commit, push."
