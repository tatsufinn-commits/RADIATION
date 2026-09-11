# S001 — LEARNINGS (session-specific)
1. **Image-only decks are recoverable.** The 3 largest PDFs (101.5/73/60.5 MB)
   had no text layer. Instead of fabricating (I.1) or immediately logging
   SIZE-SKIPPED, the session rendered pages to images and read them visually —
   a lawful recovery path between "read normally" and "skip". Candidate for a
   cerebellum routine once repeated successfully.
2. **IV.1 override pattern validated.** Commander's "learn all 8" exceeded the
   3/6 budget; the correct move — invoke IV.1, DECLARE the override in the
   FETCH PLAN line, proceed — worked exactly as designed.
3. **Append-block transport pitfall.** The session's Patch was structurally
   correct, but at application the transport files (append-blocks/, root
   PATCH_NOTES.md) were committed instead of being pasted-and-discarded.
   Fixed in v1.3.3; PATCH_NOTES application instructions must be followed
   literally at push time.
