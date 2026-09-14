#!/usr/bin/env python3
"""5300 negative fixtures — declared course-corpus (E1) and replica (E2) contracts.

Builds disposable temp trees and runs the FACTORED validator cores
(``_corpus_contract_violations``, ``_replica_contract``, ``_dup_scan``) against
them. Every adversarial shape must be flagged exactly as documented; every
sanctioned shape must pass. rc 0 = all vectors behave.

Zero-write on the repository: everything happens in tempfile dirs.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import validate as V  # import-safe since 4400 — no checks run on import


def sha_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def mk_corpus(root: str, *, derivative: bool = True, declared: bool = True,
              drift: bool = False, escape: bool = False, extra: bool = False) -> dict:
    """A minimal but schema-valid corpus tree; mutators bend one rule each."""
    courses = os.path.join(root, "Brain", "courses")
    os.makedirs(courses)
    csv_b = b"code,day,room\nPC1,M,S308\n"
    with open(os.path.join(courses, "SCHEDULE.csv"), "wb") as fh:
        fh.write(csv_b)
    if derivative:
        with open(os.path.join(courses, "SCHEDULE.md"), "w", encoding="utf-8") as fh:
            fh.write("# schedule (readable derivative)\n")
    asset = {
        "path": "Brain/courses/SCHEDULE.csv",
        "sha256": sha_bytes(csv_b),  # manifest records the ORIGINAL digest
        "media_type": "text/csv",
        "role": "source_of_readable_derivative",
        "load_policy": "on_demand_only",
        "derivative_path": "Brain/courses/SCHEDULE.md" if derivative else "Brain/courses/ABSENT.md",
        "conversion": {"status": "pre_existing", "verified_on": "2026-09-14",
                       "limitations": "Fixture asset; derivation not machine-verified."},
        "distribution_review": {"status": "commander-reviewed",
                                "notes": "Fixture entry for the negative-fixture suite."}}
    if drift:  # the FILE changed after the digest was recorded
        with open(os.path.join(courses, "SCHEDULE.csv"), "ab") as fh:
            fh.write(b"DRIFT")
    m = {"schema_name": "radiation.course_corpus.manifest/1",
         "retrieved_by": "on_demand_only", "assets": [asset] if declared else []}
    if escape:
        m = dict(m)
        m["assets"] = [dict(asset, path="Brain/courses/../escaped.bin")]
        os.makedirs(os.path.join(root, "Brain"), exist_ok=True)
        with open(os.path.join(root, "Brain", "escaped.bin"), "wb") as fh:
            fh.write(b"outside")
    json.dump(m, open(os.path.join(courses, "COURSE_CORPUS_MANIFEST.json"), "w"), indent=1)
    if extra:  # an undeclared vehicle dropped into the corpus
        with open(os.path.join(courses, "NEW_SYLLABUS.pdf"), "wb") as fh:
            fh.write(b"%PDF-1.4 undeclared")
    return m


def mk_replica(root: str, *, declare: bool = True, drift: bool = False,
               missing: bool = False, third_copy: bool = False):
    """A minimal neuron tree with one active/archive pair."""
    inter = os.path.join(root, "scaffolding", "neurons", "interneurons")
    arch = os.path.join(root, "scaffolding", "neurons", "_archive")
    os.makedirs(inter); os.makedirs(arch)
    body = "# reasoning record\nverdict: contained\n"
    for d in (inter, arch):
        with open(os.path.join(d, "TID-2026-01-01-x_reasoning.md"), "w", encoding="utf-8") as fh:
            fh.write(body)
    if drift:  # the archive twin aged out of sync — silence must NOT keep it
        with open(os.path.join(arch, "TID-2026-01-01-x_reasoning.md"), "a", encoding="utf-8") as fh:
            fh.write("stale addendum\n")
    if missing:
        os.remove(os.path.join(arch, "TID-2026-01-01-x_reasoning.md"))
    if third_copy:  # a duplicate NOT declared as a sanctioned pair
        with open(os.path.join(inter, "TID-2026-01-01-y_reasoning.md"), "w", encoding="utf-8") as fh:
            fh.write(body)
    m = {"schema_name": "radiation.replica.manifest/1",
         "retrieval_rule": ("Only the active neuron regions (sensoryneurons/ \u00b7 interneurons/ \u00b7 motorneurons/) are ordinary "
                            "working context; the _archive/ replicas are evidence/history and must never be loaded into an "
                            "assistant context alongside their canonical twin."),
         "pairs": [{"canonical_path": "scaffolding/neurons/interneurons/TID-2026-01-01-x_reasoning.md",
                    "replica_path": "scaffolding/neurons/_archive/TID-2026-01-01-x_reasoning.md",
                    "sha256": sha_bytes(body.encode()),
                    "purpose": "intentional historical snapshot",
                    "load_policy": "archive_not_boot_context"}] if declare else []}
    json.dump(m, open(os.path.join(root, "scaffolding", "neurons", "REPLICA_MANIFEST.json"), "w"), indent=1)


def main() -> int:
    vecs: list = []
    tmp = tempfile.mkdtemp(prefix="contract-tests-")

    def vec(name, ok, detail=""):
        vecs.append((name, ok))
        print(f"  {'PASS' if ok else 'FAIL'} {name}" + (f" -> {detail}" if detail and not ok else ""))

    def corpus_case(name, **kw):
        root = os.path.join(tmp, "corpus-" + name.replace(" ", "-"))
        os.makedirs(root)
        mk_corpus(root, **kw)
        bad, declared = V._corpus_contract_violations(root)
        bad = bad + V._brain_vehicle_violations(root, declared)
        return name, bad

    def replica_case(name, dup_check=False, **kw):
        root = os.path.join(tmp, "replica-" + name.replace(" ", "-"))
        os.makedirs(root)
        mk_replica(root, **kw)
        bad, allowed, _rat = V._replica_contract(root)
        if dup_check:
            dbad, _sets = V._dup_scan(root, allowed)
            bad = bad + dbad
        return name, bad

    try:
        n, bad = corpus_case("valid corpus passes")
        vec(n, bad == [], "; ".join(bad)[:90])

        n, bad = corpus_case("undeclared new vehicle fails", extra=True)
        vec(n, any("undeclared course-corpus asset" in b for b in bad), "; ".join(bad)[:90])

        n, bad = corpus_case("digest drift fails", drift=True)
        vec(n, any("digest drift" in b for b in bad), "; ".join(bad)[:90])

        n, bad = corpus_case("missing derivative fails", derivative=True and False)
        vec(n, any("derivative missing" in b for b in bad), "; ".join(bad)[:90])

        n, bad = corpus_case("manifest path escape fails", escape=True)
        vec(n, any("escapes Brain/courses/" in b for b in bad), "; ".join(bad)[:90])

        n, bad = corpus_case("manifest absent fails", declared=False)
        # declared=False keeps the manifest file but empties assets: csv becomes undeclared
        vec(n, any("undeclared course-corpus asset" in b for b in bad), "; ".join(bad)[:90])

        n, bad = replica_case("sanctioned pair passes", dup_check=True)
        vec(n, bad == [], "; ".join(bad)[:90])

        n, bad = replica_case("replica drift fails", drift=True)
        vec(n, any("replica drift" in b for b in bad), "; ".join(bad)[:90])

        n, bad = replica_case("missing twin fails", missing=True)
        vec(n, any("side missing" in b for b in bad), "; ".join(bad)[:90])

        n, bad = replica_case("undeclared third copy fails", dup_check=True, third_copy=True)
        vec(n, any("==" in b for b in bad), "; ".join(bad)[:90])

        n, bad = replica_case("undeclared pair fails as duplicate", declare=False, dup_check=True)
        vec(n, any("==" in b for b in bad), "; ".join(bad)[:90])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    ok = sum(1 for _, p in vecs if p)
    print(f"contract_tests: {ok}/{len(vecs)} vectors")
    print("declared admission is hash-bound; undeclared shapes fail; silence is not kept")
    return 0 if ok == len(vecs) else 1


if __name__ == "__main__":
    sys.exit(main())
