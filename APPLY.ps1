# APPLY.ps1 - RADIATION patch 3600 "Autopilot Pipeline & Wayfinding" (requires 3500/v2.1.1)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
$c = Get-Content "cue/autopilot-cues.md" -Raw
if ($c -notmatch "BUILD CUES") { Die "patch 3500 not applied - apply Cue-Renewal.zip FIRST" }
if (-not (Test-Path "04-incubate/TICKET_001_skill-renovation.md")) { Die "patch 3500 not applied (TICKET_001 missing)" }
$payload = @("scaffolding/neurons/README.md","scaffolding/neurons/sensoryneurons/TEMPLATE_intake.md",
  "scaffolding/neurons/sensoryneurons/TID-2026-09-13-a_intake.md","scaffolding/neurons/interneurons/TEMPLATE_reasoning.md",
  "scaffolding/neurons/interneurons/TID-2026-09-13-a_reasoning.md","scaffolding/neurons/motorneurons/TEMPLATE_orders.md",
  "scaffolding/neurons/motorneurons/TID-2026-09-13-a_orders.md","scaffolding/core/proc_self-directive.md",
  "scaffolding/core/INDEX.md","docs/WAYFINDING.md","docs/TOOLBOX.md","docs/ROADMAP.md",".gitignore",
  "scripts/status.py","cue/autopilot-doctrine.md","Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md",
  "README.md","docs/SYSTEM_STATE.md","CHANGELOG.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "OK 20 payload files"
if (git rev-parse --is-inside-work-tree 2>$null) {
  $paths = @("Brain/courses/SCHEDULE.csv","Brain/courses/desktop.ini","Brain/courses/0_CALLENDER/readme.txt",
    "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf",
    "APPLY.sh","APPLY.ps1","PATCH_NOTES.md")
  foreach ($p in $paths) { git rm --cached --ignore-unmatch --quiet $p 2>$null }
  Say "OK untracked vehicles + transport - commit to seal it"
}
$vehicles = $paths[0..7]
$moved=0; foreach ($f in $vehicles) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved vehicle(s) re-homed" } else { Say "-  vehicles already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v2\.2\.0") { Die "version not v2.2.0" }
$i = Get-Content "scaffolding/core/INDEX.md" -Raw; if ($i -notmatch "proc_self-directive") { Die "scaffold not INDEX-registered" }
if ((-not (Test-Path "docs/WAYFINDING.md")) -or (-not (Test-Path "docs/TOOLBOX.md"))) { Die "wayfinding/toolbox missing" }
python scripts/status.py | Select-Object -First 7
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 31 checks - 30 pass - 1 warn - 0 FAIL. Commit (the untrack seals), push."
