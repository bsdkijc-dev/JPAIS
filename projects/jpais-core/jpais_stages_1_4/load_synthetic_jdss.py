"""Load 15 synthetic cases and 42 KG edges into GEEKOM Neo4j & Qdrant via jpais-tunnel.

Prerequisites on Dell Precision 7540:
  ssh -fN jpais-tunnel
  source ~/JPAIS/venv/bin/activate
"""

import csv
import json
import os
import urllib.request
from pathlib import Path
from jpais_governance_gate import LegalMetadata, enforce_embedding_gate

DATA_DIR = Path(__file__).parent
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/embed")
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:16333")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:17687")


def get_bge_m3_embedding(text: str) -> list[float]:
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps({"model": "bge-m3", "input": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["embeddings"][0]


def validate_all_cases() -> list[dict]:
    cases = json.loads((DATA_DIR / "synthetic_cases.json").read_text(encoding="utf-8"))
    for c in cases:
        meta = LegalMetadata(**{k: v for k, v in c.items() if k not in {"summary", "holding"}})
        enforce_embedding_gate(meta)
    return cases


if __name__ == "__main__":
    validated = validate_all_cases()
    print(f"Governance gate passed for {len(validated)} synthetic cases.")
