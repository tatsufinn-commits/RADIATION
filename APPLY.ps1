# APPLY.ps1 - RADIATION patch 4200 "Expansion" (requires 4100/v2.4.2) - self-removing
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
$c = Get-Content "cue/autopilot-cues.md" -Raw
if ($c -notmatch "BUILD CUES") { Die "4100 content missing - extract 4100 first" }
$payload = @("docs/OPEN_SOURCES.md","subskills/active/fetch.md","subskills/active/overule.md",
  "cue/standing-directives.json","docs/MODES.md","scripts/validate.py","docs/TOOLBOX.md","docs/WAYFINDING.md",
  "09-nota/CARD_002_environmental-planning-act.md","09-nota/CORE_INDEX.md",
  "05-annotate/ANNOT_RA-10587_pd1308-repeal.md","06-triangulate/TRI_ra10587-repeal_2026-09-13.md",
  "06-triangulate/CONFLICT_REGISTER.md","docs/KNOWLEDGE_REGISTRY.md","01-research/REFERENCES.md",
  "07-inspect/DEBT_REGISTER.md","Brain/short_term/notes/PLANNING_reviewer.md",
  "scaffolding/neurons/sensoryneurons/TID-2026-09-13-f_intake.md",
  "scaffolding/neurons/interneurons/TID-2026-09-13-f_reasoning.md",
  "scaffolding/neurons/motorneurons/TID-2026-09-13-f_orders.md",
  "Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md","docs/PATCH_LEDGER.md",
  "CHANGELOG.md","README.md","docs/SYSTEM_STATE.md","docs/ROADMAP.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "OK 27 payload files"
if (git rev-parse --is-inside-work-tree 2>$null) {
  $paths = @("Brain/courses/SCHEDULE.csv","Brain/courses/desktop.ini","Brain/courses/0_CALLENDER/readme.txt",
    "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf",
    "APPLY.sh","APPLY.ps1","PATCH_NOTES.md")
  foreach ($p in $paths) { git rm --cached --ignore-unmatch --quiet $p 2>$null }
  Say "OK untrack re-run - COMMIT to seal"
}
$moved=0; foreach ($f in $paths[0..7]) { if (Test-Path $f) { $d = Join-Path "_local_backup" (Split-Path $f -Parent); New-Item -ItemType Directory -Force -Path $d | Out-Null; Move-Item $f $d -Force; $moved++ } }
if ($moved -gt 0) { Say "OK $moved vehicle(s) re-homed" } else { Say "-  vehicles already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
$r = Get-Content "README.md" -Raw; if ($r -notmatch "v2\.5\.0") { Die "version not v2.5.0" }
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/status.py | Select-Object -First 3
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 33 checks - 32 pass - 1 warn - 0 FAIL. COMMIT (seal), push. Runners self-remove."
Remove-Item $MyInvocation.MyCommand.Path -Force
