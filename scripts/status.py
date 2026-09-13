#!/usr/bin/env python3
"""status.py — the Swarm Dashboard (patch 3300, SD-3300-02).
One command, one screen: the machine's whole state. For the Commander and for any
fresh AI that must know where things stand before acting. READ-ONLY — runs the
validator in a subprocess and reads the standing records; never modifies anything.
Stdlib only. No network (check 13 stays skipped offline, reported as skipped).
"""
import json, os, re, subprocess, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def R(p): return os.path.join(ROOT, p)
def read(p):
    try: return open(R(p), encoding="utf-8").read()
    except OSError: return ""
def last_date(text):
    """v2 (4400): the FIRST COLUMN of table rows only — decay/evidence dates in
    later cells are not activity (auditor F-07: a 2027 decay read as 2027 work)."""
    ds = []
    for ln in text.splitlines():
        m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})", ln.strip())
        if m: ds.append(m.group(1))
    return max(ds) if ds else None


def validator_block():
    """v2 (4400): consume the validator's structured API (import run_all) — no
    presentation scraping. Falls back to the human line only if the import fails."""
    try:
        sys.path.insert(0, R("scripts"))
        import validate as _v
        results = _v.run_all()
        fails, warns = _v._summary(results)
        online_skipped = any(("census skipped" in r["msg"] or "SKIPPED" in r["msg"]) for r in results)
        return (str(len(results)), str(len(results)-len(fails)-len(warns)),
                str(len(warns)), str(len(fails))), \
               [f"[check {r['check']}] {r['msg']}" for r in fails], online_skipped, False
    except Exception:
        # DEGRADED MODE (4500): structured API unavailable - scraping stdout is a
        # diagnostic fallback only. Surfaced loudly; refused in --strict.
        r = subprocess.run([sys.executable, R("scripts/validate.py")],
                           capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        m = re.search(r"(\d+) checks run · (\d+) pass · (\d+) warn · (\d+) fail", out)
        fails = [l.strip() for l in out.splitlines() if l.startswith("❌")]
        return (m.groups() if m else ("?", "?", "?", "?")), fails, False, True


def calendar_block(today):
    feed = read("Brain/courses/0_CALLENDER/TERM1_FEED.txt")
    mirror = read("Brain/courses/CALENDAR.md")
    newest = None
    if feed:
        ds = re.findall(r"DTSTART[^:\r\n]*:(\d{8})", feed.replace(" ", ""))
        if ds:
            n = max(ds); newest = f"{n[:4]}-{n[4:6]}-{n[6:]}"
    gen = re.search(r"\*\*Generated:\*\*\s*(\d{4}-\d{2}-\d{2})", mirror)
    age = (today - datetime.date.fromisoformat(gen.group(1))).days if gen else None
    return newest, (gen.group(1) if gen else None), age


def register_block(today):
    try:
        d = json.load(open(R("Brain/short_term/plan/TERM1_DEADLINES.json"), encoding="utf-8"))
    except Exception:
        return None, [], 0
    w1 = d.get("term", {}).get("week1_start")
    items = [i for i in d.get("items", []) if i.get("date")]
    upcoming = sorted((i["date"], i["course"], i["title"]) for i in items
                      if i["date"] >= today.isoformat())[:4]
    return w1, upcoming, len(d.get("feed_pending", []))


def main():
    today = datetime.date.today()
    line = "═" * 66
    print(line)
    print("  ☢️  RADIATION — MACHINE STATUS")
    print(line)
    v = read("README.md")
    vm = re.search(r"Version.*?(v[0-9.]+)", v)
    print(f"  version   : {vm.group(1) if vm else '?'}")

    (tot, ok, warn, fail), fails, offline, degraded = validator_block()
    print(f"  validator : {tot} checks · {ok} pass · {warn} warn · {fail} FAIL" +
          (" · link census offline-skipped" if offline else "")
          + (" · ⚠ DEGRADED (stdout fallback — structured API unavailable)" if degraded else ""))
    for f in fails[:4]:
        print(f"    {f[:118]}")

    newest, gen, age = calendar_block(today)
    cal = f"feed newest event {newest or '?'} · mirror generated {gen or 'NEVER'}"
    if age is not None: cal += f" ({age}d ago)"
    if newest and newest < today.isoformat(): cal += "  ⚠ FEED STALE — re-export + push"
    print(f"  calendar  : {cal}")

    w1, upcoming, pending = register_block(today)
    print(f"  register  : week1_start {w1 or 'ABSENT'} · next due:")
    for dt, c, t in upcoming:
        days = (datetime.date.fromisoformat(dt) - today).days
        mark = "  <- TODAY" if days == 0 else (f"  ({days}d)" if days > 0 else "  (past)")
        print(f"    {dt} {mark:9} {c:9} {t[:44]}")
    if pending: print(f"    WARNING {pending} feed items await your attribution (feed_pending)")

    pipe = {}
    mdir = R("scaffolding/neurons/motorneurons")
    if os.path.isdir(mdir):
        for f in sorted(os.listdir(mdir)):
            # convention (3600 templates): TID-<date>-<id>_orders.md
            if f.startswith("TID-") and f.endswith("_orders.md"):
                tid = f[4:-10]
                try:
                    m2 = re.search(r"Status:\*{0,2}\s*([A-Za-z]+(?:\(\d\))?)",
                                   open(os.path.join(mdir, f), encoding="utf-8").read(2048))
                    st = m2.group(1) if m2 else "?"
                except OSError:
                    st = "?"
                if st != "CLOSED":
                    pipe[tid] = st
    print("  pipeline  : " + (f"{len(pipe)} in flight: " +
          ", ".join(f"{k}…{v}" for k, v in sorted(pipe.items())[:4]) if pipe
          else "all TID chains CLOSED"))

    log = read("docs/shrine/LOG.md"); led = read("Brain/frontal_lobe/task_ledger.md")
    hb, ld = last_date(log), last_date(led)
    beat = f"last heartbeat {hb}" if hb else "no heartbeats"
    if hb and ld and ld > hb: beat += f"  LAGS ledger ({ld}) — a session worked and filed none"
    print(f"  shrine    : {beat}")

    print(line)
    print("  rails: ship zips · push is legal effect · verify from git, never memory")
    return 0


def self_test():
    ok = 0
    t1 = last_date("| 2026-09-01 | session | later col 2027-09-13 |\n| 2026-09-14 | session | decay 2027-09-13 |")
    v1 = (t1 == "2026-09-14"); ok += v1
    print(f"  vector 1 first-column-only dates -> {'PASS' if v1 else t1}")
    t2 = last_date("prose date 2027-01-01 without table row")
    v2 = (t2 is None); ok += v2
    print(f"  vector 2 non-table dates ignored -> {'PASS' if v2 else t2}")
    t3 = last_date("| 2026-08-30 | a |\n| 2026-09-14 | b |\n| 2026-08-31 | c |")
    v3 = (t3 == "2026-09-14"); ok += v3
    print(f"  vector 3 max across unordered rows -> {'PASS' if v3 else t3}")
    print(f"status self-test: {ok}/3 vectors")
    return 0 if ok == 3 else 1

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    if "--strict" in sys.argv:
        res = None
        try:
            sys.path.insert(0, R("scripts"))
            import validate as _v
            res = _v.run_all()
        except Exception:
            res = None
        if res is None:
            print("strict: DEGRADED — structured validator API unavailable; refusing strict pass")
            sys.exit(3)
        f, _w = _v._summary(res)
        print(f"strict: {len(res)} checks, {len(f)} FAIL-class finding(s)")
        sys.exit(1 if f else 0)

    sys.exit(main())
