#!/usr/bin/env python3
"""verify_tool_io.py — B4.2 R0 advisory executor for the ten bound tool IO contracts.

Executes the existing CLI interfaces (two JSON emitters, eight prose adapters),
then validates invocation and output with radiation_core.relay._schema_check,
the ONE schema executor. Neither the adapters nor this tool grant authority.
Offline by construction: network Git transports are disabled, so the existing
Git checkers use cached remote-tracking refs. Their own disposable self-tests
may use file remotes. Public-object proof remains the separate release/preflight
battery, not this advisory local snapshot.

--json prints the bounded report; --self-test uses synthetic output only.
A non-PASS exits 1 when run directly; verify_apply consumes it as WARN only.
The validator's ignored validation_report.json is a possible child side effect.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from radiation_core.relay import _schema_check, unsupported_keywords

BOUND = (
    "validate", "agent_policy_check", "verify_policy_check", "docs_index_check",
    "render_docs", "verify_apply", "verify_cassette_runner",
    "release_truth_check", "push_preflight_check", "tool_registry_check",
)
JSON_EMITTERS = frozenset(("validate", "verify_cassette_runner"))
PROSE = frozenset(BOUND) - JSON_EMITTERS
# Private recursion marker, never an added CLI flag on any bound tool.
CHILD_ENV = "RADIATION_TOOL_IO_CHILD"
ARGV = {name: ("--json",) if name in JSON_EMITTERS else
        ("--check",) if name == "render_docs" else
        ("--strict",) if name == "verify_apply" else () for name in BOUND}


def _finding(text):
    """Bound diagnostics to the prose-schema maxLength, without erasing cause."""
    return str(text).replace("\n", " ").strip()[:400]


def _schema_findings(obj, name, where):
    """One checking path: the existing relay executor; reject unexecuted claims."""
    path = ROOT / "schemas" / name
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
        title = "radiation." + name.removesuffix(".schema.json").replace("/", ".") + "/1"
        if not isinstance(spec, dict) or spec.get("title") != title:
            return [_finding(f"{where}: schema must be an object titled {title}")]
        unsupported = unsupported_keywords(spec)
        if unsupported:
            return [_finding(f"{where}: unsupported schema keywords: {unsupported}")]
    except (OSError, ValueError, TypeError) as exc:
        return [_finding(f"{where}: schema {name} unreadable: {exc}")]
    out = []
    _schema_check(obj, name, where, out)
    return [_finding(x) for x in out[:256]]


def _load_registry():
    return json.loads((ROOT / "tools" / "TOOL_REGISTRY.json").read_text(encoding="utf-8"))


def _scope(reg):
    """Exact γ tranche, plus ONE new METADATA-ONLY executor (not recursive)."""
    bad = []
    tools = reg.get("tools") if isinstance(reg, dict) else None
    if not isinstance(tools, list) or any(not isinstance(t, dict) for t in tools):
        return {}, ["registry.tools: missing or malformed list"]
    by_id = {t.get("id"): t for t in tools}
    if len(tools) != 41 or len(by_id) != 41:
        bad.append(f"registry scope: want 41 distinct tools; found {len(tools)} rows/{len(by_id)} ids")
    bound = {t.get("id") for t in tools if t.get("inputs_schema") is not None or
             t.get("outputs_schema") is not None}
    if bound != set(BOUND):
        bad.append(f"schema-bound scope: missing {sorted(set(BOUND) - bound)}; extra {sorted(bound - set(BOUND))}")
    metadata = [t for t in tools if t.get("inputs_schema") is None and
                t.get("outputs_schema") is None and t.get("id") != "verify_tool_io"]
    if len(metadata) != 30:
        bad.append(f"METADATA-ONLY scope: want 30 other tools; found {len(metadata)}")
    self_row = by_id.get("verify_tool_io", {})
    if (self_row.get("inputs_schema") is not None or
            self_row.get("outputs_schema") is not None or
            self_row.get("entrypoint") != "scripts/verify_tool_io.py"):
        bad.append("verify_tool_io must be METADATA-ONLY; never execute its own IO schema")
    for name in BOUND:
        row = by_id.get(name, {})
        if row.get("entrypoint") != f"scripts/{name}.py":
            bad.append(f"{name}: entrypoint is not scripts/{name}.py")
        for direction in ("inputs", "outputs"):
            ref = f"schemas/tool_io/{name}.{direction}.schema.json"
            if row.get(f"{direction}_schema") != ref:
                bad.append(f"{name}: {direction}_schema must be {ref}")
    return by_id, [_finding(x) for x in bad[:30]]


def _invoke(tool, argv):
    """Exercise the real CLI without widening it or reaching a network origin."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))}
    env.update({
        CHILD_ENV: "1", "PYTHONDONTWRITEBYTECODE": "1", "RADIATION_ONLINE": "0",
        # The existing checkers call fetch (and a gate self-test creates file
        # remotes). File-only blocks network origins without redirecting those
        # fixture remotes into this repository. Cached refs are advisory only.
        "GIT_ALLOW_PROTOCOL": "file", "GIT_CONFIG_COUNT": "0",
        "GIT_TERMINAL_PROMPT": "0",
    })
    return subprocess.run(
        [sys.executable, str(ROOT / tool["entrypoint"]), *argv],
        cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=tool["timeout_seconds"],
    )


