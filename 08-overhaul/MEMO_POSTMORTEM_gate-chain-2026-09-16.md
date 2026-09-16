# MEMO POSTMORTEM — Gate Chain #75-#81: Verify-the-Face Doctrine in Production

**Date:** 2026-09-16 (draft — to be sealed in next ordered patch per directive)
**Base:** fee4a955c0781bd9d81c87906bc7c1464d038afa merge PR #2 run #81 green 22/22
**Class:** Prime exhibit of Verify-the-Face doctrine actually working

## Summary

Three consecutive pushes went red, same genus, gate family caught all three, Copilot fix team repaired inside scope. Content never defect; packaging was.

**Strong work acknowledged:** 5900 + 5900-1 + P-11-B accepted as content — desk verified item-by-item L13/L41/L79 side-by-side reconciliation with archived-pointer discipline and ratification flags; schema v0.2 authority_grant+review_after+allOf; 42-cue catalog v2 with 11 authority grants each expiring; resolver linter enforcement; TestAdmissionGate 10 vectors; 5th hostile shape with conflict-surfacing; unittest 87-all-green; observability tee+publish pipeline. Ship-shaped.

## Incident Timeline

### #75 — fcc9a7a Add CUE tranche: catalog, resolver, schema, tests (5900)
- **Run:** https://github.com/tatsufinn-commits/RADIATION/actions/runs/34995553002
- **Result:** FAILURE step 14 Release Truth Gate live check
- **Root:** EXPECTATION.json mandatory_validations[7] = `python3 -m pytest tests/test_cue_resolver.py -v`, CI setup-python 3.11 clean no pytest installed, workflow never pip-installs → ModuleNotFoundError pytest → exit 1. Steps 1-13 success, 15-17 skipped.
- **Why local green:** dependency contamination — pytest preinstalled in author sandbox, not in CI. Author-machine contamination.
- **Receipt:** Job metadata API step 14 failure, 32s exit 1

### #76 — d518f3f 5900-1 fix ledger pipe counts? Actually repair attempt
- **Run:** (second red)
- **Result:** FAILURE
- **Root:** EXPECTATION base_sha pinned to local-only `d518f3f4a75a1a0400679d1d36f882a1057d380f` which does not exist on origin, plus allowed list missing two repair-tree paths (.github/workflows/validate.yml + scripts/release_truth_check.py). Gate correctly rejected: base_sha not ancestor of origin/main, allowed mismatch.
- **Genus:** expectations authored against author's environment (local object) instead of real public executor (origin).

### PR-2-first-round — fix/release-truth-base-repin first push
- **Run:** (third red, before #80/81)
- **Result:** FAILURE
- **Root:** observability patch tee'd 25 diagnostic files (`*_output.txt`) into worktree, gate inspects tree, sees untracked files not in allowed_changes → failure. CI writes into tree gate inspects.
- **Genus:** same — CI writes assumed out-of-repo, but were in-repo.

### #80/81 — fix/release-truth-base-repin final
- **Commits:**
  - 2a16b30 Re-pin release truth base to public lineage (fcc9a7a public 5900 HEAD)
  - 04e8cd8 Declare 5900-1 infra paths in release-truth allowed_changes (repair lineage reconciliation)
  - 945eb21 Ignore CI teed diagnostics in worktree checks; declare .gitignore in release-truth allowlist
- **Result:** Run #81 green 22/22 executed steps, merge PR #2 fee4a955 sealed
- **Receipt:** public main fee4a95, 42·38·4·0, release-truth 0 findings, 87 unittest OK

## One Genus

**Expectations authored against the author's environment instead of the real public executor.**

- Local pytest present → CI absent
- Local object d518f3f present → origin absent
- Local assumption teed logs out-of-repo → CI wrote in-repo and gate inspected

Gate family caught all three — Verify-the-Face doctrine working.

## Fixes (Copilot fix team, inside scope)

- 5900-1: pytest→unittest, workflow pytest→unittest discover, gate hardening forbidden tools lint + 8th vector, observability every step tees + tail to SUMMARY + artifact, stdlib-only law
- 2a16b30: base re-pin to public fcc9a7a
- 04e8cd8: allowed list includes infra paths
- 945eb21: CI teed diagnostics gitignored / .gitignore in allowlist, worktree check ignores ignored files

## Four Laws — mandatory batch-zip protocol

### LAW-1 PUBLIC-OBJECT LAW
EXPECTATION ships only after release_truth_check 0 findings in fresh clone of exact push candidate object set — never authoring machine. Every SHA must git cat-file -t against origin. Local objects don't exist; only pushed history real.

### LAW-2 STDLIB-ONLY LAW
mandatory_validations only commands CI guarantees. pytest|pip|conda|npm|npx|node machine-rejected (check_forbidden_tools_in_validations + self-test vector 8). Never reintroduce by hand.

### LAW-3 DELTA-≡-ALLOWED LAW
Before shipping: git diff --name-status base..HEAD path set exactly equal to allowed_changes coverage (δ=∅ both directions). DELIVERY_REPORT mandatory field: "delta-vs-allowed check: ran · output ∅."

### LAW-4 CI-HYGIENE LAW
Anything CI/workflow writes (teed logs, reports, caches) must be gitignored or out-of-repo — precedents §3c validation_report.json, new §3f. Gate assumes tree only delivery touched.

## Receipts

- Run #75 FAILURE: https://github.com/tatsufinn-commits/RADIATION/actions/runs/34995553002 step 14
- Run #81 SUCCESS: merge PR #2 fee4a95 22/22
- Public main: fee4a955c0781bd9d81c87906bc7c1464d038afa
- Zips: 5900-1 160K 84fad662bf4daf0694a7e7dcf09c73f19a4c03ce6444690aeae9d234cf9f73c0, P-11-B 152K 73390a68a32bb89247ccae1f020e0145d43a0cd2e31efa0aea7897c46b9fa85f
- Gates: 42·38·4·0, release-truth 0+8/8, catalog 0+24/24, 87 unittest

## Lessons

- Fresh-clone gate is not optional — author-machine contamination is silent killer
- Stdlib-only is law, not preference — pytest dependency cost 1 red
- Delta≡Allowed prevents shadow files — tee'd diagnostics cost 1 red
- Public-object check prevents local-only SHA — d518f3f cost 1 red
- Content was never defect — packaging was, three times — gate family worked

## Next

- Base next tranche fee4a955
- Cosmetic label 7→8 vectors
- Ledger honesty rows narrating #75-#81 lineage truthfully
- This memo sealed as 08-overhaul/MEMO_POSTMORTEM_gate-chain-2026-09-16.md
- Await RD-3 + explicit per-tranche order II.7.4

**Status:** Draft for next ordered patch — do not apply until Commander orders.
