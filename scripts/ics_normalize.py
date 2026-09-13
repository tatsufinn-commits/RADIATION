#!/usr/bin/env python3
"""ics_normalize.py — the ONE iCalendar parser for RADIATION (RFC 5545 subset).

Replaces the minimal inline parser that used to live in plan_term.py. That parser
dropped RRULE entirely, so a weekly class appeared once instead of eleven times,
and every recurring deadline was invisible after its first date.

WHAT THIS HANDLES THAT THE OLD ONE DID NOT
  · RRULE expansion — FREQ/INTERVAL/BYDAY/COUNT/UNTIL
  · RDATE (extra dates) and EXDATE (cancelled single occurrences)
  · RECURRENCE-ID overrides — a rescheduled occurrence REPLACES the original
    instead of appearing beside it as a phantom second event
  · STATUS:CANCELLED filtered out
  · TZID resolved through zoneinfo (the old parser ignored the zone entirely)
  · RFC 5545 escape decoding (\\, \\; \\n) and quoted parameter values
  · DTEND honoured, so durations survive
  · series-aware diffing — "moved" now means the SERIES moved, and a single
    cancelled date inside a series is reported as such

Usage
    python3 scripts/ics_normalize.py --ics local.ics                 # summary
    python3 scripts/ics_normalize.py --ics local.ics --md            # AI-readable
    python3 scripts/ics_normalize.py --ics local.ics --json          # machine
    python3 scripts/ics_normalize.py --fetch                         # URL from env
    python3 scripts/ics_normalize.py --ics local.ics --write         # durable output
    python3 scripts/ics_normalize.py --self-test                     # fixtures

THE URL RULE (non-negotiable): the feed URL is a CREDENTIAL. It is read from the
environment variable RADIATION_ICS_URL — never from a file, never committed, never
printed. Every summary and description is scrubbed before it reaches any output.

Stdlib only. No network unless --fetch is passed.
"""
import argparse, datetime, json, os, re, sys

try:
    from zoneinfo import ZoneInfo
except ImportError:                       # Python < 3.9 — degrade, and say so
    ZoneInfo = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(ROOT, "Brain", "short_term", "plan")
DEADLINES = os.path.join(PLAN, "TERM1_DEADLINES.json")
SNAPSHOT = os.path.join(PLAN, "ICS_SNAPSHOT.local.json")      # git-ignored
OUT_MD = os.path.join(PLAN, "TERM1_CALENDAR.local.md")        # git-ignored
OUT_JSON = os.path.join(PLAN, "TERM1_CALENDAR.local.json")    # git-ignored
PUBLIC_MD = os.path.join(ROOT, "Brain", "courses", "CALENDAR.md")  # COMMITTED scrubbed mirror
ENV_URL = "RADIATION_ICS_URL"
FEED_TXT = os.path.join(ROOT, "Brain", "courses", "0_CALLENDER", "TERM1_FEED.txt")  # the committed LMS export (.txt: GitHub rejects .ics uploads; the parser reads content)
DEFAULT_TZ = "Asia/Manila"

# Same privacy rule as validator check 2.5 and plan_term.py. These never ship.
REDACT = [
    (r"\b(?:Instructor|Professors?|Prof\.)\s*[:\-]?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", "[INSTRUCTOR REDACTED]"),
    (r"\b(?:S|NW|SW|SE|NE)\d{3}\b", "[ROOM REDACTED]"),
    (r"\b(?:Section|Sec\.)\s+[A-Z]{1,2}\d{1,3}\b", "[SECTION REDACTED]"),
    # bare section tokens riding inside event titles ("AR173-1P_A54_1Q2627") — the
    # validator's CV_DENY_LOCATION caught the mirror carrying them (probe-caught
    # 2026-09-13): keep this list in step with validate.py CV_DENY_LOCATION.
    (r"(?<![A-Za-z0-9])(?:E01|A54|C5)(?![A-Za-z0-9])", "[SECTION REDACTED]"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", "[EMAIL REDACTED]"),
    (r"https?://\S+", "[URL REDACTED]"),
]
DAY_INDEX = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}
DAY_NAME = {v: k for k, v in DAY_INDEX.items()}


def scrub(s):
    for pat, rep in REDACT:
        s = re.sub(pat, rep, s)
    return s


# ─────────────────────────── parsing primitives ──────────────────────────────

