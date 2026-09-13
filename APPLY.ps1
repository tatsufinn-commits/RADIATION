# APPLY.ps1 - RADIATION patch 3700 "The Curation Gate" (requires 3600/v2.2.0)
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
if (-not (Test-Path "docs/WAYFINDING.md")) { Die "patch 3600 not applied - apply Autopilot-Pipeline-and-Wayfinding.zip FIRST" }
if (-not (Test-Path "scaffolding/neurons/README.md")) { Die "patch 3600 not applied (neuron relay missing)" }
$payload = @("scaffolding/core/proc_self-directive.md","scaffolding/core/INDEX.md","cue/standing-directives.json",
  "cue/autopilot-doctrine.md",".gitignore","Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md",
  "docs/PATCH_LEDGER.md","CHANGELOG.md","README.md","docs/SYSTEM_STATE.md","docs/ROADMAP.md",
  "scaffolding/neurons/sensoryneurons/TID-2026-09-13-b_intake.md","scaffolding/neurons/interneurons/TID-2026-09-13-b_reasoning.md",
  "scaffolding/neurons/motorneurons/TID-2026-09-13-b_orders.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "OK 15 payload files"
if (git rev-parse --is-inside-work-tree 2>$null) {
  $paths = @("Brain/courses/SCHEDULE.csv","Brain/courses/desktop.ini","Brain/courses/0_CALLENDER/readme.txt",
    "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf",
    "APPLY.sh","APPLY.ps1","PATCH_NOTES.md")
  foreach ($p in $paths) { git rm --cached --ignore-unmatch --quiet $p 2>$null }
  Say "OK untracked vehicles + transport - NOW COMMIT to seal the loop permanently"
}
$moved=0; foreach ($f in $paths[0..7]) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved vehicle(s) re-homed" } else { Say "-  vehicles already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v2\.3\.0") { Die "version not v2.3.0" }
$s = Get-Content "scaffolding/core/proc_self-directive.md" -Raw; if ($s -notmatch "CURATION GATE") { Die "scaffold not v1.1" }
python -c "import json;d=json.load(open('cue/standing-directives.json'));ids=[x['id'] for x in d['directives']];assert len(ids)==12 and 'SD-GOV-012' in ids"
if ($LASTEXITCODE -ne 0) { Die "registry not at 12" }
python scripts/status.py | Select-Object -First 5
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 31 checks - 30 pass - 1 warn - 0 FAIL. Now COMMIT (seals the untrack), push."
