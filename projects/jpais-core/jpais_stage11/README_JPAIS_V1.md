# JPAIS — Sovereign Legal AI & Judicial Knowledge Infrastructure (v1.0)

## Deployed Local Architecture (Dell Precision 7540)
- **LLM & Embeddings:** Ollama `0.40.13` (`qwen2.5:3b` + `bge-m3`, 100% GPU on Quadro T2000 4 GB VRAM)
- **Vector Store:** `jpais-qdrant` (`127.0.0.1:6333`) — `jpais_synthetic_cases` (15 cases, 1024 dims) + `jpais_public_verified`
- **Knowledge Graph:** `jpais-neo4j` (`127.0.0.1:7687`) — 15 `Case` nodes, 42 typed relationships
- **JDSS v1.0 API & UI:** FastAPI + Uvicorn (`127.0.0.1:8001`) with hybrid exact-ID + dense `bge-m3` retrieval

## Stages Completed
- **Stage 0:** Hardware, CUDA `13.2`, Docker, Governance & Readiness Audit
- **Stages 1–4:** `jpais_governance_gate.py` (P1–P5 gate, SHA-256 provenance) + 15 synthetic cases + 42 KG edges
- **Stages 5–7:** Neo4j + Qdrant ingestion & JDSS v1.0 live on `http://127.0.0.1:8001`
- **Stages 8–10:** Automated `JPAIS-001..010` eval, PERMA/SEMA drafting conflict detector, security audit (`PASS`)
- **Stage 11:** Controlled P1/P2 verified public expansion (`stage11_public_ingest.py`) with PII & duplicate guards

## GitHub Push Checklist (`bsdkijc-dev/JPAIS`)
1. Confirm `.gitignore` excludes `*.env`, `data/`, `backups/`, and `*.key`.
2. Run `python3 stage10_security_audit.py` (`status == PASS`).
3. Commit and push via SSH (`git@github.com:bsdkijc-dev/JPAIS.git`).
