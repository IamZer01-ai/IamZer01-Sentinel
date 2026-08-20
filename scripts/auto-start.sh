#!/bin/bash
# IamZer01 Sentinel - Automatic Startup & Monitoring Script
# Starts all services and enables continuous monitoring/simulation

set -e

PROJECT_DIR="/workspaces/IamZer01-Sentinel"
cd "$PROJECT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🛡️  IamZer01 Sentinel - Automatic Startup Manager     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to start services
start_services() {
    echo -e "${YELLOW}📦 Starting Docker services...${NC}"
    docker compose up -d
    sleep 5
    echo -e "${GREEN}✓ Services started${NC}"
    echo ""
}

# Function to verify services
verify_services() {
    echo -e "${YELLOW}🏥 Verifying services...${NC}"
    
    # Wait for backend to be ready
    for i in {1..30}; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ All services healthy${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    echo -e "${RED}✗ Services failed to become healthy${NC}"
    return 1
}

# Function to show access points
show_access_points() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ PLATFORM READY - ACCESS POINTS:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${YELLOW}Sentinel Backend${NC} .... ${GREEN}http://localhost:8000${NC}"
    echo -e "  ${YELLOW}API Documentation${NC} .. ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  ${YELLOW}Grafana Dashboards${NC} .. ${GREEN}http://localhost:3000${NC}"
    echo -e "  ${YELLOW}Prometheus Metrics${NC} .. ${GREEN}http://localhost:9090${NC}"
    echo -e "  ${YELLOW}Kibana Logs${NC} ........ ${GREEN}http://localhost:5601${NC}"
    echo -e "  ${YELLOW}Elasticsearch${NC} ...... ${GREEN}http://localhost:9200${NC}"
    echo ""
}

# Function to show monitoring options
show_monitoring_options() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📊 MONITORING & AUTOMATION OPTIONS:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${YELLOW}Option 1: Live Monitor Dashboard${NC}"
    echo -e "    Run in new terminal: ${GREEN}bash scripts/live-monitor.sh${NC}"
    echo -e "    Shows: Health, stats, recent alerts, events (auto-refreshes every 5s)"
    echo ""
    echo -e "  ${YELLOW}Option 2: Automated Simulations${NC}"
    echo -e "    Run in new terminal: ${GREEN}bash scripts/auto-simulate.sh${NC}"
    echo -e "    Shows: Log file at ${GREEN}/tmp/sentinel-simulation.log${NC}"
    echo -e "    Runs: Different scenarios every 30 seconds"
    echo ""
    echo -e "  ${YELLOW}Option 3: Stream Backend Logs${NC}"
    echo -e "    Run: ${GREEN}docker compose logs -f sentinel-backend${NC}"
    echo -e "    Shows: Real-time backend processing"
    echo ""
    echo -e "  ${YELLOW}Option 4: View All Logs${NC}"
    echo -e "    Run: ${GREEN}docker compose logs -f${NC}"
    echo -e "    Shows: All service logs combined"
    echo ""
}

# Function to show quick test commands
show_test_commands() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}⚡ QUICK TEST COMMANDS:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  # Check platform status"
    echo -e "  ${GREEN}curl http://localhost:8000/status | jq${NC}"
    echo ""
    echo -e "  # Run a brute force simulation"
    echo -e "  ${GREEN}curl -X POST http://localhost:8000/api/v1/simulate/brute-force | jq${NC}"
    echo ""
    echo -e "  # View generated alerts"
    echo -e "  ${GREEN}curl http://localhost:8000/api/v1/alerts | jq${NC}"
    echo ""
    echo -e "  # View detection rules"
    echo -e "  ${GREEN}curl http://localhost:8000/api/v1/detection/rules | jq${NC}"
    echo ""
    echo -e "  # View incidents"
    echo -e "  ${GREEN}curl http://localhost:8000/api/v1/incidents | jq${NC}"
    echo ""
    echo -e "  # Use CLI commands"
    echo -e "  ${GREEN}sentinel status${NC}"
    echo -e "  ${GREEN}sentinel health${NC}"
    echo -e "  ${GREEN}sentinel alerts${NC}"
    echo ""
}

# Function to ask for automation mode
ask_automation_mode() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}🤖 AUTOMATIC MONITORING MODE:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Do you want to enable automatic monitoring?"
    echo ""
    echo "  1) Enable Live Monitor (refresh every 5s)"
    echo "  2) Enable Auto Simulations (run every 30s)"
    echo "  3) Enable Both (in background)"
    echo "  4) Manual Mode (I'll do it myself)"
    echo ""
    read -p "Choose [1-4]: " -r choice
    
    case $choice in
        1)
            echo ""
            echo -e "${GREEN}🚀 Starting Live Monitor in new window...${NC}"
            new-terminal bash scripts/live-monitor.sh 2>/dev/null || bash scripts/live-monitor.sh &
            ;;
        2)
            echo ""
            echo -e "${GREEN}🚀 Starting Auto Simulator in background...${NC}"
            nohup bash scripts/auto-simulate.sh > /tmp/sentinel-auto-simulate.log 2>&1 &
            echo -e "${GREEN}✓ Simulator running in background${NC}"
            echo -e "${YELLOW}  View log: tail -f /tmp/sentinel-simulation.log${NC}"
            ;;
        3)
            echo ""
            echo -e "${GREEN}🚀 Starting Live Monitor and Auto Simulator in background...${NC}"
            nohup bash scripts/auto-simulate.sh > /tmp/sentinel-auto-simulate.log 2>&1 &
            sleep 2
            new-terminal bash scripts/live-monitor.sh 2>/dev/null || bash scripts/live-monitor.sh &
            ;;
        4)
            echo ""
            echo -e "${YELLOW}ℹ️  Manual mode selected - run commands as needed${NC}"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
}

# Function to show documentation references
show_documentation() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📖 DOCUMENTATION:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  QUICK_START.md ........... Getting started guide"
    echo "  IMPLEMENTATION.md ........ Complete architecture"
    echo "  DELIVERY_SUMMARY.md ...... Final delivery report"
    echo "  README.md ................ Feature overview"
    echo ""
    echo "Read them with: ${GREEN}cat <filename>.md${NC}"
    echo ""
}

# Main execution
main() {
    start_services
    verify_services || exit 1
    
    show_access_points
    show_monitoring_options
    show_test_commands
    show_documentation
    
    ask_automation_mode
    
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ IamZer01 Sentinel is running!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "To stop services:       ${GREEN}docker compose down${NC}"
    echo "View service logs:      ${GREEN}docker compose logs -f${NC}"
    echo "Check service status:   ${GREEN}docker compose ps${NC}"
    echo ""
}

main "$@"
