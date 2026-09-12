# ⚙️ ROUTINE — MB-Aware Fetch
**Origin:** S003 lesson (205.2 MB count-clean surprise). Status: doctrine-derived; field-prove then cite.
1. Read size flag from MANIFEST (⚠️ 50-100 MB · 🛑 >100 MB · 🛑🛑 >1 GB) BEFORE any fetch.
2. >50 MB → byte-range head recon first: `curl -r 0-5000000 -L <url> -o head.pdf; pdfinfo head.pdf`.
3. Decide: paged extraction / full fetch (justify) / SIZE-SKIPPED.
4. Log the decision + MB moved in ACCESS LOG and the Scan Declaration's FETCH PLAN.
