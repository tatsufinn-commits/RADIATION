#!/usr/bin/env python3
"""activation_conformance.py — MAS-SCAN-NOTES revision 1: ONE read-only structural evaluator.

Sole question: does a SUPPLIED, TASK-BOUND Scan Declaration have a structurally
nonempty Extraction Notes field under the ONE canonical custody object
(scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json), at that snapshot's recorded
cutoff? The rule is old law (docs/AI_RULES.md III.6 via the template
scaffolding/core/proc_scan-declaration.md); this tool adds no doctrine.

SIX RESULT VALUES, AND ONLY SIX:
  SATISFIED · MISSING · NOT APPLICABLE · UNKNOWN · CONFLICT · COMMANDER DISPOSITION

SATISFIED means ONLY that the fixed snapshot's structural evidence contract is met
at its recorded cutoff. It never means Scan completion, current session truth,
caller authentication, fresh observation, first use, replay prevention, capability
availability, or authority. Any unavailable, stale, mismatched, non-canonical,
invalidated, superseded, or uncheckable custody/currentness fact is UNKNOWN —
never SATISFIED.

NOT AN ACTIVATION ENGINE. This tool does not prove real-world work, authenticate a
caller, identify a host or model, invoke a tool, grant a capability or permission,
use a network or credential, persist a receipt, or provide cross-invocation replay
protection. It activates no child package. Authority flows only through the
Commander and the II.11 control plane — never through this exit code.

SOLE CUSTODY SELECTION: CUSTODY_PATH below is a module constant. No command option,
task field, environment value, history input, or purported disposition can
substitute another custody path — the CLI exposes no flag that reaches it, and any
unknown flag is a usage error. The object seam (custody_obj/root) exists for hermetic
tests only; it is not reachable from argv or the environment.

Stdlib only · offline · read-only · writes nothing (receipt is returned in memory).
Exit: 0 = SATISFIED · 1 = evaluated, another of the six values · 2 = usage error.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUSTODY_PATH = "scaffolding/activation_rules/MAS-SCAN-NOTES.v1.json"
CONTRACT_PATH = "docs/ACTIVATION_CONFORMANCE.md"
SCHEMA_NAME = "activation_conformance.schema.json"
RULE_ID = "MAS-SCAN-NOTES"
RULE_REVISION = 1
NOTES_FIELD = "EXTRACTION NOTES"
RESULTS = ("SATISFIED", "MISSING", "NOT APPLICABLE", "UNKNOWN", "CONFLICT",
           "COMMANDER DISPOSITION")
LIMITS = ("fixed_snapshot", "no_caller_authentication", "no_dynamic_disposition",
          "no_persistence", "no_cross_invocation_replay_protection",
          "no_activation_or_permission_grant")
PLACEHOLDERS = {"none", "n/a", "na", "tbd", "nil", "null", "-", "—", "--"}
MAX_SUBMISSION_BYTES = 65536


def _schema_findings(obj, where):
    """ONE checking path: the existing relay executor; unexecuted claims rejected."""
    out = []
    try:
        spec = json.load(open(os.path.join(ROOT, "schemas", SCHEMA_NAME), encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{where}: contract schema unreadable: {exc}"]
    try:
        sys.path.insert(0, ROOT)
        from radiation_core.relay import _schema_check, unsupported_keywords
    except Exception as exc:                      # pragma: no cover - import guard
        return [f"{where}: schema executor unavailable: {exc}"]
    unsupported = unsupported_keywords(spec)
    if unsupported:
        return [f"{where}: schema uses keywords the executor does not execute: {unsupported}"]
    _schema_check(obj, SCHEMA_NAME, where, out)
    return [str(x)[:300] for x in out]


def _digest(relpath, root):
    try:
        with open(os.path.join(root, relpath), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def _load_json(relpath, root, cap=MAX_SUBMISSION_BYTES):
    path = os.path.join(root, relpath)
    try:
        if os.path.getsize(path) > cap:
            return None, f"record exceeds {cap} bytes"
        with open(path, encoding="utf-8") as fh:
            return json.load(fh), None
    except (OSError, ValueError) as exc:
        return None, f"record unreadable: {exc}"


def notes_are_nonempty(value):
    """Structural nonemptiness only — presence, never meaning or quality."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text:
        return False
    return text.lower() not in PLACEHOLDERS


