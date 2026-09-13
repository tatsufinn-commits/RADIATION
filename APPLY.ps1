# APPLY.ps1 - RADIATION patch 4500 "Last Mile" (superset of 4200+4300+4400) - seal transaction
$ErrorActionPreference = "Stop"
function Say($m){Write-Host $m}; function Die($m){Write-Host "X $m" -ForegroundColor Red; exit 1}
if (-not (Test-Path "README.md")) { Die "run from the repository root" }
if ((Get-Content "cue/autopilot-cues.md" -Raw) -notmatch "BUILD CUES") { Die "4100 content missing - extract 4100 first" }
if (-not (Test-Path "tests/knowledge_assertions.json")) { Die "4100 not applied (assertions missing)" }
Say "RADIATION patch 4500 - Last Mile (gate: 4100 OK - supersedes 4200+4300+4400)"
$P = @("docs/OPEN_SOURCES.md","subskills/active/fetch.md","subskills/active/overule.md","cue/standing-directives.json","docs/MODES.md","docs/TOOLBOX.md","docs/WAYFINDING.md",
"09-nota/CARD_001_bp344-accessibility.md","09-nota/CARD_002_environmental-planning-act.md","09-nota/CORE_INDEX.md","05-annotate/ANNOT_RA-10587_pd1308-repeal.md","06-triangulate/TRI_ra10587-repeal_2026-09-13.md","06-triangulate/CONFLICT_REGISTER.md","docs/KNOWLEDGE_REGISTRY.md","01-research/REFERENCES.md","07-inspect/DEBT_REGISTER.md","Brain/short_term/notes/PLANNING_reviewer.md",
"docs/AI_RULES.md","docs/.readme","docs/CAPABILITIES.md","subskills/SUBSKILL_INDEX.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-13-f_intake.md","scaffolding/neurons/interneurons/TID-2026-09-13-f_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-13-f_orders.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-14-g_intake.md","scaffolding/neurons/interneurons/TID-2026-09-14-g_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-14-g_orders.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-14-h_intake.md","scaffolding/neurons/interneurons/TID-2026-09-14-h_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-14-h_orders.md",
"scaffolding/neurons/sensoryneurons/TID-2026-09-14-i_intake.md","scaffolding/neurons/interneurons/TID-2026-09-14-i_reasoning.md","scaffolding/neurons/motorneurons/TID-2026-09-14-i_orders.md",
"scaffolding/neurons/_archive/README.md",
"radiation_core/__init__.py","radiation_core/relay.py","schemas/task-envelope.schema.json","schemas/plan.schema.json","schemas/command.schema.json","schemas/outcome.schema.json","schemas/event.schema.json",
"evidence/tasks/legacy_manifest.json",
"evidence/tasks/TID-2026-09-14-h/task.json","evidence/tasks/TID-2026-09-14-h/events.ndjson","evidence/tasks/TID-2026-09-14-h/projection.json","evidence/tasks/TID-2026-09-14-h/outcomes/CMD-0001.json",
"evidence/tasks/TID-2026-09-14-i/task.json","evidence/tasks/TID-2026-09-14-i/plan.v1.json","evidence/tasks/TID-2026-09-14-i/events.ndjson","evidence/tasks/TID-2026-09-14-i/projection.json","evidence/tasks/TID-2026-09-14-i/commands/CMD-0001.json","evidence/tasks/TID-2026-09-14-i/outcomes/CMD-0005.json","evidence/tasks/TID-2026-09-14-i/artifacts/status_strict.txt",
"scripts/nota.py","scripts/validate.py","scripts/status.py","scripts/verify_apply.py","scripts/grade_exam.py","scripts/render_docs.py",
"subskills/passive/surgeon.md","subskills/passive/sentinel.md","subskills/passive/compass.md","subskills/passive/curator.md",
".github/workflows/validate.yml",".gitignore",
"Brain/frontal_lobe/task_ledger.md","docs/shrine/LOG.md","docs/PATCH_LEDGER.md","CHANGELOG.md","README.md","docs/SYSTEM_STATE.md","docs/ROADMAP.md")
$n=0; foreach ($f in $P) { if (-not (Test-Path $f)) { Die "payload missing: $f" }; $n++ }
Say "OK $n payload sentinels"
if ((Get-ChildItem "scaffolding/neurons/_archive" -Filter "TID-*" | Measure-Object).Count -ne 15) { Die "archive incomplete (want 15)" }
if ((Get-ChildItem "evidence/tasks/TID-2026-09-14-i/commands" | Measure-Object).Count -ne 5) { Die "TID-i bundle commands incomplete" }
Say "OK archive (15) + canonical bundles (h, i) present"
if (git rev-parse --is-inside-work-tree 2>$null) {
  $paths = @("Brain/courses/SCHEDULE.csv","Brain/courses/desktop.ini","Brain/courses/0_CALLENDER/readme.txt",
    "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
    "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
    "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
    "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf",
    "APPLY.sh","APPLY.ps1","PATCH_NOTES.md")
  foreach ($p in $paths) { git rm --cached --ignore-unmatch --quiet $p 2>$null }
  Say "OK untrack re-run"
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
Say "OK relay faded: $faded duplicate record(s) (II.10.4)"
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
Remove-Item "APPLY.sh" -Force -ErrorAction SilentlyContinue
Remove-Item $MyInvocation.MyCommand.Path -Force -ErrorAction SilentlyContinue
if ((Get-Content "README.md" -Raw) -notmatch "v2\.8\.0") { Die "version not v2.8.0" }
if ((Get-Content "docs/AI_RULES.md" -Raw) -notmatch "II\.10 - LEDGER COMPRESSION") { Die "II.10 absent" }
python -m radiation_core.relay --self-test 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { Die "relay self-test failed (want 6/6)" }
python -m radiation_core.relay 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { Die "relay semantic check failed" }
python scripts/status.py --self-test 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { Die "status self-test failed" }
python scripts/nota.py --check 1>$null 2>$null
if ($LASTEXITCODE -ne 0) { Die "core card gate failed" }
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/validate.py 2>&1 | Select-Object -Last 1
Say ""
Say "=== SEAL INSTRUCTIONS (finish the transaction) ==="
Say "  git add -A ; git commit -m 'Seal 4500 last-mile patch' ; git push"
Say "  Fresh clone must show: 34 checks - 33 pass - 1 warn - 0 FAIL. CI apply-report now BLOCKS."
Say "===================================================="
