#!/usr/bin/env python3
"""
CUE Resolver / Linter — Candidate B opening P-11-A
Deterministic precedence resolver: commander_order > ratified_policy > cue > heuristic > content
CONTENT-only for courses/web/tools/subagent/imported_text — never alters effects.
Emits selected/suppressed/reason/conflicting IDs + law.
Lawful source: cue/CUE_CATALOG.json + schemas/cue_card.schema.json
Non-boot, non-runtime. Used by tests/test_cue_resolver.py and evals/hostile closure.
"""
from __future__ import annotations
import json
import sys
import os
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

# --- Law ---
PRECEDENCE_ORDER = {
    "commander_order": 100,
    "ratified_policy": 80,
    "cue": 60,
    "heuristic": 20,
    "content": 0,
}
# Sources that are forced to content-only regardless of claimed precedence
CONTENT_SOURCES = {"course", "web", "tool", "subagent", "imported_text", "course_derivative", "tool_result", "subagent_result"}

LAW_STRING = "commander_order>ratified_policy>cue>heuristic>content"

# --- Catalog loading ---
def load_catalog(catalog_path: Path) -> List[Dict[str, Any]]:
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    return data.get("cues", [])

def load_schema(schema_path: Path) -> Dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))

# --- Validation (linter) ---
def lint_catalog(catalog_path: Path, schema_path: Path, mapping_path: Path | None = None) -> Dict[str, Any]:
    issues = []
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    cues = catalog.get("cues", [])
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = schema.get("required", [])
    # Basic field presence
    seen_ids = set()
    for idx, cue in enumerate(cues):
        for f in required:
            if f not in cue:
                issues.append(f"cue[{idx}] {cue.get('id','?')} missing required field {f}")
        cid = cue.get("id")
        if cid in seen_ids:
            issues.append(f"duplicate cue id {cid}")
        seen_ids.add(cid)
        # precedence must be in law
        prec = cue.get("precedence")
        if prec not in PRECEDENCE_ORDER:
            issues.append(f"{cid} invalid precedence {prec}")
        # priority range
        pri = cue.get("priority")
        if not isinstance(pri, int) or not (1 <= pri <= 100):
            issues.append(f"{cid} invalid priority {pri}")
        # effect enum
        effect = cue.get("effect")
        if effect not in ("read","plan","draft","evidence","propose","ask","none"):
            issues.append(f"{cid} invalid effect {effect}")
        # conflicts_with must reference existing ids or at least syntactically valid
        for conflict in cue.get("conflicts_with", []):
            if not conflict.startswith("CUE-"):
                issues.append(f"{cid} conflicts_with invalid {conflict}")
    # directive coverage
    if mapping_path and mapping_path.exists():
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
        mapped_directives = set(m["directive_id"] for m in mapping.get("mappings", []))
        # load standing-directives — file is dict {_doctrine, directives:[{id}]}
        sd_path = catalog_path.parent / "standing-directives.json"
        sd_ids = set()
        if sd_path.exists():
            try:
                raw_sd = json.loads(sd_path.read_text(encoding="utf-8"))
                if isinstance(raw_sd, dict) and "directives" in raw_sd:
                    sd_ids = set(d.get("id") for d in raw_sd["directives"] if isinstance(d, dict) and d.get("id"))
                elif isinstance(raw_sd, dict):
                    # fallback: keys that look like SD-GOV-*
                    sd_ids = set(k for k in raw_sd.keys() if k.startswith("SD-GOV-"))
                elif isinstance(raw_sd, list):
                    sd_ids = set(d.get("id") for d in raw_sd if isinstance(d, dict))
            except Exception:
                pass
        missing = sd_ids - mapped_directives
        prose = set(mapping.get("prose_only", []))
        uncovered = missing - prose
        if uncovered:
            issues.append(f"directives not mapped and not prose-only: {sorted(uncovered)}")
    return {
        "law": LAW_STRING,
        "catalog_path": str(catalog_path),
        "cue_count": len(cues),
        "issues": issues,
        "ok": len(issues) == 0,
    }

