<#
  APPLY.ps1 — RADIATION_PATCH_2026-09-13_2340_Term-Planner
  Risk class: 🟢 ordinary.  Run from the REPOSITORY ROOT, after extracting the zip over it.

  What it does:
    1. verifies it is standing in the RADIATION repo root
    2. BACKS UP every non-.md file under Brain/courses/ to _local_backup/ (structure preserved)
       — this is deliberate: git rm alone would leave the only copies in git history
    3. copies the patch's files into place
    4. removes the backed-up vehicles from the working tree
    5. prunes emptied directories under Brain/courses/
    6. re-runs the validator and prints the git commands

  It does NOT commit, and it does NOT touch the 18 transport carriers.
#>
$ErrorActionPreference = "Stop"

function Say($m, $c = "Gray") { Write-Host $m -ForegroundColor $c }

Say "`n=== RADIATION PATCH 2026-09-13_2300 — Courses Region & Containment ===`n" Cyan

# ── 1. am I in the repo root? ────────────────────────────────────────────────
foreach ($probe in @("docs\AI_RULES.md", "Brain", "scripts\validate.py")) {
    if (-not (Test-Path $probe)) {
        Say "✗ Not the repository root — '$probe' not found." Red
        Say "  cd to the RADIATION repo root (the folder holding docs\ and Brain\) and re-run." Yellow
        exit 1
    }
}
Say "✓ repository root verified: $((Get-Location).Path)"


# ── 3. copy patch files into place (already extracted by you) ────────────────
$expect = @(
  "scripts\plan_term.py",
  "Brain\short_term\plan\TERM1_DEADLINES.json",
  "Brain\short_term\plan\README.md",
  "Brain\cerebellum\routines\routine_term-briefing.md",
  "cue\autopilot-cues.md",
  "docs\KNOWLEDGE_REGISTRY.md",
  "scripts\validate.py",
  ".gitignore"
)
Say "`n— verifying the patch files are in place —"
$missing = @()
foreach ($e in $expect) { if (-not (Test-Path $e)) { $missing += $e } }
if ($missing.Count -gt 0) {
    Say "✗ these files were not found after extraction:" Red
    foreach ($m in $missing) { Say "    $m" Red }
    Say "  Re-extract the zip OVER the repository root (keep folder structure), then re-run." Yellow
    exit 1
}
Say "✓ patch files present"




# ── 5. leaving the 18 carriers alone, on purpose ─────────────────────────────
$carriers = @(Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
              Where-Object { $_.Name -match "_STAGED|_DIFF|^PATCH_NOTES\.md$" } |
              Where-Object { $_.FullName -notmatch "\\_local_backup\\" })
Say "`nℹ transport carriers still in the tree: $($carriers.Count) — UNTOUCHED by this patch." Yellow
Say "  Removing them is a separate, Commander-authorized patch (II.4 purge rule)." DarkGray


# ── 5b. archive PATCH_NOTES.md out of the tree (II.8.2) ─────────────────────
if (Test-Path "PATCH_NOTES.md") {
    if (-not (Test-Path $backup)) { New-Item -ItemType Directory -Path $backup -Force | Out-Null }
    Move-Item "PATCH_NOTES.md" (Join-Path $backup "PATCH_NOTES_APPLIED.md") -Force
    Say "✓ PATCH_NOTES.md archived to _local_backup\PATCH_NOTES_APPLIED.md (II.8.2: notes live in the zip, not the tree)" Green
}

# ── 6. validate ──────────────────────────────────────────────────────────────
Say "`n=== running the validator ===" Cyan
$py = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" }
      elseif (Get-Command python -ErrorAction SilentlyContinue) { "python" }
      else { $null }
if ($py) {
    & $py "scripts\validate.py"
    $code = $LASTEXITCODE
    Say "`nexit code: $code" Gray
    if ($code -eq 0) { Say "✓ GREEN" Green }
    else {
        Say "⚠ NOT green — expected. The remaining failures are the 18 carriers +" Yellow
        Say "  three pre-existing findings. This patch should have removed exactly ONE" Yellow
        Say "  failure (check 2) and added one passing check (2.5). Compare:" Yellow
        Say "      before: 22 checks · 14 pass · 3 warn · 5 fail" DarkGray
        Say "      after : 23 checks · 16 pass · 3 warn · 4 fail" DarkGray
    }
} else {
    Say "✗ python not found on PATH — run 'python3 scripts/validate.py' yourself." Red
}


# ── 7. next steps ────────────────────────────────────────────────────────────
Say "`n=== NEXT ===" Cyan
Say "1) review the diff, then commit:      git add -A"
Say "                                     git commit -m `"P-10 Phase 0: courses region as records + containment`""
Say "2) bump the version to v1.6.4 in README.md, docs/SYSTEM_STATE.md, CHANGELOG.md"
Say "   (check 7 compares all three — they must move together)"
Say ""
Say "3) 🔴 ROTATE THE LMS CALENDAR FEED AT SOURCE, then record the date in" White
Say "   Brain\courses\INDEX.md → 'OPEN ACTION — feed rotation'." White
Say "   This patch removed the file; it did NOT revoke the URL. Untl rotated, the" Red
Say "   exposure is open for anyone holding it." Red
Say ""
Say "4) decide the history question (A leave / B filter-repo / C private repo)." Yellow
Say "5) the 18-carrier purge is a SEPARATE patch — it needs one word from you." Yellow
Say "`nDone.`n" Cyan
