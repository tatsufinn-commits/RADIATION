# ─────────────────────────────────────────────────────────────────────────────
# APPLY.ps1 — RADIATION patch 2800
# ICS Normalizer (the calendar reads) + reconciliation of the cleanup.
# Apply from the repository ROOT:
#   powershell -ExecutionPolicy Bypass -File APPLY.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
function Say($m) { Write-Host $m }
function Warn($m){ Write-Host "  ! $m" -ForegroundColor Yellow }
function Die($m) { Write-Host "X $m" -ForegroundColor Red; exit 1 }

if (-not (Test-Path "README.md")) { Die "run this from the RADIATION repository root" }
if (-not (Test-Path "docs/AI_RULES.md")) { Die "docs/AI_RULES.md not found - wrong directory?" }

Say "RADIATION patch 2800 - ICS Normalizer"
Say ""

# 1. payload
Say "1/7  checking payload..."
$payload = @("scripts/ics_normalize.py","scripts/plan_term.py","docs/CAPABILITIES.md",
             "scripts/README.md",".github/workflows/validate.yml","docs/SYSTEM_STATE.md",
             "README.md","CHANGELOG.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "     OK 8 content files present"

# 2. the parser must work before anything else changes
Say "2/7  self-testing the ICS normalizer (19 assertions)..."
python scripts/ics_normalize.py --self-test
if ($LASTEXITCODE -ne 0) { Die "the ICS normalizer failed its own self-test - STOPPING, nothing else changed" }
Say "     OK parser verified"

# 3. retire the superseded schedule CSV
Say "3/7  retiring the superseded schedule CSV..."
if (Test-Path "Brain/courses/SCHEDULE.csv") {
  New-Item -ItemType Directory -Force -Path "_local_backup/Brain/courses" | Out-Null
  Move-Item "Brain/courses/SCHEDULE.csv" "_local_backup/Brain/courses/SCHEDULE.csv" -Force
  Say "     OK SCHEDULE.csv -> _local_backup/ (data lives in SCHEDULE.md)"
} else { Say "     -  SCHEDULE.csv already absent" }

# 4. RECONCILIATION - you believed A-E were deleted; group D was not.
# The course records already STATE these were deleted. They were still here, which
# made five records false. MOVED, not deleted: _local_backup/ is git-ignored, so
# they stay on disk. Extraction verified complete for every one of them.
Say "4/7  re-homing the vehicles (the records already claim they were deleted)..."
$vehicles = @(
  "Brain/courses/0_CALLENDER/ics.txt",
  "Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini",
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf"
)
$moved = 0
foreach ($f in $vehicles) {
  if (Test-Path $f) {
    $d = Join-Path "_local_backup" (Split-Path $f -Parent)
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    Move-Item $f $d -Force
    $moved++
  }
}
if ($moved -gt 0) { Say "     OK $moved vehicle(s) -> _local_backup/ (recoverable; not destroyed)" }
else { Say "     -  no vehicles found" }

# 5. untrack generated output; remove the carrier
Say "5/7  untracking generated output and the carrier..."
git ls-files --error-unmatch validation_report.json 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  git rm --cached --quiet validation_report.json
  Say "     OK validation_report.json untracked (file kept on disk)"
} else { Say "     -  validation_report.json not tracked" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force; Say "     OK PATCH_NOTES.md removed" }

# 6. verify
Say "6/7  verifying..."
$n = Get-Content "scripts/ics_normalize.py" -Raw
if ($n -notmatch "def expand_rrule")   { Die "ics_normalize.py has no RRULE expander" }
if ($n -notmatch "RECURRENCE-ID")      { Die "ics_normalize.py does not handle RECURRENCE-ID" }
if ($n -notmatch "RADIATION_ICS_URL")  { Die "ics_normalize.py does not read the URL from the environment" }
$p = Get-Content "scripts/plan_term.py" -Raw
if ($p -notmatch "ics_normalize")      { Die "plan_term.py does not delegate to the one parser" }
$c = Get-Content "docs/CAPABILITIES.md" -Raw
if ($c -notmatch "ics_normalize")      { Die "CAPABILITIES.md does not document the new script (check 21 will fail)" }
python -c "import ast;ast.parse(open('scripts/plan_term.py').read())"
if ($LASTEXITCODE -ne 0) { Die "plan_term.py has a syntax error" }
Say "     OK one parser - URL from env - plan_term delegating - registry updated"

# 7. run everything
Say "7/7  running the full check suite..."
python scripts/ics_normalize.py --self-test | Select-Object -Last 1
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/validate.py 2>&1 | Select-Object -Last 3

Say ""
Say "===================================================================="
Say "Done. Expected: 26 checks - 0 FAIL - the first clean tree this repo has had."
Say ""
Say "!  ONE THING THIS PATCH CANNOT FIX, AND IT IS THE IMPORTANT ONE:"
Say "   the LMS feed URL committed in 4a98e59 is STILL LIVE, and this is a"
Say "   public repository. Moving ics.txt does NOT revoke it - history keeps it."
Say "   Rotate the feed at source, then put the new URL in an Actions secret and"
Say "   a local env var: `$env:RADIATION_ICS_URL='https://...'`  (never a file)"
Say "===================================================================="
