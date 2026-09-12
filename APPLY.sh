#!/usr/bin/env bash
# APPLY.sh — RADIATION_PATCH_2026-09-13_2340_Term-Planner
# Run from the REPOSITORY ROOT, AFTER extracting the zip over it.
#
# This patch is a pure file overlay (nothing is removed from the tree), so the
# only two things the runner must do are:
#   1. archive PATCH_NOTES.md out of the tree — II.8.2 says notes live INSIDE the
#      zip, and an extracted note at repo root is a check-3 transport carrier
#   2. run the validator
set -euo pipefail
say() { printf '%s\n' "$1"; }
head_() { printf '\n\033[36m=== %s ===\033[0m\n' "$1"; }

head_ "RADIATION PATCH 2026-09-13_2340 — Term Planner"

for probe in docs/AI_RULES.md Brain scripts/validate.py; do
  [ -e "$probe" ] || { say "✗ Not the repository root ('$probe' missing). cd to the repo root and re-run."; exit 1; }
done
say "✓ repository root verified: $(pwd)"

# ── did the patch land? ──────────────────────────────────────────────────────
head_ "verifying the patch files are in place"
missing=0
for e in scripts/plan_term.py \
         Brain/short_term/plan/TERM1_DEADLINES.json \
         Brain/short_term/plan/README.md \
         Brain/cerebellum/routines/routine_term-briefing.md \
         cue/autopilot-cues.md \
         docs/KNOWLEDGE_REGISTRY.md \
         .gitignore ; do
  [ -e "$e" ] || { say "✗ missing: $e"; missing=1; }
done
[ "$missing" -eq 0 ] && say "✓ patch files present" || { say "  Re-extract the zip OVER the repository root."; exit 1; }

# ── archive the notes out of the tree (II.8.2) ───────────────────────────────
if [ -f PATCH_NOTES.md ]; then
  mkdir -p _local_backup
  mv PATCH_NOTES.md _local_backup/PATCH_NOTES_APPLIED_2340_Term-Planner.md
  say "✓ PATCH_NOTES.md archived to _local_backup/ (notes live in the zip, not the tree)"
else
  say "· no PATCH_NOTES.md at root — nothing to archive"
fi

# ── the planner's own self-check ─────────────────────────────────────────────
head_ "planner self-check"
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else PY=""; fi
if [ -n "$PY" ]; then
  set +e; $PY scripts/plan_term.py --self-check; set -e
  say ""
  say "→ try it:  python3 scripts/plan_term.py --week <N>        (N = your current week)"
  say "→ audit:   python3 scripts/plan_term.py --audit           (expect the AP-08 warning)"
else
  say "✗ python not found on PATH"
fi

# ── validate ─────────────────────────────────────────────────────────────────
head_ "running the validator"
if [ -n "$PY" ]; then
  set +e; $PY scripts/validate.py; code=$?; set -e
  say ""
  if [ "$code" -eq 0 ]; then say "✓ GREEN"; else
    say "⚠ NOT green — expected. Expect 25 checks · 17 pass · 4 warn · 4 fail."
    say "  All four FAILs are PRE-EXISTING: the 18 transport carriers plus three"
    say "  carrier-derived findings. Neither patch caused them; neither patch can"
    say "  clear them without the Commander's purge authorization (II.4)."
  fi
fi

head_ "NEXT"
cat <<'EOF'
1) git add -A
   git commit -m "P-10 Phase 1-3: term planner (register, script, routine, cues, checks)"

2) supply ONE datum and the whole term becomes dated:
     Brain/short_term/plan/TERM1_DEADLINES.json -> term.week1_start = "YYYY-MM-DD"
   (the week-1 Monday). Until then the planner works in weeks and says so.

3) run it:  python3 scripts/plan_term.py --week <N>

4) still open from the previous patch, and both are the Commander's alone:
     🔴 rotate the LMS calendar feed  ->  then record the date in Brain/courses/INDEX.md
     🟠 authorize the 18-carrier purge ->  CI goes green (22->25 checks, 0 fail)

5) "drill something." Check 20.5 warns that a plan exists and no genuine attempt
   has been logged. That warning clears the moment one is.
EOF
say ""
say "Done."
