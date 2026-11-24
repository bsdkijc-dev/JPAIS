"""JPAIS Stage 7: Judicial Decision Search System (JDSS v1.0).

Runs locally on Dell Precision 7540 (127.0.0.1:8001) using local Qdrant + Neo4j
when available, with automatic local JSON/CSV fallback for zero-dependency startup.
"""

from __future__ import annotations

import csv
import json
import os
import urllib.request
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "jpais_stages_1_4" if (HERE.parent / "jpais_stages_1_4").exists() else HERE

OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embed")
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
COLLECTION = "jpais_synthetic_cases"

CASES = json.loads((DATA_DIR / "synthetic_cases.json").read_text(encoding="utf-8"))
with open(DATA_DIR / "synthetic_kg_edges.csv", encoding="utf-8") as _f:
    EDGES = list(csv.DictReader(_f))

app = FastAPI(title="JPAIS JDSS v1.0 (Synthetic Prototype)", version="1.0.0")


def _semantic_qdrant_search(q: str, limit: int = 5) -> Optional[list[dict]]:
    try:
        req_e = urllib.request.Request(
            OLLAMA_EMBED_URL,
            data=json.dumps({"model": "bge-m3", "input": q}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req_e, timeout=10) as r:
            vec = json.loads(r.read())["embeddings"][0]
        req_s = urllib.request.Request(
            f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
            data=json.dumps({"vector": vec, "limit": limit, "with_payload": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req_s, timeout=10) as r:
            hits = json.loads(r.read()).get("result", [])
        return [
            {**h["payload"], "score": round(h["score"], 4), "engine": "qdrant+bge-m3"}
            for h in hits
        ]
    except Exception:
        return None


def _local_search(
    q: str = "",
    domain: Optional[str] = None,
    court: Optional[str] = None,
    regulation: Optional[str] = None,
) -> list[dict]:
    q_low = q.strip().lower()
    results = []
    for c in CASES:
        if domain and domain.lower() not in c["legal_domain"].lower():
            continue
        if court and court.lower() not in (c["issuing_institution"] + " " + c["court_satker_id"]).lower():
            continue
        if regulation and not any(regulation.lower() in r.lower() for r in c["article_references"]):
            continue
        haystack = " ".join([
            c["doc_id"], c["title"], c["issuing_institution"], c["legal_domain"],
            c["summary"], c["holding"], " ".join(c["article_references"]),
        ]).lower()
        if q_low:
            tokens = [t for t in q_low.split() if len(t) > 1]
            hits = sum(1 for t in tokens if t in haystack)
            if hits == 0:
                continue
            score = round(hits / max(len(tokens), 1), 4)
        else:
            score = 1.0
        results.append({**c, "score": score, "engine": "local-fallback"})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def _kg_neighbors(doc_id: str) -> list[dict]:
    return [
        e for e in EDGES if e["src_id"] == doc_id or e["dst_id"] == doc_id
    ]


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "mode": "synthetic-prototype",
        "cases_loaded": len(CASES),
        "kg_edges_loaded": len(EDGES),
    }


@app.get("/search")
def search(
    q: str = Query(default="", description="Semantic or keyword query"),
    domain: Optional[str] = Query(default=None),
    court: Optional[str] = Query(default=None),
    regulation: Optional[str] = Query(default=None),
    limit: int = Query(default=5, ge=1, le=20),
) -> dict:
    if q and not any([domain, court, regulation]):
        import re as _re
        exact_ids = _re.findall(r"JPAIS-(?:DOC|SYN)-\d{4}-\d{6}", q)
        pinned = [{**c, "score": 1.0, "engine": "hybrid-exact-id"} for c in CASES if c["doc_id"] in exact_ids]
        qdrant_hits = _semantic_qdrant_search(q, limit=limit)
        if qdrant_hits is not None:
            seen = {x["doc_id"] for x in pinned}
            qdrant_hits = (pinned + [h for h in qdrant_hits if h["doc_id"] not in seen])[:limit]
        if qdrant_hits is not None:
            for item in qdrant_hits:
                item["kg_relationships"] = _kg_neighbors(item["doc_id"])
            return {"query": q, "count": len(qdrant_hits), "results": qdrant_hits}

    hits = _local_search(q=q, domain=domain, court=court, regulation=regulation)[:limit]
    for item in hits:
        item["kg_relationships"] = _kg_neighbors(item["doc_id"])
    return {"query": q, "count": len(hits), "results": hits}


@app.get("/cases/{doc_id}")
def get_case(doc_id: str) -> dict:
    for c in CASES:
        if c["doc_id"] == doc_id:
            return {**c, "kg_relationships": _kg_neighbors(doc_id)}
    return {"error": f"Case {doc_id} not found"}


@app.get("/", response_class=HTMLResponse)
def ui() -> str:
    return """<!doctype html>
<html><head><meta charset="utf-8"><title>JPAIS JDSS v1.0</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;color:#0f172a}
input,button{font-size:15px;padding:8px 12px}input{width:65%}.tag{font-size:12px;background:#e2e8f0;padding:2px 6px}
.card{border-top:1px solid #cbd5e1;padding:14px 0}</style></head>
<body>
<h1>JPAIS — Judicial Decision Search System (JDSS v1.0)</h1>
<p><span class="tag">SYNTHETIC PROTOTYPE — NOT AN AUTHORITATIVE LEGAL SOURCE</span></p>
<form onsubmit="runSearch(event)">
  <input id="q" placeholder="Search case, PERMA, legal issue, or court (e.g. mediasi, PKPU, AUPB)...">
  <button type="submit">Search</button>
</form>
<div id="out"></div>
<script>
async function runSearch(e){
  e.preventDefault();
  const q=document.getElementById('q').value;
  const r=await fetch('/search?q='+encodeURIComponent(q));
  const d=await r.json();
  document.getElementById('out').innerHTML=d.results.map(x=>
    `<div class="card"><strong>${x.doc_id} — ${x.title}</strong> (${x.issuing_institution}, ${x.legal_domain})
     <br>${x.summary}<br><em>Holding:</em> ${x.holding}
     <br><small>Refs: ${x.article_references.join('; ')} | KG edges: ${x.kg_relationships.length} | Engine: ${x.engine}</small></div>`
  ).join('')||'<p>No matching synthetic cases.</p>';
}
runSearch({preventDefault:()=>{}});
</script></body></html>"""
