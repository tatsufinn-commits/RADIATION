#!/usr/bin/env bash
# APPLY.sh — RADIATION patch 4600 "Binding" (SUPERSET of 4200+4300+4400+4500)
# Seal transaction, now SELF-COMMITTING: after the gates pass, the sealed tree is
# committed automatically. PUSH remains the Commander's motor act (always).
set -euo pipefail
say(){ printf '%s\n' "$*"; }; die(){ printf '✗ %s\n' "$*" >&2; exit 1; }
[ -f README.md ] || die "run from the repository root"
grep -q "BUILD CUES" cue/autopilot-cues.md 2>/dev/null || die "4100 content missing (3500 restoration) — extract 4100 first"
[ -f tests/knowledge_assertions.json ] || die "4100 not applied (assertions missing)"
say "☢️  RADIATION patch 4600 — Binding (gate: 4100 ✓ · supersedes 4200–4500)"
P="docs/OPEN_SOURCES.md subskills/active/fetch.md subskills/active/overule.md cue/standing-directives.json docs/MODES.md docs/TOOLBOX.md docs/WAYFINDING.md \
09-nota/CARD_001_bp344-accessibility.md 09-nota/CARD_002_environmental-planning-act.md 09-nota/CORE_INDEX.md 05-annotate/ANNOT_RA-10587_pd1308-repeal.md 06-triangulate/TRI_ra10587-repeal_2026-09-13.md 06-triangulate/CONFLICT_REGISTER.md docs/KNOWLEDGE_REGISTRY.md 01-research/REFERENCES.md 07-inspect/DEBT_REGISTER.md Brain/short_term/notes/PLANNING_reviewer.md \
docs/AI_RULES.md docs/.readme docs/CAPABILITIES.md subskills/SUBSKILL_INDEX.md \
scaffolding/neurons/sensoryneurons/TID-2026-09-13-f_intake.md scaffolding/neurons/interneurons/TID-2026-09-13-f_reasoning.md scaffolding/neurons/motorneurons/TID-2026-09-13-f_orders.md \
scaffolding/neurons/sensoryneurons/TID-2026-09-14-g_intake.md scaffolding/neurons/interneurons/TID-2026-09-14-g_reasoning.md scaffolding/neurons/motorneurons/TID-2026-09-14-g_orders.md \
scaffolding/neurons/sensoryneurons/TID-2026-09-14-h_intake.md scaffolding/neurons/interneurons/TID-2026-09-14-h_reasoning.md scaffolding/neurons/motorneurons/TID-2026-09-14-h_orders.md \
scaffolding/neurons/sensoryneurons/TID-2026-09-14-i_intake.md scaffolding/neurons/interneurons/TID-2026-09-14-i_reasoning.md scaffolding/neurons/motorneurons/TID-2026-09-14-i_orders.md \
scaffolding/neurons/sensoryneurons/TID-2026-09-14-j_intake.md scaffolding/neurons/interneurons/TID-2026-09-14-j_reasoning.md scaffolding/neurons/motorneurons/TID-2026-09-14-j_orders.md \
scaffolding/neurons/_archive/README.md \
radiation_core/__init__.py radiation_core/relay.py schemas/task-envelope.schema.json schemas/plan.schema.json schemas/command.schema.json schemas/outcome.schema.json schemas/event.schema.json \
evidence/tasks/legacy_manifest.json \
evidence/tasks/TID-2026-09-14-h/task.json evidence/tasks/TID-2026-09-14-h/events.ndjson evidence/tasks/TID-2026-09-14-h/outcomes/CMD-0001.json \
evidence/tasks/TID-2026-09-14-i/task.json evidence/tasks/TID-2026-09-14-i/events.ndjson evidence/tasks/TID-2026-09-14-i/outcomes/CMD-0005.json \
evidence/tasks/TID-2026-09-14-j/task.json evidence/tasks/TID-2026-09-14-j/plan.v1.json evidence/tasks/TID-2026-09-14-j/events.ndjson evidence/tasks/TID-2026-09-14-j/projection.json evidence/tasks/TID-2026-09-14-j/commands/CMD-0001.json evidence/tasks/TID-2026-09-14-j/outcomes/CMD-0005.json evidence/tasks/TID-2026-09-14-j/artifacts/status_strict.txt \
scripts/nota.py scripts/validate.py scripts/status.py scripts/verify_apply.py scripts/grade_exam.py scripts/render_docs.py \
subskills/passive/surgeon.md subskills/passive/sentinel.md subskills/passive/compass.md subskills/passive/curator.md \
.github/workflows/validate.yml .gitignore \
Brain/frontal_lobe/task_ledger.md docs/shrine/LOG.md docs/PATCH_LEDGER.md CHANGELOG.md README.md docs/SYSTEM_STATE.md docs/ROADMAP.md"
n=0; for f in $P; do [ -f "$f" ] || die "payload missing: $f"; n=$((n+1)); done
say "     ✓ $n payload sentinels"
[ "$(ls scaffolding/neurons/_archive/TID-* 2>/dev/null | wc -l)" -eq 15 ] || die "archive incomplete (want 15 faded records)"
[ "$(ls evidence/tasks/TID-2026-09-14-j/commands/ | wc -l)" -eq 5 ] || die "TID-j bundle commands incomplete"
say "     ✓ archive (15) + canonical bundles (h, i, j) present"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rm -r --cached --ignore-unmatch --quiet \
    "Brain/courses/SCHEDULE.csv" "Brain/courses/desktop.ini" "Brain/courses/0_CALLENDER/readme.txt" "Brain/courses/0_CALLENDER/ics.txt" \
    "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf" \
    "APPLY.sh" "APPLY.ps1" "PATCH_NOTES.md" || true
  say "     ✓ untrack re-run"
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
faded=0
for pair in "sensoryneurons intake" "interneurons reasoning" "motorneurons orders"; do
  set -- $pair; stage=$1; sufx=$2
  for t in a b c d e; do f="scaffolding/neurons/$stage/TID-2026-09-13-${t}_${sufx}.md"
    [ -f "$f" ] || continue
    git rm -q --ignore-unmatch "$f" 2>/dev/null || true; rm -f "$f"; faded=$((faded+1))
  done
