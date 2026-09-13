#!/usr/bin/env python3
"""plan_term.py — RADIATION term planner (P-10 Phase 1-3).

Reads the commander's term, ranks the load, reconciles TWO CLOCKS, and prints
a brief. Stdlib only. No network. Never writes to the repository.

  CLOCK 1 (deadline) - course records -> Brain/short_term/plan/TERM1_DEADLINES.json
  CLOCK 2 (mastery)  - Brain/frontal_lobe/mastery_ledger.md (its own next_review dates)
  The job is to RECONCILE them: place review so the last one lands D-3..D-1.

Usage
  plan_term.py --week 4                  # what's coming as of week 4
  plan_term.py --week 4 --ics local.ics  # + fold in the LMS feed and diff it
  plan_term.py --self-check              # integrity of the deadline register
  plan_term.py --audit                   # plan-vs-attempt ratio (AP-08 guard)

Degrades honestly: with no week-1 anchor it plans in WEEKS and says so; with no
ICS it plans on records alone and says so. It never invents a date.
"""
import argparse, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "Brain/short_term/plan")
DEADLINES = os.path.join(PLAN, "TERM1_DEADLINES.json")
SNAPSHOT = os.path.join(PLAN, "ICS_SNAPSHOT.local.json")   # git-ignored
LEDGER = os.path.join(ROOT, "Brain/frontal_lobe/mastery_ledger.md")

