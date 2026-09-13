#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 3100 "The Deadline Engine"
# feed→register merge · auto-detected feed · CI mirror · check 22 feed-guard
# DEPENDENCY: requires patch 3000 (v1.8.0) already applied.
# Apply from the repository ROOT:   bash APPLY.sh
# Then: delete APPLY.sh + APPLY.ps1, commit, push.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
say()  { printf '%s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
[ -f scripts/nota.py ] || die "patch 3000 (v1.8.0) not applied — apply RADIATION_PATCH_2026-09-13_3000_Core-Emission.zip FIRST"
say "☢️  RADIATION patch 3100 — The Deadline Engine (dependency gate: 3000 ✓)"
say ""
say "1/6  payload…"
for f in scripts/deadline_feed.py scripts/ics_normalize.py scripts/plan_term.py \
         scripts/validate.py Brain/short_term/plan/TERM1_DEADLINES.json \
         .github/workflows/ical_fetch.yml docs/CAPABILITIES.md scripts/README.md \
         README.md docs/SYSTEM_STATE.md CHANGELOG.md \
         docs/shrine/LOG.md docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md; do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 13 files"
say "2/6  self-tests…"
python3 scripts/deadline_feed.py --self-test | tail -1 || die "engine self-test failed"
python3 scripts/ics_normalize.py --self-test | tail -1 || die "parser self-test failed"
say "3/6  idempotent reconciliation (clears the five-push-old leftovers)…"
moved=0
for f in "Brain/courses/SCHEDULE.csv" "Brain/courses/0_CALLENDER/ics.txt" \
  "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/desktop.ini" \
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"; do
  if [ -f "$f" ]; then d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1)); fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved leftover(s) → _local_backup/" || say "     – already reconciled"
find Brain/courses -mindepth 1 -type d -empty -delete 2>/dev/null || true
rm -f PATCH_NOTES.md
git ls-files --error-unmatch validation_report.json >/dev/null 2>&1 && { git rm --cached --quiet validation_report.json; say "     ✓ validation_report.json untracked"; } || true
say "4/6  feed merge (idempotent — safe to re-run)…"
python3 scripts/deadline_feed.py --write | tail -4
say "5/6  full suite…"
python3 scripts/knowledge_regression.py | tail -1
python3 scripts/validate.py 2>&1 | tail -2
say "6/6  done. Expected: 29 checks · 27 pass · 2 warn · 0 FAIL · register 26 items + 11 pending."
say "Now: delete APPLY.sh + APPLY.ps1, commit, push — the CI mirror regenerates CALENDAR.md."
