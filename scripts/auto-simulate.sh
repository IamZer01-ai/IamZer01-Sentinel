#!/bin/bash
# IamZer01 Sentinel - Continuous Automated Simulation Engine
# Runs security scenarios automatically at regular intervals

set -e

API_URL="http://localhost:8000"
SIMULATION_INTERVAL=30  # Run simulation every 30 seconds
LOG_FILE="/tmp/sentinel-simulation.log"

# Initialize log
echo "🛡️  Sentinel Automated Simulation Engine - Started at $(date)" > "$LOG_FILE"
echo "=================================================" >> "$LOG_FILE"
echo ""

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

check_api() {
    if ! curl -sf "$API_URL/health" > /dev/null 2>&1; then
        log "❌ ERROR: Backend API not responding at $API_URL"
        return 1
    fi
    return 0
}

run_scenario() {
    local scenario=$1
    local friendly_name=$2
    
    log "🎬 Running scenario: $friendly_name"
    
    RESULT=$(curl -s -X POST "$API_URL/api/v1/simulate/$scenario" 2>/dev/null || echo '{"error":"Failed"}')
    
    EVENTS=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('events_generated', 0))" 2>/dev/null || echo "0")
    ALERTS=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('alerts_generated', 0))" 2>/dev/null || echo "0")
    
    log "   ✓ Generated $EVENTS events, triggered $ALERTS alerts"
    
    echo "$RESULT" >> "$LOG_FILE"
}

get_stats() {
    STATUS=$(curl -s "$API_URL/status" 2>/dev/null || echo '{}')
    
    DETECTIONS=$(echo "$STATUS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('components', {}).get('detections_total', 0))" 2>/dev/null || echo "0")
    ALERTS=$(curl -s "$API_URL/api/v1/alerts?limit=1" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('count', 0))" 2>/dev/null || echo "0")
    INCIDENTS=$(curl -s "$API_URL/api/v1/incidents?limit=1" 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('count', 0))" 2>/dev/null || echo "0")
    
    log "📊 Statistics: Detections=$DETECTIONS, Alerts=$ALERTS, Incidents=$INCIDENTS"
}

rotate_log() {
    # Keep log file manageable
    if [ -f "$LOG_FILE" ] && [ $(wc -l < "$LOG_FILE") -gt 1000 ]; then
        tail -500 "$LOG_FILE" > "$LOG_FILE.tmp"
        mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "📝 Log rotated (keeping last 500 lines)"
    fi
}

main() {
    log "✅ Automation started"
    log "📍 API: $API_URL"
    log "⏱️  Simulation interval: ${SIMULATION_INTERVAL}s"
    log ""
    
    # Wait for API to be ready
    while ! check_api; do
        log "⏳ Waiting for API to be ready..."
        sleep 5
    done
    
    log "🚀 API is ready, starting simulations"
    log ""
    
    SCENARIO_COUNT=0
    
    while true; do
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        log "🔄 SIMULATION CYCLE $(($SCENARIO_COUNT + 1))"
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Run different scenarios in rotation
        SCENARIO_NUM=$(($SCENARIO_COUNT % 6))
        
        case $SCENARIO_NUM in
            0) run_scenario "brute-force" "Brute Force Attack" ;;
            1) run_scenario "suspicious-login" "Suspicious Login" ;;
            2) run_scenario "ioc-match" "IOC Detection" ;;
            3) run_scenario "brute-force" "Brute Force Attack (retry)" ;;
            4) run_scenario "suspicious-process" "Suspicious Process" ;;
            5) run_scenario "all-scenarios" "All Scenarios Combined" ;;
        esac
        
        log ""
        get_stats
        log ""
        
        rotate_log
        
        SCENARIO_COUNT=$((SCENARIO_COUNT + 1))
        
        log "⏰ Next simulation in ${SIMULATION_INTERVAL}s..."
        log ""
        
        sleep "$SIMULATION_INTERVAL"
    done
}

# Trap signals for graceful shutdown
trap 'log "❌ Simulation engine stopped"; exit 0' SIGTERM SIGINT

main
