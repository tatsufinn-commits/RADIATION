#!/usr/bin/env python3
"""ingest_collection.py — RADIATION collection ingestion harness (P-10 Phase 2).

The repeatable procedure, proven on the Building-Utilities collection 2026-09-13.
Stdlib for listing/diffing; PyMuPDF for PDF work (pip install pymupdf).

    python3 scripts/ingest_collection.py list   --url <drive-folder-url>
    python3 scripts/ingest_collection.py fetch  --manifest <file.json> --dest /tmp/scratch
    python3 scripts/ingest_collection.py extract --dir /tmp/scratch
    python3 scripts/ingest_collection.py verify --pdf <file.pdf> --page 55   # table check

THE THREE RULES THIS HARNESS ENFORCES (all learned the hard way):

  1. BINARIES NEVER TOUCH THE REPOSITORY.  Working directory defaults to /tmp.
     The repo holds the EXTRACT, never the vehicle (II.6 rule 8, P-04 staged).

  2. A TABLE EXTRACTED BY TEXT ORDER ALONE IS UNVERIFIED.
     On 2026-09-13, naive line-order extraction of PEC Table 2.20.2.3 produced a
     complete, plausible, and COMPLETELY WRONG occupancy->load mapping — every
     value shifted, nothing visibly broken. Coordinate extraction and a rendered
     page read were required to settle it. Legal/numeric tables MUST be verified
     before any value is graded. `verify` renders the page for exactly this.

  3. AN IMAGE-ONLY FILE IS NOT A DEAD END — IT IS A RUNG.
     See Brain/cerebellum/routines/routine_document-recovery-ladder.md.
     This harness REPORTS the rung; it does not silently skip.
"""
import argparse, hashlib, html, json, os, re, subprocess, sys, tempfile

# ── 1. LIST: enumerate a public Drive folder without an API key ──────────────
IVD = re.compile(r"window\['_DRIVE_ivd'\]\s*=\s*'(.*?)';", re.S)

def list_folder(url):
    """Read a public Drive folder listing. Returns [{id,name,size}]."""
    out = subprocess.run(["curl", "-sL", "--max-time", "60", url],
                         capture_output=True, text=True).stdout
    m = IVD.search(out)
    if not m:
        sys.exit("✗ could not find the folder listing — is the link public "
                 "(anyone-with-link) and still shared?")
    data = json.loads(m.group(1).encode("utf-8", "surrogateescape").decode("unicode_escape"))
    rows = []
    for f in data[0]:
        try:
            fid, name = f[0], f[2]
            size = next((v for v in (f[12], f[26], f[13], f[25])
                         if isinstance(v, int) and v > 10000), None)
            rows.append({"id": fid, "name": name, "size": size})
        except Exception:
            continue
    return rows

def cmd_list(a):
    rows = list_folder(a.url)
    print(f"{len(rows)} file(s)\n")
    tot = 0
    for r in sorted(rows, key=lambda x: -(x["size"] or 0)):
        mb = f"{r['size']/1048576:8.1f} MB" if r["size"] else "       ? MB"
        tot += r["size"] or 0
        print(f"  {mb}  {r['name'][:76]}")
    print(f"\ntotal: {tot/1048576:.1f} MB")
    if a.out:
        json.dump(rows, open(a.out, "w"), indent=1)
        print(f"manifest written: {a.out}")

# ── 2. FETCH ────────────────────────────────────────────────────────────────
def cmd_fetch(a):
    files = json.load(open(a.manifest))
    os.makedirs(a.dest, exist_ok=True)
    if os.path.abspath(a.dest).startswith(os.path.abspath(a.repo or "/nonexistent")):
        sys.exit("✗ refusing to fetch into the repository — binaries never touch the repo (II.6 r.8)")
    ok = fail = 0
    for i, f in enumerate(sorted(files, key=lambda x: x.get("size") or 0), 1):
        safe = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in f["name"])
        dest = os.path.join(a.dest, f"{i:02d}_{safe}")
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print(f"  [{i:02d}] cached  {safe[:58]}"); ok += 1; continue
        r = subprocess.run(["curl", "-sL", "--max-time", "600",
                            f"https://drive.google.com/uc?export=download&id={f['id']}",
                            "-o", dest, "-w", "%{http_code}"], capture_output=True, text=True)
        got = os.path.getsize(dest) if os.path.exists(dest) else 0
        head = open(dest, "rb").read(4) if got else b""
        good = r.stdout.strip() == "200" and head == b"%PDF"
        print(f"  [{i:02d}] {'OK  ' if good else 'FAIL'} {safe[:58]}  {got/1048576:.1f} MB")
        ok += good; fail += (not good)
    print(f"\nfetched {ok} · failed {fail}")

