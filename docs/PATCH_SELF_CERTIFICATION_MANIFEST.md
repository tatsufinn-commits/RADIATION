# Patch Self-Certification Manifest (WP-1 1.1)
**Basis:** Repo C template + Repo D teeth + DCO shape (facts+links only, prose rewritten per Rewrite-rule Law 5)
**Law:** Six ratified laws D029 · D1–D10 · FF-seal only · warn-and-justify · quarantine-before-delete · sequence as-written · raise-only ratchet · WP-D single gate
**Checklist:** Per 1.6 checklist scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md — this file governs patch certification
**Glossary:** docs/GLOSSARY.md defines Patch, Manifest, DCO, Return Rule per 1.3
**Teeth:** Incomplete manifests are RETURNED, not queued — Commander approval is only sign-off (single-Commander model) per 1.1

## Template — Six Checkboxes with ✅/❌ Example Each

**Raise-only — may not be tuned downward later per Law 2 — score/floor fields carry ratchet note**

### PATCH SELF-CERTIFICATION MANIFEST — Template v1

```
=== PATCH SELF-CERTIFICATION MANIFEST ===
Patch: RADIATION_PATCH_YYYY-MM-DD_HHMM_<desc>.zip
Branch: <branch> @ <sha> — ONE commit per D028 FF-form
Base: <base_sha> == lane-open main per execution header — verified YES/NO
Author: <id> — honest author identity per D1

Checkboxes (six — each with ✅/❌ example):

[ ] 1. Sequence as-written — WP-1→WP-2.3→WP-4 per Law 1
    ✅ Example: "Sequence verified — WP-1 first step of sequence per D029 Law 1 — checklist 1.6 exists"
    ❌ Example: "Skipped 1.6, built 1.2 first — sequence violated"

[ ] 2. Raise-only ratchet — no floor tunable downward per Law 2
    ✅ Example: "No floor tunable downward — data paths section carries raise-only note per Law 2"
    ❌ Example: "Lowered boot-byte cap from 40 to 30 — ratchet violated"

[ ] 3. Warn-and-justify — every gate speaks warning+justification never auto-reject per Law 3
    ✅ Example: "Gate docs warn + justification — evidence came from warnings per §4"
    ❌ Example: "Auto-rejected incomplete manifest — warn-and-justify violated"

[ ] 4. Quarantine-before-delete — decay proposes Commander disposes per Law 4 — banners not deletions
    ✅ Example: "Superseded spec got STALE banner per 1.6 checklist — nothing deleted per Law 4"
    ❌ Example: "Deleted old AGENTS.md section — quarantine-before-delete violated"

[ ] 5. Rewrite-rule — unlicensed source basis lands as facts+links only prose rewritten never quoted per Law 5
    ✅ Example: "Repo D basis rewritten as facts+links — pointer to Patch protocol — prose rewritten per Law 5"
    ❌ Example: "Quoted Repo D refusal text verbatim — rewrite-rule violated, AI-refusal content REJECTED per §4"

[ ] 6. WP-D single gate — zero network/venue/SaaS in WP-1 per Law 6 — venue mentions research-only
    ✅ Example: "Zero network — no new workflows steps hit net — venue mentions marked research-only per Law 6"
    ❌ Example: "Added live venue API call in WP-1 — WP-D single gate violated"

DCO Sign-off: Signed-off-by: <author> <email> — DCO shape per 1.1

Teeth: Incomplete manifests are RETURNED not queued — Commander approval only sign-off — return-rule recorded here per 1.1

Battery: validate 0 fail · gate 0 findings · Ran 195 OK · preflight 0 findings · render_docs ✓ · verify_apply strict FAIL-CLASS none · stable re-run ✓ per §4

Laws acknowledged: D1–D10 · six ratified laws D029 · FF-seal only

ABSENT declarations: [...]

=== END MANIFEST ===
```

## Teeth — Return Rule Recorded (1.1)

**Incomplete manifests are RETURNED, not queued** — per 1.1 teeth, Commander approval is only sign-off (single-Commander model). Any Patch arriving without complete six-checkbox manifest is RETURNED to Architect with note "incomplete manifest — six checkboxes required per 1.1 — RETURNED not queued". No queue, no silent fix, no auto-approval. This rule is recorded in 1.6 checklist and here.

## Three Exemplar Filled Manifests (Acceptance per 1.1)

### Exemplar 1 — WP-1 1.6 Checklist (PASS)

