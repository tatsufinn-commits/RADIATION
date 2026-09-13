# APPLY.ps1 - RADIATION patch 3200 "@SELFDIRECTIVES"  (requires 3100; then delete apply scripts, push)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "scripts/deadline_feed.py")) { Die "patch 3100 not applied - apply Deadline-Engine.zip FIRST" }
$payload = @("subskills/active/selfdirectives.md","subskills/SUBSKILL_INDEX.md","cue/autopilot-cues.md",
  "docs/COMMANDER_QUICKREF.md","docs/SYSTEM_STATE.md","README.md","CHANGELOG.md","docs/shrine/LOG.md",
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md","docs/ROADMAP.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
$vehicles = @("Brain/courses/SCHEDULE.csv","Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved=0; foreach ($f in $vehicles) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved leftover(s) -> _local_backup/" } else { Say "-  already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$a = Get-Content "cue/autopilot-cues.md" -Raw; if ($a -notmatch "AUTONOMY LADDER") { Die "ladder missing" }
$i = Get-Content "subskills/SUBSKILL_INDEX.md" -Raw; if ($i -notmatch "selfdirectives") { Die "not indexed" }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v1\.9\.0") { Die "version not v1.9.0" }
python scripts/validate.py 2>&1 | Select-Object -Last 2
Say "Done. Expected: 29 checks - 27 pass - 2 warn - 0 FAIL."
