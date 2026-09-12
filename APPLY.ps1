<#
  APPLY.ps1 — RADIATION_PATCH_2026-09-13_2300_Courses-Region-and-Containment
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


# ── 2. back up every non-.md file under Brain/courses/ ───────────────────────
$backup = Join-Path (Get-Location) "_local_backup"
$moved  = @()

$targets = Get-ChildItem -Path "Brain\courses" -Recurse -File -ErrorAction SilentlyContinue |
           Where-Object { $_.Extension -ne ".md" }

foreach ($f in $targets) {
    $rel    = $f.FullName.Substring((Get-Location).Path.Length + 1)
    $dest   = Join-Path $backup $rel
    $dirdir = Split-Path $dest -Parent
    if (-not (Test-Path $dirdir)) { New-Item -ItemType Directory -Path $dirdir -Force | Out-Null }
    Move-Item -LiteralPath $f.FullName -Destination $dest -Force
    $moved += $rel
}
Say "`n✓ backed up + removed from tree: $($moved.Count) vehicle(s)"
foreach ($m in $moved) { Say "    $m" DarkGray }
if ($moved.Count -gt 0) {
    Say "  → local copies live in: _local_backup\" Yellow
    Say "  → KEEP THAT FOLDER. It is git-ignored by the new .gitignore." Yellow
}


# ── 3. copy patch files into place (already extracted by you) ────────────────
$expect = @(
  ".gitignore",
  "Brain\courses\INDEX.md",
  "Brain\courses\GED103.md",
  "Brain\courses\DSS10.md",
  "Brain\courses\MEC30-7.md",
  "Brain\courses\AR173-1P.md",
  "Brain\courses\AR163-1P.md",
  "Brain\courses\AR153P.md",
  "docs\KNOWLEDGE_REGISTRY.md",
  "scripts\validate.py",
  "Brain\frontal_lobe\task_ledger.md",
  "docs\PATCH_LEDGER.md"
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
Say "✓ all $($expect.Count) patch files present (including the .gitignore dotfile)"


# ── 4. prune directories emptied by the move ─────────────────────────────────
$pruned = 0
do {
    $empty = Get-ChildItem -Path "Brain\courses" -Recurse -Directory |
             Where-Object { (Get-ChildItem -LiteralPath $_.FullName -Force | Measure-Object).Count -eq 0 }
    foreach ($d in $empty) { Remove-Item -LiteralPath $d.FullName -Force -Recurse; $pruned++ }
} while ($empty)
Say "✓ pruned $pruned emptied director(ies)"


# ── 5. leaving the 18 carriers alone, on purpose ─────────────────────────────
$carriers = @(Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue |
              Where-Object { $_.Name -match "_STAGED|_DIFF|^PATCH_NOTES\.md$" } |
              Where-Object { $_.FullName -notmatch "\\_local_backup\\" })
Say "`nℹ transport carriers still in the tree: $($carriers.Count) — UNTOUCHED by this patch." Yellow
Say "  Removing them is a separate, Commander-authorized patch (II.4 purge rule)." DarkGray


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
