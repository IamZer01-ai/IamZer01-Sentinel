#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# IamZer01 Sentinel – Backup Script
# Version 1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_ROOT/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="sentinel_backup_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "╔══════════════════════════════════════════╗"
echo "║   IamZer01 Sentinel — Backup            ║"
echo "╚══════════════════════════════════════════╝"

echo "[*] Starting backup: $BACKUP_FILE"

# Stop services to ensure data consistency
echo "[*] Stopping services..."
docker compose -f "$PROJECT_ROOT/docker-compose.yml" stop grafana influxdb elasticsearch prometheus

# Backup Docker volumes
echo "[*] Backing up Docker volumes..."
docker run --rm -v sentinel_grafana_data:/data -v "$BACKUP_DIR:/backup" alpine \
    tar czf "/backup/grafana_data_${TIMESTAMP}.tar.gz" -C /data . 2>/dev/null || true

docker run --rm -v sentinel_influxdb_data:/data -v "$BACKUP_DIR:/backup" alpine \
    tar czf "/backup/influxdb_data_${TIMESTAMP}.tar.gz" -C /data . 2>/dev/null || true

docker run --rm -v sentinel_prometheus_data:/data -v "$BACKUP_DIR:/backup" alpine \
    tar czf "/backup/prometheus_data_${TIMESTAMP}.tar.gz" -C /data . 2>/dev/null || true

docker run --rm -v sentinel_elasticsearch_data:/data -v "$BACKUP_DIR:/backup" alpine \
    tar czf "/backup/elasticsearch_data_${TIMESTAMP}.tar.gz" -C /data . 2>/dev/null || true

# Backup configuration files
echo "[*] Backing up configuration files..."
tar czf "$BACKUP_DIR/${BACKUP_FILE}" \
    -C "$PROJECT_ROOT" \
    config/ grafana/ prometheus/ exporters/ nginx/ scripts/ \
    docker-compose.yml .env.example 2>/dev/null || true

# Restart services
echo "[*] Restarting services..."
docker compose -f "$PROJECT_ROOT/docker-compose.yml" start grafana influxdb elasticsearch prometheus

echo "[+] Backup complete: $BACKUP_DIR/${BACKUP_FILE}"
echo "[+] Volume backups: $BACKUP_DIR/*_${TIMESTAMP}.tar.gz"
