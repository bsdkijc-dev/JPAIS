import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE_DIR = HERE.parent / "jpais_stages_1_4"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(GATE_DIR))

import stage11_public_ingest


class TestJPAISStage11(unittest.TestCase):
    def test_approved_public_manifest(self):
        res = stage11_public_ingest.ingest_approved_manifest(
            HERE / "approved_public_manifest_sample.json", dry_run=True
        )
        self.assertEqual(res["accepted"], ["JPAIS-DOC-2026-000101"])
        self.assertEqual(res["rejected"], [])

    def test_blocks_unverified_p3_and_pii(self):
        seen = set()
        bad_unverified = {
            "doc_id": "JPAIS-DOC-2026-000102", "title": "T", "issuing_institution": "MA",
            "legal_domain": "Civil law", "legal_authority": "PERMA", "document_date": "2026-01-01",
            "effective_date": "2026-01-01", "source_url": "https://example.org",
            "verification_status": "UNVERIFIED", "classification_p_level": "P1",
            "dataset_zone": "verified_public", "text": "Clean text"
        }
        with self.assertRaises(ValueError):
            stage11_public_ingest.validate_public_record(bad_unverified, seen)

        bad_pii = dict(bad_unverified, doc_id="JPAIS-DOC-2026-000103", verification_status="VERIFIED", text="NIK 3171012345678901")
        with self.assertRaises(ValueError):
            stage11_public_ingest.validate_public_record(bad_pii, seen)


if __name__ == "__main__":
    unittest.main()
