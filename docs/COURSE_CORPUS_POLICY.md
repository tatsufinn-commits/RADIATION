# COURSE CORPUS POLICY (`Brain/courses/`) — 5300 E1

**Ruling (Commander, 2026-09-14):** the course corpus is an **intentional personal-assistant
reference corpus**. It stays in the tracked tree **by declaration, not deletion** — this
supersedes the 5100-era removal dispositions. The source assets provide fidelity and
provenance; the Markdown derivatives are the normal AI-readable layer.

## The contract

- Every non-Markdown file below `Brain/courses/` must be an **exact entry** in
  `Brain/courses/COURSE_CORPUS_MANIFEST.json`, validated against
  `schemas/course_corpus_manifest.schema.json` (check 2.5).
- Each entry binds: `path` · `sha256` · exact `media_type` · `role` · `load_policy` ·
  `derivative_path` (for `source_of_readable_derivative` roles) · `conversion` (status,
  verified_on, **limitations**) · `distribution_review` (status + notes).
- Failures are mechanical: an **undeclared** new binary/CSV fails; a **changed digest**
  fails; a **missing derivative** fails; a path escaping `Brain/courses/` fails.
- Everything NOT under `Brain/courses/` keeps the full generic vehicle rule — no
  extension or parent-directory allowances anywhere else.
- Markdown/text records still pass the identifier/privacy rules unchanged (A1/A2
  amendments intact). On 2026-09-14 the URL *schemes* in two converted syllabi
  (`GED103_Syllabus_Q12627.md`, `SOIT_DSS10_1Q_Syllabus.md`) were redacted to plain
  domain text so citations survive without literal `http(s)://` strings — a recorded
  content edit, applied with the Commander's brief.

## What static validation does NOT inspect

Inside opaque binaries (PDF) and even inside text assets, **no content review is
automated**. The manifest's `limitations` fields state this honestly per asset; the
derivative mapping is declared by the Commander and verified only for *existence and
digest*, not for semantic fidelity.

## Publication truth

This repository is **publicly accessible now**. A future private transition does not
erase the present public commit history, caches, or forks. Nothing here marks any
asset as having been private. Rights, personal-data, and redistribution judgments are
**Commander judgments**: **a checksum is not a permission grant**, and no permission
claim is invented anywhere in the manifest. `distribution_review: commander-reviewed`
records that the Commander directed retention (brief §0, amendment A1 for the CSV) —
it records custody intent, not a copyright analysis.

## Load policy

`retrieved_by: on_demand_only` — a session reads the corpus derivatives when the task
needs them; source assets are loaded only when explicitly tasked; `desktop.ini` is
`exclude_from_ai_ingestion` (environment metadata, no knowledge role).
