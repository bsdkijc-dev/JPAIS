#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT="$HOME/JPAIS/backups/dell_local"
STAMP=$(date +%Y%m%d_%H%M%S)
DEST="$BACKUP_ROOT/$STAMP"
mkdir -p "$DEST"

# 1. Qdrant snapshot of synthetic & public collections
for COL in jpais_synthetic_cases jpais_public_verified; do
  curl -sf -X POST "http://127.0.0.1:6333/collections/$COL/snapshots" -o "$DEST/${COL}_snapshot.json" || true
done

# 2. Archive scripts, governance configs, and evaluation outputs (exclude .env and raw data)
tar --exclude='*.env' --exclude='__pycache__' -czf "$DEST/jpais_code_and_eval.tar.gz"   -C "$HOME/JPAIS/projects/jpais-core" .

# 3. Retain last 7 local backups
ls -1dt "$BACKUP_ROOT"/*/ 2>/dev/null | tail -n +8 | xargs -r rm -rf
echo "Backup completed: $DEST"
