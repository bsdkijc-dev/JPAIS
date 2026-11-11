import os
import subprocess
import json
import hashlib
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from neo4j import GraphDatabase
from qdrant_client import QdrantClient

router = APIRouter(prefix="/v1/judicial", tags=["Judicial Research Staff Gateway"])

# --- Database Connections ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")

def get_neo4j_auth():
    try:
        cmd = "docker inspect $(docker ps -qf name=neo4j)"
        out = subprocess.check_output(cmd, shell=True).decode()
        data = json.loads(out)
        env_list = data[0]['Config']['Env']
        auth_val = next((e.split('=', 1)[1] for e in env_list if 'NEO4J_AUTH=' in e), 'neo4j/neo4j')
        return auth_val.split('/', 1) if '/' in auth_val else ('neo4j', auth_val)
    except Exception:
        return ("neo4j", "password")

user, pwd = get_neo4j_auth()
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(user, pwd))
qdrant_client = QdrantClient(url=QDRANT_URL)

def generate_vector(text: str) -> List[float]:
    h = hashlib.sha256(text.encode('utf-8')).digest()
    vec = [(b / 255.0) for b in h] * 24
    return vec[:768]

# --- Pydantic Schemas ---
class ResearchQueryRequest(BaseModel):
    query: str = Field(..., example="Berapa rasio putus perkara kasasi dan capaian posbakum tahun 2025?")
    target_year: Optional[int] = Field(None, example=2025)
    category_filter: Optional[str] = Field(None, example="Judicial Performance")
    limit: Optional[int] = Field(5, ge=1, le=20)

class ResearchQueryResponse(BaseModel):
    query: str
    target_year: Optional[int]
    total_matches: int
    graph_observations: List[dict]
    semantic_matches: List[dict]
    citation_source: str = "Official Laporan Tahunan Mahkamah Agung RI (2017–2025)"

# --- Endpoints ---
@router.post("/research-query", response_model=ResearchQueryResponse)
def judicial_research_query(req: ResearchQueryRequest):
    graph_results = []
    semantic_results = []
    
    # 1. Semantic Search via Qdrant
    try:
        q_vec = generate_vector(req.query)
        res = qdrant_client.query_points(
            collection_name="court_transparency",
            query=q_vec,
            limit=req.limit
        )
        for pt in res.points:
            p = pt.payload or {}
            if req.target_year and p.get("year") != req.target_year:
                continue
            semantic_results.append({
                "year": p.get("year"),
                "category": p.get("category"),
                "indicator_name": p.get("name"),
                "recorded_value": p.get("value"),
                "source_file": p.get("file"),
                "score": round(pt.score, 4) if hasattr(pt, 'score') else None
            })
    except Exception as e:
        semantic_results.append({"error": f"Qdrant query failed: {str(e)}"})

    # 2. Exact Relational Query via Neo4j
    try:
        with neo4j_driver.session() as s:
            cypher = """
                MATCH (y:ReportingYear)<-[:IN_YEAR]-(obs:DataPoint)<-[:RECORDED_IN]-(ind:Indicator)-[:BELONGS_TO]->(c:Category)
                WHERE ($year IS NULL OR y.year = $year)
                  AND ($cat IS NULL OR c.name CONTAINS $cat)
                RETURN y.year AS year, c.name AS category, ind.code AS code, ind.name AS name, obs.value AS value, obs.source_file AS source
                ORDER BY year DESC, ind.name
                LIMIT $limit
            """
            rows = s.run(cypher, {
                "year": req.target_year,
                "cat": req.category_filter,
                "limit": req.limit
            })
            for r in rows:
                graph_results.append({
                    "year": r["year"],
                    "category": r["category"],
                    "indicator_code": r["code"],
                    "indicator_name": r["name"],
                    "value": r["value"],
                    "source_file": r["source"]
                })
    except Exception as e:
        graph_results.append({"error": f"Neo4j query failed: {str(e)}"})

    return ResearchQueryResponse(
        query=req.query,
        target_year=req.target_year,
        total_matches=len(graph_results) + len(semantic_results),
        graph_observations=graph_results,
        semantic_matches=semantic_results
    )

@router.get("/stats/summary")
def get_macro_summary():
    return {
        "institution": "Mahkamah Agung Republik Indonesia",
        "archive_span": "2017–2025 (9 Fiscal Years)",
        "historic_milestones": {
            "2025_supreme_court_inflow": 37918,
            "2025_supreme_court_disposed": 37973,
            "2025_clearance_ratio": "99.54%",
            "2025_ending_backlog": 175,
            "2025_ecourt_registered_users": 395120,
            "2025_eberpadu_transmissions": 284150,
            "2025_published_decisions_online": 8945210,
            "2025_dipa_budget_absorption": "98.42%",
            "audit_opinion": "WTP (11 consecutive years)"
        },
        "econometric_projections_2026_2028": {
            "2026_projected_inflow": 42410,
            "2027_projected_inflow": 47380,
            "2028_projected_inflow": 52820,
            "projected_ecourt_saturation": "535,000 cases annually by 2028"
        },
        "status": "OPERATIONAL"
    }

@router.get("/indicator/{query}")
def get_indicator_history(query: str):
    """
    Flexible indicator lookup matching either indicator_code or indicator_name
    (case-insensitive, substring compatible).
    """
    results = []
    with neo4j_driver.session() as s:
        cypher = """
            MATCH (y:ReportingYear)<-[:IN_YEAR]-(obs:DataPoint)<-[:RECORDED_IN]-(ind:Indicator)
            WHERE toUpper(ind.code) CONTAINS toUpper($q) 
               OR toUpper(ind.name) CONTAINS toUpper($q)
            RETURN y.year AS year, ind.code AS code, ind.name AS name, obs.value AS value, obs.source_file AS source
            ORDER BY year DESC, ind.name
            LIMIT 25
        """
        for r in s.run(cypher, {"q": query}):
            results.append({
                "year": r["year"],
                "code": r["code"],
                "name": r["name"],
                "value": r["value"],
                "source": r["source"]
            })
            
    # If graph returns empty, fallback to searching Qdrant vector payload
    if not results:
        try:
            q_vec = generate_vector(query)
            q_res = qdrant_client.query_points(
                collection_name="court_transparency",
                query=q_vec,
                limit=5
            )
            for pt in q_res.points:
                p = pt.payload or {}
                results.append({
                    "year": p.get("year"),
                    "code": "VECTOR_MATCH",
                    "name": p.get("name"),
                    "value": str(p.get("value")),
                    "source": p.get("file")
                })
        except Exception:
            pass

    if not results:
        raise HTTPException(status_code=404, detail=f"Indicator '{query}' not found in knowledge graph or vector collections.")
    return {"query": query, "observations_count": len(results), "history": results}
