"""JPAIS Stages 5-6: Ingest 15 synthetic cases & 42 KG edges into local Dell Neo4j & Qdrant.

Skips GEEKOM A8 by targeting 127.0.0.1:6333 (Qdrant), 127.0.0.1:7687 (Neo4j),
and 127.0.0.1:11434 (Ollama bge-m3). Falls back cleanly to local JSON index if
Docker services are not running.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "jpais_stages_1_4" if (HERE.parent / "jpais_stages_1_4").exists() else HERE
sys.path.insert(0, str(DATA_DIR))

from jpais_governance_gate import LegalMetadata, enforce_embedding_gate  # noqa: E402

OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embed")
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "jpais_local_dev_2026")
COLLECTION = "jpais_synthetic_cases"


def load_corpus() -> tuple[list[dict], list[dict]]:
    cases = json.loads((DATA_DIR / "synthetic_cases.json").read_text(encoding="utf-8"))
    for c in cases:
        meta = LegalMetadata(**{k: v for k, v in c.items() if k not in {"summary", "holding"}})
        enforce_embedding_gate(meta)
    with open(DATA_DIR / "synthetic_kg_edges.csv", encoding="utf-8") as f:
        edges = list(csv.DictReader(f))
    return cases, edges


def embed_text_ollama(text: str) -> list[float]:
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=json.dumps({"model": "bge-m3", "input": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["embeddings"][0]


def ingest_qdrant(cases: list[dict]) -> int:
    # Create collection (idempotent)
    req_col = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}",
        data=json.dumps({"vectors": {"size": 1024, "distance": "Cosine"}}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    try:
        urllib.request.urlopen(req_col, timeout=10).read()
    except Exception:
        pass

    points = []
    for idx, c in enumerate(cases, start=1):
        text = f"{c['title']}. {c['legal_domain']}. {c['summary']} {c['holding']} {' '.join(c['article_references'])}"
        vec = embed_text_ollama(text)
        points.append({"id": idx, "vector": vec, "payload": c})

    req_up = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points?wait=true",
        data=json.dumps({"points": points}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    with urllib.request.urlopen(req_up, timeout=30) as resp:
        res = json.loads(resp.read())
        if res.get("status") != "ok":
            raise RuntimeError(f"Qdrant upsert failed: {res}")
    return len(points)


def ingest_neo4j(cases: list[dict], edges: list[dict]) -> tuple[int, int]:
    from neo4j import GraphDatabase  # type: ignore

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        for c in cases:
            session.run(
                """
                MERGE (n:Case {id: $doc_id})
                SET n.title = $title,
                    n.domain = $legal_domain,
                    n.authority = $legal_authority,
                    n.date = $document_date,
                    n.institution = $issuing_institution,
                    n.satker_id = $court_satker_id,
                    n.p_level = $classification_p_level,
                    n.provenance = 'SYNTHETIC'
                """,
                **c,
            )
        for e in edges:
            rel = e["rel_type"]
            src_lbl = e["src_type"]
            dst_lbl = e["dst_type"]
            session.run(
                f"""
                MERGE (a:{src_lbl} {{id: $src_id}})
                MERGE (b:{dst_lbl} {{id: $dst_id}})
                MERGE (a)-[r:{rel} {{provenance: $provenance}}]->(b)
                """,
                src_id=e["src_id"],
                dst_id=e["dst_id"],
                provenance=e["provenance"],
            )
    driver.close()
    return len(cases), len(edges)


def main() -> None:
    cases, edges = load_corpus()
    print(f"Governance gate verified: {len(cases)} synthetic cases, {len(edges)} KG edges.")
    try:
        n_vec = ingest_qdrant(cases)
        print(f"Qdrant ingested {n_vec} bge-m3 vectors into '{COLLECTION}'.")
    except Exception as exc:
        print(f"Qdrant/Ollama skipped ({exc}); JDSS will use local keyword+graph fallback.")
    try:
        n_nodes, n_edges = ingest_neo4j(cases, edges)
        print(f"Neo4j ingested {n_nodes} Case nodes and {n_edges} relationships.")
    except Exception as exc:
        print(f"Neo4j skipped ({exc}); JDSS will use local CSV graph fallback.")


if __name__ == "__main__":
    main()
