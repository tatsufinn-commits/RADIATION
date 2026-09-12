# 🧰 THE OPEN-SOURCE TOOLBOX (`Brain/cerebellum/toolbox.md`)
## Procedural Arsenal — tools any session can use on the repository & collections
**Constitutional basis:** II.6 (cerebellum), write-after-proof honored via STATUS column
**Purpose (Commander's order):** weaponize tool knowledge; kill mid-flight discovery time. S001 burned turns discovering tesseract existed — future sessions read this FIRST.

> **STATUS meanings:** ✅ PROVEN = succeeded in a cited live session. 🟡 CANDIDATE = standard, widely-available tooling; promote to PROVEN with session citation after first field success. Availability check commands included — run them before relying on a tool; most sandboxes allow `apt`/`pip` install.

## 1. REPOSITORY INTERACTION (GitHub)
| Tool | What it does for us | Fast usage | Status |
|---|---|---|---|
| `git` (shallow clone) | Fetch the whole repo in seconds without history weight | `git clone --depth 1 https://github.com/tatsufinn-commits/RADIATION.git` | ✅ PROVEN (S001 boot; Architect sessions) |
| `git sparse-checkout` | Pull ONLY needed folders (e.g. just docs/ + Brain/) — boot-speed weapon for small-context sessions | `git clone --depth 1 --filter=blob:none --sparse <url> && git sparse-checkout set docs Brain` | 🟡 CANDIDATE |
| raw.githubusercontent.com | Fetch ONE file with zero clone — fastest possible single-file read | `https://raw.githubusercontent.com/tatsufinn-commits/RADIATION/main/docs/.readme` | ✅ PROVEN (S001 fetched README this way) |
| GitHub REST API | List tree/commits/releases as JSON without cloning | `https://api.github.com/repos/tatsufinn-commits/RADIATION/git/trees/main?recursive=1` | 🟡 CANDIDATE |
| `gh` (GitHub CLI) | Issues, PRs, releases from the shell; useful if the Commander ever grants a token for automation | `gh repo view tatsufinn-commits/RADIATION` | 🟡 CANDIDATE (needs auth for writes — Commander-gated) |
| `zip` / `unzip` | Patch transport per II.7 | `zip -r PATCH.zip .` | ✅ PROVEN (every Patch to date) |

## 2. DOCUMENT EXTRACTION (the S001 recovery ladder, now doctrine)
**THE LADDER — try in order, log honestly, never fabricate (I.1):**
`1) embedded text layer → 2) vision read of rendered pages → 3) install OCR → 4) SIZE-SKIPPED`

| Tool | What it does | Fast usage | Status |
|---|---|---|---|
| PyMuPDF (`pip install pymupdf`) | PDF text extraction + render pages to PNG (ladder steps 1-2); fast, handles huge PDFs page-by-page | `import fitz; doc=fitz.open(f); page.get_text()` / `page.get_pixmap()` | ✅ PROVEN (S001: rendered 29 slide pages) |
| Poppler utils (`apt install poppler-utils`) | `pdftotext` (text layer), `pdftoppm` (render), `pdfinfo` (page count BEFORE fetching — size recon) | `pdfinfo file.pdf`, `pdftotext -f 1 -l 30 file.pdf` | 🟡 CANDIDATE |
| Tesseract OCR (`apt install tesseract-ocr`) | Reads text out of IMAGES — the rescue for scanned/image-only decks | `tesseract page.png out.txt` | ✅ PROVEN (S001: recovered 3 image-only decks, ~1,600+ words/deck; v5.5.0) |
| LibreOffice headless (`apt install libreoffice`) | Converts pptx/ppt/docx/xlsx → PDF or text; the key for Office files in collections | `libreoffice --headless --convert-to pdf file.pptx` | 🟡 CANDIDATE |
| `python-pptx` / `python-docx` / `openpyxl` (pip) | Direct text/table extraction from Office XML files without conversion | `from pptx import Presentation; [s.text for s in slide.shapes...]` | 🟡 CANDIDATE |
| pandoc (`apt install pandoc`) | Universal document converter (html/docx/md/…) | `pandoc file.html -t plain` | 🟡 CANDIDATE |

## 3. DRIVE COLLECTION ACCESS (Restraint Doctrine ALWAYS applies)
| Tool | What it does | Fast usage | Status |
|---|---|---|---|
| Drive direct-download URL | Fetch ONE file by its Drive ID — the surgical fetch the 3/6 budget wants | `https://drive.google.com/uc?export=download&id=<FILE_ID>` | ✅ PROVEN (S001 downloaded 8 Planning files) |
| `gdown` (`pip install gdown`) | Robust Drive downloader — handles big-file confirmation pages that plain curl fumbles | `gdown <FILE_ID>` or `gdown --fuzzy <share-url>` | 🟡 CANDIDATE |
| `curl`/`wget` with `-r` byte ranges | Partial download of huge files — recon the first MBs instead of swallowing 601 MB | `curl -r 0-5000000 -L <url> -o head.pdf` | 🟡 CANDIDATE |
| `rclone` | Bulk Drive sync — ⚠️ FORBIDDEN for collections (no-mirroring rule II.6.5); listed only so sessions know NOT to reach for it | — | 🚫 PROHIBITED for collections |

## 4. SPEED & SEARCH UTILITIES
| Tool | What it does | Fast usage | Status |
|---|---|---|---|
| `grep -rn` / ripgrep `rg` | Instant search across the whole repo — find any law/rule/claim in ms | `grep -rn "Restraint" docs/ Brain/` | ✅ PROVEN (Architect audits) |
| `jq` | Parse GitHub API JSON | `curl ... \| jq '.tree[].path'` | 🟡 CANDIDATE |
| `find` + `wc` | Inventory/verify file counts after patches | `find . -type f -not -name .gitkeep \| wc -l` | ✅ PROVEN (every consolidation) |
| Python one-file edits | Surgical append/replace on ledgers without editor round-trips | `python3 - <<EOF` heredoc pattern | ✅ PROVEN (all Architect patch applications) |

## 5. SPEED DOCTRINE (how these compound)
1. **Recon before fetch:** `pdfinfo`/manifest sizes decide the ladder rung BEFORE spending budget.
2. **Single-file beats clone; sparse beats full; shallow beats history.**
3. **Install-on-need is lawful:** sandboxes allow apt/pip — a missing tool is a 30-second problem, not a wall (S001 precedent).
4. **Promote on proof:** first session to field-prove a 🟡 CANDIDATE appends the session citation and flips it to ✅ — this file gets sharper every run (II.5 spirit).

*(Append-only below the line for promotions and new tools; date + session citation mandatory.)*
---
