# scripts/ — the Machine Enforcement Layer (P-01)
**Every session runs this BEFORE claiming session closure:**
```
python3 scripts/validate.py && python3 scripts/knowledge_regression.py
```
- `validate.py` — 14 structural checks (form + resolvability, never truth). Exit 1 = at least one ❌ FAIL → the session is NOT closable; fix or report the failure honestly. ⚠️ WARN entries are ratification-pending items — list them in your delivery, do not "fix" canon to silence them.
- `knowledge_regression.py` — locked value assertions (`tests/knowledge_assertions.json`). Locking a value requires Shield Stamp (I.3) or in-session-verified [D] primary. A drifted verified value = exit 1 = cannot ship.
- Neither script modifies files, calls the network, or needs third-party packages.
- CI (`.github/workflows/validate.yml`) runs both on every push and PR.
- Exemptions for historical files live in `docs/ARCHIVE_NOTES.md` — additions there are 🟢 but must be justified in the patch notes.
