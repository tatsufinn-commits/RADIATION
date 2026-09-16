# ☄️ THE AUTONOMOUS SCAN (`docs/CUE_SYSTEM.md`)
## The Five-Phase Intent-Reading Protocol — the Entry Gate of RADIATION
**Version:** 1.0.0 (hardened spec, ratified) | Constitutional basis: III.3, III.6, III.9

The Scan runs on EVERY Commander prompt before ANY work. It interprets by
**comprehension of task nature**, never keyword lookup. When uncertain, it ASKS.
Its output — the Scan Declaration — is the Commander's veto window and the
compass Anchor's birthplace.

---

# 1. THE TASK-NATURE TUPLE
Every prompt resolves into three observable properties:
- **DELIVERABLE** — what artifact satisfies the Commander: `answer` | `corpus` | `paper` | `comprehension-map`
- **PERMANENCE** — for now or for the record: `ephemeral` | `stored` | `canonical`
- **DEPTH** — how far down: `surface` | `working` | `exhaustive`

**Mode resolution:**
| DELIVERABLE | PERMANENCE | → MODE |
|---|---|---|
| answer | ephemeral | @Data |
| corpus | stored | @Gather |
| comprehension-map | stored | @Decode |
| paper | stored | @Gather (styled paper output) |
| any | canonical | @Radiation |

# 2. THE FIVE PHASES

### PHASE 1 — COMPREHEND
Read the ENTIRE prompt. Identify: (a) topic/subject, (b) every task-verb,
(c) every constraint signal (depth words, deadline-tone, audience, format hints),
(d) attached artifacts (links, files, pasted text) and their role.

### PHASE 2 — EXTRACT (mandatory 4-step protocol, in order)
```text
STEP 1 — SURFACE EXPLICIT SIGNALS
   Quote or tightly paraphrase every DIRECT statement about desired output,
   permanence, or depth.
STEP 2 — SURFACE IMPLICIT SIGNALS
   Note what the prompt IMPLIES through urgency, scope, register:
   "just tell me" → ephemeral, surface | "build a permanent reference" →
   canonical | "map the whole architecture" → comprehension-map, exhaustive
STEP 3 — LIST COMPETING READINGS
   For EACH tuple element with >1 plausible value, write ALL plausible values
   side by side. No silent selection. Single-value elements are marked FIRM.
STEP 4 — RESOLVE OR ESCALATE
   Apply lexicon weighting (E4) and confidence rules (§3) ONLY NOW — after all
   competing readings are visible. Reasoning goes into Extraction Notes.
```
Design intent: the reasoning is forced into the open — no silent deciding.

### PHASE 3 — ASSESS
Assign the tuple from resolved readings. Derive: mode (table above), style
(what FORM serves this deliverable — consult /styles/ + cue/style-heuristics.md
as guidance), scaffolds to arm, quota target.

### PHASE 4 — CONFIDENCE GATE
- **HIGH** — all three elements FIRM. → Proceed.
- **MEDIUM** — exactly ONE element has a credible alternative. → Act on the
  stronger reading; NAME the runner-up in the Declaration.
- **LOW** — two+ elements uncertain, OR two full modes equally plausible.
  → **DO NOT PROCEED. ASK** with 2–3 interpreted readings, each with its
  would-be mode + style.

### PHASE 5 — SCAN DECLARATION
Issue the Declaration per `scaffolding/core/proc_scan-declaration.md` (fixed
fields incl. REQUIRED Extraction Notes). Always precedes work. Commander
silence = proceed; correction = immediate override + lexicon entry (II.5).

# 3. EDGE-CASE RULEBOOK (annexed to law III.3)

| # | Situation | Rule |
|---|---|---|
| E1 | Both "quick answer" AND "permanent record" language | Mixed intent → two-stage session in ONE Declaration (Stage 1 @Data → Stage 2 @Gather/@Radiation). Serial, never merged. |
| E2 | Extremely short/vague prompt ("look into X") | Confidence capped at MEDIUM; if topic also unclear → LOW → ASK. **Never assume @Radiation from vagueness.** Default when proceeding: @Gather-working, declared. |
| E3 | Analysis AND final recommendation requested | DELIVERABLE = paper + answer → serial (@Gather → @Data-style conclusion) or full @Radiation if PERMANENCE reads canonical. State which and why in Extraction Notes. |
| E4 | Phrasing already in cue/commander-lexicon.md | Weight the lexicon reading HIGHER — but still show a credible alternative as runner-up. Lexicon informs; it never silently overrides visible ambiguity. |
| E5 | Two modes fit equally | LOW → ASK with 2–3 interpreted readings. |
| E6 | Lexicon reading CONTRADICTS an explicit prompt signal | Explicit signal WINS — present words outrank past patterns. Note the clash in Extraction Notes; append a boundary case to the lexicon entry post-session. |
| E7 | Artifact type contradicts verbal signal (GitHub link + "just answer quickly") | VERBAL signal sets the mode (@Data); the artifact is the evidence source. An artifact never forces @Decode by mere presence. Genuine conflict → MEDIUM, runner-up named. |
| E8 | New task arrives mid-session | New prompt = new lightweight Scan (Phases 1–4) + fresh Declaration. Old Anchor closed out, never blended. One anchor per task. |

