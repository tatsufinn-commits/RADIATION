#!/usr/bin/env python3
"""tool_registry_check — ONE entry point for the tool-registry contract (5600).

Executes schemas/tool_registry.schema.json via the ONE schema executor
(radiation_core.relay), then applies the semantic rules JSON Schema cannot
express cleanly. Those rules are CODE-LEVEL checks, stated as such:

  R1 path containment   : entrypoint has no "..", is not absolute, exists
  R2 id uniqueness      : no duplicate tool ids
  R3 coverage closure   : every runnable module under scripts/, radiation_core/
                          and agents/_common/ (except __init__.py) is
                          registered exactly once; every entrypoint exists
  R4 contradiction rules:
       - effects == ["read"]                 => approval none AND scope none
       - approval != "none"                  => "write" in effects
       - mutation_scope == "none"            => "write" not in effects
       - network == "none"                   => "network" not in effects
       - credential_handling == "host_held"  => network == "declared"
  R5 cap_mapping        : every entry points at an existing cap record
                          (evidence/tasks/<TID>/artifacts/cap_record_build.json)
  R6 schema refs        : non-null inputs_schema/outputs_schema must exist on
                          disk (5710: dangling references were accepted)
  R7 test binding       : test_command must reference the entrypoint — either
                          the path itself or "-m <module>" for its module
                          (5710: 'definitely-nonexistent --oops' passed)
  R8 containment        : realpath(entrypoint) stays inside the repo root

Binding language (5710): entries with NULL IO schema fields are
METADATA-ONLY (descriptive), not schema-bound; entry/test-command/containment
rules apply to every entry either way.

Zero-write display truth is DERIVED, not stored: mutation_scope "none" means
the tool writes nothing. The registry is local and non-authorizing: an entry
GRANTS nothing (no MCP, no endpoint, no runtime — a catalog is not consent).

--self-test runs the negative-vector battery against temp registry copies.
Exit: 0 clean, 1 findings.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from radiation_core.relay import _schema_check  # ONE schema executor (II.11)

REG = os.path.join("tools", "TOOL_REGISTRY.json")
SCHEMA = "tool_registry.schema.json"


def code_level_findings(reg, root=ROOT):
    bad = []
    tools = reg.get("tools", []) if isinstance(reg, dict) else []
    ids = [t.get("id", "?") for t in tools]
    seen = set()
    for tid in ids:
        if tid in seen:
            bad.append(f"duplicate tool id: {tid!r}")
        seen.add(tid)
    # R3 coverage closure
    cover_dirs = [os.path.join("scripts"), os.path.join("radiation_core"),
                  os.path.join("agents", "_common")]
    registered = {os.path.normpath(t.get("entrypoint", "")) for t in tools}
    for d in cover_dirs:
        dp = os.path.join(root, d)
        if not os.path.isdir(dp):
            continue
        for f in sorted(os.listdir(dp)):
            if not f.endswith(".py") or f == "__init__.py":
                continue
            rel = os.path.normpath(os.path.join(d, f))
            if rel not in registered:
                bad.append(f"coverage: {rel} is not registered")
    for t in tools:
        ep = t.get("entrypoint", "")
        # R1 containment (belt and suspenders beyond the schema patterns)
        if ".." in ep.split(os.sep) or ".." in ep:
            bad.append(f"{t.get('id')}: entrypoint escapes the tree: {ep!r}")
        if os.path.isabs(ep):
            bad.append(f"{t.get('id')}: entrypoint is absolute: {ep!r}")
        if not os.path.isfile(os.path.join(root, ep)):
            bad.append(f"{t.get('id')}: entrypoint missing on disk: {ep!r}")
        for cm in t.get("cap_mapping", []):
            if not os.path.isfile(os.path.join(
                    root, "evidence", "tasks", cm, "artifacts",
                    "cap_record_build.json")):
                bad.append(f"{t.get('id')}: cap_mapping points at missing record: {cm}")
        # R4 contradiction rules (code-level semantics)
        eff, ms, ap = (t.get("effects", []), t.get("mutation_scope"),
                       t.get("approval"))
        if eff == ["read"] and (ap != "none" or ms != "none"):
            bad.append(f"{t.get('id')}: read-only tool with approval={ap!r} "
                       f"or mutation_scope={ms!r} (contradiction)")
        if ap != "none" and "write" not in eff:
            bad.append(f"{t.get('id')}: approval {ap!r} without a write effect")
        if ms == "none" and "write" in eff:
            bad.append(f"{t.get('id')}: mutation_scope none but write effect declared")
        if t.get("network") == "none" and "network" in eff:
            bad.append(f"{t.get('id')}: network none but network effect declared")
        if t.get("credential_handling") == "host_held" and t.get("network") != "declared":
            bad.append(f"{t.get('id')}: host_held credentials without a declared network")
        # R6 schema references must exist when declared (5710)
        for field in ("inputs_schema", "outputs_schema"):
            ref = t.get(field)
            if ref is not None and not os.path.isfile(os.path.join(root, ref)):
                bad.append(f"{t.get('id')}: {field} points at a missing file: {ref!r}")
        # R7 test_command must bind to the entrypoint (5710)
        cmd = str(t.get("test_command", ""))
        toks = cmd.split()
        bound = ep in cmd
        if not bound and "-m" in toks:
            mod = os.path.normpath(ep)[:-3].replace(os.sep, ".")
            bound = mod in toks
        if not bound:
            bad.append(f"{t.get('id')}: test_command does not reference the "
                       f"entrypoint ({ep!r} absent from {cmd!r})")
        # R8 realpath containment (5710)
        real = os.path.realpath(os.path.join(root, ep))
        if not real.startswith(os.path.realpath(root) + os.sep):
            bad.append(f"{t.get('id')}: entrypoint escapes the repo root by realpath")
    return bad


def check(root=ROOT, reg_path=None):
    """Returns (findings, tool_count). Schema-executed + code-level."""
    p = os.path.join(root, reg_path or REG)
    if not os.path.isfile(p):
        return ([f"{reg_path or REG} missing (the tool catalog is law)"], 0)
    try:
        reg = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return ([f"registry unparseable: {e}"], 0)
    out = []
    _schema_check(reg, SCHEMA, "tool registry", out)
    out.extend(code_level_findings(reg, root))
    return (out, len(reg.get("tools", [])))


def _mutate(base, fn):
    m = copy.deepcopy(base)
    fn(m)
    return m


def self_test():
    ok = 0
    total = 15  # vector 1 (clean) + 14 negative cases
    reg = json.load(open(os.path.join(ROOT, REG), encoding="utf-8"))

    def rejects(mut, label):
        nonlocal ok
        with tempfile.TemporaryDirectory() as td:
            rp = os.path.join(td, "reg.json")
            json.dump(mut, open(rp, "w"))
            f, _ = check(root=ROOT, reg_path=os.path.abspath(rp))
            # coverage/entrypoint rules need the real root; containment and
            # schema rules run on the mutant as-is
        return f

    def run_mutant(mut):
        with tempfile.TemporaryDirectory() as td:
            rp = os.path.join(td, "reg.json")
            json.dump(mut, open(rp, "w"))
            return check(root=ROOT, reg_path=os.path.abspath(rp))[0]


    # 1: valid registry passes
    f = run_mutant(reg)
    v1 = not f
    ok += v1
    print(f"  vector 1 shipped registry validates clean -> {'PASS' if v1 else f'FAIL {f[:2]}'}")

    def unknown_top(m): m["rogue"] = True
    def unknown_nested(m): m["tools"][0]["rogue_field"] = 1
    def dots_ep(m): m["tools"][0]["entrypoint"] = "../evil.py"
    def abs_ep(m): m["tools"][0]["entrypoint"] = "/etc/evil.py"
    def missing_ep(m): m["tools"][0]["entrypoint"] = "scripts/does_not_exist.py"
    def bool_timeout(m): m["tools"][0]["timeout_seconds"] = True
    def too_few(m):
        # always ONE below the bound, whatever the registry's size
        while len(m["tools"]) >= 20:
            m["tools"].pop()
    def too_many(m): m["tools"] = [dict(m["tools"][0], id=f"t{i}") for i in range(65)]
    def overlong(m): m["tools"][0]["description"] = "x" * 201
    def dup_id(m): m["tools"][1]["id"] = m["tools"][0]["id"]
    def contradiction(m):
        m["tools"][2]["approval"] = "commander_motor_act"
        m["tools"][2]["effects"] = ["read"]
    def coverage_hole(m): m["tools"] = [t for t in m["tools"] if t["id"] != "validate"]
    def dangling_ref(m): m["tools"][0]["inputs_schema"] = "schemas/no-such-file.json"
    def unbound_test(m): m["tools"][0]["test_command"] = "definitely-nonexistent --oops"

    cases = [
        ("unknown top-level property", unknown_top, "unknown property"),
        ("unknown nested property", unknown_nested, "unknown property"),
        ("../ entrypoint", dots_ep, "escapes|fails pattern"),
        ("absolute entrypoint", abs_ep, "absolute|fails pattern"),
        ("missing entrypoint file", missing_ep, "missing on disk"),
        ("bool as timeout", bool_timeout, "must be integer"),
        ("too few records (19)", too_few, "minItems"),
        ("too many records (65)", too_many, "maxItems"),
        ("overlong description", overlong, "maxLength"),
        ("duplicate ids", dup_id, "duplicate tool id"),
        ("read-only canonical action", contradiction, "contradiction"),
        ("coverage hole", coverage_hole, "not registered"),
        ("dangling schema reference", dangling_ref, "missing file"),
        ("test_command unbound to entrypoint", unbound_test, "does not reference"),
    ]
    for i, (label, fn, needle) in enumerate(cases, start=2):
        f = run_mutant(_mutate(reg, fn))
        import re as _re
        hit = any(_re.search(needle, x) for x in f)
        v = bool(f) and hit
        ok += v
        print(f"  vector {i} {label} rejected ({needle}) -> "
              f"{'PASS' if v else 'FAIL ' + (f[:1] or ['(no findings)'])[0]}")
    print(f"tool_registry_check self-test: {ok}/{total} vectors")
    return 0 if ok == total else 1


def main(argv=None):
    if "--self-test" in (argv or sys.argv[1:]):
        return self_test()
    f, n = check()
    for x in f:
        print("✗", x)
    print(f"tool registry: {n} tools · {len(f)} finding(s)")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