def unfold(text):
    """RFC 5545 §3.1 — a folded line continues after CRLF + one space/tab."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out = []
    for line in text.split("\n"):
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def unescape(v):
    """RFC 5545 §3.3.11 TEXT escaping."""
    out, i = [], 0
    while i < len(v):
        c = v[i]
        if c == "\\" and i + 1 < len(v):
            n = v[i + 1]
            out.append({"n": "\n", "N": "\n", ",": ",", ";": ";", "\\": "\\"}.get(n, n))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def split_prop(line):
    """Split NAME;PARAM=V;PARAM2="a,b":VALUE on the first *unquoted* colon."""
    q = False
    for i, c in enumerate(line):
        if c == '"':
            q = not q
        elif c == ":" and not q:
            head, value = line[:i], line[i + 1:]
            parts = head.split(";")
            return parts[0].upper().strip(), ";".join(parts[1:]), value
    return "", "", ""


def _tzid(params, default_tz):
    m = re.search(r'TZID=([^;:]+)', params or "")
    name = m.group(1).strip('"') if m else None
    if name and ZoneInfo:
        try:
            return ZoneInfo(name), name
        except Exception:
            return None, name                       # unknown zone → floating local
    return (ZoneInfo(default_tz) if (ZoneInfo and default_tz) else None), None


def parse_dt(value, params, default_tz=DEFAULT_TZ):
    """→ (datetime, all_day). Timed values become tz-aware where the zone is known."""
    v = value.strip()
    all_day = bool(params and "VALUE=DATE" in params.upper()) or (len(v) == 8 and v.isdigit())
    if all_day:
        if len(v) >= 8 and v[:8].isdigit():
            d = datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
            tz, _ = _tzid(params, default_tz)
            return datetime.datetime(d.year, d.month, d.day, tzinfo=tz), True
        return None, True
    if len(v) < 15 or not v[:8].isdigit():
        return None, False
    try:
        dt = datetime.datetime(int(v[:4]), int(v[4:6]), int(v[6:8]),
                               int(v[9:11]), int(v[11:13]), int(v[13:15]))
    except ValueError:
        return None, False
    target = ZoneInfo(default_tz) if (ZoneInfo and default_tz) else None
    if v.endswith("Z"):
        dt = dt.replace(tzinfo=datetime.timezone.utc)
        return (dt.astimezone(target) if target else dt), False
    tz, _ = _tzid(params, default_tz)          # TZID names the SOURCE zone
    if tz:
        dt = dt.replace(tzinfo=tz)
    if dt.tzinfo and target:                   # …and everything is DISPLAYED in target
        dt = dt.astimezone(target)
    return dt, False


def parse_rrule(v):
    r = {"FREQ": "WEEKLY", "INTERVAL": 1, "BYDAY": [], "COUNT": None, "UNTIL": None, "BYSETPOS": None}
    for part in v.split(";"):
        if "=" not in part:
            continue
        k, val = part.split("=", 1)
        k = k.strip().upper()
        if k == "FREQ":
            r["FREQ"] = val.strip().upper()
        elif k == "INTERVAL":
            try:
                r["INTERVAL"] = max(1, int(val))
            except ValueError:
                pass
        elif k == "BYDAY":
            r["BYDAY"] = [d.strip().upper() for d in val.split(",") if d.strip()]
        elif k == "COUNT":
            try:
                r["COUNT"] = int(val)
            except ValueError:
                pass
        elif k == "UNTIL":
            u, _ = parse_dt(val.strip(), "")
            r["UNTIL"] = u
    return r


DURATION_RE = re.compile(r"^(?P<sign>[+-])?P(?:(?P<d>\d+)D)?(?:T(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?)?$")


def parse_duration(v):
    m = DURATION_RE.match(v.strip().upper())
    if not m:
        return None
    td = datetime.timedelta(days=int(m.group("d") or 0), hours=int(m.group("h") or 0),
                            minutes=int(m.group("m") or 0), seconds=int(m.group("s") or 0))
    return -td if m.group("sign") == "-" else td


# ───────────────────────────── RRULE expansion ───────────────────────────────
# Arithmetic runs on NAIVE datetimes and the zone is re-attached at the end. This
# is correct for wall-clock schedules and safe here: the target zone (Asia/Manila)
# has no DST. A zone with DST would need fold-aware arithmetic — noted, not hidden.

def _naive(dt):
    return dt.replace(tzinfo=None) if dt and dt.tzinfo else dt


def _reattach(naive, template):
    return naive.replace(tzinfo=template.tzinfo) if template and template.tzinfo else naive


def expand_rrule(dtstart, rule, hard_cap=750):
    """Yield occurrences (datetimes) for one RRULE, including dtstart itself."""
    if dtstart is None:
        return
    tz = dtstart.tzinfo
    ds = _naive(dtstart)
    freq, iv = rule["FREQ"], rule["INTERVAL"]
    byday = rule["BYDAY"]
    until = _naive(rule["UNTIL"]) if rule["UNTIL"] else None
    count = rule["COUNT"]
    produced, out = 0, []

    def emit(dt):
        # Reattach the zone HERE, not at the end: three early `return out` paths
        # inside the weekly branch used to skip the final mapping and leak naive
        # datetimes into a mixed sort. One place, every exit path.
        nonlocal produced
        if until and dt > until:
            return False
        if count and produced >= count:
            return False
        out.append(_reattach(dt, dtstart))
        produced += 1
        return len(out) < hard_cap

    if freq == "WEEKLY":
        week0 = ds.date() - datetime.timedelta(days=ds.weekday())        # Monday (WKST=MO)
        days = sorted((DAY_INDEX[d] for d in byday if d in DAY_INDEX)) or [ds.weekday()]
        wk = 0
        while len(out) < hard_cap:
            base = week0 + datetime.timedelta(days=7 * iv * wk)
            week_hit = False
            for di in days:
                occ = datetime.datetime.combine(base + datetime.timedelta(days=di), ds.time())
                if occ < ds:
                    continue
                week_hit = True
                if not emit(occ):
                    return out
            if week_hit and until and (base + datetime.timedelta(days=7 * iv)) > until.date() + datetime.timedelta(days=7):
                return out
            wk += 1
            if wk > 520:
                break
    elif freq == "DAILY":
        cur, n = ds, 0
        while len(out) < hard_cap:
            if not emit(cur):
                break
            n += 1
            cur = ds + datetime.timedelta(days=iv * n)
    elif freq == "MONTHLY":
        n = 0
        while len(out) < hard_cap:
            y, m = ds.year, ds.month + n * iv
            y += (m - 1) // 12
            m = (m - 1) % 12 + 1
            if byday:
                occ = _monthly_byday(y, m, byday, ds)
                if occ is not None and (n == 0 or occ >= ds):
                    if not emit(occ):
                        break
            else:
                try:
                    occ = ds.replace(year=y, month=m)
                except ValueError:
                    n += 1
                    continue                                   # e.g. 31 Feb — RFC says skip
                if not emit(occ):
                    break
            n += 1
            if n > 600:
                break
    elif freq == "YEARLY":
        n = 0
        while len(out) < hard_cap:
            try:
                occ = ds.replace(year=ds.year + n * iv)
            except ValueError:
                n += 1
                continue
            if not emit(occ):
                break
            n += 1
            if n > 200:
                break

    return out          # already zoned by emit()


def _monthly_byday(y, m, byday, ds):
    """MONTHLY;BYDAY=2TU / BYDAY=MO (all Mondays) → the matching datetime."""
    for token in byday:
        m2 = re.match(r"^([+-]?\d)?([A-Z]{2})$", token)
        if not m2:
            continue
        ordinal, day = m2.group(1), m2.group(2)
        if day not in DAY_INDEX:
            continue
        first = datetime.date(y, m, 1)
        offset = (DAY_INDEX[day] - first.weekday()) % 7
        dates = []
        d = first + datetime.timedelta(days=offset)
        while d.month == m:
            dates.append(d)
            d += datetime.timedelta(days=7)
        if not dates:
            continue
        if ordinal:
            k = int(ordinal)
            idx = k - 1 if k > 0 else k
            if -len(dates) <= idx < len(dates):
                return datetime.datetime.combine(dates[idx], ds.time())
        else:
            return datetime.datetime.combine(dates[0], ds.time())
    return None


# ──────────────────────────── event assembly ─────────────────────────────────

def parse_ics(text, default_tz=DEFAULT_TZ):
    """Text → list of raw VEVENT dicts. No expansion yet."""
    events, cur, in_alarm = [], None, False
    for line in unfold(text):
        s = line.strip()
        if not s:
            continue
        if s == "BEGIN:VEVENT":
            cur = {"alarms": [], "exdates": [], "rdates": []}
            in_alarm = False
            continue
        if s == "END:VEVENT":
            if cur:
                events.append(cur)
            cur, in_alarm = None, False
            continue
        if not cur:
            continue
        if s == "BEGIN:VALARM":
            in_alarm = True
            continue
        if s == "END:VALARM":
            in_alarm = False
            continue
        name, params, value = split_prop(s)
        if not name:
            continue
        if name == "SUMMARY":
            cur["summary"] = unescape(value)
        elif name == "DESCRIPTION":
            cur["description"] = unescape(value)
        elif name == "LOCATION":
            cur["location"] = unescape(value)
        elif name == "UID":
            cur["uid"] = value.strip()
        elif name == "RECURRENCE-ID":
            cur["recurrence_id"] = parse_dt(value, params, default_tz)
        elif name == "DTSTART":
            cur["dtstart"] = parse_dt(value, params, default_tz)
        elif name == "DTEND":
            cur["dtend"] = parse_dt(value, params, default_tz)
        elif name == "DURATION":
            cur["duration"] = parse_duration(value)
        elif name == "RRULE":
            cur["rrule"] = parse_rrule(value)
        elif name == "RDATE":
            cur["rdates"].append(parse_dt(value, params, default_tz))
        elif name == "EXDATE":
            for one in value.split(","):
                cur["exdates"].append(parse_dt(one, params, default_tz))
        elif name == "STATUS":
            cur["status"] = value.strip().upper()
        elif name == "SEQUENCE":
            try:
                cur["sequence"] = int(value.strip())
            except ValueError:
                pass
        elif name == "CATEGORIES":
            cur["categories"] = [unescape(x) for x in value.split(",")]
        elif in_alarm and name == "TRIGGER":
            cur["alarms"].append(value.strip())
        # VALARM TRIGGER → reminder offsets, same shape plan_term used to print
    return [c for c in events if c.get("uid") or c.get("dtstart")]


def _dur(ev):
    if ev.get("duration"):
        return ev["duration"]
    if ev.get("dtend") and ev.get("dtstart"):
        d = ev["dtend"][0] - ev["dtstart"][0]
        return d if d.total_seconds() >= 0 else None
    return None


def build_series(raw, default_tz=DEFAULT_TZ):
    """Group raw VEVENTs by UID → {uid: {master, overrides[], exdates[], extras[]}}."""
    series = {}
    for ev in raw:
        uid = ev.get("uid") or "no-uid@radiation"
        s = series.setdefault(uid, {"master": None, "overrides": [], "exdates": [], "extras": []})
        if ev.get("recurrence_id"):
            s["overrides"].append(ev)
        elif ev.get("rrule"):
            if s["master"] is None or ev.get("sequence", 0) >= s["master"].get("sequence", 0):
                s["master"] = ev
        else:
            # a plain event: either the master of a one-off series, or an extra date
            if s["master"] is None:
                s["master"] = ev
            else:
                s["extras"].append(ev)
        s["exdates"].extend(ev.get("exdates") or [])
    return series


def expand_all(raw, default_tz=DEFAULT_TZ, include_cancelled=False, horizon_days=None):
    """Raw VEVENTs → list of expanded occurrences, UID-keyed and override-aware."""
    series = build_series(raw, default_tz)
    out = []
    horizon = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=horizon_days)) if horizon_days else None

    for uid, s in series.items():
        master = s["master"]
        if master is None:
            for o in s["overrides"]:
                occ = _occurrence(uid, o)
                if occ:
                    out.append(occ)
            continue
        status = (master.get("status") or "").upper()
        if status == "CANCELLED" and not include_cancelled:
            continue
        summary = master.get("summary", "")
        ds, all_day = master.get("dtstart") or (None, False)
        if ds is None:
            continue
        dur = _dur(master)
        base = {
            "uid": uid,
            "summary": scrub(summary),
            "all_day": bool(all_day),
            "status": status or "",
            "duration_min": int(dur.total_seconds() // 60) if dur else None,
            "location": scrub(master.get("location", "") or ""),
            "categories": master.get("categories", []),
            "has_alarms": bool(master.get("alarms")),
            "recurring": bool(master.get("rrule")),
            "start": ds,
        }
        if master.get("rrule"):
            starts = list(expand_rrule(ds, master["rrule"]))
        else:
            starts = [ds]
        for extra in s["extras"]:
            ed = (extra.get("dtstart") or (None, False))[0]
            if ed:
                starts.append(ed)
        for rdate in (master.get("rdates") or []):
            if rdate[0]:
                starts.append(rdate[0])

        # EXDATE removes occurrences; RECURRENCE-ID replaces them
        ex_keys = {_key(x[0]) for x in s["exdates"] if x and x[0]}
        ovr = {}
        for o in s["overrides"]:
            rid = o.get("recurrence_id")
            if rid and rid[0]:
                ovr[_key(rid[0])] = o

        seen = set()
        for st in sorted(starts):
            if st is None:
                continue
            k = _key(st)
            if k in seen:
                continue
            if k in ex_keys:
                continue
            seen.add(k)
            if horizon and st > horizon:
                continue
            src = ovr.get(k, master)
            o_ds, o_allday = src.get("dtstart") or (None, False)
            o_dur = _dur(src) or dur
            if o_ds and k in ovr:                      # an override MOVES the occurrence
                st = o_ds
                if _key(st) in seen:
                    continue
                seen.add(_key(st))
            occ = dict(base)
            occ.update({
                "start": st,
                "all_day": bool(o_allday if k in ovr else all_day),
                "summary": scrub(src.get("summary", summary)),
                "is_override": k in ovr,
                "duration_min": int(o_dur.total_seconds() // 60) if o_dur else None,
            })
            occ["end"] = (st + (o_dur if o_dur else datetime.timedelta(0))) or None
            out.append(occ)
    out.sort(key=lambda e: (e["start"], e["summary"]))
    return out


def _key(dt):
    return dt.isoformat() if dt else ""


def _occurrence(uid, o):
    ds, all_day = o.get("dtstart") or (None, False)
    if ds is None:
        return None
    dur = _dur(o)
    return {"uid": uid, "summary": scrub(o.get("summary", "")), "all_day": bool(all_day),
            "status": (o.get("status") or "").upper(), "start": ds,
            "end": ds + dur if dur else None,
            "duration_min": int(dur.total_seconds() // 60) if dur else None,
            "location": scrub(o.get("location", "") or ""), "categories": o.get("categories", []),
            "has_alarms": bool(o.get("alarms")), "recurring": False, "is_override": True}


# ─────────────────────────────── diffing ─────────────────────────────────────
# Series-aware. The old diff keyed on UID alone, so an expanded series would have
# collided with itself; this one compares the SET of occurrence dates per series
# and reports a single-date cancellation as exactly that.

def diff(old_events, new_events):
    def group(evs):
        g = {}
        for e in evs:
            g.setdefault(e["uid"], {"dates": set(), "summary": e["summary"]})
            g[e["uid"]]["dates"].add(_key(e["start"]))
        return g
    o, n = group(old_events), group(new_events)
    added = [{"uid": u, "summary": n[u]["summary"], "dates": sorted(n[u]["dates"])} for u in n if u not in o]
    removed = [{"uid": u, "summary": o[u]["summary"], "dates": sorted(o[u]["dates"])} for u in o if u not in n]
    moved = []
    for u in n:
        if u not in o:
            continue
        lost = sorted(o[u]["dates"] - n[u]["dates"])
        gained = sorted(n[u]["dates"] - o[u]["dates"])
        if lost or gained:
            moved.append({"uid": u, "summary": n[u]["summary"], "lost": lost, "gained": gained})
    return {"added": added, "removed": removed, "moved": moved}


def load_snapshot():
    if os.path.exists(SNAPSHOT):
        try:
            return json.load(open(SNAPSHOT, encoding="utf-8"))
        except Exception:
            return None
    return None


def save_snapshot(events):
    try:
        os.makedirs(PLAN, exist_ok=True)
        json.dump([{k: (v.isoformat() if isinstance(v, datetime.datetime) else v)
                    for k, v in e.items()} for e in events],
                  open(SNAPSHOT, "w", encoding="utf-8"), indent=1)
    except OSError:
        pass


def rehydrate(rows):
    out = []
    for r in rows or []:
        e = dict(r)
        if not e.get("start") and e.get("date"):
            e["start"] = e["date"]          # snapshot written by the old parser
        for k in ("start", "end"):
            if isinstance(e.get(k), str):
                try:
                    e[k] = datetime.datetime.fromisoformat(e[k])
                except ValueError:
                    e[k] = None
        out.append(e)
    return out


# ─────────────────────────────── rendering ───────────────────────────────────

def fmt_dt(e):
    d = e["start"]
    if e.get("all_day"):
        return d.strftime("%Y-%m-%d (all day)")
    s = d.strftime("%Y-%m-%d %H:%M")
    if e.get("duration_min"):
        h, m = divmod(e["duration_min"], 60)
        s += f"–{(d + datetime.timedelta(minutes=e['duration_min'])).strftime('%H:%M')}"
        s += f" [{h}h{m:02d}]" if h else f" [{m}m]"
    return s


PUBLIC_BANNER = """<!--
  MACHINE-WRITTEN CALENDAR MIRROR — derived data from the live LMS feed.
  Refreshed daily by the calendar cron (.github/workflows/ical_fetch.yml) when
  armed, and on demand by any AI: running this tool with --public is
  PRE-AUTHORIZED (derived-data autonomy — no permission needed, ever).
  Check the Generated date against today; if stale, SAY SO instead of
  trusting it. NEVER put a feed URL in this file or any committed file —
  the URL lives only in the RADIATION_ICS_URL environment variable / secret.