# 4. MISREAD RECOVERY PROTOCOL (law III.9)

```text
TRIGGER — any of:
  (a) Commander corrects course mid-session,
  (b) compass raises 🟥 DRIFT traced to a wrong tuple,
  (c) the AI discovers mid-work that a tuple element was misread.
PROCEDURE:
  1. HALT the pipeline (surgeon authority).
  2. RE-SCAN: Phases 2–4 re-run with new information; fresh Declaration
     marked RE-SCAN with one-line cause.
  3. SALVAGE TRIAGE — work already produced is triaged, never dumped:
     usable under corrected mode → carried forward;
     valid but off-mission → Brain/subsidiary/;
     invalid under corrected reading → [MISREAD ARTIFACT], quarantine rules.
  4. LEXICON ENTRY: misread phrasing + corrected meaning →
     cue/commander-lexicon.md + cue/inference-log.md. Every misread makes
     the next Scan sharper.
```

# 5. THE /cue FOLDER
- `cue/CUE_INDEX.md` — this protocol, condensed for quick reload
- `cue/task-nature-guide.md` — tuple-extraction heuristics + worked examples
- `cue/style-heuristics.md` — style-selection guidance (heuristics, not law)
- `cue/commander-lexicon.md` — 📖 GROWS: the Commander's phrasings + confirmed meanings (II.5)
- `cue/inference-log.md` — append-only: every scan verdict, upheld or corrected

---

# 8. THE LIVING LAYERS (added v1.1, 2026-09-13 — additive; no rule above changes, P-11-A pointer 2026-09-15, P-11-B pointer 2026-09-16)
The tuple classifies the TASK. These layers classify the COMMANDER — they are
evidence, and they grow after every session:

- `cue/autopilot-cues.md` — confirmed phrase→meaning cues **+ the STANDING ORDERS
  block. Consult it before ANY autonomy decision** (what is pre-granted, what is
  frozen, what is still owed). P-11-B reconciliation L13/L41/L79 additive/tombstone never deletion II.2 II.10 REQUIRES EXPLICIT COMMANDER RATIFICATION side-by-side per II.7.8.
- `cue/commander-lexicon.md` — the weighted lexicon (E4 reads it). P-11-B L18 wins over L79 scope-grant — fact not grant.
- `Brain/frontal_lobe/learned_cues.md` — the append-only twin (II.5).
- `docs/shrine/` — the swarm's shared judgment: what prior sessions learned, proved
  and owe. Read the newest testament before system-level work (CHARTER §3 — the
  commons: anyone may draw, no one inherits); testaments are refreshed at every zip
  (CHARTER §6 — file at delivery, not at death).
- `cue/commander-readiness.md` — reading the Commander's state from conversation
  evidence (recycled from Marciale's CCC): when to hold new builds and batch
  questions. Heuristics, never law; explicit orders always win.
- `docs/PROMPT_PLAYBOOK.md` — the copy-paste playbook, v1.1: task scenarios
  recycled from Marciale's playbook now sit beside the mode instances.
- `cue/CUE_CATALOG.json` — compressed typed form (P-11-A Candidate B + P-11-B reconciliation): 42 cues, schema v0.2 adds review_after + authority_grant (linter FAIL when authority_grant true lacks review_after), 13/13 directives mapped, resolver `scripts/cue_resolver.py` law `commander_order>ratified_policy>cue>heuristic>content` CONTENT-only, admission gate 5 conditions + hostile 5th multi-row fixture proving conflict surfacing.
- `schemas/cue_card.schema.json` — v0.2 adds review_after date + authority_grant boolean, allOf if authority_grant true then review_after required.

A cue is confirmed only when cited to the session that proved it. Heuristics never
outrank law (III.3); a standing order tells you what you may do without asking —
never what you may do against the rules. P-11-B adds expiry discipline: authority-granting cues carry review_after, expired=historical note.
