# 📖 THE PROMPT PLAYBOOK (`docs/PROMPT_PLAYBOOK.md`)
## Mode-Classified Copy-Paste Instances for the Commander
**Version:** 1.0.0 | How to use: find your scenario, copy the box, paste into any AI chat.

---

# BOOT

### 0.1 — Cold-Start Cockpit (boot any new AI)
```text
Read this repository, and act as per .readme
Repository: https://github.com/tatsufinn-commits/RADIATION.git

[Optional immediate task:]
@[MODE] | STYLE: [style or AUTO] | TOPIC: [your task]
```

---

# ☢️ @Radiation INSTANCES

### 1.1 — Full-Spectrum Research Run
```text
@Radiation | STYLE: [research / thesis / AUTO] | TOPIC: [subject]
Execute the full nine-skill pipeline. Curator passive is ON — ingest everything
touched. Quota: 12 primary + 20 secondary minimum. Core-bound claims need
3 independent sources. Deliver: full dossier + Nota cards + complete
evidence-graded reference list. Issue your Scan Declaration first.
```

### 1.2 — Core Admission (Nota distillation of existing verified work)
```text
@Radiation | TOPIC: Distill [dossier/topic] into Core cards.
Use scaffolding/core/proc_nota-distillation.md. Only Shield-Stamped claims are
eligible. ≤300 words per card, lineage blocks mandatory, update CORE_INDEX.md.
Emit the result as a 🟢 Patch.
```

### 1.3 — Full-System Self-Audit
```text
@Radiation | STYLE: audit | TOPIC: Audit this entire repository.
Run proc_inspection-audit.md over: Brain integrity (II.6), ungraded claims,
decayed claims, register consistency, quarantine status. Classify findings
🟥🟧🟨🟩. Deliver the audit report + updated DEBT_REGISTER append block as a Patch.
```

---

# ⚡ @Data INSTANCES

### 2.1 — Quiz / Question Rapid Answer
```text
@Data | TOPIC: [your question(s)]
Answer directly and accurately. Verify against real sources (2 primary + 3
secondary minimum, stripped triangulation) but do NOT list sources. No Brain
writes. Answer-first format, zero preamble.
```

### 2.2 — Batch Question Set
```text
@Data | TOPIC: Answer this question set: [paste questions]
Number each answer. Verify each against sources without listing them. Flag any
answer where verification fell short as [UNVERIFIED] rather than guessing.
```

### 2.3 — Fact-Check a Claim
```text
@Data | TOPIC: Fact-check: "[claim]"
Verdict: TRUE / FALSE / PARTIALLY TRUE / UNVERIFIABLE + a two-line basis.
Stripped triangulation applies — 2 independent sources minimum before a verdict.
```

---

# 📡 @Gather INSTANCES

### 3.1 — Topic Intelligence Sweep
```text
@Gather | STYLE: [research / literature-review / AUTO] | TOPIC: [subject]
Gather to quota: 10 primary + 18 secondary minimum, scout-vetted, zero padding.
Full pipeline minus Nota: annotate, triangulate, dossier everything. Deliver the
style-formatted corpus + dossier + full graded reference list. NO conclusions —
gathering is the mission.
```

### 3.2 — Source Stockpile Expansion
```text
@Gather | TOPIC: Expand the stockpile on [existing topic in Brain].
Check Brain/long_term first (II.1) — acquire only what is NOVEL. Scout vets
necessity per III.8. Integrate new matter into the existing dossier via Patch.
```

### 3.3 — Incubation Review Pass
```text
@Gather | TOPIC: Review all open tickets in 04-incubate/.
For each: hunt new external evidence, re-run triangulation, then rule
PROMOTE (criteria met) / KILL (criteria failed) / HOLD (state what's missing).
Log outcomes in GRADUATION_LOG.md. Emit as Patch.
```

---

# 🔬 @Decode INSTANCES

### 4.1 — Single-Repo Deep Decode
```text
@Decode | STYLE: msr | TOPIC: [GitHub URL]
Read the full tree (primary source) + minimum 8 secondary sources. Deliver:
architecture map, infrastructure inventory, concept extraction,
pattern/anti-pattern register, dependency graph. Use proc_decode-map.md.
```

### 4.2 — Multi-Repo Comparative Decode
```text
@Decode | STYLE: comparative-analysis | TOPIC: Compare [URL 1] vs [URL 2]
Decode each per proc_decode-map.md, then build the comparison matrix:
architecture, patterns, tradeoffs, reusable concepts. Verdict per dimension.
```

### 4.3 — Concept Extraction for Reuse
```text
@Decode | TOPIC: Extract [specific concept/pattern] from [URL] for reuse.
Scout vets scope to that concept only (no full-repo sweep). Deliver: how it
works, why it works, what it depends on, and a reuse-readiness assessment.
```

---

# 🔁 CONTINUITY INSTANCES

### 5.1 — Watch-Relief Handover (rate-limit succession)
```text
You are relieving a rate-limited AI mid-session on RADIATION.
Read this repository, and act as per .readme — then read docs/SYSTEM_STATE.md
and the last 3 task_ledger entries. The outgoing state: [paste handover block].
Resume from the declared anchor. Do not re-run completed stages; verify them.
```

### 5.2 — Recovery Boot (repo found damaged/contradictory)
```text
Read this repository, and act as per .readme. PRIORITY OVERRIDE: the repository
may be damaged or contradictory. Freeze all writes. Run @Radiation instance 1.3
(full self-audit) in READ-ONLY mode. Report findings to me before any remedy.
You may not "fix" ground truth unilaterally.
```

### 5.3 — Patch Verdict Delivery
```text
Patch verdict for [patch filename]: [APPLIED / PARTIAL — kept: … / REJECTED — reason: …]
Update the Patch Ledger (append block) and, if the verdict reveals a misread
preference, add the lexicon entry per II.5. Then stand by for the next task.
```
