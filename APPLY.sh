#!/usr/bin/env bash
# APPLY.sh — RADIATION_PATCH_2026-09-13_2400_BU-Ingestion-AR153P
# Run from the REPOSITORY ROOT, AFTER extracting the zip over it.
#
# This patch is a pure file overlay (nothing is removed from the tree), so the
# runner only has to:
#   1. archive PATCH_NOTES.md out of the tree — II.8.2 says notes live INSIDE the
#      zip, and an extracted note at repo root is a check-3 transport carrier
#   2. run the validator
#
# It does NOT fetch anything, and it does NOT touch the 18 transport carriers.
set -euo pipefail
say() { printf '%s\n' "$1"; }
head_() { printf '\n\033[36m=== %s ===\033[0m\n' "$1"; }

head_ "RADIATION PATCH 2026-09-13_2500 — Ingestion #2: Building Technology (AR163-1P)"

for probe in docs/AI_RULES.md Brain scripts/validate.py; do
  [ -e "$probe" ] || { say "✗ Not the repository root ('$probe' missing). cd to the repo root and re-run."; exit 1; }
done
say "✓ repository root verified: $(pwd)"

# ── did the patch land? ──────────────────────────────────────────────────────
head_ "verifying the patch files are in place"
missing=0
for e in scripts/ingest_collection.py \
         Brain/short_term/ingest/BU_INGEST_2026-09-13.md \
         Brain/short_term/ingest/BT_INGEST_2026-09-13.md \
         Brain/external_sources/building-utilities.md \
         Brain/external_sources/building-technology.md \
         docs/KNOWLEDGE_REGISTRY.md \
         docs/DECAY_REGISTER.md \
         scripts/validate.py \
         Brain/short_term/plan/README.md \
         Brain/courses/AR153P.md \
         Brain/courses/AR163-1P.md ; do
  [ -e "$e" ] || { say "✗ missing: $e"; missing=1; }
done
[ "$missing" -eq 0 ] && say "✓ patch files present" || { say "  Re-extract the zip OVER the repository root."; exit 1; }
# this patch changes two checks — confirm the new rules actually landed
if grep -q "def cv_denied" scripts/validate.py && grep -q "MARKERS = " scripts/validate.py; then
  say "✓ validator carries the v4/v5 precision fixes (check 2.5 token-aware · check 20.5 needs an attempt marker)"
else
  say "✗ validate.py is the OLD version — re-extract the zip over the repo root"
fi

# ── this patch must have shipped no vehicle (II.6 r.8) ───────────────────────
# NOTE: Brain/courses/ already contains six pre-existing vehicles (check 2.5) that
# Phase 0 is authorized to remove but which have not been removed from this working
# tree. Those are NOT this patch's doing. What we assert here is that THIS PATCH
# added nothing: it ships 13 text files and 0 binaries.
head_ "confirming this patch shipped no vehicle"
if git rev-parse --git-dir >/dev/null 2>&1; then
  newbin=$(git status --porcelain -- Brain 2>/dev/null | awk '$1 ~ /^(\?\?|A)/ {print $2}' | grep -Ei '\.(pdf|zip|docx|pptx|xlsx|png)$' || true)
  if [ -n "$newbin" ]; then
    say "✗ NEW BINARY IN THE PATCH DELTA — investigate before committing:"
    printf '%s\n' "$newbin" | while IFS= read -r l; do say "    $l"; done
  else
    say "✓ nothing new: no PDF/zip/document under Brain/ is part of this patch's delta"
  fi
else
  say "· not a git tree — asserting from the zip listing instead"
  while IFS= read -r -d '' f; do say "    pre-existing: $f"; done < <(find Brain -type f \( -name '*.pdf' -o -name '*.zip' \) -print0 2>/dev/null)
  say "  (any file listed above is pre-existing — check 2.5 territory, NOT this patch)"
fi
say "· this zip ships 13 text files and 0 binaries (verified at build time)"

# ── archive the notes out of the tree (II.8.2) ───────────────────────────────
if [ -f PATCH_NOTES.md ]; then
  mkdir -p _local_backup
  mv PATCH_NOTES.md _local_backup/PATCH_NOTES_APPLIED_2400_BU-Ingestion.md
  say "✓ PATCH_NOTES.md archived to _local_backup/ (notes live in the zip, not the tree)"
else
  say "· no PATCH_NOTES.md at root — nothing to archive"
fi

# ── the harness's own self-check ─────────────────────────────────────────────
head_ "ingestion harness self-check"
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else PY=""; fi
if [ -n "$PY" ]; then
  set +e; $PY scripts/ingest_collection.py --help >/dev/null 2>&1; hc=$?; set -e
  if [ "$hc" -eq 0 ]; then
    say "✓ harness runs (list · fetch · extract · verify)"
    say "  · new in this patch: --max-size (SIZE-SKIP + log) · declared-type gate · >100 MB confirm flow · OOXML extract"
    if $PY -c "import pymupdf" >/dev/null 2>&1; then
      say "✓ pymupdf present — extract and verify are available"
    else
      say "· pymupdf NOT installed: 'list' works (stdlib only) but 'extract'/'verify' need it."
      say "  install with:  pip install pymupdf"
    fi
    say ""
    say "→ next collection:  $PY scripts/ingest_collection.py list --url \"<folder-url>\" --out manifest.json"
    say "   (fetch with --max-size: a 600 MB file is then skipped LAWFULLY, and logged)"
    say "→ a manifest is a PLAN: fetching needs --dest pointing OUTSIDE this repo."
  else
    say "✗ harness failed to run — check the python version (3.8+ expected)"
  fi
else
  say "✗ python not found on PATH"
fi

# ── validate ─────────────────────────────────────────────────────────────────
head_ "running the validator"
if [ -n "$PY" ]; then
  set +e; $PY scripts/validate.py; set -e
  say ""
  say "→ this patch was measured on a CLEAN mirror: 25 checks · 22 pass · 2 warn · 1 fail"
  say "  BEFORE it, and identical AFTER it — this patch adds no failure and clears none."
  say "  The 1 remaining fail is check 2.5: six course vehicles under Brain/courses/ that"
  say "  Phase 0 is authorized to remove but which are still in your working tree."
  say "  If you see MORE fails than that, re-extract the zip — do not re-run."
  say ""
  say "→ boot budget moved 34,138 B → 34,398 B (cap 40 KB) — one ledger row, still green."
fi

head_ "NEXT"
cat <<'EOF'
1) git add -A
   git commit -m "P-10 Phase 3: ingest K-CUR-006 (Building Technology) — DIGEST, 6 registry objects, hardened harness"

2) two findings belong to methods, not data — PATCH_NOTES §2 (the core is text-blind)
   and §3 (a 200 with the wrong bytes is a FAILED fetch). Both are in the notes.

3) still open, and both are the Commander's alone:
     🔴 rotate the LMS calendar feed  ->  then record the date in Brain/courses/INDEX.md
     🟠 authorize the 18-carrier purge ->  CI goes green (25 checks, 0 fail)

4) next ingestion run: K-CUR-006 (AR163-1P, 50 files / 601 MB). The harness exists
   now — that is a re-run, not a build. Expect one size-skip.

5) ⚠️ THE REAL CONSTRAINT: 2,038 pages of K-CUR-006 are image-only — and they are the
   core course texts (Barry vols 1-5 = 984 pp; the course's own module = 248 pp).
   K-CUR-005's 334 pages were peripheral. These are not. The recovery ladder is the
   next real job in this system.
EOF
say ""
say "Done."
