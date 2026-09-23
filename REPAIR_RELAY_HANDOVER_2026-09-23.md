# №2 — REPAIR RELAY — EXPECTATION RE-PIN phantom-base cure — 2026-09-23
**From:** Build Bench (Arena Agent) · **To:** Commander (motor) · **To:** Desk · **Class:** packaging repair, forward-fix — NO revert, NO history rewrite (main protected, linear) — per RELAY_REPIN_EXPECTATION_2026-09-23.md

## §1 Pre-state (required)
- Required pre-state: `origin/main` = `d3a2d11971a78650b3cb5d68be101f026e2982cb`
- Verified via `git ls-remote origin refs/heads/main`:
```
d3a2d11971a78650b3cb5d68be101f026e2982cb  HEAD
d3a2d11971a78650b3cb5d68be101f026e2982cb  refs/heads/main
```
- Local checkout: `git checkout origin/main` → detached HEAD at d3a2d11
- Branch created: `fix/expectation-repin-2026-09-23` atop d3a2d11
- `git rev-parse HEAD` pre-state: `d3a2d11971a78650b3cb5d68be101f026e2982cb` — MATCH

## §2 Diagnosis (desk-reproduced — facts, not witnesses)
- Landed tree d3a2d11 "Shot-2 and WP-1 update": validate.py **0 fail** (42 run · 38 pass · 4 warn) — content sound, vault bytes desk-witnessed drift-free `aaa4daad…` / `10a3afb4…`, ONE warn honestly healed (shrine heartbeat row D015/D016)
- Wound: `docs/RELEASE_TRUTH_GATE/EXPECTATION.json` pins `base_sha = 902d3a33405fa7ccb6e85faa144fc605f436a0e0` — LOCAL-ONLY object, never pushed
- Gate: **4 findings** quoted:
```
base_sha 902d3a33405fa7ccb6e85faa144fc605f436a0e0 does not exist in repo
LAW-1 PUBLIC-OBJECT: base_sha 902d3a33405fa7ccb6e85faa144fc605f436a0e0 is not ancestor of origin/main (...) — local-only object, violates PUBLIC-OBJECT LAW (must git cat-file -t against origin, must be ancestor of origin/main)
LAW-3 DELTA-≡-ALLOWED: diff contains paths not in allowed_changes: [...] — δ extra in diff  (or) allowed_changes contains paths not in diff (δ≠∅) — missing base makes all 34 entries read as "not in diff"
whitespace check failed: git diff --check ... (whitespace range invalid)
```
- Preflight: same 4 — CI #135 fails by construction — both attempts
- Root genus: local composition (Shot-2 built locally at 902d3a3, WP-1 stacked on it) pushed as ONE squashed commit whose ledger referenced unpushed intermediate. Base-pin pointed at ghost.

## §3 Before/After cat-file -t proofs (LAW-1: only pushed history is real)

### BEFORE — phantom base 902d3a3
```
$ git cat-file -t 902d3a33405fa7ccb6e85faa144fc605f436a0e0
commit
$ git ls-remote origin | grep 902d3a3
(no output) — 902d3a3 NOT in origin — phantom
$ git merge-base --is-ancestor 902d3a33405fa7ccb6e85faa144fc605f436a0e0 origin/main && echo YES || echo NO
NO — phantom confirmed, NOT ancestor of origin/main
```
- Bench: commit exists locally (cat-file -t commit) BUT NOT in origin, NOT ancestor — violates LAW-1 PUBLIC-OBJECT.

### AFTER — sealed ancestor f086392a (last green seal)
```
$ git cat-file -t f086392a9cc443e374541077c5a054938e0b337a
commit
$ git merge-base --is-ancestor f086392a9cc443e374541077c5a054938e0b337a origin/main && echo YES || echo NO
YES — real, pushed, ancestor object — only pushed history is real
$ git branch -r --contains f086392a9cc443e374541077c5a054938e0b337a
  origin/HEAD -> origin/main
  origin/main
```
- Bench: commit exists, ancestor of origin/main, contained in origin/main — LAW-1 PASS.

## §4 The Cure — ONE commit touches at most THREE paths per §2

### Branch
- `fix/expectation-repin-2026-09-23` atop `d3a2d11`
- ONE commit: `f02a213dbd44e71eff144dcf423e857aece39067`
- Message: "REPAIR RELAY — EXPECTATION RE-PIN phantom-base cure 2026-09-23 — forward-fix — base 902d3a3 → f086392a — only pushed history is real — gate self-heals — no content change"

