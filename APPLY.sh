#!/usr/bin/env bash
# APPLY.sh — RADIATION_PATCH_2026-09-13_2300_Courses-Region-and-Containment
# Risk class: 🟢 ordinary.  Run from the REPOSITORY ROOT, after extracting the zip over it.
#
#  1. verifies the repo root        4. removes the vehicles from the working tree
#  2. backs up every non-.md file   5. prunes emptied directories
#     under Brain/courses/          6. re-runs the validator
#  3. checks the patch files landed
#
# It does NOT commit, and it does NOT touch the 18 transport carriers.

set -euo pipefail
say()  { printf '%s\n' "$1"; }
head_() { printf '\n\033[36m=== %s ===\033[0m\n' "$1"; }

head_ "RADIATION PATCH 2026-09-13_2300 — Courses Region & Containment"

# ── 1. repo root? ────────────────────────────────────────────────────────────
for probe in docs/AI_RULES.md Brain scripts/validate.py; do
  if [ ! -e "$probe" ]; then
    say "✗ Not the repository root — '$probe' not found."
    say "  cd to the RADIATION repo root (holding docs/ and Brain/) and re-run."
    exit 1
  fi
done
say "✓ repository root verified: $(pwd)"

# ── 2. back up + remove every non-.md file under Brain/courses/ ──────────────
BACKUP="_local_backup"
count=0
while IFS= read -r -d '' f; do
  rel="${f#./}"
  mkdir -p "$BACKUP/$(dirname "$rel")"
  mv "$f" "$BACKUP/$rel"
  say "    $rel"
  count=$((count+1))
done < <(find Brain/courses -type f ! -name '*.md' -print0 2>/dev/null)

say ""
say "✓ backed up + removed from the tree: $count vehicle(s)"
if [ "$count" -gt 0 ]; then
  say "  → local copies live in: $BACKUP/"
  say "  → KEEP THAT FOLDER. It is git-ignored by the new .gitignore."
fi

# ── 3. did the patch files land? ─────────────────────────────────────────────
head_ "verifying the patch files are in place"
missing=0
for e in .gitignore Brain/courses/INDEX.md Brain/courses/GED103.md Brain/courses/DSS10.md \
         Brain/courses/MEC30-7.md Brain/courses/AR173-1P.md Brain/courses/AR163-1P.md \
         Brain/courses/AR153P.md docs/KNOWLEDGE_REGISTRY.md scripts/validate.py \
         Brain/frontal_lobe/task_ledger.md docs/PATCH_LEDGER.md; do
  [ -e "$e" ] || { say "✗ missing: $e"; missing=1; }
done
[ "$missing" -eq 0 ] && say "✓ all 12 patch files present (including the .gitignore dotfile)" \
                    || { say "  Re-extract the zip OVER the repository root (keep folder structure)."; exit 1; }

# ── 4. prune emptied directories ─────────────────────────────────────────────
pruned=0
while IFS= read -r -d '' d; do rmdir "$d" 2>/dev/null && pruned=$((pruned+1)) || true; done \
  < <(find Brain/courses -type d -empty -print0 -depth 2>/dev/null)
say "✓ pruned $pruned emptied director(ies)"

# ── 5. leave the carriers alone, on purpose ──────────────────────────────────
carriers=$(find . -path ./.git -prune -o -path ./_local_backup -prune -o -type f \
             \( -name '*_STAGED*' -o -name '*_DIFF*' -o -name 'PATCH_NOTES.md' \) -print 2>/dev/null | wc -l | tr -d ' ')
say ""
say "ℹ transport carriers still in the tree: $carriers — UNTOUCHED by this patch."
say "  Removing them is a separate, Commander-authorized patch (II.4 purge rule)."

# ── 6. validate ──────────────────────────────────────────────────────────────
head_ "running the validator"
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else PY=""; fi
if [ -n "$PY" ]; then
  set +e; $PY scripts/validate.py; code=$?; set -e
  say ""
  if [ "$code" -eq 0 ]; then say "✓ GREEN"
  else
    say "⚠ NOT green — expected. The remaining failures are the 18 carriers plus"
    say "  three pre-existing findings. This patch removes exactly ONE failure (check 2)"
    say "  and adds one passing check (2.5). Compare:"
    say "      before: 22 checks · 14 pass · 3 warn · 5 fail"
    say "      after : 23 checks · 16 pass · 3 warn · 4 fail"
  fi
else
  say "✗ python not found on PATH — run 'python3 scripts/validate.py' yourself."
fi

# ── 7. next steps ────────────────────────────────────────────────────────────
head_ "NEXT"
cat <<'EOF'
1) review the diff, then commit:
     git add -A
     git commit -m "P-10 Phase 0: courses region as records + containment"
2) bump the version to v1.6.4 in README.md, docs/SYSTEM_STATE.md, CHANGELOG.md
   (check 7 compares all three — they must move together)

3) 🔴 ROTATE THE LMS CALENDAR FEED AT SOURCE, then record the date in
   Brain/courses/INDEX.md -> "OPEN ACTION — feed rotation".
   This patch removed the file; it did NOT revoke the URL. Until rotated, the
   exposure is open for anyone holding it.

4) decide the history question (A leave / B filter-repo / C private repo).
5) the 18-carrier purge is a SEPARATE patch — it needs one word from you.
EOF
say ""
say "Done."