# ── 3. EXTRACT: the recovery-ladder rung report ─────────────────────────────
def cmd_extract(a):
    import pymupdf as fitz   # pymupdf 1.24+: the module IS pymupdf; `fitz` is a shim
    report = []
    for p in sorted(f for f in os.listdir(a.dir) if f.lower().endswith(".pdf")):
        path = os.path.join(a.dir, p)
        try:
            d = fitz.open(path)
            n = d.page_count
            step = max(1, n // 12)
            words = sum(len(d[i].get_text().split()) for i in range(0, n, step))
            wpp = words / max(1, len(range(0, n, step)))
            rung = ("TEXT-LAYER OK" if wpp >= 50 else
                    "THIN — verify before quoting" if wpp >= 10 else
                    "IMAGE-ONLY → recovery ladder (render→vision→OCR)")
            report.append({"file": p, "pages": n, "words_per_page": round(wpp, 1), "rung": rung})
            print(f"  {p[:52]:<54} {n:>5} pp  {wpp:>7.1f} w/p  {rung}")
            d.close()
        except Exception as e:
            report.append({"file": p, "error": str(e)})
            print(f"  {p[:52]:<54}  ERROR  {e}")
    # duplicates by content hash — AP-05
    seen = {}
    for p in sorted(f for f in os.listdir(a.dir) if f.lower().endswith(".pdf")):
        h = hashlib.md5(open(os.path.join(a.dir, p), "rb").read()).hexdigest()
        seen.setdefault(h, []).append(p)
    dups = {h: v for h, v in seen.items() if len(v) > 1}
    if dups:
        print("\n  ⚠ BYTE-IDENTICAL DUPLICATES (AP-05 mirror duplication):")
        for h, v in dups.items():
            print(f"    {h[:12]}…  {' == '.join(x[:40] for x in v)}")
    tot = sum(r.get("pages", 0) for r in report)
    img = sum(r.get("pages", 0) for r in report if "IMAGE-ONLY" in r.get("rung", ""))
    print(f"\n  {len(report)} file(s) · {tot} pages · {img} page(s) image-only")
    if a.out:
        json.dump({"files": report, "duplicates": dups}, open(a.out, "w"), indent=1)
        print(f"  report written: {a.out}")

# ── 4. VERIFY: the anti-silent-corruption rung ──────────────────────────────
def cmd_verify(a):
    import pymupdf as fitz   # pymupdf 1.24+: the module IS pymupdf; `fitz` is a shim
    d = fitz.open(a.pdf)
    pg = d[a.page - 1]
    txt = pg.get_text()
    print("── TEXT-ORDER EXTRACTION (UNVERIFIED — do not grade from this alone) ──")
    print("\n".join(txt.splitlines()[:28]))
    # coordinate pass: pair each right-hand number with the left-hand label on the same line
    rows = {}
    for x0, y0, x1, y1, w, *_ in pg.get_text("words"):
        rows.setdefault(round(y0 / 3) * 3, []).append((x0, w))
    print("\n── COORDINATE PASS (row-by-row, left | right) ──")
    cut = pg.rect.width * 0.55
    for y in sorted(rows):
        items = sorted(rows[y])
        left = " ".join(w for x, w in items if x < cut)
        right = " ".join(w for x, w in items if x >= cut)
        if left or right:
            print(f"  {left[:54]:<56}| {right[:34]}")

    # ── pass statistics — INFORMATIONAL, deliberately NOT a verdict ──────────
    # The first cut of this function emitted an automatic "resolved / not resolved"
    # verdict. It was removed: on the PEC 2.20.2.3 corruption it fired correctly, and
    # on a clean single-column page (PD 1096 pipe colours) it ALSO fired — a false
    # positive. A warning that cries wolf is worse than no warning, because it trains
    # the reader to skip it, and skipping it is how a wrong table earns a grade.
    #
    # The machine cannot decide this. What it can do is lay out the evidence and
    # always produce the render, so the READER decides — which is the recovery
    # ladder's vision rung, not a substitute for it.
    nrows = len(rows) or 1
    onesided = sum(1 for y in rows
                   if not (any(x < cut for x, _ in rows[y]) and any(x >= cut for x, _ in rows[y])))
    overload = [y for y in rows if len(rows[y]) > 14]
    print(f"\n── PASS STATISTICS (no automatic verdict — you decide)")
    print(f"   {nrows} text rows · {onesided} one-sided ({onesided * 100 // nrows}%) · "
          f"{len(overload)} overloaded (>14 words)")
    print("   Reference point: a clean TWO-COLUMN table gives mostly two-sided rows and few")
    print("   overloaded ones. A single-column list is legitimately one-sided — that is fine.")
    print("   If you cannot tell which of those you are looking at, the render is what you grade.")
    print("   ⚠ A tidy-looking coordinate pass is NOT evidence of a correct one (PEC 2.20.2.3).")

    # the render must not land inside the repository (II.6 r.8 doctrine)
    out = a.out
    if not out:
        out = os.path.join(os.path.dirname(os.path.abspath(a.pdf)), "_VERIFY_page%d.png" % a.page)
    if os.path.abspath(out).startswith(os.path.abspath(a.repo) + os.sep):
        out = os.path.join(tempfile.gettempdir(), "_VERIFY_page%d.png" % a.page)
        print("   (output redirected: a render is a vehicle and may not be written into the repo)")
    pg.get_pixmap(dpi=170).save(out)
    print(f"\n── RENDERED PAGE for the vision rung: {out}")
    print("   Read the image and reconcile it against BOTH passes above.")
    print("   If they disagree, the render wins — text order mis-binds multi-line tables.")
    d.close()

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list");    l.add_argument("--url", required=True); l.add_argument("--out")
    f = sub.add_parser("fetch");   f.add_argument("--manifest", required=True); f.add_argument("--dest", default=os.path.join(tempfile.gettempdir(), "rad_ingest")); f.add_argument("--repo")
    e = sub.add_parser("extract"); e.add_argument("--dir", default="/tmp/rad_ingest"); e.add_argument("--out")
    v = sub.add_parser("verify");  v.add_argument("--pdf", required=True); v.add_argument("--page", type=int, required=True); v.add_argument("--out")
    v.add_argument("--repo", default=os.getcwd(), help="repo root; renders are refused inside it")
    a = ap.parse_args()
    {"list": cmd_list, "fetch": cmd_fetch, "extract": cmd_extract, "verify": cmd_verify}[a.cmd](a)

if __name__ == "__main__":
    main()
