#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 2600
# Schedule Record + Location Amendment (A1)
# Apply from the repository ROOT:   bash APPLY.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

EXPECTED="RADIATION"          # sanity: are we in the right repo?
say()  { printf '%s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

[ -f README.md ] && grep -q "RADIATION" README.md 2>/dev/null || die "run this from the RADIATION repository root"
[ -f docs/AI_RULES.md ] || die "docs/AI_RULES.md not found — wrong directory?"

say "☢️  RADIATION patch 2600 — Schedule Record + Location Amendment"
say ""

# ── 1. presence check: every file this patch writes must be in the zip ───────
say "1/6  checking payload…"
for f in \
  "Brain/courses/SCHEDULE.md" \
  "Brain/courses/INDEX.md" \
  "scripts/validate.py" \
  ".gitignore" \
  "README.md" \
  "docs/SYSTEM_STATE.md" \
  "CHANGELOG.md"
do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 7 content files present"

# ── 2. retire the superseded grid-form CSV ──────────────────────────────────
say "2/6  retiring the superseded CSV…"
if [ -f "Brain/courses/SCHEDULE.csv" ]; then
  mkdir -p _local_backup/Brain/courses
  mv "Brain/courses/SCHEDULE.csv" "_local_backup/Brain/courses/SCHEDULE.csv"
  say "     ✓ SCHEDULE.csv → _local_backup/ (git-ignored; identical data now lives in SCHEDULE.md)"
else
  say "     – SCHEDULE.csv already absent"
fi

# ── 3. untrack the generated validator report ───────────────────────────────
say "3/6  untracking generated output…"
if git ls-files --error-unmatch validation_report.json >/dev/null 2>&1; then
  git rm --cached --quiet validation_report.json
  say "     ✓ validation_report.json untracked (file kept on disk)"
else
  say "     – validation_report.json not tracked"
fi

# ── 4. verify the amendment actually landed ─────────────────────────────────
say "4/6  verifying the amendment…"
grep -q "CV_ALLOW_LOCATION" scripts/validate.py || die "amendment A1 not applied to validate.py"
grep -q "CV_DENY_OTHER"     scripts/validate.py || die "amendment A1 split not applied to validate.py"
python3 -c "import ast,sys; ast.parse(open('scripts/validate.py').read())" || die "validate.py has a syntax error"
say "     ✓ A1 present, validate.py parses"

# ── 5. the schedule record must carry rooms but no names ────────────────────
say "5/6  checking the schedule record…"
grep -q "S308" "Brain/courses/SCHEDULE.md" || die "SCHEDULE.md is missing its room codes (A1 intended them to be present)"
if grep -qiE "(Instructor|Professor|Prof\.)[^A-Za-z]*[A-Z][a-z]+" "Brain/courses/SCHEDULE.md"; then
  die "SCHEDULE.md appears to contain an instructor name — that prohibition is absolute"
fi
say "     ✓ rooms present · no personnel identifiers"

# ── 6. run the validator ────────────────────────────────────────────────────
say "6/6  running the validator…"
python3 scripts/validate.py 2>&1 | tail -4

say ""
say "Done. Expected: 25 checks · check 2.5 no longer lists SCHEDULE.csv."
say "Still failing by design until you act: the 5 vehicles + desktop.ini (2.5),"
say "and docs/PLAYBOOK_EVALFIRST_TEMPLATE_STAGED.md (check 3)."
say ""
say "⚠️  Rotation still pending: the LMS feed URL in commit 4a98e59 is live."
say "    No patch can fix that — rotate the feed at source."
