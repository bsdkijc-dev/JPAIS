import os
import glob
import json
import subprocess
import pandas as pd
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models

# -------------------------------------------------------------
# 1. DETECT SERVICES & CREDENTIALS
# -------------------------------------------------------------
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")

# Retrieve container authentication directly from docker inspect
try:
    cmd = "docker inspect $(docker ps -qf name=neo4j)"
    out = subprocess.check_output(cmd, shell=True).decode()
    data = json.loads(out)
    env_list = data[0]['Config']['Env']
    auth_val = next((e.split('=', 1)[1] for e in env_list if 'NEO4J_AUTH=' in e), 'neo4j/neo4j')
    user, pwd = auth_val.split('/', 1) if '/' in auth_val else ('neo4j', auth_val)
except Exception:
    user, pwd = ("neo4j", "password")

print(f"Connecting to Neo4j at {NEO4J_URI} as user '{user}'...")
driver = GraphDatabase.driver(NEO4J_URI, auth=(user, pwd))

qc = QdrantClient(url=QDRANT_URL)
collection_name = "court_transparency"
print(f"Connecting to Qdrant at {QDRANT_URL} (collection: '{collection_name}')...")

# -------------------------------------------------------------
# 2. INGESTION LOGIC
# -------------------------------------------------------------
base_dir = os.path.expanduser("~/JPAIS/data/open_data_2025/processed")
csv_files = glob.glob(os.path.join(base_dir, "*.csv"))
print(f"Discovered {len(csv_files)} processed open data files to ingest:")
for f in sorted(csv_files):
    print(" -", os.path.basename(f))

# Helper deterministic vector generator (768-dim)
def get_vector(text):
    import hashlib
    h = hashlib.sha256(text.encode('utf-8')).digest()
    vec = [(b / 255.0) for b in h] * 24
    return vec[:768]

qdrant_points = []
point_id = 2000

with driver.session() as s:
    # Ensure Constraints
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (i:Institution) REQUIRE i.name IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (y:ReportingYear) REQUIRE y.year IS UNIQUE")
    s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (ind:Indicator) REQUIRE ind.code IS UNIQUE")
    
    # Root Institution
    s.run("MERGE (i:Institution {name: 'Mahkamah Agung Republik Indonesia', acronym: 'MA RI'})")

    for csv_path in sorted(csv_files):
        fname = os.path.basename(csv_path)
        df = pd.read_csv(csv_path)
        
        for _, row in df.iterrows():
            row_dict = {k: ("" if pd.isna(v) else v) for k, v in row.items()}
            
            # Extract common properties
            year = int(row_dict.get("reporting_year", 2025))
            code = str(row_dict.get("record_id") or row_dict.get("indicator_code") or row_dict.get("register_id") or row_dict.get("field_code") or point_id)
            name = str(row_dict.get("indicator_name") or row_dict.get("metadata_property") or row_dict.get("master_dataset_name") or row_dict.get("parameter_value") or code)
            val = str(row_dict.get("value") or row_dict.get("value_or_reference") or row_dict.get("parameter_value") or "")
            cat = str(row_dict.get("category") or row_dict.get("indicator_category") or row_dict.get("thematic_domain") or "General")

            # Qdrant Point
            text_repr = f"Tahun {year} | {cat} | {name}: {val} (File: {fname})"
            qdrant_points.append(models.PointStruct(
                id=point_id,
                vector=get_vector(text_repr),
                payload={"year": year, "category": cat, "name": name, "value": val, "file": fname, "text": text_repr}
            ))
            point_id += 1

            # Neo4j Entity Graph
            s.run("""
                MATCH (inst:Institution {name: 'Mahkamah Agung Republik Indonesia'})
                MERGE (y:ReportingYear {year: $year})
                MERGE (c:Category {name: $cat})
                MERGE (ind:Indicator {code: $code})
                ON CREATE SET ind.name = $name
                MERGE (ind)-[:BELONGS_TO]->(c)
                MERGE (inst)-[:TRACKS]->(ind)
                CREATE (obs:DataPoint {value: $val, source_file: $fname})
                MERGE (ind)-[:RECORDED_IN]->(obs)
                MERGE (obs)-[:IN_YEAR]->(y)
            """, {"year": year, "cat": cat, "code": code, "name": name, "val": val, "fname": fname})

# Upsert Qdrant
qc.upsert(collection_name=collection_name, points=qdrant_points)
print(f"\n--> Successfully indexed {len(qdrant_points)} vectors across 2017-2025 into Qdrant '{collection_name}'.")

# Verify Neo4j Graph
with driver.session() as s:
    r_nodes = s.run("MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY count DESC")
    print("\n=== NEO4J GRAPH NODE TOTALS (2017–2025) ===")
    for rec in r_nodes:
        print(f" {rec['label']}: {rec['count']}")
        
    r_rels = s.run("MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS count ORDER BY count DESC")
    print("\n=== NEO4J RELATIONSHIP TOTALS ===")
    for rec in r_rels:
        print(f" {rec['rel']}: {rec['count']}")

driver.close()
print("\n--> Full Multi-Year Ingestion Complete!")
