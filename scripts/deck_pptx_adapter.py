#!/usr/bin/env python3
"""
deck_pptx_adapter.py — Optional PPTX adapter, wall-maintained (S-2-PPTX-C stage 3 of 5)

Standing interface rule (proposal, adopted): expose guardrailed verbs — plan_slide · fill_template · verify_deck — never raw primitives.
Influences (license-logged, clean-room, nothing imported): GenSlide skeleton (MIT ✓) and mcp-office's "Output Contract for machine-verifiable slide specs" governance pattern (MIT ✓; its contracts doc = nearest-further-reading when R&D sends tail).

Import-guard discipline: adapter NEVER imports pptx at module level; capability probe = try: import pptx / except ImportError → {"pptx": "AVAILABLE"} with version, or {"pptx": "ABSENT-UNKNOWN"} with failure recorded as unknown, never claimed absent-by-proxy. Same P-19 contract grammar (asserted vs observed) applies: only probe outcome asserts.

Ship no other behavior. Adapter is accommodation for tomorrow, probe is only live edge today.

No actual rendering in this stage — dry-run evidence only. No committed binaries, no WP-D canon text, no theme-registry edits, no network.

Policy: import pptx = FAIL-class outside guarded probe block — this file contains guarded probe only, never at module level.
"""

# NEVER import pptx at module level — import-guard discipline
# Only inside probe function via try/except

def probe_pptx_capability():
    """
    Capability probe: try import pptx / except ImportError → {"pptx": "AVAILABLE"} with version, or {"pptx": "ABSENT-UNKNOWN"} with failure recorded as unknown, never claimed absent-by-proxy.
    P-19 contract grammar: asserted vs observed — only probe outcome asserts.
    Returns dict with status and version or failure note.
    """
    try:
        import pptx
        ver = getattr(pptx, "__version__", "unknown")
        return {"pptx": "AVAILABLE", "version": ver, "note": "probe observed AVAILABLE — version asserted from module"}
    except ImportError as e:
        # Failure recorded as unknown, never claimed absent-by-proxy — constraint honesty ABSENT ≠ UNAVAILABLE ≠ UNKNOWN
        return {"pptx": "ABSENT-UNKNOWN", "version": None, "failure": str(e)[:200], "note": "probe observed ABSENT-UNKNOWN — failure recorded as unknown, never claimed absent-by-proxy per IP-ENV-01 grammar"}
    except Exception as e:
        # Any other exception also recorded as unknown
        return {"pptx": "ABSENT-UNKNOWN", "version": None, "failure": str(e)[:200], "note": "probe observed ABSENT-UNKNOWN — exception recorded as unknown"}

def get_adapter_status():
    """
    Returns adapter status line for verify_deck verb
    """
    cap = probe_pptx_capability()
    if cap.get("pptx") == "AVAILABLE":
        return f"adapter: AVAILABLE — pptx {cap.get('version')} — would render if fill_template invoked with adapter present"
    else:
        return f"adapter: ABSENT-UNKNOWN — blocked_at dependency canon (WP-D 🟠) — failure {cap.get('failure','')} — would_render plan only, no fake render"

if __name__ == "__main__":
    import json
    print(json.dumps(probe_pptx_capability(), indent=2))
