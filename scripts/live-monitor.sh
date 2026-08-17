#!/bin/bash
# IamZer01 Sentinel - Continuous Monitoring Dashboard
# Real-time view of all platform activity

set -e

API_URL="http://localhost:8000"
REFRESH_INTERVAL=5

clear_screen() {
    clear
}

print_header() {
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                   🛡️  SENTINEL LIVE MONITORING DASHBOARD                    ║"
    echo "║                    Real-Time Platform Activity Monitor                      ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 TIMESTAMP: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
}

print_health() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🏥 PLATFORM HEALTH"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Get health status
    HEALTH=$(curl -s "$API_URL/health" 2>/dev/null || echo '{"status":"down"}')
    STATUS=$(echo "$HEALTH" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'unknown'))" 2>/dev/null || echo "unknown")
    
    if [ "$STATUS" = "healthy" ]; then
        echo "✅ Backend API Status: HEALTHY"
    else
        echo "❌ Backend API Status: $STATUS"
    fi
    
    echo ""
}

print_stats() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📈 DETECTION STATISTICS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    STATUS_DATA=$(curl -s "$API_URL/status" 2>/dev/null || echo '{}')
    
    RULES=$(echo "$STATUS_DATA" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('detection_rules_active', 0))" 2>/dev/null || echo "0")
    DETECTIONS=$(echo "$STATUS_DATA" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('detections_total', 0))" 2>/dev/null || echo "0")
    CORRELATIONS=$(echo "$STATUS_DATA" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('correlations_total', 0))" 2>/dev/null || echo "0")
    OPEN_INCIDENTS=$(echo "$STATUS_DATA" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('open_incidents', 0))" 2>/dev/null || echo "0")
    CLOSED_INCIDENTS=$(echo "$STATUS_DATA" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('closed_incidents', 0))" 2>/dev/null || echo "0")
    
    printf "  Active Rules: %-20s | Detections Made: %-15s\n" "$RULES" "$DETECTIONS"
    printf "  Alert Correlations: %-10s | Open Incidents: %-15s\n" "$CORRELATIONS" "$OPEN_INCIDENTS"
    printf "  Closed Incidents: %-15s\n" "$CLOSED_INCIDENTS"
    
    echo ""
}

print_alerts() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚨 RECENT ALERTS (Last 5)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    ALERTS=$(curl -s "$API_URL/api/v1/alerts?limit=5" 2>/dev/null || echo '{"count":0,"alerts":[]}')
    ALERT_COUNT=$(echo "$ALERTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('count', 0))" 2>/dev/null || echo "0")
    
    if [ "$ALERT_COUNT" -eq 0 ]; then
        echo "  No alerts yet"
    else
        echo "$ALERTS" | python3 << 'PYEOF' 2>/dev/null || echo "  Error fetching alerts"
import sys, json
data = json.load(sys.stdin)
for i, alert in enumerate(data.get('alerts', [])[:5], 1):
    severity = alert.get('severity', 'unknown').upper()
    title = alert.get('title', 'Unknown')
    timestamp = alert.get('timestamp', '')
    status = alert.get('status', 'unknown')
    
    severity_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')
    
    print(f"  {i}. {severity_emoji} [{severity}] {title}")
    print(f"     Status: {status} | Time: {timestamp[:19]}")
    print()
PYEOF
    fi
    
    echo ""
}

print_events() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 RECENT EVENTS (Last 3)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    EVENTS=$(curl -s "$API_URL/api/v1/events?limit=3" 2>/dev/null || echo '{"count":0,"events":[]}')
    EVENT_COUNT=$(echo "$EVENTS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('count', 0))" 2>/dev/null || echo "0")
    
    if [ "$EVENT_COUNT" -eq 0 ]; then
        echo "  No events yet"
    else
        echo "$EVENTS" | python3 << 'PYEOF' 2>/dev/null || echo "  Error fetching events"
import sys, json
data = json.load(sys.stdin)
for i, event in enumerate(data.get('events', [])[:3], 1):
    event_type = event.get('event_type', 'unknown').upper()
    event_name = event.get('event_name', 'Unknown')
    hostname = event.get('hostname', 'N/A')
    source_ip = event.get('source_ip', 'N/A')
    
    print(f"  {i}. [{event_type}] {event_name}")
    print(f"     Host: {hostname} | Source: {source_ip}")
    print()
PYEOF
    fi
    
    echo ""
}

print_docker_status() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🐳 DOCKER SERVICES STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    RUNNING=$(docker compose ps --format json 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(len([d for d in data if 'Up' in d.get('State', '')]))" 2>/dev/null || echo "0")
    TOTAL=$(docker compose ps --format json 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")
    
    printf "  Services: %d/%d running\n" "$RUNNING" "$TOTAL"
    
    echo ""
}

print_quick_commands() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚡ QUICK COMMANDS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Run Simulation:     curl -X POST http://localhost:8000/api/v1/simulate/brute-force"
    echo "  View Alerts:        curl http://localhost:8000/api/v1/alerts"
    echo "  View Incidents:     curl http://localhost:8000/api/v1/incidents"
    echo "  View Dashboards:    http://localhost:3000 (Grafana)"
    echo "  View Logs:          docker compose logs -f sentinel-backend"
    echo "  Stop Monitoring:    Press Ctrl+C"
    echo ""
}

# Main loop
main() {
    while true; do
        clear_screen
        print_header
        print_health
        print_stats
        print_alerts
        print_events
        print_docker_status
        print_quick_commands
        
        echo "⏱️  Auto-refreshing in $REFRESH_INTERVAL seconds... (Ctrl+C to stop)"
        sleep "$REFRESH_INTERVAL"
    done
}

main
