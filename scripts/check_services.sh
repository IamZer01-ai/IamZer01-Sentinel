#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# IamZer01 Sentinel – Service Health Check
# Version 1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "╔══════════════════════════════════════════╗"
echo "║   IamZer01 Sentinel — Health Check      ║"
echo "╚══════════════════════════════════════════╝"
echo ""

FAILED=0
TOTAL=0

check_container() {
    TOTAL=$((TOTAL + 1))
    NAME="$1"
    STATUS=$(docker ps --filter "name=$NAME" --format "{{.Status}}" 2>/dev/null || echo "NOT_FOUND")

    if echo "$STATUS" | grep -q "Up"; then
        echo "  [✅] $NAME — $STATUS"
    else
        echo "  [❌] $NAME — $STATUS"
        FAILED=$((FAILED + 1))
    fi
}

check_http() {
    TOTAL=$((TOTAL + 1))
    NAME="$1"
    URL="$2"
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$URL" 2>/dev/null || echo "000")

    if [ "$CODE" = "200" ] || [ "$CODE" = "302" ] || [ "$CODE" = "401" ]; then
        echo "  [✅] $NAME — HTTP $CODE"
    else
        echo "  [❌] $NAME — HTTP $CODE"
        FAILED=$((FAILED + 1))
    fi
}

# ── Container checks ───────────────────────────────
echo "[*] Container status:"
check_container "sentinel-prometheus"
check_container "sentinel-alertmanager"
check_container "sentinel-grafana"
check_container "sentinel-influxdb"
check_container "sentinel-telegraf"
check_container "sentinel-elasticsearch"
check_container "sentinel-kibana"
check_container "sentinel-node-exporter"
check_container "sentinel-cadvisor"
check_container "sentinel-firewall-exporter"
check_container "sentinel-vuln-exporter"
check_container "sentinel-mitre-exporter"
check_container "sentinel-nginx"
echo ""

# ── HTTP endpoint checks ──────────────────────────
echo "[*] HTTP endpoint health:"
check_http "Grafana" "http://localhost:3000"
check_http "Prometheus" "http://localhost:9090/-/healthy"
check_http "Alertmanager" "http://localhost:9093/-/healthy"
check_http "Elasticsearch" "http://localhost:9200/_cluster/health"
check_http "InfluxDB" "http://localhost:8086/health"
echo ""

# ── Summary ────────────────────────────────────────
echo "╔══════════════════════════════════════════╗"
echo "║   Results: $TOTAL total, $FAILED failed          ║"
if [ "$FAILED" -eq 0 ]; then
    echo "║   ✅ All services healthy!               ║"
else
    echo "║   ❌ Some services require attention.    ║"
fi
echo "╚══════════════════════════════════════════╝"
exit $FAILED
