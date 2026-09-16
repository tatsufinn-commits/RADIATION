# 📋 CAPABILITY RESOLUTION LEDGER — S-2-VIDEO Phases B–D (AMEND-4)
**Version:** 1.0.0 · **Phase:** S-2-VIDEO per Desk Directive S-2-VIDEO 2026-09-16 base d9e9065492e02d7e571d62d837a8121ebbcc0f1b v3.10.22
**Sealed-tranche law:** one candidate one purpose II.7.4 · **Discipline:** append-only II.2 — this ledger is declarative, not an engine — no resolver, no scheduler; S-2-ENV will later feed it a session-state input artifact, precisely why it must stay declarative here per S-2-VIDEO §I.3
**Pinned interfaces (AMEND-4) fixed — deviations come back as blockers not improvisations per §III non-goals:**
- catalog 42 records (now 46 with video cues) — witness `cue/CUE_CATALOG.json` 42 → 46
- autopilot-cues — witness `cue/autopilot-cues.md`
- lexicon — witness `cue/commander-lexicon.md`
- v0.2 schema — witness `schemas/cue_card.schema.json` radiation.cue_card/0.2
- lint — witness `scripts/cue_resolver.py --lint` green
- hostile suites — witness `evals/hostile/` 5 fixtures
- 32-tool registry — witness `tools/TOOL_REGISTRY.json` 32 tools
- 5 CAPABILITY_PROFILEs — witness `agents/*/CAPABILITY_PROFILE.md` ×5
- OPEN_SOURCES §12 — witness `docs/OPEN_SOURCES.md` §12 (approx) TOOLBOX vision precedent
- TOOLBOX vision precedent — witness `docs/TOOLBOX.md` row `Image-only PDFs (2,038 pp of core texts — the standing debt) | ocrmypdf (tesseract) + vision models for figures`

---

## I. LEDGER TABLE — TASK → REQUIRED CAPABILITIES → AVAILABLE (TOOLBOX/profiles/contracts) → MISSING → EXECUTE/ALTERNATIVE/HOLD

