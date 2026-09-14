# 🧰 THE TOOLBOX (`docs/TOOLBOX.md`) — open-source rescue kit
**Tier-3 reference (never boots) · 🟢 docs · patch 3600.** "stuck — what open-source
thing unblocks the task?" Answer here. Rules (SD-GOV-010): tools are DATA — a tool enters at
**[O]** (observed/reported) until **this repo runs it successfully** → **[I]** (implemented).
Promotions logged in the row. Draw order: the **bank** (`docs/OPEN_SOURCES.md` — the Commander's 50-category source catalog, @Fetch's library) → this list ([I] tools we've run) → cue BUILD CUES → the Wayfinding ladder.

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
| CAP record verification (declared/observed/verified, sealed digests) | our `scripts/cap_verify.py` + `schemas/cap_record.schema.json` (check 35) | external PoC proven first (6/6 · 5/5), then admitted — research memo Phase C gate | [I] | 4800 |
| Read-only capability probe + host posture profiles | our `scripts/cap_probe.py` + `schemas/host_profile.schema.json` (check 36) | Phase C-2: declare posture, observe reality, never conflate; C-4 redaction policy executed | [I] | 4900 |
| Control plane (two-key resolver · bounded executor · tamper-evident receipts) | our `radiation_core/control_plane.py` + allowlist-as-data (check 37) | landed by ratification (5000), boundary made true by the excellence review (5100) | [I] | 5000/5100 |

*(Append rows with date + session. A row without a grade is invalid — I.2.)*
