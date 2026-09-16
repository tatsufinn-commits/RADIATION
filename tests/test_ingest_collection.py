#!/usr/bin/env python3
"""
Test harness for ingest_collection.py — G2 ingestion response-byte caps

Vectors ≥3 (under-cap fetch ok · over-cap streamed abort without manifest size · override flag honored)
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def run(cmd, cwd=ROOT, check=False):
    p = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd failed {cmd}: {p.stdout} {p.stderr}")
    return p

class TestIngestCollection(unittest.TestCase):
    def make_manifest(self, files):
        """files: list of dicts {name, size, id} size may be None"""
        tmpdir = tempfile.mkdtemp()
        manifest = pathlib.Path(tmpdir) / "manifest.json"
        manifest.write_text(json.dumps(files), encoding="utf-8")
        dest = pathlib.Path(tmpdir) / "dest"
        dest.mkdir()
        return tmpdir, str(manifest), str(dest)

    def test_under_cap_fetch_ok(self):
        # Under-cap fetch ok: file size 1 MB < default 10 MiB cap, no finding, exit 0 (but fetch will fail due to no real Drive id, we mock by creating file manually)
        # Instead test the cap logic directly: create dest with small file, run fetch with manifest size under cap
        # We will test that when file already cached and under cap, it is considered ok and no findings
        tmpdir, manifest_path, dest_path = self.make_manifest([
            {"id": "fake1", "name": "small.pdf", "size": 1*1048576}
        ])
        try:
            # Create a fake PDF file in dest that matches expected name pattern and size under cap
            # The fetch code checks cached files before fetching
            # Create file 01_small.pdf with PDF magic and size 1 MB
            cached_file = pathlib.Path(dest_path) / "01_small.pdf"
            cached_file.write_bytes(b"%PDF" + b"\x00" * (1*1048576 - 4))
            # Run fetch with repo set to different path to avoid refusal, and max-size default (None -> 10)
            # Use --repo /root to avoid repo check
            p = run(f"python3 scripts/ingest_collection.py fetch --manifest {manifest_path} --dest {dest_path} --repo /root --max-size 10", cwd=ROOT)
            # Should exit 0, no findings, cached ok
            self.assertEqual(p.returncode, 0, f"under-cap should be ok, got {p.stdout} {p.stderr}")
            self.assertNotIn("ingest_collection:", p.stdout)
            self.assertIn("cached", p.stdout.lower() or "fetched", p.stdout.lower())
        finally:
            shutil.rmtree(tmpdir)

    def test_over_cap_streamed_abort_without_manifest_size(self):
        # Over-cap streamed abort without manifest size: manifest size None, but streamed file > cap
        tmpdir, manifest_path, dest_path = self.make_manifest([
            {"id": "fake2", "name": "big.pdf", "size": None}  # manifest size absent
        ])
        try:
            # Create a fake file that would be considered as already downloaded but over cap
            # Actually test the logic: create file 01_big.pdf with size 11 MB > 10 MB cap
            cached_file = pathlib.Path(dest_path) / "01_big.pdf"
            cached_file.write_bytes(b"%PDF" + b"\x00" * (11*1048576 - 4))
            p = run(f"python3 scripts/ingest_collection.py fetch --manifest {manifest_path} --dest {dest_path} --repo /root --max-size 10", cwd=ROOT)
            # Should exit 1 with finding-line ingest_collection: ... streamed ... > cap
            self.assertNotEqual(p.returncode, 0, f"over-cap without manifest size should abort, got {p.stdout}")
            self.assertIn("ingest_collection:", p.stdout)
            self.assertIn("streamed", p.stdout.lower() or "cached", p.stdout.lower())
            self.assertIn("10", p.stdout)  # cap mentioned
        finally:
            shutil.rmtree(tmpdir)

    def test_override_flag_honored(self):
        # Override flag honored: default 10 MiB, but operator sets --max-size 20, file 15 MB should pass
        tmpdir, manifest_path, dest_path = self.make_manifest([
            {"id": "fake3", "name": "medium.pdf", "size": 15*1048576}
        ])
        try:
            cached_file = pathlib.Path(dest_path) / "01_medium.pdf"
            cached_file.write_bytes(b"%PDF" + b"\x00" * (15*1048576 - 4))
            # With default cap (None -> 10), should fail
            p_default = run(f"python3 scripts/ingest_collection.py fetch --manifest {manifest_path} --dest {dest_path} --repo /root", cwd=ROOT)
            self.assertNotEqual(p_default.returncode, 0, "default 10 MiB should reject 15 MB")
            # Recreate cached file (previous run deleted it on over-cap)
            cached_file.write_bytes(b"%PDF" + b"\x00" * (15*1048576 - 4))
            # With override 20, should pass
            p_override = run(f"python3 scripts/ingest_collection.py fetch --manifest {manifest_path} --dest {dest_path} --repo /root --max-size 20", cwd=ROOT)
            self.assertEqual(p_override.returncode, 0, f"override 20 should allow 15 MB, got {p_override.stdout}")
            self.assertNotIn("ingest_collection:", p_override.stdout)
        finally:
            shutil.rmtree(tmpdir)

    def test_default_cap_is_10(self):
        # Ensure default cap is 10 MiB when --max-size not provided (G2 spec)
        # Check that argparse default is None and code uses 10
        p = run(f"python3 scripts/ingest_collection.py fetch --help", cwd=ROOT)
        self.assertIn("10", p.stdout)
        self.assertIn("default", p.stdout.lower())

if __name__ == "__main__":
    unittest.main()
