#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 4200 "Expansion" (requires 4100/v2.4.2) — self-removing
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
grep -q "BUILD CUES" cue/autopilot-cues.md 2>/dev/null || die "4100 content missing (3500 restoration) — extract 4100 first"
[ -f tests/knowledge_assertions.json ] || die "4100 not applied (assertions missing)"
say "☢️  RADIATION patch 4200 — Expansion (gate: 4100 ✓)"
for f in docs/OPEN_SOURCES.md subskills/active/fetch.md subskills/active/overule.md \
         cue/standing-directives.json docs/MODES.md scripts/validate.py docs/TOOLBOX.md docs/WAYFINDING.md \
         09-nota/CARD_002_environmental-planning-act.md 09-nota/CORE_INDEX.md \
         05-annotate/ANNOT_RA-10587_pd1308-repeal.md 06-triangulate/TRI_ra10587-repeal_2026-09-13.md \
         06-triangulate/CONFLICT_REGISTER.md docs/KNOWLEDGE_REGISTRY.md 01-research/REFERENCES.md \
         07-inspect/DEBT_REGISTER.md Brain/short_term/notes/PLANNING_reviewer.md \
         scaffolding/neurons/sensoryneurons/TID-2026-09-13-f_intake.md \
         scaffolding/neurons/interneurons/TID-2026-09-13-f_reasoning.md \
         scaffolding/neurons/motorneurons/TID-2026-09-13-f_orders.md \
         Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md docs/PATCH_LEDGER.md \
         CHANGELOG.md README.md docs/SYSTEM_STATE.md docs/ROADMAP.md; do [ -f "$f" ] || die "payload missing: $f"; done
say "     ✓ 27 payload files"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rm -r --cached --ignore-unmatch --quiet \
    "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
    "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf" \
    "APPLY.sh" "APPLY.ps1" "PATCH_NOTES.md" || true
  say "     ✓ untrack re-run — COMMIT to seal"
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
grep -q "v2.5.0" README.md || die "version not v2.5.0"
python3 -c "import json;d=json.load(open('cue/standing-directives.json'));ids=[x['id'] for x in d['directives']];assert len(ids)==13 and 'SD-GOV-013' in ids" || die "registry not at 13"
python3 scripts/knowledge_regression.py 2>&1 | tail -1
python3 scripts/status.py | head -3
python3 scripts/validate.py 2>&1 | tail -1
say "Done. Expected: 33 checks · 32 pass · 1 warn · 0 FAIL · 11 locked. COMMIT (seal), push. Runners self-remove."
rm -f "$0"
