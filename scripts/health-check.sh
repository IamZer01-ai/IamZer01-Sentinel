#!/bin/bash
# IamZer01 Sentinel - Setup and Health Check Script
# Comprehensive validation and setup for the SOC platform

set -e

SENTINEL_URL="http://localhost:8000"
PROMETHEUS_URL="http://localhost:9090"
GRAFANA_URL="http://localhost:3000"
KIBANA_URL="http://localhost:5601"
ELASTICSEARCH_URL="http://localhost:9200"

echo "🛡️  IamZer01 Sentinel – Platform Validation & Setup"
echo "=================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check_service() {
    local url=$1
    local name=$2
    
    if curl -sf "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $name is healthy"
        return 0
    else
        echo -e "${RED}✗${NC} $name is unavailable"
        return 1
    fi
}

# Check Docker
echo "📦 Docker Services Status"
echo "------------------------"
docker compose ps

echo ""
echo "🏥 Service Health Checks"
echo "------------------------"

check_service "$SENTINEL_URL/health" "Sentinel Backend API" && \
check_service "$PROMETHEUS_URL" "Prometheus" && \
check_service "$GRAFANA_URL" "Grafana" && \
check_service "$KIBANA_URL" "Kibana" && \
check_service "$ELASTICSEARCH_URL" "Elasticsearch"

echo ""
echo "📊 Sentinel Platform Status"
echo "----------------------------"
curl -s "$SENTINEL_URL/status" | python3 -m json.tool

echo ""
echo "🎯 Detection Engine Status"
echo "----------------------------"
RULES=$(curl -s "$SENTINEL_URL/api/v1/detection/rules" | python3 -c "import sys, json; print(json.load(sys.stdin).get('count', 0))")
echo "Active Detection Rules: $RULES"

echo ""
echo "🚨 Current Alerts"
echo "----------------------------"
ALERTS=$(curl -s "$SENTINEL_URL/api/v1/alerts?limit=5" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Total: {data.get('count', 0)}\")")
echo "$ALERTS"

echo ""
echo "✅ Platform Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Open Grafana: $GRAFANA_URL (admin/admin)"
echo "2. Open Kibana: $KIBANA_URL"
echo "3. Open Prometheus: $PROMETHEUS_URL"
echo "4. API Docs: $SENTINEL_URL/docs"
echo "5. Run CLI: sentinel status"
echo "6. Run simulation: sentinel simulate all-scenarios"
echo ""