```
=== PATCH SELF-CERTIFICATION MANIFEST ===
Patch: RADIATION_PATCH_2026-09-22_0001_WP1-1.6-checklist.zip
Branch: wp1/contracts-and-docs-2026-09-22 @ abc123 — ONE commit
Base: f086392a9cc443e374541077c5a054938e0b337a == lane-open main YES
Author: S012 Architect — honest author identity

[✅] 1. Sequence as-written — WP-1 first step per D029 Law 1 — 1.6 built first per directive §1 ruling
[✅] 2. Raise-only ratchet — no floor lowered — checklist carries raise-only note
[✅] 3. Warn-and-justify — checklist documents gates as warning+justification never auto-reject per Law 3
[✅] 4. Quarantine-before-delete — checklist specifies STALE banners not deletions per Law 4
[✅] 5. Rewrite-rule — Repo E prompt-composition governance facts+links only prose rewritten per Law 5
[✅] 6. WP-D single gate — zero network — venue pointers none per Law 6

DCO Sign-off: Signed-off-by: S012 Architect <architect@radiation.local>
Teeth: RETURNED not queued honored — complete manifest
Battery: validate 0 fail · gate 0 · Ran 195 OK · preflight 0 · render_docs ✓ · verify_apply strict FAIL-CLASS none
Laws: D1–D10 · D029 six laws
ABSENT: none
=== END MANIFEST ===
```

### Exemplar 2 — WP-1 1.3 Glossary (PASS)

```
=== PATCH SELF-CERTIFICATION MANIFEST ===
Patch: RADIATION_PATCH_2026-09-22_0002_WP1-1.3-glossary.zip
Branch: wp1/contracts-and-docs-2026-09-22 @ def456 — ONE commit
Base: f086392a9cc443e374541077c5a054938e0b337a == YES
Author: S012 Architect

[✅] 1. Sequence — 1.3 second per §1 ruling additive before edits
[✅] 2. Raise-only — glossary pure-additive no floor lowered
[✅] 3. Warn-and-justify — glossary entries warn + justification via Avoid anti-terms per Law 3
[✅] 4. Quarantine-before-delete — glossary pure-additive nothing deleted per Law 4
[✅] 5. Rewrite-rule — Repo E CONTEXT.md term+definition+Avoid facts+links only prose rewritten per Law 5
[✅] 6. WP-D single gate — zero network per Law 6

DCO Sign-off: Signed-off-by: S012 Architect <architect@radiation.local>
Teeth: complete — queued for Commander seal
Battery: validate 0 fail · gate 0 · Ran 195 OK · preflight 0 · render_docs ✓
Laws: D1–D10 · D029
ABSENT: none
=== END MANIFEST ===
```

### Exemplar 3 — WP-1 1.4 Agent Policies (PASS with existing check)

```
=== PATCH SELF-CERTIFICATION MANIFEST ===
Patch: RADIATION_PATCH_2026-09-22_0003_WP1-1.4-agent-policies.zip
Branch: wp1/contracts-and-docs-2026-09-22 @ ghi789 — ONE commit
Base: f086392a9cc443e374541077c5a054938e0b337a == YES
Author: S012 Architect

[✅] 1. Sequence — 1.4 third per §1 ruling additive before edits
[✅] 2. Raise-only — no floor lowered — policy files ≤30 lines carry raise-only note in data paths
[✅] 3. Warn-and-justify — existence check scripts/agent_policy_check.py warns + justification per Law 3
[✅] 4. Quarantine-before-delete — additive only no deletions per Law 4
[✅] 5. Rewrite-rule — Repo D format only facts+links only prose rewritten AI-refusal REJECTED per §4 hazard per Law 5
[✅] 6. WP-D single gate — zero network — existence check stdlib only per Law 6

DCO Sign-off: Signed-off-by: S012 Architect <architect@radiation.local>
Teeth: complete
Battery: validate 0 fail · gate 0 · Ran 195 OK · preflight 0 · render_docs ✓ · agent_policy_check PASS
Laws: D1–D10 · D029
ABSENT: none
=== END MANIFEST ===
```

## Laws acknowledged
D1–D10 · six ratified laws D029 · FF-seal only · sequence as-written · raise-only ratchet · warn-and-justify · quarantine-before-delete · rewrite-rule · WP-D single gate · pure-additive where required · checklist citation per 1.6

## Research-only venue pointers
None — zero network/venue/SaaS in WP-1 per Law 6 — any venue mention marked research-only
