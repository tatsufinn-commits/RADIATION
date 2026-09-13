#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 3400 "Enforcement Sweep & Shrine Mandate"
# DEPENDENCY: requires 3300 (v2.0.0). Run from repo ROOT, delete apply scripts, push.
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
# Gates on artifacts this zip does NOT carry (extract-at-root overwrites carried files first)
grep -q "Applied Governance" subskills/active/selfdirectives.md 2>/dev/null || die "patch 3300 (v2.0.0) not applied — apply RADIATION_PATCH_2026-09-13_3300_Applied-Governance.zip FIRST"
[ -f docs/ROADMAP.md ] || die "patch 3200 not applied (docs/ROADMAP.md missing)"
say "☢️  RADIATION patch 3400 — Enforcement Sweep & Shrine Mandate (gate: 3300 ✓)"
for f in scripts/validate.py scripts/verify_apply.py scripts/ics_normalize.py \
         cue/standing-directives.json docs/AI_RULES.md docs/shrine/CHARTER.md docs/shrine/LOG.md \
         docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13_II.md Brain/frontal_lobe/task_ledger.md \
         Brain/courses/CALENDAR.md README.md docs/SYSTEM_STATE.md CHANGELOG.md docs/ROADMAP.md \
         docs/CAPABILITIES.md scripts/README.md docs/DECISION_AUTHORITY.md docs/AUDIT_2026-09-13.md \
         docs/PATCH_LEDGER.md .github/workflows/validate.yml; do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 20 payload files"
moved=0
for f in "Brain/courses/SCHEDULE.csv" "Brain/courses/0_CALLENDER/ics.txt" "Brain/courses/0_CALLENDER/readme.txt" \
  "Brain/courses/desktop.ini" "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"; do
  if [ -f "$f" ]; then d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1)); fi
done
[ "$moved" -gt 0 ] && say "     vehicles re-homed" 2>/dev/null || true
[ "$moved" -gt 0 ] && say "     ✓ $moved leftover vehicle(s) → _local_backup/" || say "     – vehicles already reconciled"
rm -f PATCH_NOTES.md
grep -q "v2.1.0" README.md || die "version not v2.1.0"
grep -q "II.9" docs/AI_RULES.md || die "II.9 mandate missing"
python3 -c "import json;d=json.load(open('cue/standing-directives.json'));ids=[x['id'] for x in d['directives']];assert len(ids)==11 and 'SD-GOV-011' in ids" || die "registry not at 11 / SD-GOV-011 missing"
grep -q "c26shrine" scripts/validate.py || die "check 26 missing"
python3 scripts/ics_normalize.py --self-test 2>&1 | tail -1
python3 scripts/verify_apply.py --self-test
python3 scripts/status.py | head -5
python3 scripts/verify_apply.py | head -12 || true
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 31 checks · 30 pass · 1 warn · 0 FAIL (warn = check 16 meta-budget, parked for the Commander)."
say "Now delete APPLY.sh APPLY.ps1, commit, push. The CI apply-report will watch every push after."
