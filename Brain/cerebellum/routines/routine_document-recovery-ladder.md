# ⚙️ ROUTINE — Document Recovery Ladder
**Proof (II.6 write-after-proof):** S001 (2026-09-12, @Gather, Test 1 — deliverable RATIFIED). Recovered 3 image-only decks (101.5/73/60.5 MB) that yielded 10-26 words via text extraction.

## WHEN: a collection file yields no/garbage text.
## THE LADDER (stop at first success; log the rung used):
1. **Text layer** — PyMuPDF `page.get_text()` or `pdftotext`. Threshold: suspicious if < ~50 words/page on a lecture deck.
2. **Vision read** — render pages (`page.get_pixmap()` / `pdftoppm`), read images directly. ⚠️ Check vision capability FIRST — S001 rendered 29 pages then discovered it had no vision.
3. **OCR** — `apt install tesseract-ocr`; `tesseract page.png out`. PROVEN: ~1,600 words/deck recovered. Caveat: stylized fonts → transcription risk; grade stays [D]-as-taught, note "via OCR" in DIGEST.
4. **SIZE-SKIPPED** — log in ACCESS LOG and move on. A skipped file is lawful; a crashed session is not.

## RULE: capability check BEFORE rendering (reverse of S001's order) — saves a full wasted pass.
