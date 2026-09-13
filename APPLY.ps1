# ─────────────────────────────────────────────────────────────────────────────
# APPLY.ps1 — RADIATION patch 2600
# Schedule Record + Location Amendment (A1)
# Apply from the repository ROOT:   powershell -ExecutionPolicy Bypass -File APPLY.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

function Say($m) { Write-Host $m }
function Die($m) { Write-Host "X $m" -ForegroundColor Red; exit 1 }

if (-not (Test-Path "README.md")) { Die "run this from the RADIATION repository root" }
if (-not (Test-Path "docs/AI_RULES.md")) { Die "docs/AI_RULES.md not found - wrong directory?" }

Say "RADIATION patch 2600 - Schedule Record + Location Amendment"
Say ""

# ── 1. presence check ───────────────────────────────────────────────────────
Say "1/6  checking payload..."
$payload = @("Brain/courses/SCHEDULE.md","Brain/courses/INDEX.md","scripts/validate.py",".gitignore","README.md","docs/SYSTEM_STATE.md","CHANGELOG.md")
foreach ($f in $payload) {
  if (-not (Test-Path $f)) { Die "payload missing: $f" }
}
Say "     OK 7 content files present"

# ── 2. retire the superseded grid-form CSV ──────────────────────────────────
Say "2/6  retiring the superseded CSV..."
if (Test-Path "Brain/courses/SCHEDULE.csv") {
  New-Item -ItemType Directory -Force -Path "_local_backup/Brain/courses" | Out-Null
  Move-Item "Brain/courses/SCHEDULE.csv" "_local_backup/Brain/courses/SCHEDULE.csv" -Force
  Say "     OK SCHEDULE.csv -> _local_backup/ (git-ignored; identical data now in SCHEDULE.md)"
} else {
  Say "     -  SCHEDULE.csv already absent"
}

# ── 3. untrack the generated validator report ───────────────────────────────
Say "3/6  untracking generated output..."
git ls-files --error-unmatch validation_report.json 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  git rm --cached --quiet validation_report.json
  Say "     OK validation_report.json untracked (file kept on disk)"
} else {
  Say "     -  validation_report.json not tracked"
}

# ── 4. verify the amendment landed ──────────────────────────────────────────
Say "4/6  verifying the amendment..."
$v = Get-Content "scripts/validate.py" -Raw
if ($v -notmatch "CV_ALLOW_LOCATION") { Die "amendment A1 not applied to validate.py" }
if ($v -notmatch "CV_DENY_OTHER")     { Die "amendment A1 split not applied to validate.py" }
python -c "import ast;ast.parse(open('scripts/validate.py').read())"
if ($LASTEXITCODE -ne 0) { Die "validate.py has a syntax error" }
Say "     OK A1 present, validate.py parses"

# ── 5. the schedule record must carry rooms but no names ────────────────────
Say "5/6  checking the schedule record..."
$s = Get-Content "Brain/courses/SCHEDULE.md" -Raw
if ($s -notmatch "S308") { Die "SCHEDULE.md is missing its room codes (A1 intended them present)" }
if ($s -match "(?i)(Instructor|Professor|Prof\.)[^A-Za-z]*[A-Z][a-z]+") {
  Die "SCHEDULE.md appears to contain an instructor name - that prohibition is absolute"
}
Say "     OK rooms present - no personnel identifiers"

# ── 6. run the validator ────────────────────────────────────────────────────
Say "6/6  running the validator..."
python scripts/validate.py 2>&1 | Select-Object -Last 4

Say ""
Say "Done. Expected: 25 checks - check 2.5 no longer lists SCHEDULE.csv."
Say "Still failing by design until you act: the 5 vehicles + desktop.ini (2.5),"
Say "and docs/PLAYBOOK_EVALFIRST_TEMPLATE_STAGED.md (check 3)."
Say ""
Say "!  Rotation still pending: the LMS feed URL in commit 4a98e59 is live."
Say "   No patch can fix that - rotate the feed at source."
