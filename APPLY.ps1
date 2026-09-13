# APPLY.ps1 - RADIATION patch 3300 "Applied Governance" (requires 3200/v1.9.0)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
$m = Get-Content "docs/MODES.md" -Raw
if ($m -notmatch "selfdirectives \(active\)") { Die "patch 3200 not applied - apply Self-Directives.zip FIRST" }
$payload = @("subskills/active/selfdirectives.md","cue/standing-directives.json","scripts/validate.py",
  "scripts/status.py","docs/CAPABILITIES.md","scripts/README.md","README.md","docs/SYSTEM_STATE.md",
  "CHANGELOG.md","docs/ROADMAP.md","Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md",
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
$vehicles = @("Brain/courses/SCHEDULE.csv","Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved=0; foreach ($f in $vehicles) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved leftover(s) -> _local_backup/" } else { Say "-  already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$s = Get-Content "subskills/active/selfdirectives.md" -Raw; if ($s -notmatch "Applied Governance") { Die "spec not v2.0" }
$r2 = Get-Content "README.md" -Raw; if ($r2 -notmatch "v2\.0\.0") { Die "version not v2.0.0" }
python scripts/status.py | Select-Object -First 6
python scripts/validate.py 2>&1 | Select-Object -Last 2
Say "Done. Expected: 30 checks - 28 pass - 2 warn - 0 FAIL. Now delete apply scripts, commit, push."