def _valid_calendar_date(text):
    if not isinstance(text, str) or len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    try:
        year, month, day = int(text[:4]), int(text[5:7]), int(text[8:10])
    except ValueError:
        return False
    if not (1 <= month <= 12 and 1 <= day <= 31 and 1900 <= year <= 2999):
        return False
    return day <= (31, 29 if (year % 4 == 0 and (year % 100 or year % 400 == 0)) else 28,
                   31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month - 1]


def _custody_unknown(custody, root):
    """Every custody/currentness failure returns a reason string, or None."""
    if not isinstance(custody, dict):
        return "custody object is not an object"
    findings = _schema_findings(custody, "custody")
    if findings:
        return f"custody fails its own closed schema: {findings[0]}"
    if custody.get("sole_path") != CUSTODY_PATH:
        return "custody is not the sole canonical object (non-canonical path)"
    if custody["identity"].get("identity_proven") is not False:
        return "custody asserts a proven identity; labels are not proof"
    state = custody["validity"].get("state")
    if state != "VALID":
        return f"custody validity state is {state!r} — not checkable as valid"
    if custody["validity"].get("invalidated_reason") is not None:
        return "custody carries an invalidation reason"
    if custody["supersession"].get("superseded") is not False or \
            custody["supersession"].get("superseded_by") is not None:
        return "custody is superseded"
    if custody["context"].get("use_status") != "RECORDED_UNUSED":
        return "custody use status is not a recording-time snapshot"
    if not _valid_calendar_date(custody["context"].get("cutoff_recorded_on")):
        return "custody cutoff is not a real calendar date"
    for entry in custody["history"].get("entries", []):
        if entry.get("result") not in RESULTS or entry.get("result") == "COMMANDER DISPOSITION":
            return "custody history carries a disallowed entry"
    digests = custody["digests"]
    for key, relpath in (("rule_digest_sha256", custody["declaration"]["template_path"]),
                         ("contract_digest_sha256", CONTRACT_PATH)):
        on_disk = _digest(relpath, root)
        if on_disk is None:
            return f"custody digest target missing: {relpath}"
        if digests.get(key) != on_disk:
            return f"custody digest mismatch for {relpath} (stale or mismatched snapshot)"
    return None


def declaration_fixture(custody, value="Explicit: fixture-only declaration text.",
                        present=True, **overrides):
    """A FIXTURE submission bound to a custody object. Fixtures prove shape only."""
    submission = {
        "schema_name": "radiation.activation_conformance.submission/1",
        "task_id": custody["task"]["task_id"],
        "rule_id": RULE_ID,
        "rule_revision": RULE_REVISION,
        "declaration_revision": custody["declaration"]["declaration_revision"],
        "field": NOTES_FIELD,
        "notes": {"present": present, "value": value},
        "history": {"basis": "recording-time-empty", "entries": []},
        "disposition": None,
    }
    submission.update(overrides)
    return submission


def _receipt(result, reasons, cutoff):
    return {
        "schema_name": "radiation.activation_conformance.receipt/1",
        "rule_id": RULE_ID,
        "rule_revision": RULE_REVISION,
        "result": result,
        "reasons": [str(r)[:300] for r in reasons][:8] or ["no reason recorded"],
        "custody_path": CUSTODY_PATH,
        "cutoff_recorded_on": cutoff or "",
        "limits": list(LIMITS),
        "persisted": False,
        "authority": "none",
        "authentication": "none",
    }


