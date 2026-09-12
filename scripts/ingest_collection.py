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

# ── format sniffing — a fetch is only "good" if the bytes match the declared type ──
MAGIC = [
    (b"%PDF",            "pdf",   "PDF"),
    (b"PK\x03\x04",       "zip",   "OOXML (xlsx/pptx/docx) — container zip"),
    (b"\xd0\xcf\x11\xe0", "ole",   "LEGACY OLE (doc/xls/ppt) — NOT extractable by this harness"),
]
def sniff(path):
    head = open(path, "rb").read(8) if os.path.exists(path) else b""
    for magic, key, label in MAGIC:
        if head.startswith(magic): return key, label
    if head[:5].lower() in (b"<!doc", b"<html"):
        return "html", "HTML page — interstitial or error page, NEVER the file itself"
    if head[:5] == b"<?xml": return "text", "XML/markup"
    return "unknown", "UNRECOGNISED — do not trust"

def office_text(path):
    """stdlib-only text pull from an OOXML container. No python-pptx / openpyxl needed."""
    import zipfile
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        return None, str(e)
    names = z.namelist()
    if any(n.startswith("ppt/slides/slide") for n in names):
        slides, chars = [], 0
        for n in sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)):
            xml = z.read(n).decode("utf-8", "ignore")
            txt = html.unescape(" ".join(re.findall(r"<a:t>(.*?)</a:t>", xml, re.S)))
            slides.append(txt); chars += len(txt)
        return {"kind": "pptx", "units": len(slides), "chars": chars,
                "sample": " | ".join(s.strip()[:80] for s in slides[:3] if s.strip())}, None
    if any(n.startswith("xl/") for n in names):
        shared = []
        if "xl/sharedStrings.xml" in names:
            s = z.read("xl/sharedStrings.xml").decode("utf-8", "ignore")
            shared = [html.unescape(re.sub(r"<[^>]+>", "", si)).strip()
                      for si in re.findall(r"<si>(.*?)</si>", s, re.S)]
        sheets = {}
        for n in sorted(n for n in names if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
            sheets[n] = len(re.findall(r"<row[ >]", z.read(n).decode("utf-8", "ignore")))
        return {"kind": "xlsx", "units": len(sheets), "chars": sum(len(s) for s in shared),
                "sample": " · ".join(s for s in shared if s)[:220], "sheets": sheets}, None
    return None, "OOXML container with no ppt/ or xl/ parts"

# ── 2. FETCH ────────────────────────────────────────────────────────────────
# A file that arrives as bytes of the wrong kind is a FAILED fetch, not a success.
# The first K-CUR-006 run downloaded Google's >100 MB "virus scan warning" PAGE as
# "Module - Building Technology.pdf" and, because the page is text, it was counted OK.
# Nothing about the run looked wrong. This table is what makes that impossible.
DECLARED = {".pdf": "pdf", ".xlsx": "zip", ".pptx": "zip", ".docx": "zip",
            ".ppt": "ole", ".xls": "ole", ".doc": "ole", ".zip": "zip",
            ".csv": "text", ".txt": "text", ".html": "text"}

def drive_get(fid, dest):
    """Fetch a Drive file, handling the >100 MB confirm-token interstitial."""
    jar = dest + ".cookies"
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    r = subprocess.run(["curl", "-sL", "--max-time", "900", "-c", jar, "-b", jar, url,
                        "-o", dest, "-w", "%{http_code}"], capture_output=True, text=True)
    http = r.stdout.strip()
    kind, _ = sniff(dest) if os.path.exists(dest) else ("missing", "")
    if kind == "html":   # the >100 MB interstitial: the download is still coming
        page = open(dest, "rb").read().decode("utf-8", "ignore")
        fields = dict(re.findall(r'name="(id|export|confirm|uuid)"\s+value="([^"]*)"', page))
        if fields.get("confirm"):
            q = "&".join(f"{k}={v}" for k, v in fields.items())
            r = subprocess.run(["curl", "-sL", "--max-time", "1800", "-c", jar, "-b", jar,
                                f"https://drive.usercontent.google.com/download?{q}",
                                "-o", dest, "-w", "%{http_code}"], capture_output=True, text=True)
            http = r.stdout.strip() + " (confirm-flow)"
    if os.path.exists(jar):
        os.remove(jar)
    return http


def cmd_fetch(a):
    files = json.load(open(a.manifest))
    os.makedirs(a.dest, exist_ok=True)
    if os.path.abspath(a.dest).startswith(os.path.abspath(a.repo or "/nonexistent")):
        sys.exit("✗ refusing to fetch into the repository — binaries never touch the repo (II.6 r.8)")
    cap = (a.max_size or 0) * 1048576
    ok = fail = skipped = 0
    skip_log = []
    # biggest first: a cap that stops the run must stop it on the biggest file, not the last one
    for i, f in enumerate(sorted(files, key=lambda x: -(x.get("size") or 0)), 1):
        size = f.get("size") or 0
        safe = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in f["name"])
        dest = os.path.join(a.dest, f"{i:02d}_{safe}")
        if cap and size > cap:
            # II.6 restraint doctrine: a skipped file is LAWFUL — but it must be LOGGED, not dropped
            skipped += 1
            skip_log.append({"name": f["name"], "size": size, "reason": f"SIZE-SKIPPED (> {a.max_size} MB cap)",
                             "id": f["id"]})
            print(f"  [{i:02d}] SKIP  {safe[:52]}  {size/1048576:.1f} MB > cap {a.max_size} MB")
            continue
        want = DECLARED.get(os.path.splitext(f["name"])[1].lower())
        def verdict(path):
            got = os.path.getsize(path) if os.path.exists(path) else 0
            kind, label = sniff(path) if got else ("missing", "NOTHING DOWNLOADED")
            type_ok = (want is None) or (kind == want)
            return kind, label, got, type_ok
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            k, _l, _g, tok = verdict(dest)
            if tok:
                print(f"  [{i:02d}] cached {safe[:52]}  [{k}]"); ok += 1; continue
            print(f"  [{i:02d}] CACHED COPY IS NOT A {want.upper()} — refetching ({safe[:40]})")
            os.remove(dest)
        http = drive_get(f["id"], dest)
        kind, label, got, type_ok = verdict(dest)
        good = type_ok and kind not in ("missing", "html", "unknown")
        warn = " ⚠ " + label if kind in ("ole", "html") else ""
        if not type_ok and got:
            warn = f" ⚠ TYPE MISMATCH — declared {want}, received {kind} ({label})"
        print(f"  [{i:02d}] {'OK  ' if good else 'FAIL'} {safe[:52]}  {got/1048576:>7.1f} MB  [{kind}]{warn}")
        if not good and got:
            skip_log.append({"name": f["name"], "size": size, "id": f["id"],
                             "reason": f"FETCH FAILED — declared {want}, received {kind}"})
        if kind == "ole":
            # it downloaded fine — what it cannot do is be read by this harness's rung 1/2
            skip_log.append({"name": f["name"], "size": size, "id": f["id"],
                             "reason": "FETCHED but UNEXTRACTABLE — legacy binary Office format (rung 3: external converter)"})
        ok += good; fail += (not good)
    # The log is built from the DESTINATION, not from this run's control flow: a file
    # that was cached on an earlier run must still appear in the record. (First cut
    # logged the OLE file only when it was freshly downloaded — the second run dropped
    # the entry. An accountability log that depends on cache state is not a log.)
    logged = {s["name"] for s in skip_log}
    for f in sorted(files, key=lambda x: -(x.get("size") or 0)):
        if f["name"] in logged: continue
        p_i = None
        for cand in os.listdir(a.dest) if os.path.isdir(a.dest) else []:
            if cand.startswith("_") or cand.endswith(".cookies"): continue
            safe = "".join(c if c.isalnum() or c in " ._-()" else "_" for c in f["name"])
            if cand.endswith(safe): p_i = os.path.join(a.dest, cand); break
        if not p_i: continue
        kind, label = sniff(p_i)
        if kind == "ole":
            skip_log.append({"name": f["name"], "size": f.get("size"), "id": f["id"],
                             "reason": "FETCHED but UNEXTRACTABLE — legacy binary Office format (rung 3: external converter)"})
        elif kind in ("html", "unknown"):
            skip_log.append({"name": f["name"], "size": f.get("size"), "id": f["id"],
                             "reason": f"NOT A USABLE FILE — received {label}"})
    print(f"\nfetched {ok} · failed {fail} · size-skipped {skipped}")
    if skip_log:
        out = os.path.join(a.dest, "_SKIP_LOG.json")
        json.dump(skip_log, open(out, "w"), indent=1)
        print(f"⚠ {len(skip_log)} file(s) NOT fetched — logged to {os.path.basename(out)} (a skip is lawful ONLY if logged)")