### Paths touched (exactly 3 — max allowed)
```
M  CHANGELOG.md
M  docs/PATCH_LEDGER.md
M  docs/RELEASE_TRUTH_GATE/EXPECTATION.json
```
- No other paths touched — gate/preflight names NO other path — HALT condition not triggered.

### EXPECTATION.json re-pin
- **base_sha:** `902d3a33405fa7ccb6e85faa144fc605f436a0e0` → `f086392a9cc443e374541077c5a054938e0b337a` (last green seal, real pushed ancestor)
- **allowed_changes:** exactly true delta re-proven fresh `git diff --name-status f086392a <candidate>` = 34 paths exact — repair touches only files already inside it so set stays 34 — confirm don't assume paste proof (see §5)
- **description / generated_by:** narrate re-pin phantom 902d3a3 → f086392 forward-fix only pushed history is real per LAW-1
- Before JSON had 34 entries with phantom base; after JSON has 34 entries with sealed base — same count, same paths, different base.

### CHANGELOG.md — one row
- Added row atop v3.10.32 (same version to keep coherence — SYSTEM_STATE v3.10.32, CHANGELOG v3.10.32, README v3.10.32):
```
## v3.10.32 — 2026-09-23 — REPAIR RELAY — EXPECTATION RE-PIN phantom-base cure — forward-fix — no content change — gate self-heals
```
- Narrative includes diagnosis, cure, battery, laws — no content change — gate self-heals.

### PATCH_LEDGER.md — one row
- Added row:
```
| 2026-09-23 | RADIATION_PATCH_2026-09-23_REPAIR_RELAY_EXPECTATION_REPIN.zip | 🟢 | docs/RELEASE_TRUTH_GATE/EXPECTATION.json M base_sha phantom 902d3a3 → sealed f086392a forward-fix only pushed history is real per LAW-1 — CHANGELOG.md M re-pin row — docs/PATCH_LEDGER.md M re-pin row | PENDING — REPAIR RELAY ... |
```

## §5 Battery (all pasted; stable re-run per §3)

### validate.py — 0 fail with warn floor handled honestly
```
42 checks run · 38 pass · 4 warn · 0 fail
```
- Warn floor: 5→4 warn drop shown as shrine-heartbeat HEAL evidence docs/shrine/LOG.md rows D015/D016 in landed delta, not hidden — healing improves census hiding corrupts — desk celebrates former punishes latter.
- Shrine LOG tail:
```
| 2026-09-22 | D015 | WP-1 contracts-and-docs 2026-09-22 tranche — 1.6 checklist + 1.3 glossary + 1.4 agent policies + 1.2 cascade + 1.1 manifest + 1.5 verify policies — branch wp1/contracts-and-docs-2026-09-22 dirty 19 files, HEAD f086392a base, 37·5·0 floor kept, 0 fail after scaffold contract + capability registry fix. |
| 2026-09-23 | D016 | WP-1 handover 2026-09-22 amended — add docs/WP1_HANDOVER_2026-09-22.md to INDEX 40→41 docs + fix shrine lag 2026-09-23 heartbeat — commit 4454830 amended to 34 files 18A+16M per 1.6 checklist — battery re-run 38·4·0 target. |
```

### release-truth gate — 0 findings
```
release-truth gate: 0 finding(s)
```
- Took 64.5s (validate + unittest + render + verify) — passes with 120s timeout.

### push_preflight_check.py --base f086392a → 0 findings
```
BASE-PIN: HEAD=f02a213dbd44e71eff144dcf423e857aece39067 declared_base=f086392a9cc443e374541077c5a054938e0b337a
LAW-5 BASE-PIN: OK — HEAD f02a213dbd44e71eff144dcf423e857aece39067 is beyond base f086392a9cc443e374541077c5a054938e0b337a but base is ancestor (candidate built on correct base) — verify-the-face passed, motor at f02a213 built from f086392
LAW-1 PUBLIC-OBJECT: OK — base f086392a9cc443e374541077c5a054938e0b337a exists and is ancestor of origin/main
LAW-3 DELTA-≡-ALLOWED: diff=34 allowed=34
LAW-3 DELTA-≡-ALLOWED: OK — diff ≡ allowed (∅ both ways) — delta-vs-allowed: ran · output ∅
LAW-4 CI-HYGIENE: OK — no unignored diagnostic artifacts
LAW-6 WHITESPACE (gate-mirror): OK — git diff --check f086392a9cc443e374541077c5a054938e0b337a..HEAD clean — preflight and gate agree, whitespace arm armed
push_preflight_check: 0 finding(s) — motor preflight PASS, safe to extract/push
```

