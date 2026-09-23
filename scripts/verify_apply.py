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
    """5500: the 5300 declared-corpus rule, mirrored read-only for the report.
    Exact manifest entries are sanctioned; everything else under Brain/ that is
    not a Markdown record keeps the generic rule. Never recommends removing
    declared corpus assets to clear itself."""
    try:
        sys.path.insert(0, ROOT)
        import validate as V
    except Exception:
        return []
    bad, declared = V._corpus_contract_violations(V.ROOT)
    return sorted(V._brain_vehicle_violations(V.ROOT, declared))


def corpus_contract_findings():
    """5500: digest/derivative/path violations of the declared corpus contract."""
    try:
        sys.path.insert(0, ROOT)
        import validate as V
    except Exception:
        return []
    bad, _declared = V._corpus_contract_violations(V.ROOT)
    return bad

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
    # v2 (4400): structured consumption — import the validator, never scrape stdout
    try:
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import validate as _v
        _results = _v.run_all()
        _f, _w = _v._summary(_results)
        tot = (str(len(_results)), str(len(_results)-len(_f)-len(_w)), str(len(_w)), str(len(_f)))
        fails = [f"[check {r['check']}] {r['msg']}" for r in _f]
        _degraded = False
    except Exception:
        _degraded = True
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
    L.append(f"  validator  : " + (" ".join(tot) + " (checks/pass/warn/fail)" if tot else "totals unparsed")
             + ("  << DEGRADED (stdout fallback — structured API unavailable)" if _degraded else ""))
    if _degraded and "--strict" in sys.argv:
        findings_fail.append("degraded mode in strict run — structured validator API unavailable")
    for f in fails[:4]: L.append("    " + f[:120])
    if fails: findings_fail.append(f"validator: {len(fails)} FAIL — reconcile, then re-run")

    veh = vehicle_audit()
    if veh:
        L.append(f"  vehicles   : {len(veh)} undeclared non-record file(s) still in Brain/")
        for p in veh[:6]: L.append("    " + p)
        findings_fail.append("vehicles present — declare them in Brain/courses/COURSE_CORPUS_MANIFEST.json "
                             "or move them out of Brain/ (APPLY runners are retired; never re-add them)")
    else:
        L.append("  vehicles   : none — Brain/ is records + declared corpus")
    cc = corpus_contract_findings()
    if cc:
        for x in cc[:4]: L.append("    corpus-contract: " + x)
        findings_fail.append(f"course-corpus contract violated x{len(cc)} — fix the manifest or the files")
    else:
        L.append("  corpus      : contract clean — Brain/ is records + declared corpus")
    # WP-2.3 advisory plug-in (ratified B2, Option-A): the verify cassette runner.
    # PASS -> silent. Any non-PASS row -> WARN-class with its stated justification.
    # NEVER FAIL-class (raise-only; warn-and-justify). A runner that cannot load is
    # itself reported as an advisory WARN, not a failure.
    try:
        import verify_cassette_runner as _vcr
        _cas = _vcr.run_cassette()
    except Exception as _e:
        _cas = [{"id": "CASSETTE_WP23", "verdict": "RETURNED",
                 "justification": f"runner unavailable: {type(_e).__name__}: {_e}"}]
    _cas_bad = [r for r in _cas if r.get("verdict") != "PASS"]
    if _cas_bad:
        L.append(f"  cassette   : ADVISORY — {len(_cas_bad)}/{len(_cas)} verify-cassette row(s) not PASS")
        for r in _cas_bad[:5]:
            L.append(f"    {r.get('verdict')} {r.get('id')}: {str(r.get('justification'))[:100]}")
        findings_warn.append("verify cassette advisory (WP-2.3): " + "; ".join(
            f"{r.get('id')} {r.get('verdict')} — {str(r.get('justification'))[:80]}" for r in _cas_bad[:3]))
    runners = [p for p in ("APPLY.sh", "APPLY.ps1", "PATCH_NOTES.md") if read(p)]
    if runners:
        L.append(f"  hygiene    : transport still in tree: {', '.join(runners)} — delete post-apply, commit")
        findings_warn.append("apply transport committed — delete and push")
    # v2 (4400): first-column dates only — decay/evidence dates are not activity (F-07)
    def _first_col(p):
        ds = [m.group(1) for ln in read(p).splitlines()
              for m in [re.match(r"\|\s*(\d{4}-\d{2}-\d{2})", ln.strip())] if m]
        return max(ds, default=None)
    d_log = _first_col("docs/shrine/LOG.md")
    d_led = _first_col("Brain/frontal_lobe/task_ledger.md")
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
