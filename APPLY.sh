#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 2800
# ICS Normalizer (the calendar reads) + reconciliation of the cleanup you
# believed was already done.
# Apply from the repository ROOT:   bash APPLY.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

say()  { printf '%s\n' "$*"; }
warn() { printf '  ⚠️  %s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

[ -f README.md ] && grep -q "RADIATION" README.md 2>/dev/null || die "run this from the RADIATION repository root"
[ -f docs/AI_RULES.md ] || die "docs/AI_RULES.md not found — wrong directory?"

say "☢️  RADIATION patch 2800 — ICS Normalizer"
say ""

# ── 1. payload ──────────────────────────────────────────────────────────────
say "1/7  checking payload…"
for f in \
  "scripts/ics_normalize.py" \
  "scripts/plan_term.py" \
  "docs/CAPABILITIES.md" \
  "scripts/README.md" \
  ".github/workflows/validate.yml" \
  "docs/SYSTEM_STATE.md" \
  "README.md" \
  "CHANGELOG.md"
do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 8 content files present"

# ── 2. the new parser must actually work before anything else is touched ────
say "2/7  self-testing the ICS normalizer (19 assertions)…"
python3 scripts/ics_normalize.py --self-test || die "the ICS normalizer failed its own self-test — STOPPING, nothing else changed"
say "     ✓ parser verified"

# ── 3. retire the superseded grid-form schedule ─────────────────────────────
say "3/7  retiring the superseded schedule CSV…"
if [ -f "Brain/courses/SCHEDULE.csv" ]; then
  mkdir -p _local_backup/Brain/courses
  mv "Brain/courses/SCHEDULE.csv" "_local_backup/Brain/courses/SCHEDULE.csv"
  say "     ✓ SCHEDULE.csv → _local_backup/ (git-ignored; the data is in SCHEDULE.md)"
else
  say "     – SCHEDULE.csv already absent"
fi

# ── 4. RECONCILIATION — you believed A–E were deleted; group D was not ──────
# The course records already STATE these were deleted ("binary deleted (II.6 r.8)",
# "vehicle removed from tree"). They were still here. That made five records false.
# They are MOVED, not deleted — _local_backup/ is git-ignored, so they stay on your
# disk and remain recoverable. Separation verified: every one was extracted first.
say "4/7  re-homing the vehicles (the records already claim they were deleted)…"
moved=0; kept=0
for f in \
  "Brain/courses/0_CALLENDER/ics.txt" \
  "Brain/courses/0_CALLENDER/readme.txt" \
  "Brain/courses/desktop.ini" \
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx" \
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx" \
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html" \
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"
do
  if [ -f "$f" ]; then
    d="_local_backup/$(dirname "$f")"
    mkdir -p "$d"
    mv "$f" "$d/"
    moved=$((moved+1))
  else
    kept=$((kept+1))
  fi
done
[ "$moved" -gt 0 ] && say "     ✓ $moved vehicle(s) → _local_backup/ (recoverable; not destroyed)" || say "     – no vehicles found"
# drop any now-empty vehicle folders
find "Brain/courses" -mindepth 1 -type d -empty -delete 2>/dev/null || true

# ── 5. untrack generated output; remove the carrier ─────────────────────────
say "5/7  untracking generated output and the carrier…"
if git ls-files --error-unmatch validation_report.json >/dev/null 2>&1; then
  git rm --cached --quiet validation_report.json
  say "     ✓ validation_report.json untracked (file kept on disk)"
else
  say "     – validation_report.json not tracked"
fi
rm -f PATCH_NOTES.md && say "     ✓ PATCH_NOTES.md removed (II.8.2 — a carrier, not a record)"

# ── 6. verify every claimed change is really in place ──────────────────────
say "6/7  verifying…"
grep -q "def expand_rrule" scripts/ics_normalize.py   || die "ics_normalize.py has no RRULE expander"
grep -q "RECURRENCE-ID" scripts/ics_normalize.py      || die "ics_normalize.py does not handle RECURRENCE-ID"
grep -q "RADIATION_ICS_URL" scripts/ics_normalize.py  || die "ics_normalize.py does not read the URL from the environment"
grep -q "ics_normalize" scripts/plan_term.py          || die "plan_term.py does not delegate to the one parser"
grep -q "ics_normalize" docs/CAPABILITIES.md          || die "CAPABILITIES.md does not document the new script (check 21 will fail)"
python3 -c "import ast;ast.parse(open('scripts/plan_term.py').read())" || die "plan_term.py has a syntax error"
say "     ✓ one parser · URL from env · plan_term delegating · registry updated"

# ── 7. run everything ──────────────────────────────────────────────────────
say "7/7  running the full check suite…"
python3 scripts/ics_normalize.py --self-test | tail -1
python3 scripts/knowledge_regression.py | tail -1
python3 scripts/validate.py 2>&1 | tail -3

say ""
say "════════════════════════════════════════════════════════════════════"
say "Done. Expected: 26 checks · 0 FAIL — the first clean tree this repo has had."
say ""
say "⚠️  ONE THING THIS PATCH CANNOT FIX, AND IT IS THE IMPORTANT ONE:"
say "    the LMS feed URL committed in 4a98e59 is STILL LIVE, and this is a"
say "    public repository. Moving ics.txt does NOT revoke it — the history keeps it."
say "    Rotate the feed at source (disable the external calendar feed, re-enable"
say "    it to mint a new URL), then put the new one in an Actions secret and a"
say "    local env var: export RADIATION_ICS_URL='https://…'   (never a file)"
say "════════════════════════════════════════════════════════════════════"
