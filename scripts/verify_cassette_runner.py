#!/usr/bin/env python3
"""verify_cassette_runner.py — WP-2.3 verify cassette runner (deterministic, stdlib-only).

Reads evals/verify_policies/CASSETTE_WP23.json and executes each row's
deterministic checks, printing one verdict per row:

  PASS              every deterministic check of the row held
  WARN-and-justify  the row was evaluable but a check failed — printed with its
                    stated justification; never FAIL-class (Law 3, raise-only)
  RETURNED          the row could not be evaluated (malformed row, unknown
                    runner, missing target) — returned to its author

Runners (J1 — the seeds are consumed by name, never rebuilt):
  seed_trace             trace JSON validity + policy_class enum + seed-name match
  activation_5830        existence/content assertions over the 5830 surfaces
  numeric_motion_5900_1  release_truth_check.py --self-test 11/11 + relay
                         numeric plan-version evidence (_plan_version)

No behavioral grading. Zero network, zero SaaS, no stdin; a normal run writes
nothing (--self-test writes fixtures to a temp dir only).
Usage:
  python3 scripts/verify_cassette_runner.py              # run the cassette
  python3 scripts/verify_cassette_runner.py --json       # machine-readable rows
  python3 scripts/verify_cassette_runner.py --self-test  # vector battery
Exit: 0 when every row is PASS (or on --self-test success); 1 otherwise.
The exit code is REPORT-class: verify_apply.py consumes it as an advisory WARN.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASSETTE = os.path.join("evals", "verify_policies", "CASSETTE_WP23.json")
VERDICTS = ("PASS", "WARN-and-justify", "RETURNED")
POLICY_CLASSES = ("required", "opt-in", "opt-out")
ROW_KEYS = ("id", "question", "expected", "runner", "verdict")
EXPECTED_ROW_IDS = (
    "WP-2.3-cassette-seed-required-SUB-001",
    "WP-2.3-cassette-seed-opt-in-SUB-002",
    "WP-2.3-cassette-seed-opt-out-SUB-003",
    "WP-2.3-cassette-A-5830-activation",
    "WP-2.3-cassette-E2-5900-1-numeric-motion",
)


class Returned(Exception):
    """The row cannot be evaluated; carries the reason."""


def _read_text(root, rel):
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        raise Returned(f"target missing: {rel}")
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def row_shape_findings(row):
    """Design B3 row shape: id · question · expected · runner · verdict."""
    bad = []
    if not isinstance(row, dict):
        return ["row is not an object"]
    for k in ROW_KEYS:
        if not isinstance(row.get(k), str) or not row.get(k):
            bad.append(f"row field {k!r} missing or not a non-empty string")
    for k in ("expected", "verdict"):
        if isinstance(row.get(k), str) and row[k] not in VERDICTS:
            bad.append(f"row field {k!r}={row[k]!r} not in {list(VERDICTS)}")
    return bad


# ---- runners -----------------------------------------------------------------
def run_seed_trace(row, root):
    target = row.get("target")
    want_class = row.get("policy_class")
    if not target or want_class not in POLICY_CLASSES:
        raise Returned("seed row needs target + policy_class in the enum")
    try:
        data = json.loads(_read_text(root, target))
    except json.JSONDecodeError as e:
        return [f"{target}: invalid JSON ({e.msg})"]
    fails = []
    pc = data.get("policy_class")
    if pc not in POLICY_CLASSES:
        fails.append(f"{target}: policy_class {pc!r} not in {list(POLICY_CLASSES)}")
    elif pc != want_class:
        fails.append(f"{target}: policy_class {pc!r} != row's {want_class!r}")
    vpol = (data.get("verify") or {}).get("policy")
    if vpol != want_class:
        fails.append(f"{target}: verify.policy {vpol!r} != {want_class!r}")
    for field, val in (("cassette_seed", data.get("cassette_seed")),
                       ("verify.seed", (data.get("verify") or {}).get("seed"))):
        if val != row["id"]:
            fails.append(f"{target}: {field} {val!r} != seed name {row['id']!r}")
    if data.get("stdlib_asserted") is not True:
        fails.append(f"{target}: stdlib_asserted is not true")
    return fails


def run_activation_5830(row, root):
    asserts = row.get("assertions")
    if not isinstance(asserts, list) or not asserts:
        raise Returned("activation row needs a non-empty assertions list")
    fails = []
    for a in asserts:
        if not isinstance(a, dict) or not a.get("path") or not a.get("contains"):
            raise Returned(f"malformed assertion: {a!r}")
        if a["contains"] not in _read_text(root, a["path"]):
            fails.append(f"{a['path']}: expected text absent: {a['contains']!r}")
    return fails


def run_numeric_motion(row, root):
    gate = row.get("gate_self_test") or {}
    relay = row.get("relay_numeric_plan") or {}
    cmd, needle = gate.get("command"), gate.get("must_contain")
    vectors = relay.get("vectors")
    if not (isinstance(cmd, list) and cmd and needle and isinstance(vectors, list) and vectors):
        raise Returned("numeric-motion row needs gate_self_test.command/must_contain + relay vectors")
    _read_text(root, cmd[0])  # target must exist, else RETURNED
    fails = []
    r = subprocess.run([sys.executable] + cmd, cwd=root, capture_output=True,
                       text=True, stdin=subprocess.DEVNULL, timeout=600)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0 or needle not in out:
        tail = out.strip().splitlines()[-1:] or ["<no output>"]
        fails.append(f"{cmd[0]} --self-test: rc={r.returncode}, {needle!r} absent (last: {tail[0][:120]})")
    if relay.get("module") != "radiation_core.relay" or relay.get("function") != "_plan_version":
        raise Returned("relay evidence must name radiation_core.relay._plan_version")
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        from radiation_core.relay import _plan_version
    except Exception as e:  # pragma: no cover - import failure is a finding
        return fails + [f"radiation_core.relay._plan_version unimportable: {e}"]
    for name, want in vectors:
        got = _plan_version(name)
        if got != want:
            fails.append(f"_plan_version({name!r}) = {got}, expected {want}")
    ranked = sorted((v[0] for v in vectors), key=_plan_version)
    if ranked and ranked[-1] != "plan.v10.json":
        fails.append(f"numeric ordering broken: highest plan ranked {ranked[-1]!r}")
    return fails


RUNNERS = {
    "seed_trace": run_seed_trace,
    "activation_5830": run_activation_5830,
    "numeric_motion_5900_1": run_numeric_motion,
}


# ---- engine ------------------------------------------------------------------
def evaluate_row(row, root=ROOT):
    """Return (verdict, justification). Never raises."""
    shape = row_shape_findings(row)
    if shape:
        return "RETURNED", "; ".join(shape)
    fn = RUNNERS.get(row["runner"])
    if fn is None:
        return "RETURNED", f"unknown runner {row['runner']!r}"
    try:
        fails = fn(row, root)
    except Returned as e:
        return "RETURNED", str(e)
    except Exception as e:  # a crashing check is not evaluable
        return "RETURNED", f"runner raised {type(e).__name__}: {e}"
    return map_verdict(fails)


def map_verdict(fails):
    """Verdict mapping: no failures → PASS; any failure → WARN-and-justify."""
    if not fails:
        return "PASS", "all deterministic checks held"
    return "WARN-and-justify", "; ".join(fails)


def load_cassette(root=ROOT, rel=CASSETTE):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return json.load(fh)


def run_cassette(root=ROOT, rel=CASSETTE):
    """Return a list of {id, verdict, expected, justification}."""
    try:
        cas = load_cassette(root, rel)
    except Exception as e:
        return [{"id": rel, "verdict": "RETURNED", "expected": "PASS",
                 "justification": f"cassette unreadable: {e}"}]
    rows = cas.get("rows") if isinstance(cas, dict) else None
    if not isinstance(rows, list) or not rows:
        return [{"id": rel, "verdict": "RETURNED", "expected": "PASS",
                 "justification": "cassette has no rows"}]
    out = []
    for row in rows:
        verdict, why = evaluate_row(row, root)
        out.append({"id": row.get("id", "?") if isinstance(row, dict) else "?",
                    "verdict": verdict,
                    "expected": row.get("expected") if isinstance(row, dict) else None,
                    "justification": why})
    return out


def summary_line(results):
    n_pass = sum(1 for r in results if r["verdict"] == "PASS")
    return f"verify cassette: {n_pass}/{len(results)} rows PASS"


# ---- self-test ---------------------------------------------------------------
def self_test():
    import tempfile
    vectors = []

    def vec(label, ok):
        vectors.append(ok)
        print(f"  vector {len(vectors)} {label} -> {'PASS' if ok else 'FAIL'}")

    live = run_cassette()
    vec("live cassette: five rows, all PASS",
        len(live) == 5 and all(r["verdict"] == "PASS" for r in live))
    vec("live cassette row ids are the five named rows, in order",
        tuple(r["id"] for r in live) == EXPECTED_ROW_IDS)
    vec("map_verdict([]) -> PASS", map_verdict([])[0] == "PASS")
    vec("map_verdict([x]) -> WARN-and-justify with justification",
        map_verdict(["x broke"]) == ("WARN-and-justify", "x broke"))
    vec("malformed row (no question) -> RETURNED",
        evaluate_row({"id": "r", "expected": "PASS", "runner": "seed_trace",
                      "verdict": "PASS"})[0] == "RETURNED")
    vec("unknown runner -> RETURNED",
        evaluate_row({"id": "r", "question": "q", "expected": "PASS",
                      "runner": "grade_behavior", "verdict": "PASS"})[0] == "RETURNED")

    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "evals", "verify_policies"))
        tp = os.path.join(td, "evals", "verify_policies", "t.json")
        seed = {"id": "WP-2.3-cassette-seed-required-SUB-001", "question": "q",
                "expected": "PASS", "runner": "seed_trace",
                "target": "evals/verify_policies/t.json",
                "policy_class": "required", "verdict": "PASS"}
        good = {"policy_class": "required", "stdlib_asserted": True,
                "cassette_seed": seed["id"],
                "verify": {"policy": "required", "seed": seed["id"]}}

        def write(obj):
            with open(tp, "w", encoding="utf-8") as fh:
                fh.write(obj if isinstance(obj, str) else json.dumps(obj))

        write(good)
        vec("synthetic seed trace -> PASS", evaluate_row(seed, td)[0] == "PASS")
        write(dict(good, cassette_seed="WP-2.3-cassette-seed-renamed"))
        vec("seed-name drift -> WARN-and-justify",
            evaluate_row(seed, td)[0] == "WARN-and-justify")
        write(dict(good, policy_class="maybe"))
        vec("policy_class outside enum -> WARN-and-justify",
            evaluate_row(seed, td)[0] == "WARN-and-justify")
        write("{not json")
        vec("invalid trace JSON -> WARN-and-justify",
            evaluate_row(seed, td)[0] == "WARN-and-justify")
        os.remove(tp)
        vec("missing trace target -> RETURNED", evaluate_row(seed, td)[0] == "RETURNED")
        act = {"id": "a", "question": "q", "expected": "PASS",
               "runner": "activation_5830", "verdict": "PASS",
               "assertions": [{"path": "doc.md", "contains": "canonical_apply"}]}
        with open(os.path.join(td, "doc.md"), "w", encoding="utf-8") as fh:
            fh.write("nothing here")
        vec("activation content assertion absent -> WARN-and-justify",
            evaluate_row(act, td)[0] == "WARN-and-justify")
        vec("unreadable cassette -> single RETURNED row",
            [r["verdict"] for r in run_cassette(td, "nope.json")] == ["RETURNED"])

    ok = sum(vectors)
    print(f"verify_cassette_runner self-test: {ok}/{len(vectors)} vectors")
    return 0 if ok == len(vectors) else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    results = run_cassette()
    if "--json" in argv:
        print(json.dumps({"rows": results, "summary": summary_line(results)}, indent=2))
    else:
        for r in results:
            print(f"  {r['verdict']:<16} {r['id']} — {r['justification']}")
        print(summary_line(results))
    return 0 if all(r["verdict"] == "PASS" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