def evaluate(submission=None, custody_obj=None, root=None):
    """Return the in-memory receipt. Never writes, never reaches a network."""
    root = root or ROOT
    cutoff = None
    if custody_obj is None:
        custody, problem = _load_json(CUSTODY_PATH, root, cap=262144)
        if problem:
            return _receipt("UNKNOWN", [f"custody unavailable: {problem}"], None)
    else:
        custody = custody_obj
    if isinstance(custody, dict):
        cutoff = (custody.get("context") or {}).get("cutoff_recorded_on")
    reason = _custody_unknown(custody, root)
    if reason:
        return _receipt("UNKNOWN", [reason], cutoff)
    if submission is None:
        return _receipt("UNKNOWN", ["no task-bound Scan Declaration was supplied"], cutoff)
    if not isinstance(submission, dict):
        return _receipt("UNKNOWN", ["submission is not an object"], cutoff)
    findings = _schema_findings(submission, "submission")
    if findings:
        return _receipt("UNKNOWN", [f"submission fails its closed schema: {findings[0]}"], cutoff)
    if submission["task_id"] != custody["task"]["task_id"]:
        return _receipt("CONFLICT", ["submission task does not bind the custody task"], cutoff)
    if (submission["rule_id"] != custody["rule_id"] or
            submission["rule_revision"] != custody["rule_revision"] or
            submission["declaration_revision"] != custody["declaration"]["declaration_revision"]):
        return _receipt("CONFLICT", ["submission rule/revision disagrees with the custody snapshot"],
                        cutoff)
    if submission["disposition"] is not None:
        return _receipt("UNKNOWN",
                        ["a live task-supplied disposition cannot be authenticated; "
                         "COMMANDER DISPOSITION stays a vocabulary shape, never a live result"],
                        cutoff)
    for entry in submission["history"].get("entries", []):
        if entry.get("result") == "COMMANDER DISPOSITION":
            return _receipt("UNKNOWN", ["submission history claims a dischargeable disposition"],
                            cutoff)
        if entry.get("persisted") is not False:
            return _receipt("UNKNOWN", ["submission history claims a persisted record"], cutoff)
    if custody["declaration"]["declaration_required"] is not True:
        return _receipt("NOT APPLICABLE", ["the rule's recorded applicability predicate is false"],
                        cutoff)
    present = submission["notes"]["present"]
    nonempty = notes_are_nonempty(submission["notes"]["value"])
    if present and nonempty:
        return _receipt("SATISFIED",
                        ["Extraction Notes structurally nonempty at the recorded cutoff; "
                         "structural conformance only — no authentication, freshness, "
                         "completeness, or authority claim"], cutoff)
    if not present and nonempty:
        return _receipt("CONFLICT", ["submission declares the field absent while carrying text"],
                        cutoff)
    return _receipt("MISSING", [f"{NOTES_FIELD} present={present} nonempty={nonempty}"], cutoff)


