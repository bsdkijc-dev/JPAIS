"""JPAIS Stage 11: Controlled Expansion to Approved Public Legal Sources.

Ingests ONLY manually exported or approved P1/P2 VERIFIED public sources
(e.g. PERMA/SEMA metadata, Master Court Registry satkers) into a dedicated
Qdrant collection ('jpais_public_verified') and Neo4j ('VERIFIED_PUBLIC'),
strictly separated from synthetic and restricted datasets.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE_DIR = HERE.parent / "jpais_stages_1_4" if (HERE.parent / "jpais_stages_1_4").exists() else HERE
sys.path.insert(0, str(GATE_DIR))

from jpais_governance_gate import (  # noqa: E402
    ClassificationLevel,
    DatasetZone,
    LegalMetadata,
    compute_sha256,
    enforce_embedding_gate,
)

OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embed")
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
PUBLIC_COLLECTION = "jpais_public_verified"

PII_PATTERNS = [
    re.compile(r"\b\d{16}\b"),  # Indonesian NIK (16 digits)
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # Email
]


def check_no_pii(text: str, doc_id: str) -> None:
    for pat in PII_PATTERNS:
        if pat.search(text):
            raise ValueError(f"PII_GUARD_BLOCKED: Potential PII detected in {doc_id}; anonymize before ingestion.")


def validate_public_record(record: dict, seen_hashes: set[str]) -> LegalMetadata:
    """Validate provenance, P1/P2 classification, PII absence, and deduplication."""
    if record.get("verification_status") != "VERIFIED":
        raise ValueError(f"UNVERIFIED_SOURCE_BLOCKED: {record.get('doc_id')} must be VERIFIED.")
    if record.get("dataset_zone") != DatasetZone.VERIFIED_PUBLIC.value:
        raise ValueError(f"ZONE_MISMATCH: {record.get('doc_id')} must use dataset_zone='verified_public'.")

    text_body = record.get("text", "")
    check_no_pii(text_body, record["doc_id"])

    sha = record.get("sha256_hash") or compute_sha256(text_body)
    if sha in seen_hashes:
        raise ValueError(f"DUPLICATE_DETECTED: {record['doc_id']} matches existing SHA-256 {sha[:12]}.")

    meta = LegalMetadata(
        doc_id=record["doc_id"],
        title=record["title"],
        issuing_institution=record["issuing_institution"],
        court_satker_id=record.get("court_satker_id"),
        legal_domain=record["legal_domain"],
        legal_authority=record["legal_authority"],
        document_date=record["document_date"],
        effective_date=record["effective_date"],
        jurisdiction=record.get("jurisdiction", "Indonesia"),
        article_references=record.get("article_references", []),
        source_url=record["source_url"],
        verification_status=record["verification_status"],
        classification_p_level=ClassificationLevel(record["classification_p_level"]),
        dataset_zone=DatasetZone(record["dataset_zone"]),
        sha256_hash=sha,
    )
    enforce_embedding_gate(meta)
    seen_hashes.add(sha)
    return meta


def ingest_approved_manifest(manifest_path: Path, dry_run: bool = True) -> dict:
    records = json.loads(manifest_path.read_text(encoding="utf-8"))
    seen_hashes: set[str] = set()
    accepted, rejected = [], []
    for rec in records:
        try:
            meta = validate_public_record(rec, seen_hashes)
            accepted.append(meta.doc_id)
        except Exception as exc:
            rejected.append({"doc_id": rec.get("doc_id"), "reason": str(exc)})
    return {"accepted": accepted, "rejected": rejected, "dry_run": dry_run}
