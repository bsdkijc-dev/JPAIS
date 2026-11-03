#!/bin/bash
set -e
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$HOME/JPAIS/backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

echo "=== Backing up JPAIS Databases ==="
# 1. Backup Qdrant snapshot via API
curl -s -X POST "http://127.0.0.1:6333/collections/synthetic_legal_corpus/snapshots" > "$BACKUP_DIR/qdrant_snapshot_meta.json"

# 2. Archive Neo4j and Qdrant data volumes safely
tar -czf "$BACKUP_DIR/neo4j_data.tar.gz" -C "$HOME/JPAIS/knowledge_graph" data/
tar -czf "$BACKUP_DIR/qdrant_data.tar.gz" -C "$HOME/JPAIS/vector_database" storage/

echo "Backup created at: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