def self_test():
    """Synthetic/hermetic vectors: no production CLI, no write, no network."""
    custody, problem = _load_json(CUSTODY_PATH, ROOT, cap=262144)
    if problem:
        print(f"  RETURNED live custody unavailable: {problem}")
        return 1
    live = declaration_fixture(custody, "Fixture: competing readings surfaced and resolved.")
    import copy

    def mutant(**changes):
        obj = copy.deepcopy(custody)
        for dotted, value in changes.items():
            node = obj
            parts = dotted.split("__")
            for part in parts[:-1]:
                node = node[part]
            node[parts[-1]] = value
        return obj

    def submit(**changes):
        return declaration_fixture(custody, **changes)

    vectors = [
        ("live custody + bound declaration",
         evaluate(live).get("result"), "SATISFIED"),
        ("absent notes", evaluate(submit(value=None, present=False)).get("result"), "MISSING"),
        ("empty notes", evaluate(submit(value="   \n\t")).get("result"), "MISSING"),
        ("placeholder notes", evaluate(submit(value="none")).get("result"), "MISSING"),
        ("false predicate",
         evaluate(live, custody_obj=mutant(declaration__declaration_required=False)).get("result"),
         "NOT APPLICABLE"),
        ("malformed submission", evaluate({"schema_name": "x"}).get("result"), "UNKNOWN"),
        ("unknown validity state",
         evaluate(live, custody_obj=mutant(validity={"state": "UNKNOWN",
                                                     "invalidated_reason": None})).get("result"),
         "UNKNOWN"),
        ("invalidated custody",
         evaluate(live, custody_obj=mutant(validity={"state": "INVALIDATED",
                                                     "invalidated_reason": "desk hold"})).get("result"),
         "UNKNOWN"),
        ("superseded custody",
         evaluate(live, custody_obj=mutant(supersession={"superseded": True,
                                                         "superseded_by": "rev2"})).get("result"),
         "UNKNOWN"),
        ("stale/mismatched contract digest",
         evaluate(live, custody_obj=mutant(digests={"rule_digest_sha256":
                                                    custody["digests"]["rule_digest_sha256"],
                                                    "contract_digest_sha256": "0" * 64})).get("result"),
         "UNKNOWN"),
        ("non-canonical custody path",
         evaluate(live, custody_obj=mutant(sole_path="scaffolding/activation_rules/elsewhere.json")).get("result"),
         "UNKNOWN"),
        ("forged proven-identity label",
         evaluate(live, custody_obj=mutant(identity={"custodian_label": "THE COMMANDER",
                                                     "custodian_class": "commander_label_assertion",
                                                     "identity_proven": True})).get("result"),
         "UNKNOWN"),
        ("missing history field", evaluate(dict(live, history=None)).get("result"), "UNKNOWN"),
        ("disallowed history (persisted claim)",
         evaluate(submit(history={"basis": "declared-by-supplier",
                                  "entries": [{"result": "SATISFIED", "persisted": True}]})).get("result"),
         "UNKNOWN"),
        ("disposition record shape (fixture only)",
         evaluate(submit(disposition={"kind": "commander_disposition", "authenticated": False,
                                      "statement": "fixture disposition, unauthenticated"})).get("result"),
         "UNKNOWN"),
        ("conflict: absent flag with text",
         evaluate(submit(present=False, value="text while absent")).get("result"), "CONFLICT"),
        ("conflict: revision disagreement",
         evaluate(submit(declaration_revision=99)).get("result"), "CONFLICT"),
        ("task binding conflict", evaluate(submit(task_id="TID-2026-01-01-z")).get("result"),
         "CONFLICT"),
        ("repeat evaluation is idempotent, never a first-use claim",
         (evaluate(live).get("result"), evaluate(live).get("result")), ("SATISFIED", "SATISFIED")),
    ]
    receipts = [evaluate(live), evaluate(submit(value=None, present=False))]
    live_receipt = receipts[0]
    checks = [(label, got, want) for label, got, want in vectors]
    checks += [
        ("no live authenticated-disposition path",
         live_receipt["result"] != "COMMANDER DISPOSITION" and
         all(r["result"] != "COMMANDER DISPOSITION"
             for r in (evaluate(submit(disposition={"kind": "commander_disposition",
                                                    "authenticated": True,
                                                    "statement": "well-formed but unauthenticated"})),)),
         True),
        ("no permission elevation in the receipt",
         live_receipt["authority"] == "none" and
         "no_activation_or_permission_grant" in live_receipt["limits"], True),
        ("no persistence in the receipt",
         live_receipt["persisted"] is False and "no_persistence" in live_receipt["limits"], True),
        ("receipt satisfies its own closed schema",
         not _schema_findings(live_receipt, "receipt"), True),
        ("schema-invalid receipt is rejected",
         bool(_schema_findings(dict(live_receipt, authority="granted"), "receipt")), True),
        ("live custody satisfies its own closed schema",
         not _schema_findings(custody, "custody"), True),
        ("live submission satisfies its own closed schema",
         not _schema_findings(live, "submission"), True),
    ]
    ok = 0
    for label, got, want in checks:
        good = got == want
        ok += good
        print(f"  {'PASS' if good else 'RETURNED'} {label}"
              + ("" if good else f" — got {got!r}, want {want!r}"))
    print(f"activation_conformance self-test: {ok}/{len(checks)} PASS")
    return 0 if ok == len(checks) else 1


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    submission_path = None
    as_json = False
    rest = []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg == "--self-test":
            return self_test()
        if arg == "--json":
            as_json = True
        elif arg == "--submission":
            if index + 1 >= len(args):
                print("usage: activation_conformance.py --submission <file> [--json]",
                      file=sys.stderr)
                return 2
            index += 1
            submission_path = args[index]
        else:
            print(f"usage: activation_conformance.py --submission <file> [--json] "
                  f"(unknown argument {arg!r}; custody path is fixed and not a flag)",
                  file=sys.stderr)
            return 2
        index += 1
    submission = None
    if submission_path:
        submission, problem = _load_json(submission_path, ROOT, cap=MAX_SUBMISSION_BYTES)
        if problem:
            receipt = _receipt("UNKNOWN", [f"submission unavailable: {problem}"], None)
            print(json.dumps(receipt, indent=2) if as_json else
                  f"  result: {receipt['result']} — {receipt['reasons'][0]}")
            return 1
    receipt = evaluate(submission)
    if as_json:
        print(json.dumps(receipt, indent=2))
    else:
        print(f"  result   : {receipt['result']}")
        print(f"  custody  : {receipt['custody_path']} (fixed)")
        print(f"  cutoff   : {receipt['cutoff_recorded_on'] or '—'}")
        for reason in receipt["reasons"]:
            print(f"  reason   : {reason}")
        print(f"  limits   : {' · '.join(receipt['limits'])}")
        print("  authority: none — a conformance result is not authentication, "
              "permission, or activation")
    return 0 if receipt["result"] == "SATISFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
