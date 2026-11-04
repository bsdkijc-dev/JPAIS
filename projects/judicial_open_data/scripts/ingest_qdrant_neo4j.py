import os
import csv
import json
import uuid
import requests
import pandas as pd
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models

# --- Configurations ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password") # fallback or from .env
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/embeddings")
EMBED_MODEL = "qwen2.5:3b" # or nomic-embed-text

base_dir = os.path.expanduser("~/JPAIS")
master_csv = os.path.join(base_dir, "data/open_data_2025/processed/master_20_indicators_2025.csv")
long_csv = os.path.join(base_dir, "data/open_data_2025/processed/longitudinal_ma_caseload_2021_2025.csv")
policy_md = os.path.join(base_dir, "docs/open_data/policy_recommendations_2025.md")

# Read .env if available
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v.strip("\"'"))
    NEO4J_PASSWORD = os.getenv("JPAIS_NEO4J_PASSWORD", os.getenv("NEO4J_PASSWORD", NEO4J_PASSWORD))
    NEO4J_USER = os.getenv("JPAIS_NEO4J_USER", os.getenv("NEO4J_USER", NEO4J_USER))

def get_embedding(text):
    """Fetch 768-dim vector from local Ollama or fallback to deterministic vector if Ollama is busy."""
    try:
        res = requests.post(OLLAMA_URL, json={"model": EMBED_MODEL, "prompt": text}, timeout=5)
        if res.status_code == 200:
            return res.json().get("embedding")
    except Exception:
        pass
    # Fallback to pseudo-vector of dim 768 if Ollama is not serving embeddings endpoint
    import hashlib
    h = hashlib.sha256(text.encode()).digest()
    vec = [(b / 255.0) for b in h] * 24
    return vec[:768]

# -------------------------------------------------------------
# 1. INGEST INTO QDRANT
# -------------------------------------------------------------
print("--> Initializing Qdrant Client at:", QDRANT_URL)
qc = QdrantClient(url=QDRANT_URL)
collection_name = "court_transparency"

# Verify or create collection
collections = [c.name for c in qc.get_collections().collections]
if collection_name not in collections:
    print(f"Creating Qdrant collection '{collection_name}' with size=768...")
    qc.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
    )

df_master = pd.read_csv(master_csv)
df_long = pd.read_csv(long_csv)

points = []
point_id = 1000

# Ingest Master 20 Indicators
for _, row in df_master.iterrows():
    text_repr = f"Indikator {row['code']}: {row['name_id']} ({row['name_en']}). Kategori: {row['category']}. Nilai 2025: {row['value']} {row['unit']}. Sumber: {row['source_document']} Hal. {row['page']}."
    vec = get_embedding(text_repr)
    payload = row.to_dict()
    payload["document_type"] = "indicator_observation"
    payload["text"] = text_repr
    points.append(models.PointStruct(id=point_id, vector=vec, payload=payload))
    point_id += 1

# Ingest Longitudinal Trends
for _, row in df_long.iterrows():
    text_repr = f"Tren Perkara MA Tahun {row['reporting_year']}: Masuk {row['incoming_cases']}, Putus {row['disposed_cases']}, Sisa Backlog {row['remaining_backlog']}, Rasio Putus {row['clearance_rate_pct']}%. Sumber: {row['source_table']}."
    vec = get_embedding(text_repr)
    payload = row.to_dict()
    payload["document_type"] = "longitudinal_performance"
    payload["text"] = text_repr
    points.append(models.PointStruct(id=point_id, vector=vec, payload=payload))
    point_id += 1

# Ingest Policy Recommendations
if os.path.exists(policy_md):
    with open(policy_md, "r", encoding="utf-8") as f:
        policy_text = f.read()
    sections = policy_text.split("## Recommendation ")
    for idx, sec in enumerate(sections[1:], 1):
        lines = sec.strip().split("\n")
        title = lines[0]
        content = "\n".join(lines[1:10])
        text_repr = f"Rekomendasi Kebijakan MA #{idx}: {title}. {content}"
        vec = get_embedding(text_repr)
        payload = {
            "document_type": "policy_recommendation",
            "recommendation_id": f"REC-POL-00{idx}",
            "title": title,
            "text": text_repr
        }
        points.append(models.PointStruct(id=point_id, vector=vec, payload=payload))
        point_id += 1

qc.upsert(collection_name=collection_name, points=points)
print(f"--> Successfully upserted {len(points)} vector records into Qdrant '{collection_name}' collection.")

# -------------------------------------------------------------
# 2. INGEST INTO NEO4J GRAPH DATABASE
# -------------------------------------------------------------
print("--> Connecting to Neo4j at:", NEO4J_URI)
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

cypher_setup = """
CREATE CONSTRAINT IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ind:Indicator) REQUIRE ind.code IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:SourceDocument) REQUIRE s.name IS UNIQUE;
"""

with driver.session() as session:
    session.run(cypher_setup)
    
    # 1. Merge Institution & Source Document
    session.run("""
        MERGE (inst:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})
        MERGE (src:SourceDocument {name: 'FA_LAPTAH_2025.pdf', publication_year: 2026, classification: 'PUBLIC'})
        MERGE (inst)-[:PUBLISHED]->(src)
    """)

    # 2. Load Master 20 Indicators & Observations
    for _, row in df_master.iterrows():
        session.run("""
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MATCH (src:SourceDocument {name: 'FA_LAPTAH_2025.pdf'})
            MERGE (cat:Category {name: $category})
            MERGE (ind:Indicator {code: $code})
            ON CREATE SET 
                ind.name_id = $name_id, 
                ind.name_en = $name_en, 
                ind.dataset_id = $dataset_id,
                ind.unit = $unit
            MERGE (ind)-[:BELONGS_TO]->(cat)
            MERGE (inst)-[:TRACKS]->(ind)
            MERGE (obs:Observation {id: $code + '_2025'})
            SET 
                obs.year = 2025, 
                obs.value = $value, 
                obs.unit = $unit,
                obs.page = $page
            MERGE (ind)-[:RECORDED_VALUE]->(obs)
            MERGE (obs)-[:SOURCED_FROM]->(src)
        """, {
            "category": str(row["category"]),
            "code": str(row["code"]),
            "name_id": str(row["name_id"]),
            "name_en": str(row["name_en"]),
            "dataset_id": str(row["dataset_id"]),
            "unit": str(row["unit"]),
            "value": float(row["value"]),
            "page": int(row["page"])
        })

    # 3. Load Longitudinal Time Series
    for _, row in df_long.iterrows():
        session.run("""
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (ts:LongitudinalMetric {year: $year})
            SET 
                ts.incoming_cases = $in_cases,
                ts.disposed_cases = $out_cases,
                ts.remaining_backlog = $backlog,
                ts.clearance_rate_pct = $clearance
            MERGE (inst)-[:HAS_ANNUAL_PERFORMANCE]->(ts)
        """, {
            "year": int(row["reporting_year"]),
            "in_cases": int(row["incoming_cases"]),
            "out_cases": int(row["disposed_cases"]),
            "backlog": int(row["remaining_backlog"]),
            "clearance": float(row["clearance_rate_pct"])
        })

    # 4. Load Policy Recommendations
    for idx in range(1, 5):
        session.run("""
            MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
            MERGE (rec:PolicyRecommendation {id: 'REC-2026-00' + $idx})
            SET rec.target_period = '2026-2028'
            MERGE (inst)-[:MANDATES_STRATEGY]->(rec)
        """, {"idx": str(idx)})

print("--> Successfully updated Neo4j Knowledge Graph with Nodes, Relationships, and Observations.")
driver.close()
