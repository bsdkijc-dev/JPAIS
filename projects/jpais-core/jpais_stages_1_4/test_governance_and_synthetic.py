import csv
import json
import unittest
from pathlib import Path
from jpais_governance_gate import (
    ClassificationLevel,
    DatasetZone,
    LegalMetadata,
    compute_sha256,
    enforce_embedding_gate,
)

DIR = Path(__file__).parent


class TestJPAISStages1To4(unittest.TestCase):
    def test_synthetic_corpus_count_and_gate(self):
        cases = json.loads((DIR / "synthetic_cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 10)
        self.assertLessEqual(len(cases), 20)
        for c in cases:
            meta = LegalMetadata(**{k: v for k, v in c.items() if k not in {"summary", "holding"}})
            enforce_embedding_gate(meta)

    def test_kg_relationship_count(self):
        with open(DIR / "synthetic_kg_edges.csv", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 30)
        self.assertLessEqual(len(rows), 50)

    def test_p3_p5_blocked_from_embedding(self):
        for level in (ClassificationLevel.P3, ClassificationLevel.P4, ClassificationLevel.P5):
            meta = LegalMetadata(
                doc_id="JPAIS-DOC-2026-999999",
                title="Restricted Test",
                issuing_institution="Test",
                legal_domain="Criminal law",
                legal_authority="Test",
                document_date="2026-01-01",
                effective_date="2026-01-01",
                source_url="local://restricted/test",
                verification_status="VERIFIED",
                classification_p_level=level,
                dataset_zone=DatasetZone.VERIFIED_PUBLIC,
                sha256_hash=compute_sha256("restricted"),
            )
            with self.assertRaises(PermissionError):
                enforce_embedding_gate(meta)


if __name__ == "__main__":
    unittest.main()