done
say "     ✓ relay faded: $faded duplicate record(s) (II.10.4)"
rm -f PATCH_NOTES.md APPLY.ps1   # cross-remove: THIS runner retires BOTH (F-02)
rm -f "$0"                        # unlink self BEFORE validation (c3 must not find us)
grep -q "v2.9.0" README.md || die "version not v2.9.0"
grep -q "II.10 — LEDGER COMPRESSION" docs/AI_RULES.md || die "II.10 absent"
python3 -m radiation_core.relay --self-test >/dev/null 2>&1 || die "relay self-test failed (want 11/11)"
python3 -m radiation_core.relay >/dev/null 2>&1 || die "relay semantic check failed"
python3 scripts/status.py --self-test >/dev/null 2>&1 || die "status self-test failed"
python3 scripts/nota.py --check >/dev/null 2>&1 || die "core card gate failed"
python3 scripts/knowledge_regression.py 2>&1 | tail -1
python3 scripts/validate.py 2>&1 | tail -1
say ""
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [ "${1:-}" = "--no-commit" ]; then
    say "  – auto-commit skipped (--no-commit): seal manually (git add -A && git commit)"
  else
    git add -A
    if git diff --cached --quiet; then
      say "  ✓ tree already sealed — nothing to commit"
    else
      if git commit -q -m "Seal 4600 binding patch"; then
        say "  ✓ AUTO-COMMITTED the sealed tree: $(git log --oneline -1)"
      else
        say "  ✗ commit failed (git identity/config?) — seal manually: git add -A && git commit"
      fi
    fi
  fi
fi
say "  → PUSH (the Commander's motor act): git push"
say "  → PROVE IT: fresh clone -> python3 scripts/validate.py = 34 checks · 33 pass · 1 warn · 0 FAIL"
say "    CI apply-report is BLOCKING — a red seal stops the merge."
