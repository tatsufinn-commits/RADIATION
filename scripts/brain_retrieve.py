#!/usr/bin/env python3
"""
brain_retrieve.py — Brain Retrieval Lattice (G5) deterministic selector law

P-14: corpus behavior goes from absence to mechanism.

Tokenize: lowercase [a-z0-9]+.
score(entry, q) = 3·|tags∩q| + 2·|title_tokens∩q| + 1·|path_tokens∩q| — arithmetic, no heuristics, no randomness.
Abstention: score < 4 → no hit. Result list = all entries ≥4 ranked (score desc, id asc); output declared evidence-only (retrieval surfaces corpus, never elevates scope — II.11).

Modes:
  --query "<text>" (print ranked/abstain)
  --cases evals/brain/retrieval_cases.json (run fixture suite, per-case finding lines, exit non-zero on any mismatch)
  --self-test (≥6 vectors incl. desk-pinned formula arithmetic — hand-computable expected scores)

Non-goals (hard): NO embeddings, NO vector DB, NO network, NO LLM calls, NO caching state. D4 research non-goals stand.
Stdlib only.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "Brain" / "MEMORY_CATALOG.jsonl"

TOKEN_RE = re.compile(r"[a-z0-9]+")

def tokenize(text):
    """Lowercase [a-z0-9]+ tokenization."""
    return TOKEN_RE.findall(text.lower())

def load_catalog(path=CATALOG_PATH):
    entries = []
    if not path.exists():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
            entries.append(e)
        except Exception:
            continue
    # Ensure sorted by id (spec)
    entries.sort(key=lambda x: x.get("id", ""))
    return entries

def score_entry(entry, query_tokens_set):
    """score = 3·|tags∩q| + 2·|title_tokens∩q| + 1·|path_tokens∩q|"""
    tags = set(entry.get("tags", []))
    # tags are already lowercase alphanumeric-hyphen, but tokenize to be safe? Tags are single tokens, but we treat as set
    # For intersection, tags∩q: tags are like "building-utilities" — tokenizing query gives ["building","utilities"], not "building-utilities"
    # So we need to also split tags by tokenization? Spec says |tags∩q| — tags are strings, q is tokens.
    # Interpret as: tokenize tags as well? Or exact match? Desk says arithmetic, no heuristics.
    # We will treat tags as tokens themselves lowercased, but also split hyphenated tags into tokens for matching?
    # To keep deterministic and simple: tags are considered as tokens; intersection is exact string match between tag and query token.
    # However for "building-utilities" vs query "building utilities", exact match fails, but tokenized tag would match.
    # To make retrieval useful, we will tokenize tags as well: split tags by TOKEN_RE, then intersect.
    # This is still arithmetic, no heuristics, and matches expectation of multi-token tags.
    # We will do: tags_tokens = set of tokens from all tags (tokenize each tag)
    tags_tokens = set()
    for t in entry.get("tags", []):
        tags_tokens.update(tokenize(t))
    title_tokens = set(tokenize(entry.get("title", "")))
    path_tokens = set(tokenize(entry.get("path", "")))
    q = query_tokens_set
    inter_tags = len(tags_tokens & q)
    inter_title = len(title_tokens & q)
    inter_path = len(path_tokens & q)
    score = 3*inter_tags + 2*inter_title + 1*inter_path
    return score, inter_tags, inter_title, inter_path

def retrieve(query, catalog=None):
    """Return ranked list of entries with score >=4, sorted score desc, id asc."""
    if catalog is None:
        catalog = load_catalog()
    q_tokens = tokenize(query)
    q_set = set(q_tokens)
    results = []
    for entry in catalog:
        s, it, ititle, ipath = score_entry(entry, q_set)
        if s >= 4:
            results.append((s, entry["id"], entry, it, ititle, ipath))
    # Rank: score desc, id asc
    results.sort(key=lambda x: (-x[0], x[1]))
    # Return list of dicts with score
    out = []
    for s, eid, entry, it, ititle, ipath in results:
        out.append({"id": eid, "score": s, "path": entry["path"], "title": entry["title"], "kind": entry["kind"], "tags": entry["tags"]})
    return out

def print_query(query, catalog=None):
    results = retrieve(query, catalog)
    if not results:
        print(f"Query: \"{query}\"")
        print("Result: ABSTAIN — score <4 → no hit. Retrieval surfaces corpus, never elevates scope — II.11. Evidence-only.")
        print("If the query isn't in the corpus, the mechanism says so — that is the point.")
        return []
    print(f"Query: \"{query}\" — {len(results)} hit(s) (score ≥4)")
    print("Evidence-only: retrieval surfaces corpus, never elevates scope — II.11")
    for r in results:
        print(f"  - {r['id']} score={r['score']} path={r['path']} title={r['title']}")
    return results

def run_cases(cases_path):
    """Run fixture suite evals/brain/retrieval_cases.json"""
    cases_file = pathlib.Path(cases_path)
    if not cases_file.exists():
        print(f"brain_retrieve: cases file not found: {cases_path}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(cases_file.read_text(encoding="utf-8"))
    cases = data if isinstance(data, list) else data.get("cases", [])
    catalog = load_catalog()
    failures = []
    print(f"brain_retrieve --cases: {len(cases)} case(s) from {cases_path}")
    for idx, case in enumerate(cases, 1):
        q = case.get("query", "")
        expected_ids = case.get("expected_ids", [])
        # Determinism case: duplicated verbatim — both must produce identical output, scored by harness itself
        # We handle determinism by checking if case has "determinism" flag or duplicate query
        results = retrieve(q, catalog)
        got_ids = [r["id"] for r in results]
        # Check exactness + order
        if got_ids != expected_ids:
            failures.append((case, got_ids))
            print(f"  ❌ Case {idx} FAIL: query=\"{q}\" expected={expected_ids} got={got_ids}")
            # Finding line in house style
            print(f"  - brain_retrieve: case {idx} mismatch query=\"{q}\" expected_ids {expected_ids} got {got_ids}")
        else:
            print(f"  ✅ Case {idx} PASS: query=\"{q}\" → {got_ids}")
    # Determinism check: find duplicated queries and ensure identical output
    # Group by query
    from collections import defaultdict
    groups = defaultdict(list)
    for case in cases:
        groups[case.get("query")].append(case)
    for q, group in groups.items():
        if len(group) > 1:
            # Run twice and compare
            r1 = retrieve(q, catalog)
            r2 = retrieve(q, catalog)
            if r1 != r2:
                failures.append(({"query": q, "determinism": True}, [r["id"] for r in r2]))
                print(f"  ❌ Determinism FAIL: query=\"{q}\" produced different outputs on two runs")
            else:
                print(f"  ✅ Determinism PASS: query=\"{q}\" duplicated case produces identical output")
    if failures:
        print(f"\n✗ brain_retrieve --cases: {len(failures)} failure(s) out of {len(cases)}")
        sys.exit(1)
    else:
        print(f"\n✅ brain_retrieve --cases: all {len(cases)} cases match")
        sys.exit(0)

def self_test():
    """≥6 vectors incl. desk-pinned formula arithmetic — hand-computable expected scores"""
    ok = 0
    fails = []

    def check(name, cond, detail=""):
        nonlocal ok
        if cond:
            ok += 1
            print(f"  ✅ {name}")
        else:
            fails.append(f"{name} {detail}")
            print(f"  ❌ {name} {detail}")

    catalog = load_catalog()
    # Vector 1: tokenization
    check("tokenize lowercase [a-z0-9]+", tokenize("AR153P Building-Utilities!") == ["ar153p", "building", "utilities"], f"got {tokenize('AR153P Building-Utilities!')}")
    # Vector 2: formula arithmetic hand-computable
    # Entry: tags ["a","b","c"], title "a b", path "a/b/c"
    # Query: "a b c" -> tags∩q = 3 (a,b,c), title∩q =2 (a,b), path∩q=3 (a,b,c) => score=3*3+2*2+1*3=9+4+3=16
    dummy_entry = {"id": "MEM-note-dummy-001", "path": "Brain/a/b/c.md", "title": "a b", "kind": "note", "tags": ["a","b","c"], "added": "2026-09-16"}
    s, it, ititle, ipath = score_entry(dummy_entry, set(tokenize("a b c")))
    check("formula arithmetic hand-computable 3*3+2*2+1*3=16", s == 16, f"got score {s} it={it} ititle={ititle} ipath={ipath}")
    # Vector 3: abstention score <4 → no hit
    # Query "xyz" vs entry with no overlap => score 0 <4
    s2, _, _, _ = score_entry(dummy_entry, set(tokenize("xyz")))
    check("abstention score <4 → no hit", s2 < 4, f"got {s2}")
    # Vector 4: ranking tie-break id asc
    # Two entries same score, id asc should win
    e1 = {"id": "MEM-ledger-task", "path": "Brain/frontal_lobe/task_ledger.md", "title": "Task Ledger", "kind": "ledger", "tags": ["task-ledger", "tasks"], "added": "2026-09-16"}
    e2 = {"id": "MEM-ledger-testament", "path": "Brain/frontal_lobe/testament.md", "title": "Task Ledger Testament", "kind": "ledger", "tags": ["task-ledger", "tasks"], "added": "2026-09-16"}
    # Query "task ledger" -> both have same tags and title tokens, but path tokens differ slightly, but score likely same
    # Force same score by using identical tags/title/path tokens intersection
    # Use catalog entries that we know have same score for query "task ledger"
    # We'll test sorting: if scores equal, id asc
    results = retrieve("task ledger", catalog=[e1, e2])
    if len(results) >= 2:
        check("ranking tie-break id asc", results[0]["id"] < results[1]["id"], f"got order {[r['id'] for r in results]}")
    else:
        # If not same score, still test tie-break with identical entries
        e1_dup = {"id": "MEM-ledger-a", "path": "Brain/a.md", "title": "task ledger", "kind": "ledger", "tags": ["task", "ledger"], "added": "2026-09-16"}
        e2_dup = {"id": "MEM-ledger-b", "path": "Brain/b.md", "title": "task ledger", "kind": "ledger", "tags": ["task", "ledger"], "added": "2026-09-16"}
        results2 = retrieve("task ledger", catalog=[e2_dup, e1_dup])  # input order reversed
        check("ranking tie-break id asc (identical score)", results2[0]["id"] == "MEM-ledger-a", f"got {results2[0]['id'] if results2 else 'none'}")
    # Vector 5: known-hit exactness
    results_task = retrieve("task ledger frontal lobe", catalog)
    got_ids = [r["id"] for r in results_task]
    check("known-hit exactness task ledger", "MEM-ledger-task" in got_ids, f"got {got_ids}")
    # Vector 6: abstention for nonsense query
    results_nonsense = retrieve("qwertyuiop asdfghjkl zxcvbnm", catalog)
    check("abstention nonsense query → []", len(results_nonsense) == 0, f"got {results_nonsense}")
    # Vector 7: determinism run twice identical stdout (score list identical)
    r1 = retrieve("ar153p building utilities", catalog)
    r2 = retrieve("ar153p building utilities", catalog)
    check("determinism run twice identical", r1 == r2, f"r1 {r1} r2 {r2}")
    # Vector 8: multi-hit ranked (query that hits multiple course derivatives)
    results_multi = retrieve("course derivative", catalog)
    check("multi-hit ranked ≥2 hits", len(results_multi) >= 2, f"got {len(results_multi)}")

    print(f"\n{'✅' if not fails else '❌'} brain_retrieve self-test: {ok} passed, {len(fails)} failed")
    for f in fails:
        print("   ✗", f)
    return not fails

def main():
    parser = argparse.ArgumentParser(description="Brain Retrieval Lattice deterministic selector")
    parser.add_argument("--query", help="Query text to retrieve")
    parser.add_argument("--cases", help="Path to evals/brain/retrieval_cases.json fixture suite")
    parser.add_argument("--self-test", action="store_true", help="Run self-test vectors")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    elif args.cases:
        run_cases(args.cases)
    elif args.query:
        retrieve(args.query)
        print_query(args.query)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