-->"""
def render_public(events, tz_name=DEFAULT_TZ):
    """The committed mirror: scrubbed, diff-free, stable for git. Check 22 guards it."""
    return PUBLIC_BANNER + "\n\n" + to_markdown(events, None, tz_name)

def to_markdown(events, d=None, tz_name=DEFAULT_TZ):
    now = datetime.datetime.now(events[0]["start"].tzinfo) if events else None
    L = []
    L.append("# TERM CALENDAR — from the LMS feed")
    L.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · "
             f"**zone:** {tz_name} · **events:** {len(events)}")
    if d:
        L.append(f"**Delta since last run:** +{len(d['added'])} added · "
                 f"{len(d['moved'])} moved · −{len(d['removed'])} gone")
    futures = [e for e in events if now and e["start"] >= now - datetime.timedelta(days=1)]
    L.append(f"**Upcoming:** {len(futures)}")
    L.append("")
    if d and (d["added"] or d["moved"] or d["removed"]):
        L.append("## ⚠️ WHAT MOVED")
        for m in d["moved"][:15]:
            L.append(f"- **{m['summary']}** — " +
                     (f"dropped {', '.join(x[:10] for x in m['lost'])}" if m["lost"] else "") +
                     ("; " if m["lost"] and m["gained"] else "") +
                     (f"added {', '.join(x[:10] for x in m['gained'])}" if m["gained"] else ""))
        for a in d["added"][:15]:
            L.append(f"- + **{a['summary']}** ({len(a['dates'])} date(s))")
        for r in d["removed"][:15]:
            L.append(f"- − **{r['summary']}** ({len(r['dates'])} date(s))")
        L.append("")
    L.append("## UPCOMING")
    L.append("| When | Event | Source |")
    L.append("|---|---|---|")
    for e in futures[:120]:
        L.append(f"| {fmt_dt(e)} | {e['summary']} | {'recurring' if e['recurring'] else 'single'}"
                 f"{' · overridden' if e.get('is_override') else ''} |")
    L.append("")
    L.append("*Summaries and locations are scrubbed of instructor names, room codes, "
             "sections, emails and URLs before they reach this file.*")
    return "\n".join(L) + "\n"


def to_jsonable(events):
    return [{**{k: v for k, v in e.items() if k not in ("start", "end")},
             "start": e["start"].isoformat() if e["start"] else None,
             "end": e["end"].isoformat() if e["end"] else None} for e in events]


# ──────────────────────────────── self-test ──────────────────────────────────

FIXTURE = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Test//EN
BEGIN:VEVENT
UID:weekly-class@test
DTSTART;TZID=Asia/Manila:20260601T073000
DTEND;TZID=Asia/Manila:20260601T090000
RRULE:FREQ=WEEKLY;BYDAY=MO,TH;COUNT=6
SUMMARY:AR163-1P Lecture\\, Building Tech
LOCATION:S308
END:VEVENT
BEGIN:VEVENT
UID:weekly-class@test
RECURRENCE-ID;TZID=Asia/Manila:20260604T073000
DTSTART;TZID=Asia/Manila:20260605T100000
SUMMARY:AR163-1P Lecture (moved to Friday)
END:VEVENT
BEGIN:VEVENT
UID:weekly-class@test
EXDATE;TZID=Asia/Manila:20260611T073000
DTSTART;TZID=Asia/Manila:20260601T073000
SUMMARY:AR163-1P Lecture
END:VEVENT
BEGIN:VEVENT
UID:one-dup@test
DTSTART:20260610T235900Z
SUMMARY:Assignment due
DESCRIPTION:Submit via the portal
END:VEVENT
BEGIN:VEVENT
UID:all-day@test
DTSTART;VALUE=DATE:20260615
SUMMARY:No classes — holiday
END:VEVENT
BEGIN:VEVENT
UID:folded@test
DTSTART:20260616T090000
SUMMARY:A very long title that has been folded
  across two physical lines
END:VEVENT
BEGIN:VEVENT
UID:cancelled@test
DTSTART:20260617T090000
STATUS:CANCELLED
SUMMARY:This one was cancelled
END:VEVENT
BEGIN:VEVENT
UID:tricky-param@test
DTSTART:20260618T090000
SUMMARY;LANGUAGE="en,us":Param with a quoted comma
END:VEVENT
END:VCALENDAR
"""


