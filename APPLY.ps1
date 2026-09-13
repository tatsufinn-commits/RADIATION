# APPLY.ps1 - RADIATION patch 3900 "Reflex Arc" (requires 3800/v2.3.1)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
$i = Get-Content "09-nota/CORE_INDEX.md" -Raw
if ($i -notmatch "CARD_001") { Die "patch 3800 not applied - apply First-Light.zip FIRST" }
$payload = @("scripts/validate.py","scripts/status.py","07-inspect/TABLETOP_injection_2026-09-13.md",
  "scaffolding/neurons/sensoryneurons/TID-2026-09-13-d_intake.md",
  "scaffolding/neurons/interneurons/TID-2026-09-13-d_reasoning.md",
  "scaffolding/neurons/motorneurons/TID-2026-09-13-d_orders.md",
  "Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md","docs/PATCH_LEDGER.md",
  "CHANGELOG.md","README.md","docs/SYSTEM_STATE.md","docs/ROADMAP.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "OK 13 payload files"
if (git rev-parse --is-inside-work-tree 2>$null) {
  $paths = @("Brain/courses/SCHEDULE.csv","Brain/courses/desktop.ini","Brain/courses/0_CALLENDER/readme.txt",
    "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf",
    "APPLY.sh","APPLY.ps1","PATCH_NOTES.md")
  foreach ($p in $paths) { git rm --cached --ignore-unmatch --quiet $p 2>$null }
  Say "OK untrack re-run - COMMIT to seal the loop permanently"
}
$moved=0; foreach ($f in $paths[0..7]) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved vehicle(s) re-homed" } else { Say "-  vehicles already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v2\.4\.0") { Die "version not v2.4.0" }
$v = Get-Content "scripts/validate.py" -Raw; if ($v -notmatch "c27relay") { Die "check 27 missing" }
python scripts/status.py | Select-Object -First 4
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 32 checks - 31 pass - 1 warn - 0 FAIL. COMMIT (seal), push."
