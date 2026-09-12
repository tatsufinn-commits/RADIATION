# 🟡 DECISION MEMO — public-repo link exposure (P-04 §5; presented 2026-09-12, NO action taken)
`Brain/external_sources/*.md` publishes Drive links to scanned textbooks, a paid standard (NSCP 2015), and lecturer decks in a PUBLIC repo. Anyone-with-link + public index ≈ publication; a flagged Drive account breaks the catalog.
| Option | Effect | Cost |
|---|---|---|
| A. Repo → private | everything stays; no public link index | loses copy-pastable-repo property |
| B. Public repo, links out (recommended) | catalogs keep names/digests/file-IDs; URLs → git-ignored vault_links.local.md | one gitignore line + a convention |
| C. Split repos (public OS + private vault) | public and link-free | two clones per boot |
**Recommendation: B.** Decision lands in CHANGELOG + an amendment row if II.6 changes. No file moved, no link edited pending the Commander's ruling.
