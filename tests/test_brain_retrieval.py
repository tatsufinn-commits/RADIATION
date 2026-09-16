#!/usr/bin/env python3
"""
Test harness for brain_retrieve.py — P-14 Brain Retrieval Lattice (G5)

Vectors ≥6, bound to (a)+(c): id-uniqueness/paths-exist/jsonl-valid-vs-schema · known-hit exactness · abstention · formula arithmetic · ranking tie-break · determinism
"""
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "Brain" / "MEMORY_CATALOG.jsonl"
SCHEMA_PATH = ROOT / "schemas" / "memory_catalog_entry.schema.json"
CASES_PATH = ROOT / "evals" / "brain" / "retrieval_cases.json"

TOKEN_RE = re.compile(r"[a-z0-9]+")

def tokenize(text):
    return TOKEN_RE.findall(text.lower())

def load_catalog():
    entries = []
    for line in CATALOG_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries

def run_cmd(cmd, cwd=ROOT):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    return p

class TestBrainRetrieval(unittest.TestCase):
    def test_id_uniqueness_paths_exist_jsonl_valid_vs_schema(self):
        """id-uniqueness / paths-exist / jsonl-valid-vs-schema"""
        self.assertTrue(CATALOG_PATH.exists(), "MEMORY_CATALOG.jsonl must exist")
        self.assertTrue(SCHEMA_PATH.exists(), "memory_catalog_entry schema must exist")
        entries = load_catalog()
        self.assertGreaterEqual(len(entries), 20, "Seed ≥20 entries")
        ids = [e.get("id") for e in entries]
        self.assertEqual(len(ids), len(set(ids)), "ids must be unique")
        # Sorted by id
        sorted_ids = sorted(ids)
        self.assertEqual(ids, sorted_ids, "entries must be sorted by id")
        # Paths exist
        for e in entries:
            p = ROOT / e.get("path", "")
            self.assertTrue(p.exists(), f"path must exist: {e.get('path')} for id {e.get('id')}")
        # jsonl valid vs schema (basic checks, not full JSON schema executor)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        required = schema.get("required", [])
        pattern_id = re.compile(schema["properties"]["id"]["pattern"])
        pattern_path = re.compile(schema["properties"]["path"]["pattern"])
        kind_enum = set(schema["properties"]["kind"]["enum"])
        for e in entries:
            for field in required:
                self.assertIn(field, e, f"missing required field {field} in {e.get('id')}")
            self.assertRegex(e["id"], pattern_id, f"id pattern mismatch {e['id']}")
            self.assertRegex(e["path"], pattern_path, f"path pattern mismatch {e['path']}")
            self.assertIn(e["kind"], kind_enum, f"kind enum mismatch {e['kind']}")
            self.assertGreaterEqual(len(e["tags"]), 3, f"tags ≥3 for {e['id']}")
            self.assertRegex(e["added"], r"^\d{4}-\d{2}-\d{2}$", f"added date pattern for {e['id']}")

    def test_known_hit_exactness(self):
        """known-hit exactness bound to evals/brain/retrieval_cases.json"""
        self.assertTrue(CASES_PATH.exists(), "retrieval_cases.json must exist")
        cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        # Run brain_retrieve --cases via subprocess to ensure harness itself passes
        p = run_cmd(f"python3 scripts/brain_retrieve.py --cases {CASES_PATH}")
        self.assertEqual(p.returncode, 0, f"cases suite should all-match, got {p.stdout} {p.stderr}")
        # Also test one known-hit manually
        p2 = run_cmd(f"python3 scripts/brain_retrieve.py --query 'ar153p building utilities'")
        self.assertIn("MEM-course_derivative-ar153p", p2.stdout)

    def test_abstention(self):
        """abstention for unrelated/nonsense queries → expected_ids: []"""
        p = run_cmd(f"python3 scripts/brain_retrieve.py --query 'qwertyuiop asdfghjkl'")
        self.assertIn("ABSTAIN", p.stdout)
        # Also via cases
        cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        abstention_cases = [c for c in cases if not c.get("expected_ids")]
        self.assertGreaterEqual(len(abstention_cases), 4, "≥4 abstention cases required")
        for case in abstention_cases:
            self.assertEqual(case["expected_ids"], [], f"abstention case must have []: {case}")

    def test_formula_arithmetic_hand_computed(self):
        """formula arithmetic one hand-computed case: score = 3·|tags∩q| + 2·|title∩q| + 1·|path∩q|"""
        # Hand-computed: tags ["a","b","c"], title "a b", path "a/b/c", query "a b c" => 3*3+2*2+1*3=16
        # This vector is also in self-test, but we reproduce here
        dummy_entry = {"id": "MEM-note-dummy-001", "path": "Brain/a/b/c.md", "title": "a b", "kind": "note", "tags": ["a","b","c"], "added": "2026-09-16"}
        # Import score function from brain_retrieve
        sys.path.insert(0, str(ROOT / "scripts"))
        import brain_retrieve
        s, it, ititle, ipath = brain_retrieve.score_entry(dummy_entry, set(tokenize("a b c")))
        self.assertEqual(s, 16, f"hand-computed 3*3+2*2+1*3=16, got {s} it={it} ititle={ititle} ipath={ipath}")
        self.assertEqual(it, 3)
        self.assertEqual(ititle, 2)
        self.assertEqual(ipath, 3)

    def test_ranking_tie_break_id_asc(self):
        """ranking tie-break id asc when scores equal"""
        # Two entries with identical score, id asc should win
        e1 = {"id": "MEM-ledger-a", "path": "Brain/a.md", "title": "task ledger", "kind": "ledger", "tags": ["task", "ledger"], "added": "2026-09-16"}
        e2 = {"id": "MEM-ledger-b", "path": "Brain/b.md", "title": "task ledger", "kind": "ledger", "tags": ["task", "ledger"], "added": "2026-09-16"}
        sys.path.insert(0, str(ROOT / "scripts"))
        import brain_retrieve
        # Input order reversed, but output should be id asc
        results = brain_retrieve.retrieve("task ledger", catalog=[e2, e1])
        self.assertGreaterEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "MEM-ledger-a", f"tie-break id asc expected MEM-ledger-a first, got {results[0]['id']}")
        self.assertEqual(results[1]["id"], "MEM-ledger-b")

    def test_determinism_run_twice_identical(self):
        """determinism run twice identical stdout"""
        p1 = run_cmd(f"python3 scripts/brain_retrieve.py --query 'ar153p building utilities'")
        p2 = run_cmd(f"python3 scripts/brain_retrieve.py --query 'ar153p building utilities'")
        self.assertEqual(p1.stdout, p2.stdout, "determinism: run twice identical stdout")
        # Also test via cases file duplicated verbatim
        cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
        # Find duplicated query
        from collections import Counter
        queries = [c["query"] for c in cases]
        dup_queries = [q for q, cnt in Counter(queries).items() if cnt > 1]
        self.assertGreaterEqual(len(dup_queries), 1, "≥1 determinism case duplicated verbatim required")
        for q in dup_queries:
            r1 = run_cmd(f"python3 scripts/brain_retrieve.py --query '{q}'")
            r2 = run_cmd(f"python3 scripts/brain_retrieve.py --query '{q}'")
            self.assertEqual(r1.stdout, r2.stdout, f"determinism for duplicated query {q}")

if __name__ == "__main__":
    unittest.main()
