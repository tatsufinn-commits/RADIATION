# APPLY.ps1 - RADIATION patch 4300 "Compression" (superset of 4200; base: v2.4.2) - self-removing
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
if ((Get-Content "cue/autopilot-cues.md" -Raw) -notmatch "BUILD CUES") { Die "4100 content missing - extract 4100 first" }
if (-not (Test-Path "tests/knowledge_assertions.json")) { Die "4100 not applied (assertions missing)" }
Say "RADIATION patch 4300 - Compression (gate: 4100 OK - supersedes 4200)"
$P = @("docs/OPEN_SOURCES.md","subskills/active/fetch.md","subskills/active/overule.md","cue/standing-directives.json","docs/MODES.md","scripts/validate.py","docs/TOOLBOX.md","docs/WAYFINDING.md","docs/AI_RULES.md","docs/.readme",
"09-nota/CARD_002_environmental-planning-act.md","09-nota/CORE_INDEX.md","05-annotate/ANNOT_RA-10587_pd1308-repeal.md","06-triangulate/TRI_ra10587-repeal_2026-09-13.md","06-triangulate/CONFLICT_REGISTER.md","docs/KNOWLEDGE_REGISTRY.md","01-research/REFERENCES.md","07-inspect/DEBT_REGISTER.md","Brain/short_term/notes/PLANNING_reviewer.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-13-f_intake.md","scaffolding/neurons/interneurons/TID-2026-09-13-f_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-13-f_orders.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-14-g_intake.md","scaffolding/neurons/interneurons/TID-2026-09-14-g_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-14-g_orders.md",
"scaffolding/neurons/_archive/README.md",
"scaffolding/neurons/_archive/TID-2026-09-13-a_intake.md","scaffolding/neurons/_archive/TID-2026-09-13-a_reasoning.md","scaffolding/neurons/_archive/TID-2026-09-13-a_orders.md",
"scaffolding/neurons/_archive/TID-2026-09-13-b_intake.md","scaffolding/neurons/_archive/TID-2026-09-13-b_reasoning.md","scaffolding/neurons/_archive/TID-2026-09-13-b_orders.md",
"scaffolding/neurons/_archive/TID-2026-09-13-c_intake.md","scaffolding/neurons/_archive/TID-2026-09-13-c_reasoning.md","scaffolding/neurons/_archive/TID-2026-09-13-c_orders.md",
"scaffolding/neurons/_archive/TID-2026-09-13-d_intake.md","scaffolding/neurons/_archive/TID-2026-09-13-d_reasoning.md","scaffolding/neurons/_archive/TID-2026-09-13-d_orders.md",
"scaffolding/neurons/_archive/TID-2026-09-13-e_intake.md","scaffolding/neurons/_archive/TID-2026-09-13-e_reasoning.md","scaffolding/neurons/_archive/TID-2026-09-13-e_orders.md",
"Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md","docs/PATCH_LEDGER.md","CHANGELOG.md","README.md","docs/SYSTEM_STATE.md","docs/ROADMAP.md")
$n=0; foreach ($f in $P) { if (-not (Test-Path $f)) { Die "payload missing: $f" }; $n++ }
Say "OK $n payload files"
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
$faded=0
foreach ($pair in @(@("sensoryneurons","intake"),@("interneurons","reasoning"),@("motorneurons","orders"))) {
  foreach ($t in "a","b","c","d","e") {
    $f = "scaffolding/neurons/$($pair[0])/TID-2026-09-13-$($t)_$($pair[1]).md"
    if (Test-Path $f) { git rm --ignore-unmatch --quiet $f 2>$null; Remove-Item $f -Force -ErrorAction SilentlyContinue; $faded++ }
  }
}
Say "OK relay faded: $faded TID record(s) -> _archive/ (II.10.4; never deleted)"
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
if ((Get-Content "README.md" -Raw) -notmatch "v2\.6\.0") { Die "version not v2.6.0" }
if ((Get-Content "docs/AI_RULES.md" -Raw) -notmatch "II\.10 - LEDGER COMPRESSION") { Die "II.10 absent" }
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/status.py | Select-Object -First 3
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say "Done. Expected: 33 checks - 32 pass - 1 warn - 0 FAIL. COMMIT (seal), push. Runners self-remove."
Remove-Item $MyInvocation.MyCommand.Path -Force
