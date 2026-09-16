# Temporal Media Cues — Validation Battery (S-2-VIDEO Phases B–D)

**Purpose:** land IP-Video-01 Phases B–D as in-repo cue/doctrine machinery per desk's 8 amendments + Gap-Report Domain-3 merge per Desk Directive S-2-VIDEO 2026-09-16 base d9e9065 v3.10.22

**NOT in this tranche:** Phase E (heavy perception implementation — needs separate desk verdict + Commander countersign) and Phase-R (live empirical test — needs Commander's own word + one supplied test clip) per S-2-VIDEO §III non-goals

**Pinned interfaces (AMEND-4) fixed:**
- catalog 42 records (now 46 with video cues) — witness cue/CUE_CATALOG.json
- autopilot-cues — cue/autopilot-cues.md
- lexicon — cue/commander-lexicon.md
- v0.2 schema — schemas/cue_card.schema.json radiation.cue_card/0.2
- lint — scripts/cue_resolver.py --lint green
- hostile suites — evals/hostile/ 5 fixtures
- 32-tool registry — tools/TOOL_REGISTRY.json 32 tools
- 5 CAPABILITY_PROFILEs — agents/*/CAPABILITY_PROFILE.md ×5
- OPEN_SOURCES §12 — docs/OPEN_SOURCES.md §12 TOOLBOX vision precedent
- TOOLBOX vision precedent — docs/TOOLBOX.md row Image-only PDFs ocrmypdf + vision models

**State ladder (AMEND-7):** `perceived | derived | transcript_only | frames_only | inaccessible` with rule temporal artifact ALWAYS reports its state by name — never "I watched the video." — witness cue/TEMPORAL_MEDIA_PERCEPTION.md §I + DESK_DIRECTIVE_S2_VIDEO_2026-09-16.md:14

**Lineage convention (Domain-3 merge):** provenance chain `ORIGINAL → frame/audio transcript → translation → summary → claim` becomes named lineage block convention extending existing `ingest → ANNOT → TRI → CARD` card lineage (witness precedent: 09-nota/CARD_001_bp344-accessibility.md Lineage: field)

**Custody + dependency law (AMEND-8 + AMEND-5):**
- II.6 custody: video/audio binaries never enter repo; session-local, delete-the-binary, extract is only survivor (`find …*.mp4/mov = 0`)
- LAW-2 mirror: no heavy dependencies — no ffmpeg-whisper-style ambition embedded anywhere, no external media toolchain invoked or required by repo machinery. External perception tools where mentioned are TOOLBOX-grade DATA at [O], never wiring. Phase E tooling decisions explicitly deferred.

**Validation battery per AMEND-7 measurable:**
- Positive triggers asserting machinery fires ONLY on temporal-media intent — see positive_triggers.json
- Negative fixtures proving zero false-triggers across full existing suite (42-cue catalog + hostile suite stay clean — rerun and paste) — see negative_triggers.json
- Resolver --lint green with new rows — `python3 scripts/cue_resolver.py --lint` → {"issues": [], "ok": true} cue_count 46
- TestCase-law tests for new vectors — tests/test_temporal_media_cues.py TestCase classes only, 143 → 143+Y

**House law P-19-fix:** unittest.TestCase only — bare functions are not tests; discover count must move by exactly its vectors, before/after pasted.
