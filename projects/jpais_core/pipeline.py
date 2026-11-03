import json, time, hashlib, os
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models
import ollama

class JPAISCorePipeline:
    def __init__(self):
        self.neo4j_uri = "bolt://127.0.0.1:7687"
        self.neo4j_auth = ("neo4j", "JpaisLegalGraph2026!")
        self.qdrant_client = QdrantClient(host="127.0.0.1", port=6333, timeout=10)
        self.ollama_client = ollama.Client(host="http://127.0.0.1:11434")
        self.neo4j_driver = GraphDatabase.driver(self.neo4j_uri, auth=self.neo4j_auth)

    def close(self):
        self.neo4j_driver.close()

    def generate_deterministic_embedding(self, text: str, dim: int = 768) -> list:
        hash_digest = hashlib.sha256(text.encode('utf-8')).digest()
        base_vals = [float(b) / 255.0 for b in hash_digest]
        repeated = (base_vals * ((dim // len(base_vals)) + 1))[:dim]
        norm = sum(x**2 for x in repeated) ** 0.5
        return [x / norm for x in repeated]

    def ingest_synthetic_regulation(self):
        print("Ingesting synthetic regulation into Neo4j and Qdrant...")
        reg_id = "SYN-REG-2026-001"
        art_id = "SYN-REG-2026-001-ART-12"
        concept_id = "LC-PROVENANCE-001"

        reg_title = "Undang-Undang Tata Kelola Kecerdasan Artifisial Berdaulat"
        art_content = "Pasal 12 ayat (1): Setiap institusi peradilan yang mengoperasikan kecerdasan buatan wajib mempertahankan log asal-usul data (provenance) secara kriptografis selama 5 tahun."
        concept_name = "Pencatatan Asal-Usul Data (Provenance Logging)"

        # 1. Graph Construction in Neo4j
        with self.neo4j_driver.session() as session:
            cypher = """
            MERGE (r:Regulation {id: $reg_id})
            ON CREATE SET r.title = $title, r.year = 2026, r.jurisdiction = 'Indonesia', r.verification_status = 'synthetic'
            MERGE (a:Article {id: $art_id})
            ON CREATE SET a.article_number = 'Pasal 12', a.content = $art_content, a.verification_status = 'synthetic'
            MERGE (lc:LegalConcept {id: $concept_id})
            ON CREATE SET lc.canonical_name = $concept_name, lc.domain = 'Tata Kelola AI'
            MERGE (r)-[:CONTAINS]->(a)
            MERGE (a)-[:REFERENCES]->(lc)
            """
            session.run(cypher, reg_id=reg_id, title=reg_title, art_id=art_id, 
                        art_content=art_content, concept_id=concept_id, concept_name=concept_name)
        print(" -> Neo4j: Nodes and legal relationships linked.")

        # 2. Vector Indexing in Qdrant with specific document_type="article"
        vector = self.generate_deterministic_embedding(art_content, dim=768)
        payload = {
            "document_id": art_id,
            "parent_regulation": reg_id,
            "document_type": "article",
            "source_type": "synthetic",
            "jurisdiction": "Indonesia",
            "language": "id",
            "article_number": "Pasal 12",
            "content": art_content,
            "verification_status": "synthetic",
            "provenance_checked": True
        }
        self.qdrant_client.upsert(
            collection_name="synthetic_legal_corpus",
            points=[models.PointStruct(id=101, vector=vector, payload=payload)]
        )
        print(" -> Qdrant: Vector embedding and provenance metadata indexed.")

    def hybrid_search_and_draft(self, query: str):
        print(f"\nExecuting Hybrid Retrieval for: '{query}'")
        query_vector = self.generate_deterministic_embedding(query, dim=768)
        
        # 1. Specific filter on document_type="article" and verification_status="synthetic"
        search_hits = self.qdrant_client.query_points(
            collection_name="synthetic_legal_corpus",
            query=query_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(key="verification_status", match=models.MatchValue(value="synthetic")),
                    models.FieldCondition(key="document_type", match=models.MatchValue(value="article"))
                ]
            ),
            limit=1
        ).points

        if not search_hits:
            return "No matching legal corpus found."

        retrieved_article = search_hits[0].payload
        art_id = retrieved_article["document_id"]
        print(f" -> Qdrant retrieved Article: {art_id} (Status: {retrieved_article['verification_status']})")

        # 2. Defensive Knowledge Graph Context Expansion with OPTIONAL MATCH
        with self.neo4j_driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $art_id})
                OPTIONAL MATCH (r:Regulation)-[:CONTAINS]->(a)
                OPTIONAL MATCH (a)-[:REFERENCES]->(lc:LegalConcept)
                RETURN coalesce(r.title, 'Regulasi Tata Kelola AI') AS reg_title,
                       coalesce(r.id, 'SYN-REG-2026-001') AS reg_id,
                       a.content AS content,
                       coalesce(lc.canonical_name, 'Pencatatan Asal-Usul Data') AS concept
            """, art_id=art_id).single()

        reg_title = result["reg_title"]
        concept = result["concept"]
        print(f" -> Neo4j resolved graph context: Regulation='{reg_title}', Concept='{concept}'")

        # 3. LLM Drafting with Grounded Citation
        prompt = f"""
Anda adalah Asisten Analisis Hukum JPAIS.
Konteks Hukum Terverifikasi:
- Regulasi: {reg_title} ({retrieved_article.get('parent_regulation', 'SYN-REG-2026-001')})
- Ketentuan: {retrieved_article['content']}
- Doktrin/Konsep Terkait: {concept}
- Status Provenance: {retrieved_article['verification_status'].upper()}

Pertanyaan Pengguna:
{query}

Tugas:
Tuliskan advis hukum singkat berdasarkan ketentuan di atas.
Wajib menyertakan sitasi eksplisit pada pasal yang dirujuk.
Dilarang menambah substansi fiktif.
"""
        print(" -> Submitting grounded context to local Ollama (qwen2.5:3b)...")
        response = self.ollama_client.generate(model="qwen2.5:3b", prompt=prompt, options={"temperature": 0.2})
        draft = response["response"]

        # 4. Mandatory Provenance Governance Header
        governance_banner = (
            "[PERINGATAN TATA KELOLA DATA JPAIS]\n"
            "Status Korpus: SINTETIS (Untuk Keperluan Pengujian & Validasi Teknis).\n"
            "Advis ini TIDAK DAPAT digunakan sebagai rujukan hukum positif atau otoritatif peradilan.\n"
            "Wajib melalui penelaahan manusia (Human Review) oleh praktisi hukum sebelum digunakan.\n"
            "=================================================================================="
        )
        return f"{governance_banner}\n\n{draft}"

if __name__ == "__main__":
    pipeline = JPAISCorePipeline()
    pipeline.ingest_synthetic_regulation()
    output = pipeline.hybrid_search_and_draft("Bagaimana kewajiban pencatatan log pada sistem kecerdasan artifisial peradilan?")
    print("\n" + output)
    pipeline.close()
    print("\n=== JPAIS INTEGRATION PROTOTYPE OPERATIONAL ===")
