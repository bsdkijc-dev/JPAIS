# JPAIS Docker Services Inventory

## 1. Neo4j Community (Knowledge Graph)
- Container Name: `jpais-neo4j`
- Image: `neo4j:5-community`
- HTTP Port: `127.0.0.1:7474` (Restricted to localhost)
- Bolt Port: `127.0.0.1:7687` (Restricted to localhost)
- Persistent Data: `~/JPAIS/knowledge_graph/data`
- Memory Allocation: Initial Heap 2 GB, Max Heap 4 GB, Pagecache 2 GB (Total Budget: ~6 GB RAM)
- Authentication: Configured via `.env`

## 2. Qdrant Vector Database
- Container Name: `jpais-qdrant`
- Image: `qdrant/qdrant:latest`
- HTTP Port: `127.0.0.1:6333` (Restricted to localhost)
- gRPC Port: `127.0.0.1:6334` (Restricted to localhost)
- Persistent Storage: `~/JPAIS/vector_database/storage`
- Snapshots: `~/JPAIS/vector_database/snapshots`
- Memory Allocation: Dynamic (~2–4 GB RAM budget)