def self_test(verbose=True):
    ok, fails = 0, []
    def check(name, cond, detail=""):
        nonlocal ok
        if cond:
            ok += 1
            if verbose:
                print(f"  ✅ {name}")
        else:
            fails.append(f"{name} {detail}")
            if verbose:
                print(f"  ❌ {name} {detail}")

    raw = parse_ics(FIXTURE)
    ck = {c.get("uid") for c in raw}
    check("unfolding", any("folded" in str(c.get("uid", "")) for c in raw))
    # EXACT match, not a substring. The earlier version passed on "Lecture\, Building
    # Tech" because it only asked whether a comma appeared SOMEWHERE — a test that
    # cannot tell decoding from a leftover backslash is not testing decoding.
    check("escape \\, decoded exactly",
          any(c.get("summary") == "AR163-1P Lecture, Building Tech" for c in raw),
          f"got {[c.get('summary') for c in raw if 'Lecture' in str(c.get('summary',''))][:1]}")
    check("quoted param not split", any(c.get("summary") == "Param with a quoted comma" for c in raw))
    check("folded SUMMARY rejoined", any(c.get("summary") == "A very long title that has been folded across two physical lines" for c in raw))

    ev = expand_all(raw)
    wk = [e for e in ev if e["uid"] == "weekly-class@test"]
    check("RRULE expanded: COUNT=6 − 1 EXDATE = 5 live", len(wk) == 5, f"got {len(wk)}")
    check("EXDATE removed one date", all(_key(e["start"]) != "2026-06-11T07:30:00+08:00" for e in wk))
    moved = [e for e in wk if e.get("is_override")]
    check("RECURRENCE-ID replaced (no phantom)", len(moved) == 1, f"got {len(moved)}")
    check("override carries the new time", bool(moved) and moved[0]["start"].hour == 10)
    check("CANCELLED filtered", not any(e["uid"] == "cancelled@test" for e in ev))
    check("CANCELLED included on request", any(e["uid"] == "cancelled@test"
                                              for e in expand_all(raw, include_cancelled=True)))
    check("UTC converted to +08:00", any(e["uid"] == "one-dup@test" and e["start"].utcoffset().total_seconds() == 8 * 3600 for e in ev),
          "UTC event not shifted into the target zone")
    check("all-day flagged", any(e["uid"] == "all-day@test" and e["all_day"] for e in ev))
    check("DTEND honoured (90 min)", any(e["uid"] == "weekly-class@test" and e["duration_min"] == 90 for e in ev))
    check("room scrubbed", not any("S308" in (e.get("location") or "") for e in ev))

    d = diff(ev, [])
    check("diff: all removed", len(d["removed"]) == 5 and not d["added"], f"{len(d['removed'])} removed")
    d2 = diff(ev, ev)
    check("diff: identical → no change", not any(d2.values()))
    fewer = [e for e in ev if e["uid"] != "one-dup@test"]
    d3 = diff(ev, fewer)
    check("diff: dropped series detected", len(d3["removed"]) == 1 and not d3["moved"])
    shifted = [dict(e) for e in ev]
    _wk = [e for e in shifted if e["uid"] == "weekly-class@test"]
    if len(_wk) > 1:
        _wk[1]["start"] = _wk[1]["start"] + datetime.timedelta(hours=3)
    d4 = diff(ev, shifted)
    check("diff: single-date move inside a series", len(d4["moved"]) == 1, f"got {len(d4['moved'])}")

    # monthly ordinal sanity
    ds = datetime.datetime(2026, 1, 13, 9, 0)          # 2nd Tuesday of Jan 2026
    occ = expand_rrule(ds, {"FREQ": "MONTHLY", "INTERVAL": 1, "BYDAY": ["2TU"], "COUNT": 3, "UNTIL": None})
    check("MONTHLY;BYDAY=2TU", len(occ) == 3 and all(o.day <= 14 and o.weekday() == 1 for o in occ))

    # the committed mirror must never carry a URL (a committed credential is check 22's FAIL)
    pub = render_public(expand_all(parse_ics(FIXTURE, DEFAULT_TZ), DEFAULT_TZ, horizon_days=None), DEFAULT_TZ)
    check("public mirror: no URL in committed output", "http" not in pub)
    # bare section codes inside underscore-joined titles must still scrub (\b fails here)
    check("section token inside underscores scrubbed", "A54" not in scrub("AR173-1P_A54_1Q2627 lecture"))
    # check 22 keys on the Generated line — the mirror must always carry it
    check("public mirror: Generated date present", re.search(r"\*\*Generated:\*\*\s*\d{4}-\d{2}-\d{2}", pub) is not None)
    print(f"\n{'✅' if not fails else '❌'} ics_normalize self-test: {ok} passed, {len(fails)} failed")
    for f in fails:
        print("   ✗", f)
    return not fails