### Ran 195 OK
```
Ran 195 tests in 11.638s
OK (skipped=3)
```

### render_docs ✓
```
✅ render_docs --check: generated blocks match reality
```

### verify_apply strict FAIL-CLASS none
```
versions   : README v3.10.32 · CHANGELOG top v3.10.32
validator  : 42 38 4 0 (checks/pass/warn/fail)
FAIL-CLASS : none
WARN-CLASS : 11 feed items await Commander attribution
```

### fresh stage-≡-allowed proof (≡ pasting, both directions ∅)
```
$ git diff --name-status f086392a HEAD | wc -l
34
$ git diff --name-status f086392a HEAD | sort
A	CLAUDE.md
A	CODEX.md
A	CURSOR.md
A	agents/BOUNDARIES.md
A	agents/CONTRACTS.md
A	agents/DATA_PATHS.md
A	agents/WORKFLOW.md
A	docs/GLOSSARY.md
A	docs/PATCH_SELF_CERTIFICATION_MANIFEST.md
A	docs/WP1_HANDOVER_2026-09-22.md
A	evals/verify_policies/README.md
A	evals/verify_policies/trace_opt_in.json
A	evals/verify_policies/trace_opt_out.json
A	evals/verify_policies/trace_required.json
A	scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md
A	scaffolding/checklists/WP1_1.6_CHANGE_CONTROL_CHECKLIST.md.contract.json
A	scripts/agent_policy_check.py
A	scripts/verify_policy_check.py
M	AGENTS.md
M	CHANGELOG.md
M	README.md
M	cue/CUE_CATALOG.json
M	docs/CAPABILITIES.md
M	docs/INDEX.md
M	docs/PATCH_LEDGER.md
M	docs/RELEASE_TRUTH_GATE/EXPECTATION.json
M	docs/SYSTEM_STATE.md
M	docs/WARN_LEDGER.md
M	docs/shrine/LOG.md
M	schemas/cue_card.schema.json
M	schemas/subskill_card.schema.json
M	scripts/subskill_check.py
M	subskills/SUBSKILL_CATALOG.json
M	tools/TOOL_REGISTRY.json

$ cat docs/RELEASE_TRUTH_GATE/EXPECTATION.json | python3 -c "import json; print(len(json.load(open(...))['allowed_changes']))"
34

# diff ≡ allowed: ∅ both ways — per push_preflight_check LAW-3 OK
```

## §6 Form of the Seal
- Branch: `fix/expectation-repin-2026-09-23` atop `d3a2d11` — verified via `git rev-parse HEAD` = `d3a2d11` pre-state, `git ls-remote origin` = `d3a2d11`
- ONE commit: `f02a213dbd44e71eff144dcf423e857aece39067` — touches at most 3 paths (EXPECTATION, CHANGELOG, PATCH_LEDGER)
- Push: branch ready locally — push attempted but no credential in arena sandbox (`fatal: could not read Username for 'https://github.com': No such device or address`) — **Commander to push**: `git push origin fix/expectation-repin-2026-09-23`
- Handover: this doc №2 §6 adapted with pre-state d3a2d11, phantom-base finding quoted (see §2), before/after cat-file -t proofs (see §3), battery pasted (see §5)
- Commander seals FAST-FORWARD sha-pin: `git checkout main && git merge --ff-only f02a213dbd44e71eff144dcf423e857aece39067` — CI must paste green (validate 0 fail, gate 0, preflight 0, 195 OK)
- CI expected: green — previous CI #135 red by construction due to phantom base; after re-pin, gate 0, preflight 0, validate 0 fail

## §7 Laws Restated (second time earned)
- **LAW-1: only pushed history is real.** Every base_sha, seal-parent, built-on-X must resolve to object `git ls-remote origin` can see. Bench pastes `git cat-file -t <base>` AND `git merge-base --is-ancestor <base> origin/main` — see §3.
- **Motor runs preflight before ANY hand push.** `push_preflight_check.py` printed exact 4 findings CI later echoed at d3a2d11 — sixty seconds on ground hours saved in air. No seal rides without pasted preflight 0 findings — see §5 preflight 0. Sovereign included wall is for every hand cheapest for strongest.

