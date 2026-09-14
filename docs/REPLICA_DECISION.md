# REPLICA_DECISION — the 12-pair tranche awaits a Commander ruling

**Status:** `commander-review-requested` (2026-09-14) — an **open governed exception**.
Validator check 11.6 surfaces it as WARN on every run; it is never
indistinguishable from a ratified PASS, and no Architect may self-ratify a
`commander-review-requested` record or read "request" as approval.

## Inventory (generated from `scaffolding/neurons/REPLICA_MANIFEST.json` — hash-bound)

| # | canonical (active) | replica (archive) | sha256 | purpose | load policy |
|---|---|---|---|---|---|
| 1 | `scaffolding/neurons/sensoryneurons/TID-2026-09-13-a_intake.md` | `scaffolding/neurons/_archive/TID-2026-09-13-a_intake.md` | `sha256:da030339be05…` | intentional historical snapshot | archive_not_boot_context |
| 2 | `scaffolding/neurons/motorneurons/TID-2026-09-13-a_orders.md` | `scaffolding/neurons/_archive/TID-2026-09-13-a_orders.md` | `sha256:3557ce4ff08f…` | intentional historical snapshot | archive_not_boot_context |
| 3 | `scaffolding/neurons/interneurons/TID-2026-09-13-a_reasoning.md` | `scaffolding/neurons/_archive/TID-2026-09-13-a_reasoning.md` | `sha256:84defe88f27e…` | intentional historical snapshot | archive_not_boot_context |
| 4 | `scaffolding/neurons/sensoryneurons/TID-2026-09-13-b_intake.md` | `scaffolding/neurons/_archive/TID-2026-09-13-b_intake.md` | `sha256:a96f30aad1fe…` | intentional historical snapshot | archive_not_boot_context |
| 5 | `scaffolding/neurons/motorneurons/TID-2026-09-13-b_orders.md` | `scaffolding/neurons/_archive/TID-2026-09-13-b_orders.md` | `sha256:df1b5896b509…` | intentional historical snapshot | archive_not_boot_context |
| 6 | `scaffolding/neurons/interneurons/TID-2026-09-13-b_reasoning.md` | `scaffolding/neurons/_archive/TID-2026-09-13-b_reasoning.md` | `sha256:427761a28d80…` | intentional historical snapshot | archive_not_boot_context |
| 7 | `scaffolding/neurons/sensoryneurons/TID-2026-09-13-c_intake.md` | `scaffolding/neurons/_archive/TID-2026-09-13-c_intake.md` | `sha256:0cd5aca611d8…` | intentional historical snapshot | archive_not_boot_context |
| 8 | `scaffolding/neurons/motorneurons/TID-2026-09-13-c_orders.md` | `scaffolding/neurons/_archive/TID-2026-09-13-c_orders.md` | `sha256:11bab0c1930d…` | intentional historical snapshot | archive_not_boot_context |
| 9 | `scaffolding/neurons/interneurons/TID-2026-09-13-c_reasoning.md` | `scaffolding/neurons/_archive/TID-2026-09-13-c_reasoning.md` | `sha256:4d645b021e6c…` | intentional historical snapshot | archive_not_boot_context |
| 10 | `scaffolding/neurons/sensoryneurons/TID-2026-09-13-d_intake.md` | `scaffolding/neurons/_archive/TID-2026-09-13-d_intake.md` | `sha256:9dc3c9d3ec5b…` | intentional historical snapshot | archive_not_boot_context |
| 11 | `scaffolding/neurons/motorneurons/TID-2026-09-13-d_orders.md` | `scaffolding/neurons/_archive/TID-2026-09-13-d_orders.md` | `sha256:0172c57009f9…` | intentional historical snapshot | archive_not_boot_context |
| 12 | `scaffolding/neurons/interneurons/TID-2026-09-13-d_reasoning.md` | `scaffolding/neurons/_archive/TID-2026-09-13-d_reasoning.md` | `sha256:3d032e69ac2e…` | intentional historical snapshot | archive_not_boot_context |

All 24 files stay on disk in **both** options. No option deletes anything.

## Option A — ratify the exact 12 named pairs

The Commander rules: *the twelve pairs above, at the recorded digests, in
their recorded roles, are ratified.* The manifest's `ratification.status`
becomes `commander-ratified` (digest re-verified at ratification), check 11.6
flips to its ratified PASS note, and the exception closes. Any future drift
outside the ratified digests still fails check 11 via the hash-bound contract.

## Option B — ratify only a narrower named subset

The Commander names the surviving pairs explicitly (the 5300-era discussion
considered a 4-pair core). Mechanics: named survivors keep full pair status;
every other pair is marked `decommissioned-by-order` in the manifest with the
order reference and date — **the files remain on disk as retained records**
(removal is a separate, explicit Commander order). Check 11's duplicate
exemption covers only declared pairs, so a decommissioned pair that still
hash-matches its twin would re-surface as a duplicate finding: option B
therefore requires either (a) ratified-differentiation of the retained copy,
or (b) a Commander order moving the retired twin out of scan scope — decided
at ratification time, not by the Architect.

## Required from the Commander

One of: `RATIFY-12` (Option A), `NARROW: <named pairs>` (Option B), or
explicit retention without ratification (exception stays open and loud).