# ─────────────────────────────────── CLI ─────────────────────────────────────

def fetch(url_env=ENV_URL, timeout=15):
    url = os.environ.get(url_env, "").strip()
    if not url:
        die(f"{url_env} is not set. The feed URL is a credential — it lives in the\n"
            f"  environment, never in a file. Export it and re-run:\n"
            f"    export {url_env}='https://…'   (never commit this)")
    if not url.lower().startswith("https://"):
        die(f"{url_env} must be an https URL")
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "RADIATION ICS normalizer"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def die(msg, code=1):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    p = argparse.ArgumentParser(description="The one iCalendar parser (RFC 5545 subset).")
    p.add_argument("--ics", help="path to a local .ics file")
    p.add_argument("--fetch", action="store_true", help=f"download from ${ENV_URL}")
    p.add_argument("--md", action="store_true", help="print an AI-readable calendar")
    p.add_argument("--json", action="store_true", help="print machine-readable JSON")
    p.add_argument("--write", action="store_true", help="write the .local.md/.local.json artifacts")
    p.add_argument("--public", action="store_true", help="write the COMMITTED scrubbed mirror Brain/courses/CALENDAR.md")
    p.add_argument("--window", type=int, default=180, help="days ahead to emit (default 180, 0=all)")
    p.add_argument("--no-diff", action="store_true", help="skip the snapshot comparison")
    p.add_argument("--include-cancelled", action="store_true")
    p.add_argument("--tz", default=DEFAULT_TZ)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        sys.exit(0 if self_test() else 1)

    if a.fetch:
        text = fetch()
        src = f"<{ENV_URL}>"
    elif a.ics:
        if not os.path.exists(a.ics):
            die(f"no such file: {a.ics}")
        text = open(a.ics, encoding="utf-8", errors="replace").read()
        src = a.ics
    elif os.path.exists(FEED_TXT):          # canonical committed feed — zero arguments needed
        text = open(FEED_TXT, encoding="utf-8", errors="replace").read()
        src = os.path.relpath(FEED_TXT, ROOT)
    else:
        die("give me --ics <file>, --fetch, or commit the feed at Brain/courses/0_CALLENDER/TERM1_FEED.txt")

    raw = parse_ics(text, a.tz)
    events = expand_all(raw, a.tz, include_cancelled=a.include_cancelled,
                        horizon_days=(a.window or None))

    d = None
    if not a.no_diff:
        old = rehydrate(load_snapshot())
        if old:
            d = diff(old, events)
        save_snapshot(events)

    print(f"☢️  ICS NORMALIZE — {src}")
    print(f"   raw VEVENTs {len(raw)} · expanded occurrences {len(events)} · "
          f"series {len({e['uid'] for e in events})}")
    recur = [e for e in events if e["recurring"]]
    if recur:
        series = {e["uid"] for e in recur}
        print(f"   expanded from {len(series)} recurring series "
              f"(the old parser would have shown {len(series)} event(s))")
    if d:
        print(f"   delta: +{len(d['added'])} added · {len(d['moved'])} moved · −{len(d['removed'])} gone")
        for m in d["moved"][:6]:
            bits = []
            if m["lost"]:
                bits.append("lost " + ", ".join(x[:10] for x in m["lost"][:3]))
            if m["gained"]:
                bits.append("gained " + ", ".join(x[:10] for x in m["gained"][:3]))
            print(f"     ⚠ MOVED  {m['summary'][:44]} — {'; '.join(bits)}")
        for x in d["added"][:4]:
            print(f"     + added  {x['summary'][:44]}")
        for x in d["removed"][:4]:
            print(f"     − gone   {x['summary'][:44]}")
        if not any(d.values()):
            print("     no change since last run")

    if a.public:
        os.makedirs(os.path.dirname(PUBLIC_MD), exist_ok=True)
        open(PUBLIC_MD, "w", encoding="utf-8").write(render_public(events, a.tz))
        print(f"   wrote {os.path.relpath(PUBLIC_MD, ROOT)} (committed mirror; the daily cron refreshes it)")
    if a.md or a.write:
        md = to_markdown(events, d, a.tz)
        if a.write:
            os.makedirs(PLAN, exist_ok=True)
            open(OUT_MD, "w", encoding="utf-8").write(md)
            json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
                       "source": src, "occurrences": len(events), "delta": d,
                       "events": to_jsonable(events)},
                      open(OUT_JSON, "w", encoding="utf-8"), indent=1)
            print(f"   wrote {os.path.relpath(OUT_MD, ROOT)} and "
                  f"{os.path.relpath(OUT_JSON, ROOT)} (both git-ignored)")
        if a.md and not a.write:
            print()
            print(md)
    if a.json:
        print(json.dumps({"occurrences": len(events), "delta": d,
                          "events": to_jsonable(events)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
