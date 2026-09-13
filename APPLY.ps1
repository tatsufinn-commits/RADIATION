# APPLY.ps1 - RADIATION patch 3100 "The Deadline Engine"
# DEPENDENCY: requires patch 3000 (v1.8.0). powershell -ExecutionPolicy Bypass -File APPLY.ps1
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
if (-not (Test-Path "scripts/nota.py")) { Die "patch 3000 (v1.8.0) not applied - apply Core-Emission.zip FIRST" }
Say "RADIATION patch 3100 - The Deadline Engine (gate: 3000 OK)"
$payload = @("scripts/deadline_feed.py","scripts/ics_normalize.py","scripts/plan_term.py","scripts/validate.py",
  "Brain/short_term/plan/TERM1_DEADLINES.json",".github/workflows/ical_fetch.yml","docs/CAPABILITIES.md",
  "scripts/README.md","README.md","docs/SYSTEM_STATE.md","CHANGELOG.md","docs/shrine/LOG.md",
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "     OK 13 files"
python scripts/deadline_feed.py --self-test | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Die "engine self-test failed" }
python scripts/ics_normalize.py --self-test | Select-Object -Last 1
$vehicles = @("Brain/courses/SCHEDULE.csv","Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved=0; foreach ($f in $vehicles) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "     OK $moved leftover(s) -> _local_backup/" } else { Say "     -  already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
python scripts/deadline_feed.py --write | Select-Object -Last 4
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/validate.py 2>&1 | Select-Object -Last 2
Say "Done. Expected: 29 checks - 27 pass - 2 warn - 0 FAIL - register 26 items + 11 pending."
Say "Now: delete APPLY.sh + APPLY.ps1, commit, push - CI regenerates CALENDAR.md."
