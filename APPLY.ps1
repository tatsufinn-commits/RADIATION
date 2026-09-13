# ─────────────────────────────────────────────────────────────────────────────
# APPLY.ps1 — RADIATION patch 2700 (DELTA on e76ef8c)
# Situation Layer + Capability Registry
# Apply from the repository ROOT:
#   powershell -ExecutionPolicy Bypass -File APPLY.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

function Say($m) { Write-Host $m }
function Die($m) { Write-Host "X $m" -ForegroundColor Red; exit 1 }

if (-not (Test-Path "README.md")) { Die "run this from the RADIATION repository root" }
if (-not (Test-Path "docs/AI_RULES.md")) { Die "docs/AI_RULES.md not found - wrong directory?" }

Say "RADIATION patch 2700 - Situation Layer + Capability Registry"
Say ""

# ── 1. presence check ───────────────────────────────────────────────────────
# 2700 is a DELTA on e76ef8c. SCHEDULE.md, INDEX.md and .gitignore already
# landed with patch 2600 and are NOT shipped again.
Say "1/6  checking payload..."
$payload = @("docs/SYSTEM_STATE.md","docs/CAPABILITIES.md","scripts/validate.py",
             "scripts/README.md",".github/workflows/validate.yml","README.md","CHANGELOG.md")
foreach ($f in $payload) {
  if (-not (Test-Path $f)) { Die "payload missing: $f" }
}
Say "     OK 7 content files present"

# ── 2. retire the superseded grid-form CSV ──────────────────────────────────
Say "2/6  retiring the superseded CSV..."
if (Test-Path "Brain/courses/SCHEDULE.csv") {
  New-Item -ItemType Directory -Force -Path "_local_backup/Brain/courses" | Out-Null
  Move-Item "Brain/courses/SCHEDULE.csv" "_local_backup/Brain/courses/SCHEDULE.csv" -Force
  Say "     OK SCHEDULE.csv -> _local_backup/ (git-ignored; data lives in SCHEDULE.md)"
} else {
  Say "     -  SCHEDULE.csv already absent"
}

# ── 3. untrack generated output + the transport carrier ─────────────────────
Say "3/6  untracking generated output and the carrier..."
git ls-files --error-unmatch validation_report.json 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  git rm --cached --quiet validation_report.json
  Say "     OK validation_report.json untracked (file kept on disk)"
} else {
  Say "     -  validation_report.json not tracked"
}
if (Test-Path "PATCH_NOTES.md") {
  Remove-Item "PATCH_NOTES.md" -Force
  Say "     OK PATCH_NOTES.md deleted (II.8.2 - it is a carrier, not a record)"
} else {
  Say "     -  PATCH_NOTES.md already absent"
}

# ── 4. verify the Situation Layer + the registry landed ─────────────────────
Say "4/6  verifying the Situation Layer and the registry..."
$ss = Get-Content "docs/SYSTEM_STATE.md" -Raw
if ($ss -notmatch "THE SITUATION") { Die "SYSTEM_STATE.md has no Situation Layer" }
if ($ss -notmatch "FREE")          { Die "the schedule is not inlined in Tier 0" }
if ($ss -notmatch "AR173-1P")      { Die "the inline schedule is missing its courses" }
$v = Get-Content "scripts/validate.py" -Raw
if ($v -notmatch "check 21" -and $v -notmatch "c21\(\)") { Die "check 21 (capability drift guard) is missing" }
if ($v -notmatch "CV_ALLOW_LOCATION") { Die "amendment A1 missing (should be present from 2600)" }
python -c "import ast;ast.parse(open('scripts/validate.py').read())"
if ($LASTEXITCODE -ne 0) { Die "validate.py has a syntax error" }
Say "     OK Situation Layer present - schedule inlined - check 21 armed - parses"

# ── 5. the schedule record must still carry rooms but no names ──────────────
Say "5/6  checking the schedule record..."
if (Test-Path "Brain/courses/SCHEDULE.md") {
  $s = Get-Content "Brain/courses/SCHEDULE.md" -Raw
  if ($s -notmatch "S308") { Die "SCHEDULE.md is missing its room codes (A1 intended them present)" }
  if ($s -match "(?i)(Instructor|Professor|Prof\.)[^A-Za-z]*[A-Z][a-z]+") {
    Die "SCHEDULE.md appears to contain an instructor name - that prohibition is absolute"
  }
  Say "     OK rooms present - no personnel identifiers"
} else {
  Die "Brain/courses/SCHEDULE.md is missing - apply patch 2600 first"
}

# ── 6. run the validator ────────────────────────────────────────────────────
Say "6/6  running the validator..."
python scripts/validate.py 2>&1 | Select-Object -Last 4

Say ""
Say "Done. Expected: 26 checks - exactly ONE fail - check 2.5."
Say "That last fail is yours to clear: delete the 5 vehicles + desktop.ini"
Say "under Brain/courses/ (extraction verified complete - the course records"
Say "already state they were deleted, so removing them makes the records true)."
Say "Do that and the tree reaches 0 FAIL for the first time."
Say ""
Say "!  Rotation still pending: the LMS feed URL in commit 4a98e59 is live."
Say "   No patch can fix that - rotate the feed at source."