def _prose_adapter(name, result, spec):
    """The γ finding-report shape, not a new --json interface on a prose tool."""
    needle = spec["properties"]["needle"]["const"]
    problems = []
    if result.returncode != 0:
        problems.append(_finding(f"exit {result.returncode} (want 0)"))
        # Carry the source's actionable finding lines, not an opaque code.
        details = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines()
                   if line.strip().startswith(("- ", "✗", "❌"))]
        problems.extend(_finding(line) for line in details[:12])
        if not details:
            problems.append(_finding("output: " + (result.stdout + result.stderr).strip()[:360]))
    if needle not in result.stdout:
        problems.append(_finding(f"success needle {needle!r} missing from stdout"))
    return {
        "schema_name": f"radiation.tool_io.{name}.outputs/1",
        "ok": not problems, "exit": result.returncode,
        "findings": problems[:256], "needle": needle,
    }


def _row(name, verdict, problems=()):
    findings = [_finding(f) for f in problems if str(f).strip()][:256]
    return {"id": name, "verdict": verdict, "expected": "PASS",
            "findings": findings,
            "justification": "; ".join(findings[:3]) if findings else "input and output schema executed; live contract holds"}


def _run_one(name, tool):
    argv = ARGV[name]
    inp = f"tool_io/{name}.inputs.schema.json"
    out = f"tool_io/{name}.outputs.schema.json"
    record = {"schema_name": f"radiation.tool_io.{name}.inputs/1",
              "cwd": "repo-root", "argv": list(argv)}
    bad = _schema_findings(record, inp, f"{name}.inputs")
    if bad:
        return _row(name, "RETURNED", bad)
    try:
        spec = json.loads((ROOT / "schemas" / out).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        return _row(name, "RETURNED", [f"{name}.outputs schema unreadable: {exc}"])
    try:
        result = _invoke(tool, argv)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        return _row(name, "RETURNED", [f"{name} cannot execute: {type(exc).__name__}: {exc}"])
    if name in JSON_EMITTERS:
        try:
            payload = json.loads(result.stdout)
        except (ValueError, TypeError) as exc:
            return _row(name, "RETURNED", [f"{name}: JSON envelope unreadable: {exc}; "
                                           f"exit {result.returncode}; stderr {result.stderr[:180]}"])
    else:
        try:
            payload = _prose_adapter(name, result, spec)
        except (KeyError, TypeError) as exc:
            return _row(name, "RETURNED", [f"{name}: prose schema missing needle: {exc}"])
    bad = _schema_findings(payload, out, f"{name}.outputs")
    if bad:
        return _row(name, "WARN-and-justify", bad)
    if name in JSON_EMITTERS and result.returncode != 0:
        return _row(name, "WARN-and-justify", [f"{name}: exit {result.returncode} (want 0)"])
    if name in PROSE and not payload["ok"]:
        return _row(name, "WARN-and-justify", payload["findings"])
    return _row(name, "PASS")


def run_io():
    """Execute exactly ten existing contracts; return a bounded advisory report."""
    try:
        registry = _load_registry()
        by_id, scope_findings = _scope(registry)
    except (OSError, ValueError, TypeError) as exc:
        by_id, scope_findings = {}, [_finding(f"registry unreadable: {exc}")]
    rows = ([_row(name, "RETURNED", scope_findings) for name in BOUND]
            if scope_findings else [_run_one(name, by_id[name]) for name in BOUND])
    n_pass = sum(r["verdict"] == "PASS" for r in rows)
    return {"schema_name": "radiation.tool_io.report/1", "rows": rows,
            "scope_findings": scope_findings,
            "summary": f"verify tool_io: {n_pass}/{len(BOUND)} tools PASS"}


def self_test():
    """Synthetic, hermetic vectors only: no production CLI or remote is called."""
    from copy import deepcopy
    reg = _load_registry()
    sample = {"schema_name": "radiation.tool_io.validate.inputs/1",
              "cwd": "repo-root", "argv": ["--json"]}
    prose = json.loads((ROOT / "schemas/tool_io/docs_index_check.outputs.schema.json").read_text())
    good = subprocess.CompletedProcess([], 0, "docs_index_check: 0 finding(s)\n", "")
    no_needle = subprocess.CompletedProcess([], 0, "looks fine\n", "")
    bad_exit = subprocess.CompletedProcess([], 1, "  - broken link\n", "")
    bound, scope = _scope(reg)
    mutant = deepcopy(reg)
    next(t for t in mutant["tools"] if t["id"] == "verify_tool_io")["inputs_schema"] = "schemas/x.json"
    wrapped = _prose_adapter("docs_index_check", good, prose)
    checks = (
        ("scope 10/30 + self unbound", not scope and len(bound) == 41),
        ("self-binding rejected", bool(_scope(mutant)[1])),
        ("valid input accepted", not _schema_findings(sample, "tool_io/validate.inputs.schema.json", "v")),
        ("closed input rejects extra", bool(_schema_findings(dict(sample, extra=1), "tool_io/validate.inputs.schema.json", "v"))),
        ("input rejects wrong flag", bool(_schema_findings(dict(sample, argv=["--not-real"]), "tool_io/validate.inputs.schema.json", "v"))),
        ("prose success maps ok", wrapped["ok"] and wrapped["exit"] == 0),
        ("prose output schema executed", not _schema_findings(wrapped, "tool_io/docs_index_check.outputs.schema.json", "v")),
        ("missing needle visible", not _prose_adapter("docs_index_check", no_needle, prose)["ok"]),
        ("exit failure visible", bool(_prose_adapter("docs_index_check", bad_exit, prose)["findings"])),
        ("closed output rejects extra", bool(_schema_findings(dict(wrapped, rogue=1), "tool_io/docs_index_check.outputs.schema.json", "v"))),
    )
    for label, ok in checks:
        print(f"  {'PASS' if ok else 'RETURNED'} {label}")
    print(f"verify tool_io self-test: {sum(ok for _, ok in checks)}/{len(checks)} PASS")
    return 0 if all(ok for _, ok in checks) else 1


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1 or any(arg not in ("--json", "--self-test") for arg in args):
        print("usage: verify_tool_io.py [--json | --self-test]", file=sys.stderr)
        return 2
    if "--self-test" in args:
        return self_test()
    report = run_io()
    if "--json" in args:
        print(json.dumps(report, indent=2))
    else:
        for r in report["rows"]:
            print(f"  {r['verdict']:<16} {r['id']} — {r['justification']}")
        print(report["summary"])
    return 0 if not report["scope_findings"] and all(
        r["verdict"] == "PASS" for r in report["rows"]) else 1


if __name__ == "__main__":
    sys.exit(main())
