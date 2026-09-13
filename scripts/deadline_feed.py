#!/usr/bin/env python3
"""deadline_feed.py — the Deadline Engine (patch 3100).
Ingests the committed LMS feed (Brain/courses/0_CALLENDER/TERM1_FEED.txt — a
Blackboard export; GitHub rejects the .ics extension, the parser reads content)
into the term register (TERM1_DEADLINES.json).

Design laws:
  CONSERVATIVE ATTRIBUTION — a course code in the title wins; then fuzzy match
  against EXISTING register items (their dates anchor the week-based records);
  then a citable content-keyword table; anything else is UNATTRIBUTED for the
  Commander, never guessed.
  IDEMPOTENT — re-runs skip what they already merged (feed_id = hash of
  summary+date). The Commander re-exports daily; the register must not dup.
  STALE-HONEST — pre-term items are counted and skipped, never silently kept.

Dry-run by default. --write commits changes to the register. Stdlib only.
"""
import argparse, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "Brain", "courses", "0_CALLENDER", "TERM1_FEED.txt")
REGISTER = os.path.join(ROOT, "Brain", "short_term", "plan", "TERM1_DEADLINES.json")

# content → course keyword table (citable: each row names its evidence)
KEYWORDS = [
    (r"\bAR173\b|PLANNING 2|URBAN DESIGN", "AR173-1P", "explicit course code in summary"),
    (r"\bAR163\b|BUILDING TECHNOLOGY|BUILDING LAWS", "AR163-1P", "explicit course code / course-title match"),
    (r"\bAR153P\b|PLUMBING|SANITARY|\bSP1\d\d\b|\bSP2\d\d\b|\bBU\d\b|WATER LINE|ISOME", "AR153P",
     "Building-Utilities domain (K-CUR-005 built for AR153P; SP=coversheet plates)"),
    (r"FORCE VECTOR|FORCE SYSTEM|RESULTANT|RIGID BOD|EQUILIBRIUM|INTERNAL FORCE|CENTROID|MOMENT|STATICS|MEC30", "MEC30-7",
     "Statics-of-Rigid-Bodies content (course record's own syllabus terms)"),
    (r"DATA SCIENCE|PYTHON|PANDAS|NOTEBOOK", "DSS10", "course-title match"),
    (r"PHILIPPINE HISTORY|READINGS IN", "GED103", "course-title match"),
]
TYPE_PATTERNS = [
    (r"exam|EXAM", "exam"), (r"quiz|QUIZ|\bSQ\d|\bLQ\d", "quiz"),
    (r"assessment", "assessment"), (r"coursera", "coursera"),
    (r"homework|classwork|\bHW\b", "homework"), (r"plate", "plate"),
    (r"collaborative|group", "groupwork"), (r"activity", "activity"),
    (r"assignment", "assignment"), (r"due|deadline|submit", "deadline"),
]
WEEK1_INFERRED = "2026-08-24"
WEEK1_NOTE = ("INFERRED from Coursera Progress Report Week 1 ending Sun 2026-08-30 "
              "(feed TERM1_FEED.txt); W3 ending 2026-09-13 confirms the cadence. "
              "Awaiting Commander confirm; change term.week1_start_source to 'commander' to ratify.")


def feed_id(summary, date):
    return hashlib.sha1(f"{summary}|{date}".encode()).hexdigest()[:12]


STOP = {"of", "a", "the", "in", "and", "to", "for"}

def norm_tokens(title):
    t = title.lower()
    t = re.sub(r"progress\s+report", "pr", t)          # Coursera Progress Report = PR
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\bpr\s*(\d+)", r"pr \1", t)           # pr2 → pr 2 (either spelling aligns)
    t = re.sub(r"\bweek\b", " ", t)
    return [w for w in t.split() if w and w not in STOP]


def match_existing(title, items):
    """Return an existing register item whose title is substantially the same task."""
    toks = set(norm_tokens(title))
    nums = set(re.findall(r"\d+", " ".join(toks)))     # PR2 must not eat PR3
    best, best_score = None, 0
    for it in items:
        rtoks = set(norm_tokens(it.get("title", "")))
        if not rtoks:
            continue
        rnums = set(re.findall(r"\d+", " ".join(rtoks)))
        if nums and rnums and nums != rnums:
            continue
        score = len(toks & rtoks) / max(1, len(toks | rtoks))
        if score > best_score:
            best, best_score = it, score
    return best if best_score >= 0.55 else None