# ── 3. EXTRACT: the recovery-ladder rung report ─────────────────────────────
def cmd_extract(a):
    import pymupdf as fitz   # pymupdf 1.24+: the module IS pymupdf; `fitz` is a shim
    report, others = [], []
    paths = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir)
                   if not f.startswith("_") and os.path.isfile(os.path.join(a.dir, f)))
    for path in paths:
        p = os.path.basename(path)
        kind, label = sniff(path)
        if kind != "pdf":
            o = {"file": p, "type": kind, "size": os.path.getsize(path)}
            if kind == "zip":
                info, err = office_text(path)
                if info:
                    o.update(info)
                    rung = f"EXTRACTED ({info['kind']}) — {info['units']} unit(s), {info['chars']} chars"
                    print(f"  {p[:50]:<52}          {rung}")
                    print(f"       sample: {info.get('sample','')[:110]}")
                else:
                    o["error"] = err; rung = f"OOXML NOT EXTRACTABLE — {err}"
                    print(f"  {p[:50]:<52}          {rung}")
            elif kind == "ole":
                rung = "LEGACY OLE — rung 3 (external converter) required; not a text-layer failure"
                print(f"  {p[:50]:<52}          {rung}")
            else:
                rung = "NON-PDF, NON-OOXML — logged, not extracted"
                print(f"  {p[:50]:<52}          {rung}")
            o["rung"] = rung; others.append(o); continue
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
            print(f"  {p[:50]:<52} {n:>5} pp  {wpp:>7.1f} w/p  {rung}")
            d.close()
        except Exception as e:
            report.append({"file": p, "error": str(e)})
            print(f"  {p[:50]:<52}  ERROR  {e}")
    # duplicates by content hash — AP-05
    seen = {}
    for path in paths:
        h = hashlib.md5(open(path, "rb").read()).hexdigest()
        seen.setdefault(h, []).append(os.path.basename(path))
    dups = {h: v for h, v in seen.items() if len(v) > 1}
    if dups:
        print("\n  ⚠ BYTE-IDENTICAL DUPLICATES (AP-05 mirror duplication):")
        for h, v in dups.items():
            print(f"    {h[:12]}…  {' == '.join(x[:40] for x in v)}")
    tot = sum(r.get("pages", 0) for r in report)
    img = sum(r.get("pages", 0) for r in report if "IMAGE-ONLY" in r.get("rung", ""))
    thin = [r for r in report if "THIN" in r.get("rung", "")]
    print(f"\n  {len(report)} PDF(s) · {tot} pages · {img} page(s) image-only"
          f" · {len(thin)} thin file(s)" + (f" · {len(others)} non-PDF object(s)" if others else ""))
    if dedup := sum(r.get("pages", 0) for h, v in dups.items()
                    for r in report if r["file"] in v[1:]):
        print(f"  duplicated payload: {dedup} page(s) reachable from a second filename")
    if a.out:
        json.dump({"files": report, "non_pdf": others, "duplicates": dups}, open(a.out, "w"), indent=1)
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
    f.add_argument("--max-size", type=float, default=0, help="MB cap; larger files are SIZE-SKIPPED and logged (0 = no cap)")
    e = sub.add_parser("extract"); e.add_argument("--dir", default="/tmp/rad_ingest"); e.add_argument("--out")
    v = sub.add_parser("verify");  v.add_argument("--pdf", required=True); v.add_argument("--page", type=int, required=True); v.add_argument("--out")
    v.add_argument("--repo", default=os.getcwd(), help="repo root; renders are refused inside it")
    a = ap.parse_args()
    {"list": cmd_list, "fetch": cmd_fetch, "extract": cmd_extract, "verify": cmd_verify}[a.cmd](a)

if __name__ == "__main__":
    main()
