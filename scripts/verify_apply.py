#!/usr/bin/env python3
"""verify_apply.py — the post-apply auditor (patch 3400, roadmap Enforcement Sweep).
Born of a real failure: the Commander extracted a patch and pushed WITHOUT running
APPLY — a later merge then resurrected files the apply should have re-homed, and the
tree validated red with nobody watching. This command answers, in one screen:
"did the last apply actually land, and what still needs a human?"

READ-ONLY. Stdlib only. Exit 0 normally (it REPORTS, it does not gate);
--strict exits 1 on FAIL-class findings (for local use and for CI, where the
workflow step is marked continue-on-error so the report can never block a push).
Self-test: python3 scripts/verify_apply.py --self-test
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def read(p):
    try: return open(os.path.join(ROOT, p), encoding="utf-8").read()
    except OSError: return ""
def dates(txt):
    return re.findall(r"\d{4}-\d{2}-\d{2}", txt)

def parse_readme_version(t):
    m = re.search(r"\*\*Version:\*\*\s*(v[\d.]+)", t)
    return m.group(1) if m else None

def parse_changelog_top(t):
    m = re.search(r"^## (v[\d.]+)", t, re.M)
    return m.group(1) if m else None

def parse_totals(out):
    m = re.search(r"(\d+) checks run \u00b7 (\d+) pass \u00b7 (\d+) warn \u00b7 (\d+) fail", out)
    return tuple(m.groups()) if m else None

def head_date():
    try:
        r = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs"],
                           capture_output=True, text=True)
        return r.stdout.strip() or None
    except Exception:
        return None

def vehicle_audit():
    """The 3400 generic rule, mirrored read-only for the report."""
    bad = []
    brain = os.path.join(ROOT, "Brain")
    for dp, dn, fn in os.walk(brain):
        for f in fn:
            p = os.path.relpath(os.path.join(dp, f), ROOT)
            if f.endswith(".md") or f == ".gitkeep": continue
            if p in ("Brain/courses/0_CALLENDER/TERM1_FEED.txt",): continue
            if p.startswith("Brain/short_term/plan/") and p.endswith(".json"): continue
            if p.startswith("Brain/short_term/drills/"): continue
            bad.append(p)
    return sorted(bad)

def main():
    if "--self-test" in sys.argv:
        s1 = parse_readme_version("**Version:** v2.1.0 · Ratified") == "v2.1.0"
        s2 = parse_changelog_top("intro\n## v2.1.0 — 2026\nbody\n## v2.0.0") == "v2.1.0"
        s3 = parse_totals("31 checks run · 29 pass · 2 warn · 0 fail") == ("31","29","2","0")
        s4 = parse_totals("no totals here") is None
        s5 = dates("x 2026-09-12 y 2026-09-13")[-1] == "2026-09-13"
        s6 = vehicle_audit.__doc__ is not None
        ok = sum((s1,s2,s3,s4,s5,s6))
        print(f"verify_apply self-test: {ok}/6 OK")
        return 0 if ok == 6 else 1

    findings_fail, findings_warn = [], []
    v_readme = parse_readme_version(read("README.md"))
    v_change = parse_changelog_top(read("CHANGELOG.md"))
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "validate.py")],
                       capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    tot = parse_totals(out)
    fails = [l.strip() for l in out.splitlines() if l.startswith("\u274c")]
    L = []
    L.append("=" * 66)
    L.append("  APPLY REPORT (verify_apply.py — read-only audit)")
    L.append("=" * 66)
    L.append(f"  versions   : README {v_readme} · CHANGELOG top {v_change}" +
             ("" if v_readme == v_change else "   << DRIFT"))
    if v_readme != v_change:
        findings_fail.append(f"version drift: README {v_readme} vs CHANGELOG {v_change} — an apply did not finish")
    L.append(f"  validator  : " + (" ".join(tot) + " (checks/pass/warn/fail)" if tot else "totals unparsed") )
    for f in fails[:4]: L.append("    " + f[:120])
    if fails: findings_fail.append(f"validator: {len(fails)} FAIL — reconcile, then re-run")

    veh = vehicle_audit()
    if veh:
        L.append(f"  vehicles   : {len(veh)} unsanctioned non-record file(s) still in Brain/ — APPLY did not run")
        for p in veh[:6]: L.append("    " + p)
        findings_fail.append("vehicles present — run APPLY.sh from the latest patch (idempotent)")
    else:
        L.append("  vehicles   : none — Brain/ is records-only")
    runners = [p for p in ("APPLY.sh", "APPLY.ps1", "PATCH_NOTES.md") if read(p)]
    if runners:
        L.append(f"  hygiene    : transport still in tree: {', '.join(runners)} — delete post-apply, commit")
        findings_warn.append("apply transport committed — delete and push")
    d_log = max(dates(read("docs/shrine/LOG.md")), default=None)
    d_led = max(dates(read("Brain/frontal_lobe/task_ledger.md")), default=None)
    hd = head_date()
    shrine = f"last heartbeat {d_log or 'NONE'}"
    if d_log and ((d_led and d_led > d_log) or (hd and hd > d_log)):
        shrine += "   << LAGS (II.9 mandate: file a heartbeat)"
        findings_warn.append("shrine heartbeat lags — AI_RULES II.9")
    L.append(f"  shrine     : {shrine}")
    try:
        d = json.load(open(os.path.join(ROOT, "Brain/short_term/plan/TERM1_DEADLINES.json"), encoding="utf-8"))
        pend = len(d.get("feed_pending", []))
        unrat = read("docs/PENDING_RATIFICATIONS.md").count("- [ ]")
        L.append(f"  register   : week1_start {d.get('term',{}).get('week1_start','ABSENT')} · feed_pending {pend} · {unrat} unchecked ratification(s)")
        if pend: findings_warn.append(f"{pend} feed items await Commander attribution")
    except Exception:
        L.append("  register   : TERM1_DEADLINES.json unreadable")
    L.append("=" * 66)
    if findings_fail or findings_warn:
        L.append("  FAIL-CLASS : " + ("; ".join(findings_fail) if findings_fail else "none"))
        L.append("  WARN-CLASS : " + ("; ".join(findings_warn) if findings_warn else "none"))
    else:
        L.append("  verdict    : apply landed clean — nothing needs a human")
    print("\n".join(L))
    if "--strict" in sys.argv and findings_fail:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
