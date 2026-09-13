#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 2900 "Succession & Signal"
# shrine · outputs/ · the calendar's cron · checks 22/23 · cue-layer refresh
# Apply from the repository ROOT:   bash APPLY.sh
# Then: delete APPLY.sh + APPLY.ps1, commit, push. Your push is legal effect.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
say()  { printf '%s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

[ -f README.md ] && grep -q "RADIATION" README.md 2>/dev/null || die "run this from the RADIATION repository root"
[ -f docs/AI_RULES.md ] || die "docs/AI_RULES.md not found — wrong directory?"

say "☢️  RADIATION patch 2900 — Succession & Signal"
say ""

# ── 1. payload ──────────────────────────────────────────────────────────────
say "1/6  checking payload…"
for f in \
  "docs/shrine/CHARTER.md" \
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md" \
  "docs/shrine/templates/TESTAMENT_TEMPLATE.md" \
  "docs/shrine/LOG.md" \
  "outputs/README.md" \
  "outputs/2026-09-13_six-point-review.md" \
  ".github/workflows/ical_fetch.yml" \
  "scripts/ics_normalize.py" \
  "scripts/validate.py" \
  "Brain/courses/CALENDAR.md" \
  "cue/autopilot-cues.md" \
  "docs/CUE_SYSTEM.md" \
  "docs/COMMANDER_QUICKREF.md" \
  "docs/SKILLS.md" \
  "Brain/BRAIN_INDEX.md" \
  "BOOT_SEQUENCE.md" \
  "docs/SYSTEM_STATE.md" \
  "docs/CAPABILITIES.md" \
  "scripts/README.md" \
  ".github/workflows/validate.yml" \
  "README.md" \
  "CHANGELOG.md" \
  "Brain/frontal_lobe/task_ledger.md" \
  "Brain/temporal_lobe/INDEX.md" \
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/SESSION.md" \
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/deliverables.md" \
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/learnings.md"
do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 27 files present"

# ── 2. the parser must work before anything else is touched ────────────────
say "2/6  self-testing the ICS normalizer…"
python3 scripts/ics_normalize.py --self-test | tail -1 || die "self-test failed — STOPPING, nothing else changed"

# ── 3. reconciliation your last three pushes skipped (idempotent) ──────────
say "3/6  reconciliation (the records claim these were deleted — making it true)…"
moved=0
for f in \
  "Brain/courses/SCHEDULE.csv" \
  "Brain/courses/0_CALLENDER/ics.txt" \
  "Brain/courses/0_CALLENDER/readme.txt" \
  "Brain/courses/desktop.ini" \
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"
do
  if [ -f "$f" ]; then
    d="_local_backup/$(dirname "$f")"; mkdir -p "$d"; mv "$f" "$d/"; moved=$((moved+1))
  fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved file(s) → _local_backup/ (recoverable; not destroyed)" || say "     – already reconciled"
find Brain/courses -mindepth 1 -type d -empty -delete 2>/dev/null || true
if git ls-files --error-unmatch validation_report.json >/dev/null 2>&1; then
  git rm --cached --quiet validation_report.json; say "     ✓ validation_report.json untracked"
else say "     – validation_report.json not tracked"; fi
rm -f PATCH_NOTES.md && say "     ✓ PATCH_NOTES.md removed (carrier)"

# ── 4. verify every claim the patch makes ──────────────────────────────────
say "4/6  verifying…"
grep -q "THE SUCCESSION SHRINE" docs/shrine/CHARTER.md            || die "shrine charter missing"
grep -q "OPEN DEBTS" docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md || die "testament lacks its debts — a testament without debts is propaganda"
grep -q "STANDING ORDERS" cue/autopilot-cues.md                   || die "standing orders block missing"
grep -q "MORTALITY DOCTRINE" docs/shrine/LOG.md                   || die "heartbeat LOG missing"
grep -q "def c22" scripts/validate.py                             || die "check 22 not registered"
grep -q "def c23" scripts/validate.py                             || die "check 23 not registered"
grep -q '\-\-public' scripts/ics_normalize.py                     || die "--public not implemented"
grep -q "RADIATION_ICS_URL" .github/workflows/ical_fetch.yml || die "cron workflow broken"
grep -q "v1.7.0" README.md                                        || die "version not v1.7.0"
python3 -c "import ast;ast.parse(open('scripts/validate.py').read());ast.parse(open('scripts/ics_normalize.py').read())" || die "syntax error"
say "     ✓ shrine · testament · standing orders · checks 22/23 · --public · cron · v1.7.0"

# ── 5. run everything ──────────────────────────────────────────────────────
say "5/6  running the full check suite…"
python3 scripts/knowledge_regression.py | tail -1
python3 scripts/validate.py 2>&1 | tail -3

# ── 6. close ───────────────────────────────────────────────────────────────
say "6/6  done."
say ""
say "════════════════════════════════════════════════════════════════════"
say "Expected: 29 checks · 27 pass · 2 warn · 0 FAIL — the first clean tree."
say ""
say "Now: delete APPLY.sh and APPLY.ps1, commit, push."
say ""
say "⚠️  STILL OWED, and only you can do it: ROTATE THE FEED URL exposed in"
say "    4a98e59 (history keeps it — this is public). Then, in order:"
say "    1. repo Settings → Secrets → Actions → new secret:"
say "         RADIATION_ICS_URL = <the NEW feed URL>"
say "    2. trigger .github/workflows/calendar-daily once (or wait for 01:30 Manila)"
say "    3. CALENDAR.md becomes real, and the timer takes over."
say "════════════════════════════════════════════════════════════════════"
