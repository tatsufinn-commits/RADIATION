#!/usr/bin/env python3
"""V0.1A verdict-record shape, semantic, limitation, and append-only tests."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from radiation_core import relay

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/verdict_record.schema.json"
DEST = ROOT / "evidence/verdict/records.jsonl"


def valid_record():
    return {
        "schema_name": "radiation.verdict/0.1a", "record_id": "VR-2026-09-30-A",
        "created_at": "2026-09-30T00:00:00Z",
        "objective": {"statement": "Choose a documentation path", "scope": ["advisory comparison"], "exclusions": ["implementation"]},
        "considered_paths": [
            {"path_id": "A", "summary": "minimal", "tradeoffs": "less detail"},
            {"path_id": "B", "summary": "expanded", "tradeoffs": "more review"}],
        "selection": {"path_id": "A", "rationale": "bounded fit"},
        "rejected_residuals": [{"path_id": "B", "residual": "detail remains available later"}],
        "capability_limitations": ["manual advice only"], "retained_blockers": ["Commander decision remains required"],
        "outcome": "advisory", "analyze_invoked": 0, "advisory_only": True,
        "execution_authorized": False, "blockers_cleared": False,
        "advisory_seal": {"record_complete": True, "meaning": "record-completeness-only-not-commander-approval-or-repository-seal"},
        "commander_visibility": {"reported": False, "verified": False, "authentication_claimed": False},
        "history": {"supersedes_record_id": "", "rewrites_prior_record": False}}


def findings(record):
    out = []
    relay._schema_check(record, "verdict_record.schema.json", "record", out)
    if out:
        return out
    ids = [p["path_id"] for p in record["considered_paths"]]
    residual_ids = [r["path_id"] for r in record["rejected_residuals"]]
    selected = record["selection"]["path_id"]
    if len(ids) != len(set(ids)): out.append("considered path IDs must be unique")
    if selected not in ids: out.append("selection must reference a considered path")
    if len(residual_ids) != len(set(residual_ids)): out.append("residual path IDs must be unique")
    if set(residual_ids) != set(ids) - {selected}: out.append("residuals must exactly cover unselected paths")
    if record["history"]["supersedes_record_id"] == record["record_id"]: out.append("record cannot supersede itself")
    return out


class VerdictRecordTests(unittest.TestCase):
    def mutate(self, dotted, value):
        obj = copy.deepcopy(valid_record()); node = obj; parts = dotted.split(".")
        for part in parts[:-1]: node = node[int(part)] if part.isdigit() else node[part]
        if parts[-1].isdigit(): node[int(parts[-1])] = value
        else: node[parts[-1]] = value
        return obj

    def test_valid_record_and_executor_supported_schema(self):
        self.assertEqual(findings(valid_record()), [])
        schema = json.loads(SCHEMA.read_text())
        self.assertEqual(relay.unsupported_keywords(schema, []), [])

    def test_tracked_destination_is_empty(self):
        self.assertEqual(DEST.read_bytes(), b"")

    def test_malformed_and_missing_selection_rejected(self):
        obj = valid_record(); del obj["selection"]
        self.assertTrue(findings(obj))
        self.assertTrue(findings(self.mutate("schema_name", "wrong")))

    def test_multiple_selection_shape_rejected(self):
        self.assertTrue(findings(self.mutate("selection", [valid_record()["selection"], valid_record()["selection"]])))

    def test_unique_paths_and_selection_membership(self):
        self.assertTrue(findings(self.mutate("considered_paths.1.path_id", "A")))
        self.assertTrue(findings(self.mutate("selection.path_id", "Z")))

    def test_residual_exactness(self):
        self.assertTrue(findings(self.mutate("rejected_residuals", [])))
        obj = valid_record(); obj["rejected_residuals"].append({"path_id": "A", "residual": "selected cannot be rejected"})
        self.assertTrue(findings(obj))

    def test_hard_non_execution_constants(self):
        for field, value in (("analyze_invoked", 1), ("advisory_only", False),
                             ("execution_authorized", True), ("blockers_cleared", True)):
            with self.subTest(field=field): self.assertTrue(findings(self.mutate(field, value)))

    def test_authentication_and_approval_claims_rejected(self):
        self.assertTrue(findings(self.mutate("commander_visibility.authentication_claimed", True)))
        self.assertTrue(findings(self.mutate("commander_visibility.verified", True)))
        self.assertTrue(findings(self.mutate("advisory_seal.meaning", "Commander approved")))

    def test_history_rewrite_and_self_link_rejected(self):
        self.assertTrue(findings(self.mutate("history.rewrites_prior_record", True)))
        self.assertTrue(findings(self.mutate("history.supersedes_record_id", "VR-2026-09-30-A")))

    def test_append_only_candidate_history(self):
        first = json.dumps(valid_record(), sort_keys=True, separators=(",", ":")) + "\n"
        second_obj = valid_record(); second_obj["record_id"] = "VR-2026-09-30-B"; second_obj["history"]["supersedes_record_id"] = "VR-2026-09-30-A"; second_obj["outcome"] = "hold"
        second = json.dumps(second_obj, sort_keys=True, separators=(",", ":")) + "\n"
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "records.jsonl"; p.write_text(first); before = p.read_bytes(); p.write_bytes(before + second.encode())
            after = p.read_bytes(); self.assertEqual(after[:len(before)], before)
            self.assertEqual([json.loads(x)["record_id"] for x in after.splitlines()], ["VR-2026-09-30-A", "VR-2026-09-30-B"])

if __name__ == "__main__": unittest.main()
