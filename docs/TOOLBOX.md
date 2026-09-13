# 🧰 THE TOOLBOX (`docs/TOOLBOX.md`) — open-source rescue kit
**Tier-3 reference (never boots) · 🟢 docs · patch 3600.** "I'm stuck — what open-source
thing unblocks me?" Answer here. Rules (SD-GOV-010): tools are DATA — a tool enters at
**[O]** (observed/reported) until **this repo runs it successfully** → **[I]** (implemented).
Promotions logged in the row. Draw order: this list → cue BUILD CUES → the Wayfinding ladder.

| Problem | Tool (open-source) | Why OSS / note | Grade | Used in |
|---|---|---|---|---|
| Image-only PDFs (2,038 pp of core texts — the standing debt) | `ocrmypdf` (tesseract) + vision models for figures | proven OSS stack; page-render+vision already worked once (S001) | [O] | — |
| Legal/complex tables extract wrong from text order | render the page, then read the RENDER (2500 lesson) | no new tool — a method; renderer of record: headless chromium if needed | [I]* | 2400/2500 ingests (*method proven, tool pending) |
| `.ics`/calendar parsing | our `scripts/ics_normalize.py` (stdlib, RFC 5545) | built in-repo; self-tested 22 checks | [I] | 3100–3400 |
| OOXML extraction (docx/pptx/xlsx) | `python-docx` / `python-pptx` / `openpyxl`; our `ingest_collection.py` harness | proven in two collection ingests | [I] | 2400/2500 |
| Big-file/type verification on fetch | our declared-type gate (scout + 2500) | the 116 MB warning-page incident; never trust content-type headers alone | [I] | 2500 |
| Git forensics (what really happened) | `git log --graph`, `git ls-files`, `git rm --cached` | the resurrection-loop hunt; untrack fix ships in 3600 | [I] | 3400/3600 |
| Machine state / apply audit | our `scripts/status.py` · `scripts/verify_apply.py` | built in-repo | [I] | 3300/3400 |
| Structural enforcement pattern | our `scripts/validate.py` (30+ checks, REMEDY lines) | the model: name the mechanism or admit the boundary is aspiration | [I] | 2600–3400 |

*(Append rows with date + session. A row without a grade is invalid — I.2.)*