def map_course(title):
    for pat, course, why in KEYWORDS:
        if re.search(pat, title, re.I):
            return course, why
    return None, None


def map_type(title):
    for pat, typ in TYPE_PATTERNS:
        if re.search(pat, title, re.I):
            return typ
    return "task"


def meeting_series(events):
    """Titles occurring 3+ times are recurring class meetings, not deadlines.
    (Probe-caught: AR173's twice-weekly meeting title was anchoring itself into
    the deadline register — the planner would have scheduled 'class' as homework.)"""
    counts = {}
    for ev in events:
        counts[ev["summary"]] = counts.get(ev["summary"], 0) + 1
    return {s for s, n in counts.items() if n >= 3}


def load_feed(path):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import ics_normalize as icsn  # THE one parser — delegation, never a second one
    import datetime
    evs = icsn.expand_all(icsn.parse_ics(open(path, encoding="utf-8").read(), "Asia/Manila"),
                          "Asia/Manila", horizon_days=None)
    out = []
    for e in evs:
        out.append({"summary": e["summary"], "date": e["start"].date().isoformat()})
    return out


def run(feed_path, register_path, write=False):
    import datetime
    events = load_feed(feed_path)
    reg = json.load(open(register_path, encoding="utf-8"))
    items = reg.get("items", [])
    course_k = {c.get("code"): c.get("k_id") for c in reg.get("courses", []) if isinstance(c, dict)}
    w1 = reg.get("term", {}).get("week1_start") or WEEK1_INFERRED
    w1d = datetime.date.fromisoformat(w1)

    existing_ids = {it.get("feed_id") for it in items + reg.get("feed_pending", [])
                    if it.get("feed_id")}
    meetings = meeting_series(events)
    added, anchored, stale, dup, meetings_skipped = [], [], 0, 0, 0
    for ev in events:
        if ev["summary"] in meetings:
            meetings_skipped += 1
            continue
        fid = feed_id(ev["summary"], ev["date"])
        d = datetime.date.fromisoformat(ev["date"])
        if d < w1d:
            stale += 1
            continue
        if fid in existing_ids:
            dup += 1
            continue
        hit = match_existing(ev["summary"], items)
        course, why = (hit["course"], "anchored to existing register item") if hit else map_course(ev["summary"])
        if hit is not None:
            hit["date"] = ev["date"]                       # the week-based record gains a real date
            hit["feed_id"] = fid
            anchored.append((ev, hit["course"]))
            continue
        pending = course is None
        if pending:
            why = "no code, no register match, no keyword — Commander decides"
            # sibling hint: same title-family lives in exactly one course → SUGGEST, never assign
            base = {w for w in norm_tokens(ev["summary"]) if not w.isdigit()}
            sib = {it["course"] for it in items
                   if it.get("course") and base and base <= set(norm_tokens(it.get("title", ""))) | {"*"}}
            if len(sib) == 1:
                why += f" (likely {sib.pop()}: its sibling series is registered)"
        else:
            k_id = course_k.get(course)
        entry = {"course": course, "k_id": None if pending else course_k.get(course),
                 "week": ((d - w1d).days // 7) + 1,
                 "type": map_type(ev["summary"]), "title": ev["summary"], "weight": None,
                 "module": None, "source": f"LMS feed (TERM1_FEED.txt) · {why}",
                 "date": ev["date"], "feed_id": fid}
        if pending:
            # UNATTRIBUTED items NEVER enter items[] — check 20's register integrity
            # is a feature: only well-formed deadlines get ranked. Pending goes to
            # the Commander's queue with its hint attached.
            reg.setdefault("feed_pending", []).append(entry)
            added.append(entry)
        else:
            items.append(entry)
            added.append(entry)

    changed = bool(added) or bool(anchored)
    if reg.get("term", {}).get("week1_start") is None:
        reg["term"]["week1_start"] = WEEK1_INFERRED
        reg["term"]["week1_start_note"] = WEEK1_NOTE
        reg["term"]["week1_start_source"] = "inferred"
        changed = True
    if added or anchored:
        reg.setdefault("derived_from", []).append(
            f"LMS feed merge {datetime.date.today().isoformat()}: "
            f"{len(added)} added · {len(anchored)} anchored · {stale} stale skipped · {dup} dups skipped")

    print(f"   feed events : {len(events)} · meeting-series skipped: {meetings_skipped} "
          f"({len(meetings)} series — meetings live in SCHEDULE.md, not the deadline register)")
    print(f"   stale (<{w1}) : {stale} skipped · already-merged dups: {dup} skipped")
    print(f"   anchored    : {len(anchored)} existing week-based records now carry real dates")
    for ev, c in anchored[:8]:
        print(f"     · {ev['date']} → {c}: {ev['summary'][:52]}")
    print(f"   added       : {len(added)}")
    for n in added[:8]:
        print(f"     · {n['date']} {(n['course'] or 'UNATTRIBUTED'):12} {n['title'][:48]}")
    unattr = reg.get("feed_pending", [])
    if unattr:
        print(f"   ⚠ {len(unattr)} feed_pending (unattributed — Commander's queue, with hints):")
        for n in unattr[:8]:
            print(f"     · {n['date']} {n['title'][:58]}")
    if write:
        json.dump(reg, open(register_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(register_path, "a", encoding="utf-8").write("\n")
        print(f"   ✍ register written ({len(items)} items)")
    else:
        print("   (dry-run — rerun with --write to apply)")
    return 0


def self_test():
    ok, fails = 0, []
    def check(name, cond):
        nonlocal ok
        ok += 1 if cond else 0
        if not cond: fails.append(name)
    check("PR aliasing merges Progress Report Week 2 into 'Coursera PR2'",
          match_existing("Coursera Progress Report: Week 2",
                         [{"title": "Coursera PR1"}, {"title": "Coursera PR2"}])["title"] == "Coursera PR2")
    check("PR numbering disagreement does NOT match",
          match_existing("Coursera Progress Report: Week 3", [{"title": "Coursera PR1"}]) is None)
    check("unrelated titles do not match",
          match_existing("Assessment 4", [{"title": "Coursera PR1"}]) is None)
    c, w = map_course("AR173-1P_A54: PLANNING 2 — FUNDAMENTALS")
    check("explicit code wins", c == "AR173-1P" and "explicit" in w)
    c, _ = map_course("SP200 Sanitary Plumbing Layout")
    check("plumbing → AR153P", c == "AR153P")
    c, _ = map_course("Homework/Classwork 6: Internal Forces")
    check("statics content → MEC30-7", c == "MEC30-7")
    c, _ = map_course("Mystery Item")
    check("unknown stays unattributed", c is None)
    check("type inference", map_type("SQ1*") == "quiz" and map_type("Assessment 1") == "assessment")
    check("feed_id stable", feed_id("a", "2026-09-13") == feed_id("a", "2026-09-13"))
    ms = meeting_series([{"summary": "CLASS X"}] * 3 + [{"summary": "Quiz 1"}, {"summary": "Quiz 1"}])
    check("meeting series (3+ identical) detected, single deadlines untouched", "CLASS X" in ms and "Quiz 1" not in ms)
    c, _ = map_course("Homework/Classwork 2: Force System Resultants")
    check("force-system resultants → MEC30-7", c == "MEC30-7")
    print(f"✅ deadline_feed self-test: {ok} passed, {len(fails)} failed" + (f" — {fails}" if fails else ""))
    return not fails


def main():
    p = argparse.ArgumentParser(description="LMS feed → term register (the Deadline Engine).")
    p.add_argument("--feed", default=FEED)
    p.add_argument("--register", default=REGISTER)
    p.add_argument("--write", action="store_true", help="apply to the register (default: dry-run)")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        sys.exit(0 if self_test() else 1)
    if not os.path.exists(a.feed):
        sys.exit(f"no feed at {a.feed}")
    sys.exit(run(a.feed, a.register, a.write))


if __name__ == "__main__":
    main()
