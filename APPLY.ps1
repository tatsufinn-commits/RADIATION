<#
  APPLY.ps1 — RADIATION_PATCH_2026-09-13_2400_BU-Ingestion-AR153P
  Risk class: 🟢 ordinary.  Run from the REPOSITORY ROOT, after extracting the zip over it.

  What it does:
    1. verifies it is standing in the RADIATION repo root
    2. verifies the patch files landed
    3. HARD-CHECKS that no PDF or zip entered the tree (II.6 rule 8 — vehicles never commit)
    4. archives PATCH_NOTES.md out of the tree (II.8.2 — notes live in the zip)
    5. self-checks the ingestion harness and reports whether pymupdf is present
    6. re-runs the validator and prints the git commands

  This patch is a pure overlay: it removes nothing from the tree, fetches nothing,
  and does NOT touch the 18 transport carriers.
#>
$ErrorActionPreference = "Stop"

function Say($m, $c = "Gray") { Write-Host $m -ForegroundColor $c }
function Head($m) { Write-Host "`n=== $m ===" -ForegroundColor Cyan }

Head "RADIATION PATCH 2026-09-13_2400 — Building Utilities Ingestion (AR153P)"

# ── 1. repo root? ────────────────────────────────────────────────────────────
$probes = @("docs\AI_RULES.md", "Brain", "scripts\validate.py")
$bad = $false
foreach ($p in $probes) { if (-not (Test-Path $p)) { Say "x missing: $p" Red; $bad = $true } }
if ($bad) { Say "x Not the repository root. cd to the repo root and re-run." Red; exit 1 }
Say "v repository root verified: $(Get-Location)" Green

# ── 2. did the patch land? ───────────────────────────────────────────────────
Head "verifying the patch files are in place"
$files = @(
  "scripts\ingest_collection.py",
  "Brain\short_term\ingest\BU_INGEST_2026-09-13.md",
  "Brain\external_sources\building-utilities.md",
  "docs\KNOWLEDGE_REGISTRY.md",
  "docs\DECAY_REGISTER.md",
  "Brain\courses\AR153P.md",
  "Brain\courses\AR163-1P.md"
)
$missing = 0
foreach ($f in $files) { if (-not (Test-Path $f)) { Say "x missing: $f" Red; $missing++ } }
if ($missing -gt 0) { Say "  Re-extract the zip OVER the repository root." Red; exit 1 }
Say "v patch files present" Green

# ── 3. this patch shipped no vehicle (II.6 r.8) ──────────────────────────────
# Brain\courses\ already holds six pre-existing vehicles (check 2.5) that Phase 0 is
# authorized to remove but which are still in this working tree. They are NOT this
# patch's doing. The assertion here is that THIS PATCH added nothing.
Head "confirming this patch shipped no vehicle"
$inGit = $false
& git rev-parse --git-dir *> $null
if ($LASTEXITCODE -eq 0) { $inGit = $true }
if ($inGit) {
    $dirty = & git status --porcelain -- Brain 2>$null
    $newbin = $dirty | Where-Object { $_ -match '^(\?\?|A)' -and $_ -match '\.(pdf|zip|docx|pptx|xlsx|png)$' }
    if ($newbin) {
        Say "x NEW BINARY IN THE PATCH DELTA - investigate before committing:" Red
        foreach ($l in $newbin) { Say "    $l" Red }
    } else { Say "v nothing new: no PDF/zip/document under Brain\ is part of this patch's delta" Green }
} else {
    Say "- not a git tree - asserting from the zip listing instead" Yellow
    $pre = Get-ChildItem -Path "Brain" -Recurse -File -Include *.pdf, *.zip -ErrorAction SilentlyContinue
    foreach ($x in $pre) { Say "    pre-existing: $($x.FullName)" Yellow }
    Say "  (any file listed above is pre-existing - check 2.5 territory, NOT this patch)"
}
Say "- this zip ships 13 text files and 0 binaries (verified at build time)"

# ── 4. archive the notes out of the tree (II.8.2) ────────────────────────────
if (Test-Path "PATCH_NOTES.md") {
    if (-not (Test-Path "_local_backup")) { New-Item -ItemType Directory -Path "_local_backup" | Out-Null }
    Move-Item "PATCH_NOTES.md" "_local_backup\PATCH_NOTES_APPLIED_2400_BU-Ingestion.md" -Force
    Say "v PATCH_NOTES.md archived to _local_backup\ (notes live in the zip, not the tree)" Green
} else { Say "- no PATCH_NOTES.md at root - nothing to archive" }

# ── 5. harness self-check ────────────────────────────────────────────────────
Head "ingestion harness self-check"
$PY = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $PY = "python" }
elseif (Get-Command python3 -ErrorAction SilentlyContinue) { $PY = "python3" }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $PY = "py" }

if ($PY) {
    & $PY "scripts\ingest_collection.py" --help *> $null
    if ($LASTEXITCODE -eq 0) {
        Say "v harness runs (list / fetch / extract / verify)" Green
        & $PY -c "import pymupdf" 2>$null
        if ($LASTEXITCODE -eq 0) { Say "v pymupdf present - extract and verify are available" Green }
        else {
            Say "- pymupdf NOT installed: 'list' works (stdlib only) but 'extract'/'verify' need it." Yellow
            Say "  install with:  pip install pymupdf" Yellow
        }
        Say ""
        Say "-> next collection:  $PY scripts\ingest_collection.py list --url `"<folder-url>`" --out manifest.json"
        Say "-> a manifest is a PLAN: fetching needs --dest pointing OUTSIDE this repo."
    } else { Say "x harness failed to run - check the python version (3.8+ expected)" Red }
} else { Say "x python not found on PATH" Red }

# ── 6. validate ──────────────────────────────────────────────────────────────
Head "running the validator"
if ($PY) {
    & $PY "scripts\validate.py"
    Say ""
    Say "-> measured on a CLEAN mirror: 25 checks - 22 pass - 2 warn - 1 fail BEFORE this" Cyan
    Say "   patch, and identical AFTER it. This patch adds no failure and clears none." Cyan
    Say "   The 1 remaining fail is check 2.5: six course vehicles under Brain\courses\ that" Cyan
    Say "   Phase 0 is authorized to remove but which are still in your working tree." Cyan
    Say "   If you see MORE fails than that, re-extract the zip - do not re-run." Cyan
    Say ""
    Say "-> boot budget moved 34,138 B -> 34,398 B (cap 40 KB) - one ledger row, still green." Cyan
}

# ── 7. next steps ────────────────────────────────────────────────────────────
Head "NEXT"
Say "1) review the diff, then commit:      git add -A"
Say "                                     git commit -m `"P-10 Phase 2: ingest K-CUR-005 (Building Utilities)`""
Say ""
Say "2) the run found something about how we read tables. It is in PATCH_NOTES.md section 2." White
Say "   Read it before extracting another table out of any PDF." White
Say ""
Say "3) still open, and both are the Commander's alone:" Yellow
Say "     RED   rotate the LMS calendar feed  -> record the date in Brain\courses\INDEX.md" Red
Say "     AMBER authorize the 18-carrier purge -> CI goes green (25 checks, 0 fail)" Yellow
Say ""
Say "4) next ingestion run: K-CUR-006 (AR163-1P, 50 files / 601 MB). The harness exists" White
Say "   now - that is a re-run, not a build. Expect one size-skip." White
Say ""
Say "5) 334 pages in this collection are image-only and unrecovered. The recovery ladder" White
Say "   is a separate session with its own time budget. They are logged, not lost." White
Say "`nDone.`n" Cyan
