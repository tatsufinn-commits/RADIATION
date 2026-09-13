#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3300 "Applied Governance"
# DEPENDENCY: requires patch 3200 (v1.9.0). Apply from repo ROOT, then delete apply scripts, push.
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
# Gate on a 3200 artifact this zip does NOT carry — extract-at-root overwrites the
# version line before any version grep could read it (same trap as 3000; caught in
# stacked acceptance AGAIN — the lesson repeats until it is law).
grep -q "selfdirectives (active)" docs/MODES.md 2>/dev/null || die "patch 3200 (v1.9.0) not applied — apply RADIATION_PATCH_2026-09-13_3200_Self-Directives.zip FIRST (extract at root, bash its APPLY.sh)"
say "☢️  RADIATION patch 3300 — Applied Governance (gate: 3200 ✓)"
for f in subskills/active/selfdirectives.md cue/standing-directives.json scripts/validate.py \
         scripts/status.py docs/CAPABILITIES.md scripts/README.md README.md docs/SYSTEM_STATE.md \
         CHANGELOG.md docs/ROADMAP.md Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md \
         docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md; do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 13 files"
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
python3 -c "import json;d=json.load(open('cue/standing-directives.json'));assert len(d['directives'])==10" || die "registry corrupted"
grep -q "Applied Governance" subskills/active/selfdirectives.md || die "spec not v2.0"
grep -q "v2.0.0" README.md || die "version not v2.0.0"
python3 scripts/status.py | head -6
python3 scripts/validate.py 2>&1 | tail -2
say "Done. Expected: 30 checks · 28 pass · 2 warn · 0 FAIL. Now delete apply scripts, commit, push."
