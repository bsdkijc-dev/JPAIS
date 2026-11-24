"""JPAIS Stage 9: AI-Assisted Regulatory Drafting Prototype (PERMA / SEMA).

Enforces statutory hierarchy verification, conflict detection, append-only drafting
history, unsupported-proposition flagging, and mandatory human legal review.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

STATUTORY_HIERARCHY = {
    "UUD 1945": 1,
    "UU": 2,
    "PP": 3,
    "PERPRES": 4,
    "PERMA": 5,
    "SEMA": 6,
    "SK KMA": 7,
}


def detect_conflicts(clauses: List[Dict]) -> List[Dict]:
    """Detect hierarchy conflicts or unsupported propositions in draft clauses."""
    findings = []
    for cl in clauses:
        cid = cl["clause_id"]
        if not cl.get("supporting_doc_ids"):
            findings.append({
                "clause_id": cid,
                "severity": "BLOCKER",
                "issue": "UNSUPPORTED_PROPOSITION: No verified source doc_id attached.",
            })
        if cl.get("overrides_higher_norm"):
            findings.append({
                "clause_id": cid,
                "severity": "CRITICAL_CONFLICT",
                "issue": f"HIERARCHY_CONFLICT: Draft {cl.get('instrument_type', 'PERMA')} cannot override higher statutory norm ({cl['overrides_higher_norm']}).",
            })
    return findings


def create_draft_package(
    draft_title: str,
    instrument_type: str,
    clauses: List[Dict],
    history_path: Path,
) -> Dict:
    if instrument_type not in STATUTORY_HIERARCHY:
        raise ValueError(f"Unknown instrument_type: {instrument_type}")

    conflicts = detect_conflicts(clauses)
    payload = {
        "draft_title": draft_title,
        "instrument_type": instrument_type,
        "hierarchy_rank": STATUTORY_HIERARCHY[instrument_type],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "clauses": clauses,
        "conflict_findings": conflicts,
        "human_review_required": True,
        "approval_status": "PENDING_HUMAN_REVIEW",
    }
    payload["draft_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()

    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
    return payload


if __name__ == "__main__":
    sample_clauses = [
        {
            "clause_id": "Pasal 1",
            "instrument_type": "PERMA",
            "text": "Pengadilan wajib memverifikasi kelayakan prodeo secara elektronik.",
            "rationale": "Memperluas akses keadilan bagi masyarakat tidak mampu.",
            "supporting_doc_ids": ["JPAIS-SYN-2026-000011"],
            "overrides_higher_norm": None,
        },
        {
            "clause_id": "Pasal 2",
            "instrument_type": "PERMA",
            "text": "Data perkara P3-P5 dapat dipublikasikan tanpa anonimisasi.",
            "rationale": "Uji deteksi konflik hierarki dan proposisi tanpa dasar.",
            "supporting_doc_ids": [],
            "overrides_higher_norm": "UU No. 27 Tahun 2022 (UU PDP)",
        },
    ]
    pkg = create_draft_package(
        "Rancangan PERMA Sintetis Akses Keadilan Digital",
        "PERMA",
        sample_clauses,
        Path(__file__).resolve().parent / "drafting_history.jsonl",
    )
    print(f"Stage 9 Draft Created: {len(pkg['conflict_findings'])} conflicts flagged, human_review_required={pkg['human_review_required']}")
