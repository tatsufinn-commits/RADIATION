# scripts/ — the Machine Enforcement Layer (P-01)
**Every session runs this BEFORE claiming session closure:**
```
python3 scripts/validate.py && python3 scripts/knowledge_regression.py
```
- `validate.py` — the structural validator (form + resolvability, never truth; the live
  check count is printed by every run — never trust a number written in a file). Offline
  by default; check 13's link census runs only with `RADIATION_ONLINE=1` (CI sets it). Exit 1 = at least one ❌ FAIL → the session is NOT closable; fix or report the failure honestly. ⚠️ WARN entries are ratification-pending items — list them in your delivery, do not "fix" canon to silence them.
- `knowledge_regression.py` — locked value assertions (`tests/knowledge_assertions.json`). Locking a value requires Shield Stamp (I.3) or in-session-verified [D] primary. A drifted verified value = exit 1 = cannot ship.
- Neither script modifies files, calls the network, or needs third-party packages.
- CI (`.github/workflows/validate.yml`) runs both on every push and PR.
- Exemptions for historical files live in `docs/ARCHIVE_NOTES.md` — additions there are 🟢 but must be justified in the patch notes.

## The other nine scripts
`validate.py` and `knowledge_regression.py` are the closure pair. Five more tools exist
for session work — **the full registry, with exact invocations, inputs and gotchas, is
`docs/CAPABILITIES.md`.** Read it before doing by hand what a script already does:
`plan_term.py` · `ingest_collection.py` · `export_anki.py` · `grade_exam.py` ·
`decay_compute.py` · `ics_normalize.py` · `nota.py` · `module_scaffold.py` ·
`deadline_feed.py`.

**Check 21 enforces this directory against that registry:** every `.py` here must be
named in `docs/CAPABILITIES.md`, and the check count stated above must be the true one.
That guard exists because this file once carried a check count years out of date while claiming to be current.
