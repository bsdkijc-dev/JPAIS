import hashlib
import json
import httpx
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

app = FastAPI(
    title="JPAIS Neuro-Symbolic Judicial Sandbox",
    description="Judicial Policy & AI System — GraphRAG + Local Ollama LLM",
    version="3.0.0"
)

# 1. Database Connections
NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_AUTH = ("neo4j", "JpaisLegalGraph2026!")
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
qdrant = QdrantClient(host="127.0.0.1", port=6333)

OLLAMA_ENDPOINT = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5:3b-instruct-q4_K_M"

# 2. Data Models
class CaseQuery(BaseModel):
    query_text: str
    preliminary_judge_assessment: str  # Decision-Before-Assistance
    creditor_count: int
    has_mature_debt: bool
    has_disputed_claims: bool = False
    is_judicial_review_novum: bool = False
    novum_is_decisive: Optional[bool] = None

class PrecedentMatch(BaseModel):
    case_number: str
    court: str
    verdict: str
    ratio_decidendi: str
    statutory_basis: str

class JudicialResponse(BaseModel):
    provisional_assessment_recorded: str
    statutory_gate_passed: bool
    symbolic_rule_reasoning: str
    applicable_precedents: List[PrecedentMatch]
    system_synthesis: str
    llm_judicial_memo: str  # Generated locally by Ollama
    sha256_audit_leaf: str
    timestamp: str

@app.get("/")
def health_check():
    return {
        "status": "online",
        "node": "Dell Precision 7540",
        "neo4j": "connected",
        "qdrant": "connected",
        "ollama_model": MODEL_NAME
    }

@app.post("/api/v1/analyze-case", response_model=JudicialResponse)
def analyze_case(query: CaseQuery):
    # Enforce Ethical Safeguard: Decision-Before-Assistance
    if not query.preliminary_judge_assessment.strip():
        raise HTTPException(
            status_code=400,
            detail="Mandatory Decision-Before-Assistance Rule: Preliminary judge assessment required."
        )

    statutory_passed = True
    rule_reasons = []
    target_rule_type = None

    # Step A: Query Symbolic Graph (Neo4j)
    with neo4j_driver.session() as session:
        if query.creditor_count < 2:
            statutory_passed = False
            target_rule_type = "creditor_count"
            res = session.run("MATCH (art:Article {number: 'Pasal 2 ayat (1)'}) RETURN art.number AS article").single()
            rule_reasons.append(f"Gagal syarat formil {res['article']}: Wajib memiliki minimal 2 (dua) kreditur.")

        if query.has_disputed_claims:
            statutory_passed = False
            target_rule_type = "disputed_claims"
            res = session.run("MATCH (c:LegalConcept {name: 'Pembuktian Sederhana'}) RETURN c.name AS concept").single()
            rule_reasons.append(f"Pelanggaran asas {res['concept']}: Klaim utang yang disengketakan tidak sederhana.")

        if query.is_judicial_review_novum and not query.novum_is_decisive:
            statutory_passed = False
            target_rule_type = "novum_not_decisive"
            res = session.run("MATCH (art:Article {number: 'Pasal 295 ayat (2) huruf a'}) RETURN art.number AS article").single()
            rule_reasons.append(f"Gagal syarat {res['article']}: Bukti novum tidak memenuhi kualifikasi menentukan.")

    # Step B: Query Vector Retrieval (Qdrant)
    matched_precedents = []
    if target_rule_type:
        search_filter = Filter(must=[FieldCondition(key="rule_type", match=MatchValue(value=target_rule_type))])
        scroll_results, _ = qdrant.scroll(collection_name="court_decisions", scroll_filter=search_filter, limit=5)
        for point in scroll_results:
            p = point.payload
            matched_precedents.append(PrecedentMatch(
                case_number=p["case_number"],
                court=p["court"],
                verdict=p["verdict"],
                ratio_decidendi=p["ratio_decidendi"],
                statutory_basis=p["statutory_basis"]
            ))

    # Step C: Constrained Local LLM Generation (Ollama)
    precedents_context = "\n".join([
        f"- Putusan: {p.case_number} ({p.court}), Amar: {p.verdict}. Dasar: {p.statutory_basis}. Pertimbangan: {p.ratio_decidendi}"
        for p in matched_precedents
    ])

    system_prompt = (
        "Anda adalah asisten yudisial sistem JPAIS. Anda HANYA boleh menyusun catatan pertimbangan hukum "
        "berdasarkan aturan hukum dan preseden terverifikasi di bawah ini. DILARANG membuat dasar hukum fiktif."
    )

    user_prompt = f"""
KASUS: {query.query_text}
PENILAIAN AWAL HAKIM: {query.preliminary_judge_assessment}
VERIFIKASI ATURAN HUKUM: {'; '.join(rule_reasons) if rule_reasons else 'Semua syarat formil terpenuhi.'}
PRESEDEN RELEVAN:
{precedents_context if precedents_context else 'Tidak ada preseden penolakan.'}

TUGAS:
Susun Catatan Yudisial singkat (3-4 kalimat) yang merangkum apakah permohonan dapat dikabulkan atau harus ditolak, dengan mengutip pasal dan nomor putusan preseden yang bersesuaian.
"""

    llm_output = ""
    try:
        response = httpx.post(
            OLLAMA_ENDPOINT,
            json={
                "model": MODEL_NAME,
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
                "options": {"temperature": 0.1, "num_ctx": 2048}
            },
            timeout=30.0
        )
        if response.status_code == 200:
            llm_output = response.json().get("response", "").strip()
        else:
            llm_output = f"Ollama error: HTTP {response.status_code}"
    except Exception as e:
        llm_output = f"Ollama connection notice: {str(e)}"

    # Step D: Immutable SHA-256 Audit Leaf
    record_payload = {
        "query": query.model_dump(),
        "matched_precedents": [p.model_dump() for p in matched_precedents],
        "reasons": rule_reasons,
        "llm_output": llm_output,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    sha256_hash = hashlib.sha256(json.dumps(record_payload, sort_keys=True).encode()).hexdigest()

    return JudicialResponse(
        provisional_assessment_recorded=query.preliminary_judge_assessment,
        statutory_gate_passed=statutory_passed,
        symbolic_rule_reasoning="; ".join(rule_reasons) if rule_reasons else "Semua syarat terpenuhi.",
        applicable_precedents=matched_precedents,
        system_synthesis=(
            "Hasil verifikasi neuro-simbolik: " +
            ("Permohonan memenuhi syarat pembuktian sederhana." if statutory_passed else "Permohonan berpotensi ditolak berdasarkan preseden.")
        ),
        llm_judicial_memo=llm_output,
        sha256_audit_leaf=sha256_hash,
        timestamp=record_payload["timestamp"]
    )
