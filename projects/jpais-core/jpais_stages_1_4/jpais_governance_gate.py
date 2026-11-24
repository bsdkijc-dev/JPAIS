"""JPAIS Stages 1-3: Data Governance Gate, Provenance & Metadata Schema.

Designed to extend ~/JPAIS/projects/jpais-core/rag_pipeline.py without
overwriting existing working configurations. Zero external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import re
from typing import List, Optional


class ClassificationLevel(str, Enum):
    """P1-P5 publication & handling classification per JPAIS Governance Workbook v1.0."""
    P1 = "P1"  # Public: open release & Qdrant embedding permitted
    P2 = "P2"  # Controlled/Transformed: review required before release
    P3 = "P3"  # Restricted: no public release, no external/cloud embedding
    P4 = "P4"  # Confidential/Protected: strict access control, no embedding
    P5 = "P5"  # Prohibited: never ingest, embed, or publish


class DatasetZone(str, Enum):
    SYNTHETIC = "synthetic"
    VERIFIED_PUBLIC = "verified_public"
    RESTRICTED = "restricted"


@dataclass
class LegalMetadata:
    """Extended 15-field metadata & provenance schema for JPAIS Layer 2."""
    doc_id: str
    title: str
    issuing_institution: str
    legal_domain: str
    legal_authority: str
    document_date: str
    effective_date: str
    source_url: str
    verification_status: str  # SYNTHETIC | VERIFIED | UNVERIFIED
    classification_p_level: ClassificationLevel
    dataset_zone: DatasetZone
    sha256_hash: str
    court_satker_id: Optional[str] = None
    jurisdiction: str = "Indonesia"
    article_references: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not re.match(r"^JPAIS-(DOC|SYN)-\d{4}-\d{6}$", self.doc_id):
            raise ValueError(f"Invalid doc_id format: {self.doc_id}")
        if len(self.sha256_hash) != 64:
            raise ValueError("sha256_hash must be 64 hex characters")
        int(self.sha256_hash, 16)
        self.sha256_hash = self.sha256_hash.lower()
        self.classification_p_level = ClassificationLevel(self.classification_p_level)
        self.dataset_zone = DatasetZone(self.dataset_zone)


def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def enforce_embedding_gate(meta: LegalMetadata) -> None:
    """Deterministic gate blocking restricted (P3-P5) or unverified documents from Qdrant."""
    if meta.classification_p_level in {
        ClassificationLevel.P3,
        ClassificationLevel.P4,
        ClassificationLevel.P5,
    }:
        raise PermissionError(
            f"EMBEDDING BLOCKED: {meta.doc_id} has classification {meta.classification_p_level.value} (P3-P5 prohibited)."
        )
    if meta.dataset_zone == DatasetZone.RESTRICTED:
        raise PermissionError(
            f"EMBEDDING BLOCKED: {meta.doc_id} resides in restricted zone."
        )
    if meta.verification_status not in {"SYNTHETIC", "VERIFIED"}:
        raise ValueError(
            f"EMBEDDING BLOCKED: {meta.doc_id} has verification_status={meta.verification_status}."
        )
