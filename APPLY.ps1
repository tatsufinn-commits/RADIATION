# APPLY.ps1 - RADIATION patch 3400 "Enforcement Sweep & Shrine Mandate" (requires 3300/v2.0.0)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
$s = Get-Content "subskills/active/selfdirectives.md" -Raw
if ($s -notmatch "Applied Governance") { Die "patch 3300 (v2.0.0) not applied - apply Applied-Governance.zip FIRST" }
if (-not (Test-Path "docs/ROADMAP.md")) { Die "patch 3200 not applied (docs/ROADMAP.md missing)" }
$payload = @("scripts/validate.py","scripts/verify_apply.py","scripts/ics_normalize.py",
  "cue/standing-directives.json","docs/AI_RULES.md","docs/shrine/CHARTER.md","docs/shrine/LOG.md",
  "docs/shrine/members/ARCHITECT_TESTAMENT_2026-09-13_II.md","Brain/frontal_lobe/task_ledger.md",
  "Brain/courses/CALENDAR.md","README.md","docs/SYSTEM_STATE.md","CHANGELOG.md","docs/ROADMAP.md",
  "docs/CAPABILITIES.md","scripts/README.md","docs/DECISION_AUTHORITY.md","docs/AUDIT_2026-09-13.md",
  "docs/PATCH_LEDGER.md",".github/workflows/validate.yml")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "OK 20 payload files"
$vehicles = @("Brain/courses/SCHEDULE.csv","Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved=0; foreach ($f in $vehicles) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved leftover vehicle(s) -> _local_backup/" } else { Say "-  vehicles already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v2\.1\.0") { Die "version not v2.1.0" }
$a = Get-Content "docs/AI_RULES.md" -Raw; if ($a -notmatch "II\.9") { Die "II.9 mandate missing" }
python scripts/ics_normalize.py --self-test | Select-Object -Last 1
python scripts/verify_apply.py --self-test
python scripts/status.py | Select-Object -First 5
python scripts/verify_apply.py | Select-Object -First 12
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 31 checks - 30 pass - 1 warn - 0 FAIL (warn = check 16 meta-budget, parked)."
Say "Now delete APPLY.sh APPLY.ps1, commit, push. The CI apply-report will watch every push after."
