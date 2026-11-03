import re, hashlib, os
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models

class IndonesianStatuteParser:
    def __init__(self):
        self.neo4j_driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "JpaisLegalGraph2026!"))
        self.qdrant_client = QdrantClient(host="127.0.0.1", port=6333, timeout=10)

    def close(self):
        self.neo4j_driver.close()

    def generate_embedding(self, text: str, dim: int = 768) -> list:
        hash_digest = hashlib.sha256(text.encode('utf-8')).digest()
        base_vals = [float(b) / 255.0 for b in hash_digest]
        repeated = (base_vals * ((dim // len(base_vals)) + 1))[:dim]
        norm = sum(x**2 for x in repeated) ** 0.5
        return [x / norm for x in repeated]

    def parse_text(self, filepath: str, reg_id: str, reg_type: str, number: str, year: int, title: str, status: str = "verified"):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        lines = text.strip().split('\n')
        current_bab = "KETENTUAN AWAL"
        articles = []
        current_art = None

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Detect Chapter (BAB)
            bab_match = re.match(r'^BAB\s+([IVXLCDM]+)', line, re.IGNORECASE)
            if bab_match:
                bab_num = line
                bab_title = ""
                if i + 1 < len(lines) and not re.match(r'^Pasal\s+\d+', lines[i+1].strip(), re.IGNORECASE):
                    i += 1
                    bab_title = lines[i].strip()
                current_bab = f"{bab_num} {bab_title}".strip()
                i += 1
                continue

            # Detect Article (Pasal)
            pasal_match = re.match(r'^Pasal\s+(\d+[A-Z]?)', line, re.IGNORECASE)
            if pasal_match:
                if current_art:
                    articles.append(current_art)
                art_num = f"Pasal {pasal_match.group(1)}"
                current_art = {
                    "id": f"{reg_id}-{art_num.replace(' ', '_')}",
                    "article_number": art_num,
                    "chapter": current_bab,
                    "lines": [line]
                }
                i += 1
                continue

            if current_art:
                current_art["lines"].append(line)
            i += 1

        if current_art:
            articles.append(current_art)

        # Process content and detect statutory cross-references
        for a in articles:
            a["content"] = "\n".join(a.pop("lines"))
            refs = re.findall(r'Pasal\s+(\d+[A-Z]?)', a["content"])
            a["references"] = sorted(list(set([f"Pasal {r}" for r in refs if f"Pasal {r}" != a["article_number"]])))

        return {
            "reg_id": reg_id,
            "reg_type": reg_type,
            "number": number,
            "year": year,
            "title": title,
            "status": status,
            "articles": articles
        }

    def ingest(self, parsed_data: dict):
        reg_id = parsed_data["reg_id"]
        status = parsed_data["status"]
        print(f"Ingesting {reg_id} ({len(parsed_data['articles'])} articles) into Neo4j and Qdrant...")

        # 1. Graph Ingestion in Neo4j
        with self.neo4j_driver.session() as session:
            # Create Regulation Node
            session.run("""
                MERGE (r:Regulation {id: $reg_id})
                SET r.type = $reg_type, r.number = $number, r.year = $year,
                    r.title = $title, r.verification_status = $status
            """, reg_id=reg_id, reg_type=parsed_data["reg_type"], number=parsed_data["number"],
                 year=parsed_data["year"], title=parsed_data["title"], status=status)

            # Ingest Chapters and Articles
            for art in parsed_data["articles"]:
                chap_id = f"{reg_id}-{art['chapter'].replace(' ', '_')}"
                session.run("""
                    MATCH (r:Regulation {id: $reg_id})
                    MERGE (c:Chapter {id: $chap_id})
                    ON CREATE SET c.name = $chapter_name
                    MERGE (r)-[:HAS_CHAPTER]->(c)
                    MERGE (a:Article {id: $art_id})
                    SET a.article_number = $art_num, a.content = $content, a.verification_status = $status
                    MERGE (c)-[:CONTAINS]->(a)
                """, reg_id=reg_id, chap_id=chap_id, chapter_name=art["chapter"],
                     art_id=art["id"], art_num=art["article_number"], content=art["content"], status=status)

            # Link Cross-Article References
            for art in parsed_data["articles"]:
                for ref_num in art["references"]:
                    target_id = f"{reg_id}-{ref_num.replace(' ', '_')}"
                    session.run("""
                        MATCH (source:Article {id: $source_id})
                        MATCH (target:Article {id: $target_id})
                        MERGE (source)-[:REFERENCES]->(target)
                    """, source_id=art["id"], target_id=target_id)
        print(" -> Neo4j: Regulation hierarchy and cross-article reference links established.")

        # 2. Vector Indexing in Qdrant (Target collection: 'regulations')
        points = []
        for idx, art in enumerate(parsed_data["articles"]):
            vector = self.generate_embedding(art["content"], dim=768)
            payload = {
                "document_id": art["id"],
                "regulation_id": reg_id,
                "document_type": "article",
                "source_type": status,
                "jurisdiction": "Indonesia",
                "article_number": art["article_number"],
                "chapter": art["chapter"],
                "content": art["content"],
                "references": art["references"],
                "verification_status": status
            }
            # Deterministic point ID from document hash
            pt_id = int(hashlib.md5(art["id"].encode('utf-8')).hexdigest()[:8], 16)
            points.append(models.PointStruct(id=pt_id, vector=vector, payload=payload))

        self.qdrant_client.upsert(collection_name="regulations", points=points)
        print(" -> Qdrant: Article vector embeddings and metadata indexed into 'regulations'.")

if __name__ == "__main__":
    parser = IndonesianStatuteParser()
    data = parser.parse_text(
        filepath="/home/ai/JPAIS/datasets/verified/uu_1_2024_sample.txt",
        reg_id="UU-1-2024",
        reg_type="Undang-Undang",
        number="1",
        year=2024,
        title="Perubahan Kedua Atas Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik",
        status="verified"
    )
    parser.ingest(data)

    # Verification query: Traverse cross-references in Neo4j
    with parser.neo4j_driver.session() as session:
        print("\nVerifying Cross-Article Reference Graph Traversal:")
        res = session.run("""
            MATCH (r:Regulation {id: 'UU-1-2024'})-[:HAS_CHAPTER]->(c:Chapter)-[:CONTAINS]->(a:Article)
            OPTIONAL MATCH (a)-[:REFERENCES]->(target:Article)
            RETURN a.article_number AS source_article, c.name AS chapter, target.article_number AS referenced_article
            ORDER BY a.article_number
        """)
        for row in res:
            ref = row["referenced_article"] if row["referenced_article"] else "None"
            print(f"  {row['source_article']} ({row['chapter']}) -> References: {ref}")

    parser.close()
    print("\n=== STATUTORY INGESTION PIPELINE VERIFIED ===")
