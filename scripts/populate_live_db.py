import time
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Connect to Neo4j
print("Connecting to Neo4j on 127.0.0.1:7687...")
NEO4J_URI = "bolt://127.0.0.1:7687"

# Test standard credentials (new or default)
auth_candidates = [
    ("neo4j", "JpaisLegalGraph2026!"),
    ("neo4j", "neo4j")
]

driver = None
for user, pwd in auth_candidates:
    try:
        d = GraphDatabase.driver(NEO4J_URI, auth=(user, pwd))
        d.verify_connectivity()
        driver = d
        print(f" Connected to Neo4j using credentials '{user}:{pwd}'.")
        break
    except Exception:
        continue

if not driver:
    print("❌ Could not authenticate with standard passwords. Check with: sudo docker logs jpais-neo4j")
    exit(1)

with driver.session() as session:
    # Build Symbolic Ontology & Statutory Framework
    session.run("""
    MERGE (uu37:Regulation {id: "UU_37_2004", name: "UU No. 37 Tahun 2004"})
    MERGE (uu5:Regulation {id: "UU_5_2004", name: "UU No. 5 Tahun 2004"})

    MERGE (art2:Article {id: "UU_37_2004_Art_2_1", number: "Pasal 2 ayat (1)"})
    MERGE (art295:Article {id: "UU_37_2004_Art_295_2_a", number: "Pasal 295 ayat (2) huruf a"})
    MERGE (art30:Article {id: "UU_5_2004_Art_30", number: "Pasal 30 ayat (2) dan (3)"})

    MERGE (uu37)-[:CONTAINS]->(art2)
    MERGE (uu37)-[:CONTAINS]->(art295)
    MERGE (uu5)-[:CONTAINS]->(art30)

    MERGE (c1:LegalConcept {name: "Pembuktian Sederhana", status: "Eksplisit"})
    MERGE (c2:LegalConcept {name: "Novum Menentukan", status: "Eksplisit"})
    MERGE (c3:LegalConcept {name: "Dissenting Opinion", status: "Doktrinal"})

    MERGE (art2)-[:DEFINES]->(c1)
    MERGE (art295)-[:DEFINES]->(c2)
    MERGE (art30)-[:DEFINES]->(c3)

    // Ingest Empirical Decisions from Data Sheets
    MERGE (d1:CourtDecision {caseNumber: "12/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", verdict: "Ditolak", ratioDecidendi: "Gagal buktikan 2 kreditur; force majeure tidak sederhana."})
    MERGE (d1)-[:INTERPRETS]->(art2)
    MERGE (d1)-[:APPLIES]->(c1)

    MERGE (d2:CourtDecision {caseNumber: "28/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", verdict: "Ditolak", ratioDecidendi: "Gagal buktikan keberadaan dua kreditur atau lebih."})
    MERGE (d2)-[:INTERPRETS]->(art2)
    MERGE (d2)-[:APPLIES]->(c1)

    MERGE (d3:CourtDecision {caseNumber: "18/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst", verdict: "Ditolak", ratioDecidendi: "Legal standing kreditur WNA diragukan, tidak sederhana."})
    MERGE (d3)-[:INTERPRETS]->(art2)
    MERGE (d3)-[:APPLIES]->(c1)

    MERGE (d4:CourtDecision {caseNumber: "17 PK/Pdt.Sus-Pailit/2020", verdict: "Ditolak", ratioDecidendi: "Novum tidak memenuhi kualifikasi novum menentukan."})
    MERGE (d4)-[:INTERPRETS]->(art295)
    MERGE (d4)-[:APPLIES]->(c2)

    MERGE (d5:CourtDecision {caseNumber: "420/Pdt.Sus-PKPU/2021/PN.Niaga.Jkt.Pst", verdict: "Homologasi", ratioDecidendi: "Perdamaian disahkan secara sah."})
    """)
    print(" Populated Neo4j Knowledge Graph with legal concepts & court precedents.")
driver.close()

# 2. Connect to Qdrant
print("Connecting to Qdrant on 127.0.0.1:6333...")
qdrant = QdrantClient(host="127.0.0.1", port=6333)
collection_name = "court_decisions"

# Recreate collection with 4-dim normalized test vectors
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
)

cases_payload = [
    {
        "id": 1,
        "vector": [0.8, 0.1, 0.5, 0.1],
        "payload": {
            "case_number": "12/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst",
            "court": "Central Jakarta Commercial Court",
            "verdict": "Ditolak",
            "statutory_basis": "Pasal 2 ayat (1) UU No. 37/2004",
            "ratio_decidendi": "Gagal membuktikan 2 kreditur dan ketiadaan bukti utang asli.",
            "rule_type": "creditor_count"
        }
    },
    {
        "id": 2,
        "vector": [0.85, 0.1, 0.45, 0.1],
        "payload": {
            "case_number": "28/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst",
            "court": "Central Jakarta Commercial Court",
            "verdict": "Ditolak",
            "statutory_basis": "Pasal 2 ayat (1) UU No. 37/2004",
            "ratio_decidendi": "Gagal membuktikan Termohon memiliki dua kreditur atau lebih.",
            "rule_type": "creditor_count"
        }
    },
    {
        "id": 3,
        "vector": [0.3, 0.2, 0.9, 0.1],
        "payload": {
            "case_number": "18/Pdt.Sus-Pailit/2020/PN.Niaga.Jkt.Pst",
            "court": "Central Jakarta Commercial Court",
            "verdict": "Ditolak",
            "statutory_basis": "Pasal 2 ayat (1) & Asas Pembuktian Sederhana",
            "ratio_decidendi": "Legal standing kreditur WNA diragukan sehingga tidak sederhana.",
            "rule_type": "disputed_claims"
        }
    },
    {
        "id": 4,
        "vector": [0.1, 0.9, 0.1, 0.3],
        "payload": {
            "case_number": "17 PK/Pdt.Sus-Pailit/2020",
            "court": "Mahkamah Agung RI (PK)",
            "verdict": "Ditolak",
            "statutory_basis": "Pasal 295 ayat (2) huruf a UU No. 37/2004",
            "ratio_decidendi": "Novum tidak memenuhi kualifikasi novum menentukan.",
            "rule_type": "novum_not_decisive"
        }
    }
]

points = [PointStruct(id=c["id"], vector=c["vector"], payload=c["payload"]) for c in cases_payload]
qdrant.upsert(collection_name=collection_name, points=points)
print(f" Ingested {len(points)} precedent records into Qdrant vector index.")
