#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# IamZer01 Sentinel – Deploy Script
# Version 1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "╔══════════════════════════════════════════╗"
echo "║   IamZer01 Sentinel — Deployment        ║"
echo "╚══════════════════════════════════════════╝"

# ── Check prerequisites ─────────────────────────────────
echo "[*] Checking prerequisites..."

command -v docker >/dev/null 2>&1 || { echo "[-] docker not found. Install Docker first."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "[-] docker compose not found."; exit 1; }

# ── Load environment ────────────────────────────────────
if [ -f config/.env ]; then
    echo "[*] Loading environment from config/.env"
    set -a; source config/.env; set +a
elif [ -f .env ]; then
    echo "[*] Loading environment from .env"
    set -a; source .env; set +a
else
    echo "[!] No .env file found. Using defaults."
fi

# ── Create required directories ─────────────────────────
echo "[*] Creating data directories..."
mkdir -p data/{prometheus,grafana,influxdb,elasticsearch}
mkdir -p logs
mkdir -p backups

# ── Pull images and build ───────────────────────────────
echo "[*] Pulling Docker images..."
docker compose pull

echo "[*] Building custom exporters..."
docker compose build firewall-exporter vuln-exporter mitre-exporter

# ── Deploy ──────────────────────────────────────────────
echo "[*] Deploying stack..."
docker compose up -d

# ── Wait for services ──────────────────────────────────
echo "[*] Waiting for services to become healthy..."
sleep 10

# ── Check status ────────────────────────────────────────
echo ""
echo "[*] Running containers:"
docker compose ps

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Deployment Complete!                   ║"
echo "║                                          ║"
echo "║   Grafana:       http://localhost:3000   ║"
echo "║   Prometheus:    http://localhost:9090   ║"
echo "║   Alertmanager:  http://localhost:9093   ║"
echo "║   Kibana:        http://localhost:5601   ║"
echo "║   InfluxDB:      http://localhost:8086   ║"
echo "╚══════════════════════════════════════════╝"
