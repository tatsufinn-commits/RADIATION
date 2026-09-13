#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 2700 (DELTA on e76ef8c)
# Situation Layer + Capability Registry
# Apply from the repository ROOT:   bash APPLY.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

say()  { printf '%s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

[ -f README.md ] && grep -q "RADIATION" README.md 2>/dev/null || die "run this from the RADIATION repository root"
[ -f docs/AI_RULES.md ] || die "docs/AI_RULES.md not found — wrong directory?"

say "☢️  RADIATION patch 2700 — Situation Layer + Capability Registry"
say ""

# ── 1. presence check: every file this patch writes must be in the zip ───────
# 2700 is a DELTA on e76ef8c. SCHEDULE.md, INDEX.md and .gitignore already landed
# with patch 2600 and are NOT shipped again.
say "1/6  checking payload…"
for f in \
  "docs/SYSTEM_STATE.md" \
  "docs/CAPABILITIES.md" \
  "scripts/validate.py" \
  "scripts/README.md" \
  ".github/workflows/validate.yml" \
  "README.md" \
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
  say "     ✓ SCHEDULE.csv → _local_backup/ (git-ignored; identical data lives in SCHEDULE.md)"
else
  say "     – SCHEDULE.csv already absent"
fi

# ── 3. untrack generated output + the transport carrier ─────────────────────
say "3/6  untracking generated output and the carrier…"
if git ls-files --error-unmatch validation_report.json >/dev/null 2>&1; then
  git rm --cached --quiet validation_report.json
  say "     ✓ validation_report.json untracked (file kept on disk)"
else
  say "     – validation_report.json not tracked"
fi
if [ -f "PATCH_NOTES.md" ]; then
  rm -f PATCH_NOTES.md
  say "     ✓ PATCH_NOTES.md deleted (II.8.2 — it is a carrier, not a record)"
else
  say "     – PATCH_NOTES.md already absent"
fi

# ── 4. verify the Situation Layer + the registry landed ─────────────────────
say "4/6  verifying the Situation Layer and the registry…"
grep -q "THE SITUATION" docs/SYSTEM_STATE.md || die "SYSTEM_STATE.md has no Situation Layer"
grep -q "FREE" docs/SYSTEM_STATE.md || die "the schedule is not inlined in Tier 0"
grep -q "AR173-1P" docs/SYSTEM_STATE.md || die "the inline schedule is missing its courses"
grep -q "check 21\|c21()" scripts/validate.py || die "check 21 (capability drift guard) is missing"
grep -q "CV_ALLOW_LOCATION" scripts/validate.py || die "amendment A1 missing (should already be present from 2600)"
python3 -c "import ast;ast.parse(open('scripts/validate.py').read())" || die "validate.py has a syntax error"
say "     ✓ Situation Layer present · schedule inlined · check 21 armed · validate.py parses"

# ── 5. the schedule record must still carry rooms but no names ──────────────
say "5/6  checking the schedule record…"
if [ -f "Brain/courses/SCHEDULE.md" ]; then
  grep -q "S308" "Brain/courses/SCHEDULE.md" || die "SCHEDULE.md is missing its room codes (amendment A1 intended them present)"
  if grep -qiE "(Instructor|Professor|Prof\.)[^A-Za-z]*[A-Z][a-z]+" "Brain/courses/SCHEDULE.md"; then
    die "SCHEDULE.md appears to contain an instructor name — that prohibition is absolute"
  fi
  say "     ✓ rooms present · no personnel identifiers"
else
  die "Brain/courses/SCHEDULE.md is missing — apply patch 2600 first"
fi

# ── 6. run the validator ────────────────────────────────────────────────────
say "6/6  running the validator…"
python3 scripts/validate.py 2>&1 | tail -4

say ""
say "Done. Expected: 26 checks · exactly ONE fail — check 2.5."
say "That last fail is yours to clear: delete the 5 vehicles + desktop.ini"
say "under Brain/courses/ (extraction verified complete — the course records"
say "already state they were deleted, so removing them makes the records true)."
say "Do that and the tree reaches 0 FAIL for the first time."
say ""
say "⚠️  Rotation still pending: the LMS feed URL in commit 4a98e59 is live."
say "    No patch can fix that — rotate the feed at source."