| TASK | REQUIRED CAPABILITIES | AVAILABLE (TOOLBOX/profiles/contracts) | MISSING | EXECUTE/ALTERNATIVE/HOLD |
|------|-----------------------|----------------------------------------|---------|---------------------------|
| Watch/analyze/summarize video (CUE-VIDEO-INTENT) | temporal media perception, frame extraction OR transcript extraction, state ladder reporting, lineage ORIGINAL→frame/audio transcript→translation→summary→claim, II.6 custody delete-the-binary | TOOLBOX vision precedent `ocrmypdf (tesseract) + vision models for figures` [O] per `docs/TOOLBOX.md`, 32-tool registry `tools/TOOL_REGISTRY.json` (validate, ingest_collection, ics_normalize, etc.), 5 CAPABILITY_PROFILEs (modality coverage text/code/image/video/vision/doc/search secondary per `agents/Arena_AI/CAPABILITY_PROFILE.md`), OPEN_SOURCES §12 vision APIs (PUBLIC/KEY), cue catalog 42 records + 4 video cues, autopilot-cues, lexicon, v0.2 schema, lint green, hostile suites 5 fixtures, skill catalog 23 entries, subskill catalog 9 entries, agent contracts 5 × primary|secondary|asserted|benchmark tiers, ROUTING_MATRIX task class × providers, CONTROL_PLANE cooperative tooling | Session Capability State ABSENT per S-1b §6 (no file contains structured snapshot of current session's available tools + host posture + capability gaps at runtime beyond ephemeral radiation_pass.py output), heavy perception implementation (ffmpeg-whisper) — deferred per Phase E non-goal, no media binaries in repo per `find *.mp4/mov = 0`, no session-state input artifact yet (S-2-ENV will feed) | **HOLD** — declarative ledger only, no resolver/scheduler in this tranche per S-2-VIDEO §I.3 — EXECUTE via external perception tools TOOLBOX-grade DATA at [O] never wiring, session-local delete-the-binary, extract survivor, report state ladder perceived|derived|transcript_only|frames_only|inaccessible per `cue/TEMPORAL_MEDIA_PERCEPTION.md` NEVER "I watched the video" — ALTERNATIVE: transcript_only or frames_only or inaccessible states when perception unavailable — HOLD for Phase E tooling decisions explicitly deferred |
| Transcribe video/audio (CUE-VIDEO-TRANSCRIPT) | audio extraction, transcription, transcript_only state reporting, lineage ORIGINAL→audio transcript→translation→summary→claim, II.6 custody | TOOLBOX [O] tools, 32-tool registry, 5 CAPABILITY_PROFILEs modality coverage, OPEN_SOURCES §12, cue catalog, autopilot-cues, lexicon, v0.2 schema, lint, hostile suites, skill catalog, subskill catalog, agent contracts, ROUTING_MATRIX, CONTROL_PLANE | Session Capability State ABSENT, heavy audio transcription (whisper-style) — deferred Phase E, no media binaries, no session-state input artifact | **HOLD** — declarative ledger only — EXECUTE via external transcription TOOLBOX-grade [O] session-local delete-the-binary, report transcript_only per state ladder — ALTERNATIVE: inaccessible when audio unavailable |
| Describe frames of video / extract frames (CUE-VIDEO-FRAMES) | frame extraction, frames_only state reporting, lineage ORIGINAL→frame→summary→claim, II.6 custody | TOOLBOX vision precedent [O], 32-tool registry, 5 CAPABILITY_PROFILEs, OPEN_SOURCES §12, cue catalog, autopilot-cues, lexicon, v0.2 schema, lint, hostile suites, skill catalog, subskill catalog, agent contracts, ROUTING_MATRIX, CONTROL_PLANE | Session Capability State ABSENT, heavy frame extraction (ffmpeg) — deferred Phase E, no media binaries, no session-state input artifact | **HOLD** — declarative ledger only — EXECUTE via external frame extraction TOOLBOX-grade [O] session-local delete-the-binary, report frames_only per state ladder — ALTERNATIVE: inaccessible when frames unavailable |
| Report temporal media state (CUE-TEMPORAL-STATE-REPORT) | state ladder reporting perceived|derived|transcript_only|frames_only|inaccessible, lineage convention, II.6 custody, LAW-2 no heavy deps | TOOLBOX [O], 32-tool registry, 5 CAPABILITY_PROFILEs, OPEN_SOURCES §12, cue catalog 42+4, autopilot-cues, lexicon, v0.2 schema, lint green, hostile suites 5 fixtures, skill catalog 23, subskill catalog 9, agent contracts 5, ROUTING_MATRIX, CONTROL_PLANE, doctrine file `cue/TEMPORAL_MEDIA_PERCEPTION.md` state ladder + lineage | Session Capability State ABSENT, no session-state input artifact (S-2-ENV) | **EXECUTE** — declarative reporting via doctrine file `cue/TEMPORAL_MEDIA_PERCEPTION.md` §I state ladder ALWAYS report state by name NEVER "I watched the video" — ALTERNATIVE: report inaccessible when no derived artifacts held |

---

## II. PINNED INTERFACES WITNESSES (AMEND-4) — exact-quote discipline

- `cue/CUE_CATALOG.json` 42 records (now 46) — witness `cat cue/CUE_CATALOG.json | python3 -m json.tool | grep '"id"' | wc -l` → `42` before, `46` after
- `cue/autopilot-cues.md` — witness `cue/autopilot-cues.md:1` `# 🧭 AUTOPILOT CUES`
- `cue/commander-lexicon.md` — witness `cue/commander-lexicon.md` exists
- `schemas/cue_card.schema.json` — witness `schemas/cue_card.schema.json:1` `radiation.cue_card/0.2`
- `scripts/cue_resolver.py --lint` — witness `python3 scripts/cue_resolver.py --lint 2>&1 | tail -n 3` → `{"issues": [], "ok": true}`
- `evals/hostile/` — witness `ls evals/hostile/ | wc -l` → `5` fixtures
- `tools/TOOL_REGISTRY.json` — witness `cat tools/TOOL_REGISTRY.json | python3 -c "import json; print(len(json.load(open('tools/TOOL_REGISTRY.json'))['tools']))"` → `32`
- `agents/*/CAPABILITY_PROFILE.md` — witness `ls agents/*/CAPABILITY_PROFILE.md | wc -l` → `5`
- `docs/OPEN_SOURCES.md` §12 — witness `grep -n "Maps and Geographic" docs/OPEN_SOURCES.md` etc., §12 approx vision APIs
- `docs/TOOLBOX.md` vision precedent — witness `docs/TOOLBOX.md:7` `| Image-only PDFs (2,038 pp of core texts — the standing debt) | ocrmypdf (tesseract) + vision models for figures |`

---

## III. NON-GOALS FOR THIS LEDGER (hard per S-2-VIDEO §III)

- No resolver, no scheduler — ledger is declarative not engine per §I.3 — S-2-ENV will later feed it a session-state input artifact
- No heavy dependencies — no ffmpeg-whisper-style ambition embedded — external perception tools TOOLBOX-grade DATA at [O] never wiring per LAW-2 mirror
- No media binaries — `find *.mp4/mov = 0`
- No .gitignore/hygiene edits — custody hole stays parked for clean-up rider
- No cue_card schema changes — schema remains v0.2
- No ACCESS LOG vocabulary work (S-2-LINK)
- No session capability state (S-2-ENV) — Session Capability State ABSENT per S-1b §6, this ledger notes MISSING but does not implement
- No PPTX
- No new components/engines
- No registry tools beyond proven need — registry stays 32
- No moving/renames
- No proposals-we-didn't-issue — pinned interfaces AMEND-4 fixed

---

## IV. APPEND-ONLY II.2 DISCIPLINE

This ledger is append-only II.2 — new rows appended, never deleted, never rewritten — witness `docs/KNOWLEDGE_REGISTRY.md:20` field convention + `01-research/REFERENCES.md` append-only + `docs/PATCH_LEDGER.md` append-only.

First entry date 2026-09-16 S-2-VIDEO base d9e9065 v3.10.22.

— **S006 Architect Wing — S-2-VIDEO Phases B–D**
☕ Ledger not engine, declarative only