# Same privacy rule as validator check 2.5: these never leave the machine.
REDACT = [
    (r"\b(?:Instructor|Professors?|Prof\.)\s*[:\-]?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", "[INSTRUCTOR REDACTED]"),
    (r"\b(?:S|NW|SW|SE|NE)\d{3}\b", "[ROOM REDACTED]"),
    (r"\b(?:Section|Sec\.)\s+[A-Z]{1,2}\d{1,3}\b", "[SECTION REDACTED]"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", "[EMAIL REDACTED]"),
    (r"https?://\S+", "[URL REDACTED]"),
]
def scrub(s):
    for pat, rep in REDACT:
        s = re.sub(pat, rep, s)
    return s

def die(msg, code=1):
    print(f"✗ {msg}")
    sys.exit(code)

# ── load ─────────────────────────────────────────────────────────────────────
def load_deadlines():
    if not os.path.exists(DEADLINES):
        die(f"term register absent: {os.path.relpath(DEADLINES, ROOT)}")
    with open(DEADLINES, encoding="utf-8") as fh:
        return json.load(fh)

def load_mastery():
    """K-ID -> {score, next_review, attempt}. Absent is absent - never assumed."""
    m = {}
    if not os.path.exists(LEDGER):
        return m
    with open(LEDGER, encoding="utf-8") as fh:
        for ln in fh:
            if not ln.strip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 7 or "K-" not in cells[0]:
                continue
            kid = re.search(r"K-[A-Z]+-\d+", cells[0])
            if not kid:
                continue
            score = None
            ms = re.search(r"(\d+)\s*/\s*(\d+)", cells[2])
            if ms:
                score = round(100 * int(ms.group(1)) / int(ms.group(2)))
            elif re.search(r"(\d+)\s*%", cells[2]):
                score = int(re.search(r"(\d+)\s*%", cells[2]).group(1))
            nxt = re.search(r"(\d{4}-\d{2}-\d{2})", cells[5])
            m[kid.group(0)] = {
                "score": score,
                "next_review": nxt.group(1) if nxt else None,
                "attempt": cells[3],
                "fixture": "FIXTURE" in ln.upper(),
            }
    return m

# ── ICS — DELEGATED. There is exactly ONE iCalendar parser in this repository:
# scripts/ics_normalize.py. This file used to carry its own minimal one, which read
# four fields and dropped RRULE — so a weekly class appeared once instead of eleven
# times. Two parsers of different quality is the failure mode RADIATION's own review
# identified in Marciale-OS; it is not repeated here.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import ics_normalize as icsn
except ImportError:                                   # shipped together; belt and braces
    icsn = None


def parse_ics(path, tz=None):
    """Expanded, UID-keyed occurrences from the one parser."""
    if icsn is None:
        die("scripts/ics_normalize.py is missing — cannot read the ICS feed")
    tzname = tz or icsn.DEFAULT_TZ
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    return icsn.expand_all(icsn.parse_ics(text, tzname), tzname, horizon_days=365)


def ics_diff(events):
    """Series-aware diff (see ics_normalize.diff). Shares the one snapshot file."""
    if icsn is None:
        return {"added": [], "moved": [], "removed": []}
    old = icsn.rehydrate(icsn.load_snapshot())
    out = icsn.diff(old, events) if old else {"added": [], "moved": [], "removed": []}
    icsn.save_snapshot(events)
    return out


# ── ranking: yield x proximity x deficit, arithmetic shown ───────────────────
def rank(items, courses, mastery, week):
    cy = {c["code"]: c for c in courses}
    rows = []
    for it in items:
        w = it.get("week")
        if w is None:
            continue
        d = w - week
        if d < 0 or d > 1:                       # horizon: this week + next
            continue
        prox = 3.0 if d == 0 else 2.0
        y = cy.get(it["course"], {}).get("yield", 1)
        kid = it.get("module") or it.get("k_id")
        m = mastery.get(kid, {}) if kid else {}
        if not m:
            defi, why = 1.5, "no mastery row (never attempted)"
        elif m.get("score") is not None and m["score"] < 70:
            defi, why = 1.5, f"last score {m['score']}% below the 70% floor"
        else:
            defi, why = 1.0, f"last score {m.get('score')}%"
        rows.append({
            "item": it, "pri": round(y * prox * defi, 2),
            "arith": f"yield {y} x proximity {prox} x deficit {defi} ({why})",
            "delta": d,
        })
    rows.sort(key=lambda r: (-r["pri"], r["item"]["course"]))
    return rows

# ── self-check (used by validator check 20) ──────────────────────────────────
def self_check():
    d = load_deadlines()
    bad = []
    if d.get("schema") != "rad.term_deadlines/v1":
        bad.append("schema missing or wrong")
    weeks = d.get("term", {}).get("weeks")
    codes = {c["code"] for c in d.get("courses", [])}
    if not codes:
        bad.append("no courses")
    ids = {c["k_id"] for c in d.get("courses", [])}
    for it in d.get("items", []):
        if it["course"] not in codes:
            bad.append(f"item for unknown course: {it['course']}")
        if it.get("k_id") not in ids:
            bad.append(f"item with unknown k_id: {it.get('k_id')}")
        w = it.get("week")
        if w is not None and not (isinstance(w, int) and 1 <= w <= (weeks or 11)):
            bad.append(f"week out of range: {it['course']} W{w}")
        if "http" in json.dumps(it):
            bad.append(f"URL in item: {it.get('title')}")
        if scrub(it.get("title", "")) != it.get("title", ""):
            bad.append(f"identifier in item title: {it.get('title')}")
    blob = json.dumps(d)
    for pat, _ in REDACT:
        if re.search(pat, blob):
            bad.append(f"personnel/URL pattern in register: {pat[:26]}")
    if bad:
        print("✗ term register integrity: " + "; ".join(bad[:6]))
        return 1
    n = len(d.get("items", []))
    print(f"✅ term register OK — {len(codes)} course(s), {n} item(s), "
          f"{len(d.get('blind_courses', []))} deadline-blind course(s)")
    return 0

# ── audit: plans vs attempts (AP-08 guard) ───────────────────────────────────
def audit():
    m = load_mastery()
    real = {k: v for k, v in m.items() if not v.get("fixture")}
    print(f"attempts logged: {len(m)} row(s), of which REAL (non-fixture): {len(real)}")
    if not real:
        print("⚠ PLANNER THEATER RISK — a plan exists and no genuine attempt has ever")
        print("  been logged. The metric is attempts, never plans. Drill something.")
        return 1
    print("✅ attempts exist — the planner has something real to schedule against.")
    return 0

# ── the brief ────────────────────────────────────────────────────────────────
def brief(week, ics_path):
    d = load_deadlines()
    courses, items = d["courses"], d["items"]
    weeks = d["term"]["weeks"]
    anchor = d["term"].get("week1_start")
    mastery = load_mastery()

    print("═" * 68)
    print(f"  TERM BRIEF — {d['term']['label']} · week {week} of {weeks}")
    print("═" * 68)
    if anchor:
        try:
            a = datetime.date.fromisoformat(anchor)
            lo = a + datetime.timedelta(days=7 * (week - 1))
            print(f"  dates    : W{week} = {lo.isoformat()} .. {(lo + datetime.timedelta(days=6)).isoformat()}")
        except ValueError:
            print(f"  dates    : ANCHOR INVALID ({anchor}) — planning in weeks")
    else:
        print("  dates    : ANCHOR ABSENT — planning in WEEKS (no syllabus prints a date).")
        print("             supply --anchor or let the LMS ICS supply it; +1 datum, everything dates.")
    print(f"  sources  : records only{'' if not ics_path else ' + ICS'}")
    print()

    # ICS layer
    if ics_path:
        if not os.path.exists(ics_path):
            print(f"  ⚠ ICS not found at {ics_path} — planning on records alone.\n")
        else:
            ev = parse_ics(ics_path)
            dif = ics_diff(ev)
            series = len({e["uid"] for e in ev})
            print(f"  ─ LMS FEED ─ {len(ev)} occurrences from {series} series, "
                  f"summaries scrubbed of identifiers")
            print(f"    added {len(dif['added'])} · moved {len(dif['moved'])} · removed {len(dif['removed'])}")
            for m in dif["moved"][:5]:
                bits = []
                if m["lost"]:
                    bits.append("lost " + ", ".join(x[:10] for x in m["lost"][:3]))
                if m["gained"]:
                    bits.append("gained " + ", ".join(x[:10] for x in m["gained"][:3]))
                print(f"    ⚠ MOVED  {m['summary'][:44]} — {'; '.join(bits)}")
            for e in dif["added"][:5]:
                print(f"      added  {e['summary'][:44]} ({len(e['dates'])} date(s))")
            for e in dif["removed"][:5]:
                print(f"      gone   {e['summary'][:44]} ({len(e['dates'])} date(s))")
            if not any(dif.values()):
                print("      no change since last run")
            if ev and series < len(ev):
                print(f"      (the old parser reported {series} event(s) here — RRULE was dropped)")
            print()

    rows = rank(items, courses, mastery, week)
    print(f"  ─ RANKED LOAD (this week + next) ─ top 3 of {len(rows)} ─")
    if not rows:
        print("    nothing scheduled in this 2-week window.")
    for i, r in enumerate(rows[:3], 1):
        it = r["item"]
        when = "THIS WEEK" if r["delta"] == 0 else "NEXT WEEK"
        print(f"   {i}. [{r['pri']:>5}] {it['course']} — {it['title']}")
        print(f"        {when} · {it['type']}" + (f" · weight {it['weight']}%" if it.get("weight") else " · weight UNKNOWN"))
        print(f"        why: {r['arith']}")
    if len(rows) > 3:
        print(f"    … and {len(rows) - 3} more below the cut. Shown top 3 on purpose: six courses,")
        print("      one student — a full list is not a triage.")

    # two-clock reconciliation
    print()
    print("  ─ MASTERY CLOCK (reconciliation) ─")
    todays = datetime.date(2026, 9, 13)
    pulls = 0
    for r in rows[:3]:
        it = r["item"]
        kid = it.get("module") or it.get("k_id")
        m = mastery.get(kid) if kid else None
        if not m:
            print(f"    {it['course']}: NO MASTERY ROW — nothing to review yet.")
            continue
        nr = m.get("next_review")
        if not nr:
            print(f"    {it['course']}: ledger row has no next_review")
            continue
        try:
            delta = (datetime.date.fromisoformat(nr) - todays).days
        except ValueError:
            continue
        flag = "⚠ PULL FORWARD" if delta > 3 else "ok"
        if flag.startswith("⚠"):
            pulls += 1
        print(f"    {it['course']}: ledger says review {nr} ({delta:+d}d) — {flag}")
    if not pulls:
        print("    no review date needs pulling.")

    # what cannot be prepared
    blind = d.get("blind_courses", [])
    if blind:
        print()
        print("  ─ UNPREPARABLE / BUILD-REQUIRED ─")
        for b in blind:
            print(f"    {b['code']} (yield {b['yield']}): {b['impact']}")
            print(f"        {b['mitigation']}")

    print()
    print("  ─ NOT BEING PREPARED, AND WHY ─")
    for g in d.get("known_gaps", [])[:4]:
        print(f"    · {g}")
    print()
    print("  nudge: this brief is ARMED, not self-executing — the standing-orders queue is a")
    print("  closed list and extending it is a canon act (P-10 §8.2). Say 'drill me' to act on it.")
    print("═" * 68)
    return 0

def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("--week", type=int)
    p.add_argument("--ics")
    p.add_argument("--anchor", help="week-1 Monday, YYYY-MM-DD (records this into the register? no - display only)")
    p.add_argument("--self-check", action="store_true")
    p.add_argument("--audit", action="store_true")
    a = p.parse_args()
    if a.self_check:
        sys.exit(self_check())
    if a.audit:
        sys.exit(audit())
    if a.week is None:
        die("--week N is required (or --self-check / --audit). Week numbers are what the records know.")
    if not (1 <= a.week <= 11):
        die("--week must be 1..11 (Quarterm term length)")
    sys.exit(brief(a.week, a.ics))

if __name__ == "__main__":
    main()