## §8 Content vs Ledger
- Content: fine — vault bytes drift-free `aaa4daad570e8cba4175c124846b79624f4492d2df0ed5e07577e973aa513bb6` / `10a3afb4c4f2682fc0ff4ea4a2419a64c57161020b45d47368e1abe60c2a1e91` — desk-witnessed
- Ledger: merely needed feet on ground — base_pin phantom → sealed — gate self-heals — no content change — one commit then green.

## §9 Trace Table (base SHA trace, re-runnable witness per standing orders)
| Step | Command | Expected | Actual |
|------|---------|----------|--------|
| Pre-state | `git ls-remote origin refs/heads/main` | d3a2d11 | d3a2d11 verified |
| Before cat-file phantom | `git cat-file -t 902d3a3` | commit | commit (local-only) |
| Before ls-remote phantom | `git ls-remote origin \| grep 902d3a3` | NOT in origin | NOT in origin — phantom |
| Before ancestor phantom | `git merge-base --is-ancestor 902d3a3 origin/main` | NO | NO — phantom confirmed |
| After cat-file sealed | `git cat-file -t f086392a` | commit | commit |
| After ancestor sealed | `git merge-base --is-ancestor f086392a origin/main` | YES | YES — real pushed history |
| Diff count | `git diff --name-status f086392a HEAD \| wc -l` | 34 | 34 exact |
| Allowed count | `cat EXPECTATION.json \| allowed_changes len` | 34 | 34 exact |
| Delta ≡ allowed | `push_preflight_check --base f086392a` | 0 findings ∅ both | 0 findings ∅ both — see §5 |
| Validate | `python3 scripts/validate.py` | 0 fail 38·4·0 | 42 38 4 0 — see §5 |
| Gate | `python3 scripts/release_truth_check.py` | 0 findings | 0 findings — see §5 |
| Preflight | `python3 scripts/push_preflight_check.py --base f086392a` | 0 findings | 0 findings — see §5 |
| Unittest | `python3 -m unittest discover -s tests` | 195 OK | 195 OK — see §5 |
| Render | `python3 scripts/render_docs.py --check` | ✓ | ✓ — see §5 |
| Verify | `python3 scripts/verify_apply.py --strict` | FAIL-CLASS none | FAIL-CLASS none — see §5 |

## §10 Commander Actions (motor)
1. Verify pre-state: `git ls-remote origin refs/heads/main` = `d3a2d11` — already verified.
2. Fetch: `git fetch origin`
3. Checkout repair branch (if pushed) or cherry-pick local commit f02a213:
   - If branch pushed: `git checkout fix/expectation-repin-2026-09-23`
   - If not pushed (arena sandbox no credential): create branch from local /tmp/radiation-wp1 — commit f02a213 exists at /tmp/radiation-wp1 — or apply patch: `git checkout -b fix/expectation-repin-2026-09-23 origin/main && git cherry-pick f02a213` (but f02a213 is local-only, need to export patch)
4. Verify battery: re-run §5 commands — expect 0 fail, 0 findings, 195 OK.
5. Push: `git push origin fix/expectation-repin-2026-09-23`
6. Seal: `git checkout main && git merge --ff-only fix/expectation-repin-2026-09-23` — sha-pin f02a213 — FF only.
7. Push main: `git push origin main`
8. CI: paste green — validate 0 fail, gate 0, preflight 0, 195 OK, render ✓, FAIL-CLASS none.

---

**Honest author identity:** Build Bench (Arena Agent WP-1) — built, Commander seals — per three chairs you build→Commander seals→desk rules.
**State-note duty before stand-down:** Branch fix/expectation-repin-2026-09-23 ready at f02a213 atop d3a2d11 — ONE commit 3 paths — battery green — push credential missing in arena sandbox — handover complete — awaiting Commander motor push + FF seal.
**CI witness never bench:** CI #135 red by construction (phantom base) — after re-pin, CI must be green — pasted preflight 0 findings is ground truth.
**Nothing lands on red main:** d3a2d11 RED per desk due to gate 4 findings — repair f02a213 makes gate 0 — green required before main lands.

— THE BENCH
