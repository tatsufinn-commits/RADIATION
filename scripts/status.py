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
    ds = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return max(ds) if ds else None


def validator_block():
    r = subprocess.run([sys.executable, R("scripts/validate.py")],
                       capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) checks run · (\d+) pass · (\d+) warn · (\d+) fail", out)
    fails = [l.strip() for l in out.splitlines() if l.startswith("❌")]
    return (m.groups() if m else ("?", "?", "?", "?")), fails, ("census skipped" in out or "SKIPPED" in out)


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

    (tot, ok, warn, fail), fails, offline = validator_block()
    print(f"  validator : {tot} checks · {ok} pass · {warn} warn · {fail} FAIL" +
          (" · link census offline-skipped" if offline else ""))
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

    pipe = []
    ndir = R("scaffolding/neurons")
    if os.path.isdir(ndir):
        for stage in ("sensoryneurons", "interneurons", "motorneurons"):
            sd = os.path.join(ndir, stage)
            if os.path.isdir(sd):
                for f in sorted(os.listdir(sd)):
                    if f.startswith("TID_") and f.endswith(".md"):
                        try:
                            m = re.search(r"Status:\s*([A-Za-z]+(?:\(\d\))?)",
                                          open(os.path.join(sd, f), encoding="utf-8").read(2048))
                            st = m.group(1) if m else "?"
                        except OSError:
                            st = "?"
                        if st not in ("CLOSED",):
                            pipe.append(f"{f[4:14]}…{st}")
    print("  pipeline  : " + (f"{len(pipe)} in flight: {', '.join(pipe[:4])}" if pipe
                              else "nothing in flight (all TIDs CLOSED)"))

    log = read("docs/shrine/LOG.md"); led = read("Brain/frontal_lobe/task_ledger.md")
    hb, ld = last_date(log), last_date(led)
    beat = f"last heartbeat {hb}" if hb else "no heartbeats"
    if hb and ld and ld > hb: beat += f"  LAGS ledger ({ld}) — a session worked and filed none"
    print(f"  shrine    : {beat}")

    print(line)
    print("  rails: ship zips · push is legal effect · verify from git, never memory")
    return 0


if __name__ == "__main__":
    sys.exit(main())
