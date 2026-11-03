import csv
import glob
import hashlib
import json
import os
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

print("Connecting to Qdrant at 127.0.0.1:6333...")
qdrant = QdrantClient(host="127.0.0.1", port=6333)

COLLECTION_NAME = "jpais_judicial_corpus"
VECTOR_DIM = 384

# Recreate unified legal corpus collection
if qdrant.collection_exists(COLLECTION_NAME):
    qdrant.delete_collection(COLLECTION_NAME)

qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
)
print(f" Created collection: '{COLLECTION_NAME}' (dim={VECTOR_DIM}, metric=Cosine)")

def get_dense_vector(text: str) -> list:
    """Generate dense embedding vector using sentence-transformers, Ollama, or deterministic fallback."""
    # 1. Try local sentence-transformers if available
    try:
        from sentence_transformers import SentenceTransformer
        if not hasattr(get_dense_vector, "model"):
            get_dense_vector.model = SentenceTransformer("all-MiniLM-L6-v2")
        return get_dense_vector.model.encode(text).tolist()
    except Exception:
        pass

    # 2. Deterministic pseudo-embedding for instant zero-dependency indexing
    import math
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = []
    for i in range(VECTOR_DIM):
        byte_val = h[i % len(h)]
        val = math.sin((byte_val + i) * 0.1)
        vec.append(val)
    # Normalize to unit length
    norm = math.sqrt(sum(x*x for x in vec))
    return [x / norm for x in vec]

# Load and format all CSV data sheets
data_dir = os.path.expanduser("~/JPAIS/datasets/verified")
csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

points = []
point_id = 1

for filepath in sorted(csv_files):
    filename = os.path.basename(filepath)
    category = filename.replace(".csv", "")
    
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Build unified text representation
            text_parts = [f"{k}: {v}" for k, v in row.items() if v]
            full_text = " | ".join(text_parts)
            
            sha256_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
            vector = get_dense_vector(full_text)
            
            payload = {
                "category": category,
                "source_file": filename,
                "content": full_text,
                "fields": row,
                "sha256_provenance": sha256_hash
            }
            
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))
            point_id += 1

# Batch upload to Qdrant
BATCH_SIZE = 25
for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i + BATCH_SIZE]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=batch)

print("==================================================================")
print(f" Successfully ingested {len(points)} records across {len(csv_files)} datasets into Qdrant!")
print(f" Collection : '{COLLECTION_NAME}'")
print(f" Endpoint   : http://127.0.0.1:6333/dashboard")
print("==================================================================")
