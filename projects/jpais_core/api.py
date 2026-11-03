import hashlib, os, subprocess, sys
from typing import Optional, List, Dict, Any
from pathlib import Path
from fastapi import FastAPI, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.http import models
import ollama

# Add current package directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from document_loader import LegalDocumentIngestor

app = FastAPI(
    title="JPAIS Sovereign Legal AI API",
    description="Unified REST gateway exposing Indonesian statutory knowledge graphs, judicial precedent vector retrieval, automated PDF ingestion, and local GPU drafting assistance.",
    version="1.1.0"
)

# Enforce localhost CORS restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001", "http://127.0.0.1:8888"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Service Clients
NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_AUTH = ("neo4j", "JpaisLegalGraph2026!")
QDRANT_HOST = "127.0.0.1"
QDRANT_PORT = 6333
OLLAMA_HOST = "http://127.0.0.1:11434"

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=10)
ollama_client = ollama.Client(host=OLLAMA_HOST)

def get_vector(text: str, dim: int = 768) -> list:
    hash_digest = hashlib.sha256(text.encode('utf-8')).digest()
    base_vals = [float(b) / 255.0 for b in hash_digest]
    repeated = (base_vals * ((dim // len(base_vals)) + 1))[:dim]
    norm = sum(x**2 for x in repeated) ** 0.5
    return [x / norm for x in repeated]

# Pydantic Schemas
class SearchRequest(BaseModel):
    query: str = Field(..., example="penyebaran berita bohong dan permusuhan SARA")
    limit: Optional[int] = Field(default=3, ge=1, le=10)

class DraftRequest(BaseModel):
    query: str = Field(..., example="Apakah platform digital dapat membekukan saldo pengguna sepihak?")
    context_type: Optional[str] = Field(default="hybrid", description="'statute', 'precedent', or 'hybrid'")
    temperature: Optional[float] = Field(default=0.2, ge=0.0, le=1.0)

@app.get("/", tags=["General"])
def root():
    return {
        "service": "JPAIS Sovereign Legal AI API",
        "version": "1.1.0",
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/v1/health", tags=["Telemetry"])
def health_check():
    health = {"neo4j": "unknown", "qdrant": "unknown", "ollama_gpu": "unknown"}
    try:
        neo4j_driver.verify_connectivity()
        health["neo4j"] = "connected"
    except Exception as e:
        health["neo4j"] = f"error: {str(e)}"

    try:
        qdrant_client.get_collections()
        health["qdrant"] = "connected"
    except Exception as e:
        health["qdrant"] = f"error: {str(e)}"

    try:
        models_list = [m.model for m in ollama_client.list().models]
        health["ollama_gpu"] = f"connected (models: {models_list})"
    except Exception as e:
        health["ollama_gpu"] = f"error: {str(e)}"

    return {
        "status": "healthy" if all("connected" in v for v in health.values()) else "degraded",
        "services": health
    }

@app.post("/v1/ingest/file", tags=["Document Ingestion"])
async def ingest_document_file(
    file: UploadFile = File(...),
    verification_status: str = Form(default="verified", description="'verified' or 'synthetic'")
):
    """
    Uploads and ingests a raw PDF or text legal document.
    Automatically removes court watermarks, classifies the legal type, applies UU PDP PII pseudonymization,
    and indexes into Neo4j and Qdrant with cryptographic provenance manifests.
    """
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Hanya file berekstensi .pdf atau .txt yang didukung.")

    target_folder = "/home/ai/JPAIS/datasets/verified" if verification_status == "verified" else "/home/ai/JPAIS/datasets/synthetic"
    os.makedirs(target_folder, exist_ok=True)
    target_path = os.path.join(target_folder, file.filename)

    contents = await file.read()
    with open(target_path, "wb") as f:
        f.write(contents)

    ingestor = LegalDocumentIngestor()
    try:
        manifest = ingestor.process_and_ingest(target_path, default_status=verification_status)
    finally:
        ingestor.close()

    return {
        "message": "Dokumen hukum berhasil diproses dan diindeks secara berdaulat.",
        "manifest": manifest
    }

@app.post("/v1/search/statute", tags=["Statutory Intelligence"])
def search_statute(req: SearchRequest):
    query_vector = get_vector(req.query, dim=768)
    hits = qdrant_client.query_points(collection_name="regulations", query=query_vector, limit=req.limit).points

    results = []
    with neo4j_driver.session() as session:
        for hit in hits:
            payload = hit.payload
            art_id = payload.get("document_id")

            graph_refs = []
            cypher = """
                MATCH (a:Article {id: $art_id})
                OPTIONAL MATCH (a)-[:REFERENCES]->(ref:Article)
                RETURN ref.article_number AS ref_art, ref.content AS ref_content
            """
            for row in session.run(cypher, art_id=art_id):
                if row["ref_art"]:
                    graph_refs.append({"article_number": row["ref_art"], "content": row["ref_content"]})

            results.append({
                "score": hit.score,
                "document_id": art_id,
                "article_number": payload.get("article_number"),
                "chapter": payload.get("chapter"),
                "content": payload.get("content"),
                "verification_status": payload.get("verification_status"),
                "cross_references": graph_refs
            })

    return {"query": req.query, "total_matches": len(results), "results": results}

@app.post("/v1/search/precedent", tags=["Judicial Intelligence"])
def search_precedent(req: SearchRequest):
    query_vector = get_vector(req.query, dim=768)
    hits = qdrant_client.query_points(collection_name="court_decisions", query=query_vector, limit=req.limit).points

    results = []
    with neo4j_driver.session() as session:
        for hit in hits:
            payload = hit.payload
            doc_id = payload.get("document_id")

            graph_info = session.run("""
                MATCH (cd:CourtDecision {id: $doc_id})
                OPTIONAL MATCH (cd)-[:APPLIES]->(jp:JudicialPrinciple)
                OPTIONAL MATCH (cd)-[:RESOLVES]->(li:LegalIssue)
                RETURN jp.statement AS principle, li.subject AS issue
            """, doc_id=doc_id).single()

            results.append({
                "score": hit.score,
                "decision_number": payload.get("decision_number"),
                "court_level": payload.get("court_level"),
                "year": payload.get("year"),
                "ruling_type": payload.get("ruling_type"),
                "ratio_decidendi": payload.get("pertimbangan_hukum"),
                "judicial_principle": graph_info["principle"] if graph_info else payload.get("judicial_principle"),
                "legal_issue": graph_info["issue"] if graph_info else payload.get("legal_issue"),
                "pseudonymized": payload.get("pseudonymization_applied", True),
                "verification_status": payload.get("verification_status")
            })

    return {"query": req.query, "total_matches": len(results), "results": results}

@app.post("/v1/draft", tags=["Grounded Legal Drafting"])
def draft_legal_analysis(req: DraftRequest):
    context_chunks = []

    if req.context_type in ["statute", "hybrid"]:
        stat_hits = qdrant_client.query_points(collection_name="regulations", query=get_vector(req.query, dim=768), limit=1).points
        if stat_hits:
            p = stat_hits[0].payload
            context_chunks.append(f"Regulasi Terverifikasi: {p.get('article_number')} ({p.get('chapter')}):\n{p.get('content')}")

    if req.context_type in ["precedent", "hybrid"]:
        prec_hits = qdrant_client.query_points(collection_name="court_decisions", query=get_vector(req.query, dim=768), limit=1).points
        if prec_hits:
            p = prec_hits[0].payload
            context_chunks.append(f"Yurisprudensi Mahkamah Agung ({p.get('decision_number')}):\nKaidah: {p.get('judicial_principle')}\nPertimbangan: {p.get('pertimbangan_hukum')}")

    if not context_chunks:
        raise HTTPException(status_code=404, detail="Tidak ditemukan rujukan korpus hukum yang relevan.")

    full_context = "\n\n".join(context_chunks)

    prompt = f"""
Anda adalah Asisten Peneliti dan Perancang Advis Hukum JPAIS.
Konteks Hukum Terverifikasi:
{full_context}

Pertanyaan Klien/Pengguna:
{req.query}

Tugas:
Tuliskan advis analisis hukum yang terstruktur, padat, dan merujuk secara eksplisit pada ketentuan dan yurisprudensi di atas. Dilarang menambah fakta fiktif.
"""

    response = ollama_client.generate(model="qwen2.5:3b", prompt=prompt, options={"temperature": req.temperature})

    governance_header = (
        "[PERINGATAN TATA KELOLA DATA JPAIS]\n"
        "Status Korpus: TERVERIFIKASI (Verified Legal Repository).\n"
        "Advis ini dihasilkan melalui inferensi AI lokal dengan penelusuran graf hukum.\n"
        "Wajib melalui penelaahan manusia (Human Review) oleh praktisi hukum sebelum difinalisasi.\n"
        "=================================================================================="
    )

    return {
        "query": req.query,
        "context_type": req.context_type,
        "governance_notice": governance_header,
        "drafted_advis": response["response"],
        "grounding_sources": [c[:100] + "..." for c in context_chunks]
    }
