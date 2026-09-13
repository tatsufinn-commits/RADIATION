#!/usr/bin/env python3
"""render_docs.py — generated-facts pipeline (patch 4400; auditor plan item 5).
DISCOVERY OVER CONFIGURATION: every generated fact is computed from reality —
the scripts on disk, the workflow files, the validator itself, the registries.
Docs carrying <!-- GENERATED:<block>:START/END --> markers are machine-owned
between the markers; narrative outside them stays hand-written. If reality and
docs disagree, CI fails (render_docs --check) — the drift class the audit named
is closed by generation, not by vigilance.
Stdlib only. Exit 0 = in sync (--check) or written (--apply); 1 = drift."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def R(p): return os.path.join(ROOT, p)
def read(p):
    try: return open(R(p), encoding="utf-8").read()
    except OSError: return ""

def script_inventory():
    inv = []
    sd = R("scripts")
    for f in sorted(os.listdir(sd)):
        if not f.endswith(".py") or f.startswith("_"): continue
        src = open(os.path.join(sd, f), encoding="utf-8").read()
        m = re.search(r"""(['"]){3}(.*?)\1""", src, re.S)
        doc = (m.group(2).strip().splitlines()[0] if m else "—")
        doc = re.sub(r"^[a-z_]+\.py\s*[—–-]\s*", "", doc)
        writes = bool(re.search(r"open\([^)]*['\"][wa]", src)) or "--write" in src or "--public" in src
        network = bool(re.search(r"curl|urllib|requests|http[s]?://", src)) and "http[s]?://" not in doc[:0]
        if re.search(r"https?://", src) and not re.search(r"curl|urllib|requests", src): network = False
        inv.append({"name": f[:-3], "purpose": doc, "writes": writes, "network": network})
    ci = set()
    for wf in ("validate.yml", "ical_fetch.yml"):
        t = read(f".github/workflows/{wf}")
        ci |= set(re.findall(r"scripts/([a-z_]+)\.py", t))
    for it in inv: it["ci"] = it["name"] in ci
    return inv

def machine_facts():
    sys.path.insert(0, R("scripts"))
    import validate as _v
    checks = len(_v.run_all())   # findings reported, same number the summary line prints
    try:
        a = json.load(open(R("tests/knowledge_assertions.json"), encoding="utf-8"))["assertions"]
        locked = sum(1 for x in a if x.get("locked")); total = len(a)
    except Exception: locked = total = -1
    kpat = r"\bK-(?:LAW|STD|CUR|BK|MOD|MTH|REF|EXT)(?:-[A-Z0-9]+)*-\d{3}\b"
    kids = len(set(re.findall(kpat, read("docs/KNOWLEDGE_REGISTRY.md"))))
    try:
        sys.path.insert(0, R("scripts"))
        import nota as _nota
        cards = _nota.canonical_cards()
        admitted = sum(1 for p in cards if _nota.parse_card(p)[0] and _nota.parse_card(p)[0]["status"] == "ADMITTED")
    except Exception: cards, admitted = [], 0
    reg = json.load(open(R("cue/standing-directives.json"), encoding="utf-8"))
    npass = len(os.listdir(R("subskills/passive"))) if os.path.isdir(R("subskills/passive")) else 0
    nact = len(os.listdir(R("subskills/active"))) if os.path.isdir(R("subskills/active")) else 0
    inv = script_inventory()
    nci = sum(1 for it in inv if it["ci"])
    return (f"**Machine facts (GENERATED — hand edits here are a CI failure; source: render_docs.py):** "
            f"{checks} validator checks · knowledge locks {locked}/{total} "
            f"({total-locked} pending) · {kids} K-IDs · Core {admitted}/{len(cards)} cards canonical · "
            f"registry {len(reg['directives'])} directives · subskills {npass} passive + {nact} active · "
            f"scripts {len(inv)} ({nci} exercised in CI)")

PASSIVE_ROWS = {
 "surgeon": ("Chief passive: constitutional enforcement, halt authority", "ALL modes, unconditional", "manual protocol; mechanized where: validator FAIL-class gates (checks 2.5/3/11) + blocking CI"),
 "sentinel": ("Integrity watch: contradictions, ungraded claims, broken refs, decay", "ALL modes", "manual protocol; mechanized where: checks 1b/11/12/17 + regression locks"),
 "compass": ("Anti-drift: anchors the mission, classifies deviation", "ALL modes", "manual protocol (advisory — no machine control backs it yet)"),
 "curator": ("CONDITIONAL passive: ingestion of touched sources", "passive under @Radiation; invocable @Gather/@Decode; dormant @Data", "manual protocol; ingest_collection.py is the tool it drives"),
}
ACTIVE_ROWS = {
 "scout": ("Source-necessity gatekeeper; builds the Acquisition Plan BEFORE anything is fetched", "@Gather, @Decode, @Radiation", "manual protocol; check 13's link census audits the artifacts it produces"),
 "colony": ("Bulk link/resource-dump triage; feeds curator's ingestion queue", "@Gather, @Decode, @Radiation", "manual protocol (advisory)"),
 "selfdirectives": ("Self-governed task generation: cue → tier grade (🟢/🟡/🔴) → bounded execution → evidence closure", "ALL modes (declared + logged)", "manual protocol; mechanized where: registry check 25 + meta-budget check 16"),
 "fetch": ("Retrieval strategist over the open-source bank (docs/OPEN_SOURCES.md, 50 categories): Brain → registers → bank → TOOLBOX → scout-gated online", "UNIVERSAL (⚙️×6) — all modes, silent where read-only", "manual protocol; SD-GOV-010 + scout gate govern it (advisory in-context)"),
 "overule": ("COMMANDER-TRIGGERED (⚙️×6\\*): overrules AI-flagged rules under his deadline authority; never the stop-lines; every use logs a make-good debt (SD-GOV-013)", "Commander trigger ONLY", "manual protocol; boundary pinned by registry SD-GOV-013 (check 25)"),
}
def _row(name, role, cov, enf, cols):
    return f"| `{name}` | {role} | {cov} | {enf} |" if cols == 4 else f"| `{name}` | {role} | {cov} |"

def subskill_blocks():
    p = [row for n in sorted(os.listdir(R("subskills/passive"))) if n.endswith(".md") and not n.startswith("TEMPLATE")
         for row in [_row(n[:-3], *PASSIVE_ROWS.get(n[:-3], ("see file", "ALL modes", "manual protocol (advisory)")), 4)]]
    a = [row for n in sorted(os.listdir(R("subskills/active"))) if n.endswith(".md") and not n.startswith("TEMPLATE")
         for row in [_row(n[:-3], *ACTIVE_ROWS.get(n[:-3], ("see file", "see MODES.md", "manual protocol (advisory)")), 4)]]
    ph = ("| Subskill | Role | Mode coverage | Enforcement reality (4400 labeling law) |\n|---|---|---|---|\n")
    ah = ("| Subskill | Role | Available in | Enforcement reality (4400 labeling law) |\n|---|---|---|---|\n")
    return ("### PASSIVES (generated 4400 — the enforcement column is the honest one)\n" + ph + "\n".join(p),
            "### ACTIVES (generated 4400 — includes every ⚙️ subskill; discovery parity is check-pinned)\n" + ah + "\n".join(a))

def capability_block():
    inv = script_inventory()
    lines = ["", "### INVENTORY (GENERATED — reality, not memory; hand edits here are a CI failure)",
             "", "| Script | Purpose | Writes | Network | In CI |", "|---|---|---|---|---|"]
    for it in inv:
        lines.append(f"| `{it['name']}.py` | {it['purpose'][:110]} | {'yes' if it['writes'] else 'no'} | "
                     f"{'yes' if it['network'] else 'no'} | {'yes' if it['ci'] else 'no'} |")
    return "\n".join(lines)

def block(name, body):
    return f"<!-- GENERATED:{name}:START -->\n{body}\n<!-- GENERATED:{name}:END -->"

def targets():
    p, a = subskill_blocks()
    return {
 "docs/SYSTEM_STATE.md": {"machine-facts": machine_facts()},
 "docs/CAPABILITIES.md": {"capability-inventory": capability_block()},
 "subskills/SUBSKILL_INDEX.md": {"subskill-passives": p, "subskill-actives": a},
    }

MARK = re.compile(r"<!-- GENERATED:([a-z-]+):START -->\n.*?\n<!-- GENERATED:\1:END -->", re.S)

def apply_blocks(write=True):
    drift = []
    for path, blocks in targets().items():
        t = read(path)
        if not t: drift.append(f"{path}: MISSING"); continue
        orig = t
        for name, body in blocks.items():
            nb = block(name, body)
            if f"<!-- GENERATED:{name}:START -->" in t:
                pat = re.compile(r"<!-- GENERATED:" + re.escape(name) + r":START -->\n.*?\n<!-- GENERATED:" + re.escape(name) + r":END -->", re.S)
                t = pat.sub(nb, t, count=1)
            else:
                t = t.rstrip("\n") + "\n\n" + nb + "\n"
        if t != orig:
            if write:
                open(R(path), "w", encoding="utf-8").write(t)
                print(f"  rendered: {path}")
            else:
                drift.append(path)
    return drift

def main():
    check = "--check" in sys.argv
    drift = apply_blocks(write=not check)
    if check:
        if drift:
            for d in drift: print(f"  ✗ docs drift: {d} (run scripts/render_docs.py to regenerate)")
            print(f"\n❌ render_docs --check: {len(drift)} file(s) out of sync with reality")
            return 1
        print("✅ render_docs --check: generated blocks match reality")
        return 0
    print("✅ rendered. Next commits own these blocks — CI now fails if reality and docs diverge.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
