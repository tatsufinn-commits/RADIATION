# ─────────────────────────────────────────────────────────────────────────────
# APPLY.ps1 — RADIATION patch 3000 "Core Emission & The Net"
# DEPENDENCY: requires patch 2900 (v1.7.0) ALREADY APPLIED.
#   powershell -ExecutionPolicy Bypass -File APPLY.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
function Say($m) { Write-Host $m }
function Die($m) { Write-Host "X $m" -ForegroundColor Red; exit 1 }

if (-not (Test-Path "README.md")) { Die "run this from the RADIATION repository root" }
if ((-not (Test-Path "docs/shrine/CHARTER.md"))) { Die "patch 2900 (Swarm-Memory) is NOT applied yet - apply it FIRST" }
$ch = Get-Content "docs/shrine/CHARTER.md" -Raw
if ($ch -notmatch "commons") { Die "patch 2900 (Swarm-Memory) is NOT applied yet - apply it FIRST" }

Say "RADIATION patch 3000 - Core Emission & The Net"
Say "     dependency gate: v1.7.0 present OK"
Say ""

Say "1/6  checking payload..."
$payload = @("scripts/nota.py","scripts/module_scaffold.py","scripts/validate.py",
  "tests/knowledge_assertions.json","docs/CAPABILITIES.md","scripts/README.md",
  ".github/workflows/validate.yml","docs/SYSTEM_STATE.md","README.md","CHANGELOG.md",
  "cue/autopilot-cues.md","cue/commander-readiness.md","docs/PROMPT_PLAYBOOK.md",
  "docs/CUE_SYSTEM.md","docs/COMMANDER_QUICKREF.md","docs/SKILLS.md",
  "Brain/BRAIN_INDEX.md","Brain/frontal_lobe/testament.md","docs/shrine/CHARTER.md")
foreach ($f in $payload) { if (-not (Test-Path $f)) { Die "payload missing: $f" } }
Say "     OK 19 files present"

Say "2/6  self-testing the new tools..."
python scripts/nota.py --self-test | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Die "nota self-test failed - STOPPING" }
python scripts/module_scaffold.py --self-test | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Die "module_scaffold self-test failed - STOPPING" }
python scripts/ics_normalize.py --self-test | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Die "ICS self-test failed - STOPPING" }

Say "3/6  reconciliation (idempotent)..."
$vehicles = @("Brain/courses/SCHEDULE.csv",
  "Brain/courses/0_CALLENDER/ics.txt","Brain/courses/0_CALLENDER/readme.txt",
  "Brain/courses/desktop.ini",
  "Brain/courses/DSS10_INTRODUCTION_TO_DATA_SCIENCE/SOIT_DSS10_1Q_ Syllabus.docx",
  "Brain/courses/GED103_READINGS_IN_PHILIPPINE_HISTORY/GED103 Syllabus_Q12627.docx",
  "Brain/courses/MEC30-7_STATICS_OF_RIGID_BODIES_FOR_CE/MEC30-7 Course Calendar 1Q.html",
  "Brain/courses/AR173-1P_PLANNING_2/AR173-1P (Fundamentals of Urban Design and Community Architecture)-CLASS SCHEDULE.pdf")
$moved = 0
foreach ($f in $vehicles) {
  if (Test-Path $f) {
    $d = Join-Path "_local_backup" (Split-Path $f -Parent)
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    Move-Item $f $d -Force; $moved++
  }
}
if ($moved -gt 0) { Say "     OK $moved leftover file(s) -> _local_backup/" } else { Say "     -  already reconciled" }
if (Test-Path "PATCH_NOTES.md") { Remove-Item "PATCH_NOTES.md" -Force }
git ls-files --error-unmatch validation_report.json 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) { git rm --cached --quiet validation_report.json }

Say "4/6  verifying..."
$n = Get-Content "scripts/nota.py" -Raw
if ($n -notmatch "never admits") { Die "nota.py contract broken" }
$m = Get-Content "scripts/module_scaffold.py" -Raw
if ($m -notmatch "index_state") { Die "module_scaffold broken" }
$v = Get-Content "scripts/validate.py" -Raw
if ($v -notmatch "RADIATION_ONLINE") { Die "check 13 online gate missing" }
if ($v -notmatch "DRILL\\b") { Die "check 18 hardening missing" }
$k = Get-Content "tests/knowledge_assertions.json" -Raw
if ($k -notmatch "KR-CUR-001") { Die "new locked assertions missing" }
$c = Get-Content "docs/CAPABILITIES.md" -Raw
if (($c -notmatch "nota.py") -or ($c -notmatch "module_scaffold")) { Die "registry not updated (check 21 will fail)" }
$r2 = Get-Content "README.md" -Raw
if ($r2 -notmatch "v1\.8\.0") { Die "version not v1.8.0" }
Say "     OK tools - online gate - check-18 hardening - 9 locked - registry - v1.8.0"

Say "5/6  running the full check suite..."
python scripts/knowledge_regression.py | Select-Object -Last 1
python scripts/nota.py --check | Select-Object -Last 1
python scripts/validate.py 2>&1 | Select-Object -Last 3

Say "6/6  done."
Say "Expected: 29 checks - 27 pass - 2 warn - 0 FAIL - 9 locked / 5 pending."
Say "Now: delete APPLY.sh and APPLY.ps1, commit, push."
Say "STILL OWED: rotate the feed URL exposed in 4a98e59, then set RADIATION_ICS_URL."
