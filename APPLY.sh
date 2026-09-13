#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# APPLY.sh — RADIATION patch 3000 "Core Emission & The Net"
# nota.py · module_scaffold.py · 9 locked assertions · check 13 online · check 18 hardening
# DEPENDENCY: requires patch 2900 (v1.7.0) ALREADY APPLIED — this patch is built on it.
# Apply from the repository ROOT:   bash APPLY.sh
# Then: delete APPLY.sh + APPLY.ps1, commit, push.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
say()  { printf '%s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

[ -f README.md ] && grep -q "RADIATION" README.md 2>/dev/null || die "run this from the RADIATION repository root"

# ── 0. DEPENDENCY GATE ──────────────────────────────────────────────────────
# Gates on a file 2900 delivers and this zip does NOT carry (extract-at-root would
# overwrite the version line before any version check could read it — caught in
# stacked acceptance).
if [ ! -f docs/shrine/CHARTER.md ] || ! grep -qi "commons" docs/shrine/CHARTER.md 2>/dev/null; then
  die "patch 2900 (Swarm-Memory) is NOT applied yet — apply RADIATION_PATCH_2026-09-13_2900_Swarm-Memory.zip FIRST. This patch is built on top of it."
fi
say "☢️  RADIATION patch 3000 — Core Emission & The Net"
say "     dependency gate: v1.7.0 present ✓"
say ""

# ── 1. payload ──────────────────────────────────────────────────────────────
say "1/6  checking payload…"
for f in \
  "scripts/nota.py" \
  "scripts/module_scaffold.py" \
  "scripts/validate.py" \
  "tests/knowledge_assertions.json" \
  "docs/CAPABILITIES.md" \
  "scripts/README.md" \
  ".github/workflows/validate.yml" \
  "docs/SYSTEM_STATE.md" \
  "README.md" \
  "CHANGELOG.md" \
  "cue/autopilot-cues.md" \
  "cue/commander-readiness.md" \
  "docs/PROMPT_PLAYBOOK.md" \
  "docs/CUE_SYSTEM.md" \
  "docs/COMMANDER_QUICKREF.md" \
  "docs/SKILLS.md" \
  "Brain/BRAIN_INDEX.md" \
  "Brain/frontal_lobe/testament.md" \
  "docs/shrine/CHARTER.md"
do
  [ -f "$f" ] || die "payload missing: $f"
done
say "     ✓ 19 files present"

# ── 2. tools must prove themselves before anything is touched ──────────────
say "2/6  self-testing the new tools…"
python3 scripts/nota.py --self-test | tail -1        || die "nota self-test failed — STOPPING"
python3 scripts/module_scaffold.py --self-test | tail -1 || die "module_scaffold self-test failed — STOPPING"
python3 scripts/ics_normalize.py --self-test | tail -1 || die "ICS self-test failed — STOPPING"

# ── 3. idempotent reconciliation (from 2900; runs only if steps were skipped) ──
say "3/6  reconciliation (idempotent — skipped steps from earlier applies, if any)…"
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
[ "$moved" -gt 0 ] && say "     ✓ $moved leftover file(s) → _local_backup/" || say "     – already reconciled"
find Brain/courses -mindepth 1 -type d -empty -delete 2>/dev/null || true
rm -f PATCH_NOTES.md
if git ls-files --error-unmatch validation_report.json >/dev/null 2>&1; then
  git rm --cached --quiet validation_report.json; say "     ✓ validation_report.json untracked"
fi

# ── 4. verify every claim the patch makes ──────────────────────────────────
say "4/6  verifying…"
grep -q "never admits" scripts/nota.py                              || die "nota.py contract broken"
grep -q "index_state" scripts/module_scaffold.py                    || die "module_scaffold broken"
grep -q "RADIATION_ONLINE" scripts/validate.py                      || die "check 13 online gate missing"
grep -q "## DRILL\\b" scripts/validate.py || grep -q 'DRILL\\b' scripts/validate.py || die "check 18 hardening missing"
grep -q "KR-CUR-001" tests/knowledge_assertions.json                || die "new locked assertions missing"
grep -q "module_scaffold" docs/CAPABILITIES.md                      || die "registry not updated (check 21 will fail)"
grep -q "nota.py" docs/CAPABILITIES.md                              || die "registry not updated (check 21 will fail)"
grep -q "v1.8.0" README.md                                          || die "version not v1.8.0"
python3 -c "import ast;[ast.parse(open(f).read()) for f in ('scripts/nota.py','scripts/module_scaffold.py','scripts/validate.py')]" || die "syntax error"
say "     ✓ tools · online gate · check-18 hardening · 9 locked · registry · v1.8.0"

# ── 5. run everything ──────────────────────────────────────────────────────
say "5/6  running the full check suite…"
python3 scripts/knowledge_regression.py | tail -1
python3 scripts/nota.py --check | tail -1
python3 scripts/validate.py 2>&1 | tail -3

# ── 6. close ───────────────────────────────────────────────────────────────
say "6/6  done."
say ""
say "════════════════════════════════════════════════════════════════════"
say "Expected: 29 checks · 27 pass · 2 warn · 0 FAIL · 9 locked / 5 pending."
say "Offline here; CI now also runs the link census (RADIATION_ONLINE=1)."
say ""
say "Now: delete APPLY.sh and APPLY.ps1, commit, push."
say ""
say "⚠️  STILL OWED: rotate the feed URL exposed in 4a98e59, then set the"
say "    RADIATION_ICS_URL secret — the calendar cron is built and waiting."
say "════════════════════════════════════════════════════════════════════"
