#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# IamZer01 Sentinel – Endpoint Connectivity & Metrics Check
# Version 1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

echo "╔══════════════════════════════════════════╗"
echo "║   IamZer01 Sentinel — Endpoint Check    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

check_metrics() {
    NAME="$1"
    URL="$2"
    echo "[*] $NAME ($URL)"

    RESPONSE=$(curl -s --max-time 5 "$URL" 2>/dev/null || echo "CONNECTION_FAILED")

    if [ "$RESPONSE" = "CONNECTION_FAILED" ]; then
        echo "  ❌ Could not connect"
    elif echo "$RESPONSE" | grep -q "^# HELP\|^# TYPE\|^# EOF\|^#"; then
        LINES=$(echo "$RESPONSE" | wc -l)
        echo "  ✅ Connected — $LINES metric lines"
    elif echo "$RESPONSE" | head -1 | grep -q "^\w"; then
        LINES=$(echo "$RESPONSE" | wc -l)
        echo "  ✅ Connected — $LINES lines of data"
    else
        echo "  ⚠️  Connected — unexpected response format"
    fi
    echo ""
}

# ── Exporter Metrics ──────────────────────────────
echo "── Exporters ──"
check_metrics "Firewall Exporter" "http://localhost:8001/metrics"
check_metrics "Vulnerability Exporter" "http://localhost:8002/metrics"
check_metrics "MITRE Exporter" "http://localhost:8003/metrics"
check_metrics "Prometheus Targets" "http://localhost:9090/api/v1/targets"
check_metrics "Node Exporter" "http://localhost:9100/metrics"

# ── Summary ────────────────────────────────────────
echo "── Prometheus Targets ──"
curl -s http://localhost:9090/api/v1/targets 2>/dev/null | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
active = sum(1 for t in data['data']['activeTargets'] if t['health'] == 'up')
total = len(data['data']['activeTargets'])
print(f'  Active targets: {active}/{total}')
for t in data['data']['activeTargets']:
    status = '✅' if t['health'] == 'up' else '❌'
    print(f'  {status} {t[\"labels\"][\"job\"]:25s} → {t[\"labels\"].get(\"instance\", \"unknown\")}')
" 2>/dev/null || echo "  ❌ Could not query Prometheus API"
