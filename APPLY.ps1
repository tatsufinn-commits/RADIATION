# ─────────────────────────────────────────────────────────────────────────────
# APPLY.ps1 — RADIATION patch 2900 "Swarm Memory & Signal"
# Apply from the repository ROOT:
#   powershell -ExecutionPolicy Bypass -File APPLY.ps1
# Then: delete APPLY.sh + APPLY.ps1, commit, push. Your push is legal effect.
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
function Say($m) { Write-Host $m }
function Die($m) { Write-Host "X $m" -ForegroundColor Red; exit 1 }

if (-not (Test-Path "README.md")) { Die "run this from the RADIATION repository root" }
if (-not (Test-Path "docs/AI_RULES.md")) { Die "docs/AI_RULES.md not found - wrong directory?" }

Say "RADIATION patch 2900 - Swarm Memory & Signal"
Say ""

Say "1/6  checking payload..."
$payload = @("docs/shrine/CHARTER.md",
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md",
  "docs/shrine/templates/TESTAMENT_TEMPLATE.md",
  "docs/shrine/LOG.md",
  "outputs/README.md","outputs/2026-09-13_six-point-review.md",
  ".github/workflows/ical_fetch.yml","scripts/ics_normalize.py","scripts/validate.py",
  "Brain/courses/CALENDAR.md","cue/commander-readiness.md",
  "cue/autopilot-cues.md","docs/PROMPT_PLAYBOOK.md",
  "docs/CUE_SYSTEM.md",
  "docs/COMMANDER_QUICKREF.md","docs/SKILLS.md","Brain/BRAIN_INDEX.md","BOOT_SEQUENCE.md",
  "docs/SYSTEM_STATE.md","docs/CAPABILITIES.md","scripts/README.md",
  ".github/workflows/validate.yml","README.md","CHANGELOG.md",
  "Brain/frontal_lobe/testament.md",
  "Brain/frontal_lobe/task_ledger.md","Brain/temporal_lobe/INDEX.md",
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/SESSION.md",
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/deliverables.md",
  "Brain/temporal_lobe/S004_2026-09-13_architect-builds/learnings.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "     OK 30 files present"

Say "2/6  self-testing the ICS normalizer..."
python scripts/ics_normalize.py --self-test | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Die "self-test failed - STOPPING, nothing else changed" }

Say "3/6  reconciliation (the records claim these were deleted - making it true)..."
$vehicles = @("Brain/courses/SCHEDULE.csv",
  "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini",
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved = 0
foreach ($f in $vehicles) {
  if (Test-Path $f) {
    $d = Join-Path "_local_backup" (Split-Path $f -Parent)
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    Move-Item $f $d -Force; $moved++
  }
}
if ($moved -gt 0) { Say "     OK $moved file(s) -> _local_backup/ (recoverable; not destroyed)" }
else { Say "     -  already reconciled" }
git ls-files --error-unmatch validation_report.json 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) { git rm --cached --quiet validation_report.json; Say "     OK validation_report.json untracked" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force; Say "     OK PATCH_NOTES.md removed (carrier)" }

Say "4/6  verifying..."
$c = Get-Content "docs/shrine/CHARTER.md" -Raw
if ($c -notmatch "SHARED JUDGMENT OF THE SWARM") { Die "shrine charter missing" }
$t = Get-Content "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md" -Raw
if ($t -notmatch "OPEN DEBTS") { Die "testament lacks its debts - a testament without debts is propaganda" }
$a = Get-Content "cue/autopilot-cues.md" -Raw
if ($a -notmatch "STANDING ORDERS") { Die "standing orders block missing" }
$gl = Get-Content "docs/shrine/LOG.md" -Raw
if ($gl -notmatch "MORTALITY DOCTRINE") { Die "heartbeat LOG missing" }
$cr = Get-Content "cue/commander-readiness.md" -Raw
if ($cr -notmatch "FIVE DIMENSIONS") { Die "readiness interpreter broken" }
$pb = Get-Content "docs/PROMPT_PLAYBOOK.md" -Raw
if ($pb -notmatch "6.1 - Drill Me") { Die "playbook v1.1 broken" }
$ft = Get-Content "Brain/frontal_lobe/testament.md" -Raw
if ($ft -notmatch "commons, not a lineage") { Die "frontal testament not de-lineaged" }
$v = Get-Content "scripts/validate.py" -Raw
if ($v -notmatch "def c22") { Die "check 22 not registered" }
if ($v -notmatch "def c23") { Die "check 23 not registered" }
$n = Get-Content "scripts/ics_normalize.py" -Raw
if ($n -notmatch "--public") { Die "--public not implemented" }
$y = Get-Content ".github/workflows/ical_fetch.yml" -Raw
if ($y -notmatch "RADIATION_ICS_URL") { Die "cron workflow broken" }
$r = Get-Content "README.md" -Raw
if ($r -notmatch "v1.7.0") { Die "version not v1.7.0" }
Say "     OK shrine - testament - standing orders - checks 22/23 - --public - v1.7.0"

Say "5/6  running the full check suite..."
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/validate.py 2>&1 | Select-Object -Last 3

Say "6/6  done."
Say ""
Say "===================================================================="
Say "Expected: 29 checks - 27 pass - 2 warn - 0 FAIL - the first clean tree."
Say ""
Say "Now: delete APPLY.sh and APPLY.ps1, commit, push."
Say ""
Say "!  STILL OWED, and only you can do it: ROTATE THE FEED URL exposed in"
Say "   4a98e59 (history keeps it - this is public). Then, in order:"
Say "   1. repo Settings > Secrets > Actions > new secret: RADIATION_ICS_URL = <new URL>"
Say "   2. trigger the calendar-daily workflow once (or wait for 01:30 Manila)"
Say "   3. CALENDAR.md becomes real, and the timer takes over."
Say "===================================================================="