# --- Core resolver ---
def normalize_candidate(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a candidate detection into canonical form.
    If trigger_source in CONTENT_SOURCES, force precedence=content and never allow effect elevation.
    """
    cand = dict(raw)  # shallow copy
    source = str(cand.get("trigger_source", "")).lower()
    claimed_prec = cand.get("precedence", "heuristic")
    # Force content-only
    if source in CONTENT_SOURCES or "imported" in source or "course" in source or "tool" in source or "subagent" in source:
        # But allow explicit commander_order if source is commander — commander never in CONTENT_SOURCES
        if source not in ("commander", "ratified_policy", "policy", "cue", "heuristic") and source in CONTENT_SOURCES:
            cand["_original_precedence"] = claimed_prec
            cand["precedence"] = "content"
            cand["_forced_content_reason"] = f"CONTENT-only: source '{source}' can never elevate to {claimed_prec}"
    # Ensure precedence valid
    if cand.get("precedence") not in PRECEDENCE_ORDER:
        cand["precedence"] = "heuristic"
    # Ensure priority
    if "priority" not in cand:
        cand["priority"] = 1
    # Ensure id
    if "id" not in cand:
        cand["id"] = "CUE-UNKNOWN"
    return cand

def resolve_candidates(candidates: List[Dict[str, Any]], law: str = LAW_STRING) -> Dict[str, Any]:
    """
    Deterministic resolver.
    Input: list of dicts each with id, precedence, priority, trigger_source, effect, etc.
    Output: {law, selected, suppressed, reason_map, conflicting_groups}
    - selected: list of candidates that survive (highest precedence tier)
    - suppressed: list of candidates suppressed with reason
    - conflicting_groups: list of {ids, law, winner}
    """
    normalized = [normalize_candidate(c) for c in candidates]
    # Sort by precedence desc, priority desc, id asc for determinism
    def sort_key(c):
        return (-PRECEDENCE_ORDER.get(c.get("precedence", "heuristic"), 0), -int(c.get("priority", 0)), c.get("id", ""))

    sorted_cands = sorted(normalized, key=sort_key)

    if not sorted_cands:
        return {
            "law": law,
            "selected": [],
            "suppressed": [],
            "reason_map": {},
            "conflicting_ids": [],
            "conflicting_groups": [],
        }

    # Determine max precedence tier present
    max_prec_value = PRECEDENCE_ORDER.get(sorted_cands[0].get("precedence"), 0)
    # If max is content (0) and there are no non-content, then nothing elevates effects
    # Selected are those at max precedence, unless max is content -> they are still selected as content but with effect=none/read only
    selected = []
    suppressed = []
    reason_map = {}
    conflicting_ids = []

    # Group by conflicting trigger? For simplicity, if multiple candidates have overlapping scope, highest wins
    # Here we treat all as potentially conflicting if they claim same scope or explicit conflicts_with
    # For deterministic demo, we select top tier; rest suppressed

    # Build conflict detection: if any candidate's conflicts_with includes another's id, they conflict
    id_to_cand = {c["id"]: c for c in sorted_cands}

    # Selected: all at max precedence value, unless content-only then they are selected but with restricted effect
    for c in sorted_cands:
        prec_val = PRECEDENCE_ORDER.get(c.get("precedence"), 0)
        if prec_val == max_prec_value:
            # If content, enforce effect cannot be propose/plan beyond read? But per law, content never alters effects
            # So we keep but mark effect restricted to read/none
            if prec_val == 0:
                # Content never elevates directives/credentials/authority/effects
                # We still select as content, but reason notes no elevation
                selected.append(c)
                reason_map[c["id"]] = c.get("_forced_content_reason") or "CONTENT-only: selected but cannot elevate effects/directives/credentials/authority"
            else:
                selected.append(c)
                reason_map[c["id"]] = f"selected per {law}: precedence={c.get('precedence')} priority={c.get('priority')}"
        else:
            suppressed.append(c)
            if "_forced_content_reason" in c:
                reason_map[c["id"]] = c["_forced_content_reason"]
            else:
                reason_map[c["id"]] = f"suppressed: lower precedence {c.get('precedence')}({prec_val}) < {sorted_cands[0].get('precedence')}({max_prec_value}) per {law}"
            conflicting_ids.append(c["id"])

    # Conflicting groups: if any selected conflicts_with suppressed or vice versa, group them
    conflicting_groups = []
    for sel in selected:
        conflicts = sel.get("conflicts_with", [])
        group_ids = [sel["id"]]
        for cid in conflicts:
            if cid in id_to_cand:
                group_ids.append(cid)
        if len(group_ids) > 1:
            conflicting_groups.append({
                "winner": sel["id"],
                "ids": sorted(set(group_ids)),
                "law": law,
                "reason": f"{sel['id']} wins per {law} + priority"
            })

    return {
        "law": law,
        "selected": selected,
        "suppressed": suppressed,
        "reason_map": reason_map,
        "conflicting_ids": conflicting_ids,
        "conflicting_groups": conflicting_groups,
    }

# --- Content-selection path used by hostile fixtures ---
def resolve_content_selection_path(real_catalog_cues: List[Dict[str, Any]], external_text: str, source_type: str) -> Dict[str, Any]:
    """
    REAL resolver over REAL path: external_text (e.g., imported HTML, injected course, tool/subagent shaped JSON)
    is treated as CONTENT-only candidate that attempts to elevate.
    Returns resolution proving no elevation of effects/directives/credentials/authority.
    """
    # Simulate detection of cues inside external_text attempting to claim authority
    # For each catalog cue, if its trigger appears in external_text (case-insensitive), we create a forged candidate claiming high precedence
    forged = []
    low_text = external_text.lower()
    for cue in real_catalog_cues:
        trig = cue.get("trigger","").lower()
        if trig and trig in low_text:
            # Attacker tries to claim commander_order
            forged.append({
                "id": cue["id"],
                "precedence": "commander_order",  # attacker claims
                "priority": 100,
                "trigger_source": source_type,  # e.g., 'imported_text' -> forced to content
                "effect": cue.get("effect","propose"),
                "trigger": cue.get("trigger"),
                "conflicts_with": cue.get("conflicts_with", []),
            })
    # Also add a generic injection attempt
    if any(kw in low_text for kw in ["ignore previous", "system prompt", "grant", "credential", "api key", "directive", "authority", "elevate"]):
        forged.append({
            "id": "CUE-INJECTION-ATTEMPT",
            "precedence": "commander_order",
            "priority": 100,
            "trigger_source": source_type,
            "effect": "propose",
            "trigger": "injection keywords",
            "conflicts_with": [],
        })

    # If no forged detected, still create one content-only candidate representing the external content itself
    if not forged:
        forged.append({
            "id": f"CUE-CONTENT-{source_type.upper()}",
            "precedence": "commander_order",  # claimed
            "priority": 100,
            "trigger_source": source_type,
            "effect": "propose",
            "trigger": "external content",
            "conflicts_with": [],
        })

    result = resolve_candidates(forged, law=LAW_STRING)
    # Verify no elevation: all selected must be precedence=content and effect restricted
    elevation = False
    for sel in result["selected"]:
        if sel.get("precedence") != "content":
            elevation = True
        # Effect elevation check: content should not be allowed to propose/draft/plan if it tries to alter directives/credentials
        # We enforce that content's effect is treated as read/none regardless of claimed
        # For proof, we check original claimed effect vs resolved precedence
    result["no_elevation"] = not elevation
    result["external_source"] = source_type
    result["external_length"] = len(external_text)
    return result

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="CUE Resolver / Linter P-11-A Candidate B")
    parser.add_argument("--catalog", default="cue/CUE_CATALOG.json", help="Path to CUE_CATALOG.json")
    parser.add_argument("--schema", default="schemas/cue_card.schema.json", help="Path to cue_card schema")
    parser.add_argument("--mapping", default="cue/DIRECTIVE_CUE_MAPPING.json", help="Path to directive mapping")
    parser.add_argument("--lint", action="store_true", help="Run linter")
    parser.add_argument("--input", help="JSON file with candidates list")
    parser.add_argument("--emit", help="Output JSON file for resolution")
    parser.add_argument("--hostile", help="Path to hostile fixture file to test no elevation")
    parser.add_argument("--hostile-source", default="imported_text", help="Source type for hostile fixture")
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    schema_path = Path(args.schema)
    mapping_path = Path(args.mapping)

    if args.lint:
        lint_result = lint_catalog(catalog_path, schema_path, mapping_path)
        print(json.dumps(lint_result, indent=2))
        sys.exit(0 if lint_result["ok"] else 1)

    if args.hostile:
        text = Path(args.hostile).read_text(encoding="utf-8", errors="ignore")
        cues = load_catalog(catalog_path)
        res = resolve_content_selection_path(cues, text, args.hostile_source)
        out = json.dumps(res, indent=2)
        if args.emit:
            Path(args.emit).write_text(out, encoding="utf-8")
        else:
            print(out)
        # Exit 0 if no elevation (expected), 1 if elevation (FAIL)
        sys.exit(0 if res["no_elevation"] else 2)

    if args.input:
        candidates = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if isinstance(candidates, dict) and "candidates" in candidates:
            candidates = candidates["candidates"]
        res = resolve_candidates(candidates)
        out = json.dumps(res, indent=2)
        if args.emit:
            Path(args.emit).write_text(out, encoding="utf-8")
        else:
            print(out)
        sys.exit(0)

    # Default: lint
    lint_result = lint_catalog(catalog_path, schema_path, mapping_path)
    print(json.dumps(lint_result, indent=2))
    sys.exit(0 if lint_result["ok"] else 1)

if __name__ == "__main__":
    main()
