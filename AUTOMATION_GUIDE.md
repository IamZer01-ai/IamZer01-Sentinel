# 🛡️ IamZer01 Sentinel – Automatic Execution & Visibility Guide

## 🚀 Quick Start (Automatic Mode)

### Option 1: Full Automatic Startup with UI
```bash
cd /workspaces/IamZer01-Sentinel
chmod +x scripts/*.sh
bash scripts/auto-start.sh
```

This will:
1. ✅ Start all 14 Docker services
2. ✅ Verify everything is healthy
3. ✅ Show you all access points
4. ✅ Let you choose monitoring mode (live dashboard, auto-simulator, or both)

---

## 👀 How to See Execution

### Method 1: Live Monitoring Dashboard (Real-Time, Every 5 Seconds)

```bash
bash scripts/live-monitor.sh
```

**What you'll see:**
- Platform health status (✅ or ❌)
- Detection statistics (rules, detections, alerts, incidents)
- Last 5 alerts with severity indicators
- Recent events
- Docker service status
- Auto-refreshes every 5 seconds

**Example output:**
```
╔════════════════════════════════════════════════════════════════════════════╗
║                   🛡️  SENTINEL LIVE MONITORING DASHBOARD                    ║
║                    Real-Time Platform Activity Monitor                      ║
╚════════════════════════════════════════════════════════════════════════════╝

📊 TIMESTAMP: 2026-08-17 10:45:23

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 PLATFORM HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Backend API Status: HEALTHY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 DETECTION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Active Rules: 7                  | Detections Made: 42
  Alert Correlations: 0            | Open Incidents: 0
  Closed Incidents: 0

🚨 RECENT ALERTS (Last 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 🔴 [CRITICAL] Known IOC Detection
     Status: new | Time: 2026-08-17 10:45:12

  2. 🟠 [HIGH] Brute Force - Multiple Failed Logins
     Status: new | Time: 2026-08-17 10:45:05
```

**Stop with:** `Ctrl+C`

---

### Method 2: Automated Simulation Runner (Background Process)

```bash
bash scripts/auto-simulate.sh
```

**What it does:**
- Runs different security scenarios every 30 seconds
- Cycles through: Brute Force → Suspicious Login → IOC Detection → etc.
- Logs everything to `/tmp/sentinel-simulation.log`
- Shows: Events generated, alerts triggered, statistics

**Watch the simulation in real-time:**
```bash
tail -f /tmp/sentinel-simulation.log
```

**Example log output:**
```
🛡️  Sentinel Automated Simulation Engine - Started at Fri Aug 17 10:45:00 2026
==================================================

[2026-08-17 10:45:05] ✅ Automation started
[2026-08-17 10:45:05] 📍 API: http://localhost:8000
[2026-08-17 10:45:05] ⏱️  Simulation interval: 30s
[2026-08-17 10:45:05]
[2026-08-17 10:45:05] 🚀 API is ready, starting simulations
[2026-08-17 10:45:05]
[2026-08-17 10:45:05] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2026-08-17 10:45:05] 🔄 SIMULATION CYCLE 1
[2026-08-17 10:45:05] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2026-08-17 10:45:05] 🎬 Running scenario: Brute Force Attack
[2026-08-17 10:45:05]    ✓ Generated 10 events, triggered 2 alerts
[2026-08-17 10:45:05]
[2026-08-17 10:45:05] 📊 Statistics: Detections=52, Alerts=2, Incidents=0
```

**Stop with:** `Ctrl+C`

---

### Method 3: Backend Logs (Real Processing Details)

```bash
docker compose logs -f sentinel-backend
```

**What you'll see:**
- Every API request to the backend
- Detection engine processing
- Alert generation
- Storage operations
- Errors and warnings

**Example:**
```
sentinel-backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
sentinel-backend  | INFO:     Application startup complete
sentinel-backend  | INFO:     POST /api/v1/simulate/brute-force
sentinel-backend  | INFO:     Simulation: Generating 10 brute force events
sentinel-backend  | INFO:     Detection Engine: Evaluating 10 events
sentinel-backend  | INFO:     Rule 'Brute Force Detection' matched
sentinel-backend  | INFO:     Generated Alert: alert-id-123
sentinel-backend  | INFO:     Stored in Elasticsearch
sentinel-backend  | INFO:     Response: 201 Created
```

---

### Method 4: All Service Logs (Complete System View)

```bash
docker compose logs -f
```

Shows logs from all 14 services simultaneously, color-coded by service.

**Stop with:** `Ctrl+C`

---

### Method 5: Web Dashboards (Visual Monitoring)

Open these in your browser to see real-time data:

#### Grafana (Metrics Dashboards)
```
http://localhost:3000
```
- Login: admin / admin
- Shows: CPU, memory, network, detection trends
- Create custom dashboards with real Prometheus data

#### Prometheus (Metrics Browser)
```
http://localhost:9090
```
- Query metrics directly
- Example queries:
  - `sentinel_detections_total` – Total detections
  - `sentinel_open_incidents` – Active incidents
  - `up` – Which services are healthy

#### Kibana (Log Analysis)
```
http://localhost:5601
```
- Browse events, alerts, and incidents stored in Elasticsearch
- Create custom visualizations
- Search by hostname, username, severity

#### Elasticsearch (Raw Data)
```
http://localhost:9200/_cat/indices
```
- View stored indices
- Query events directly

#### Backend API Documentation
```
http://localhost:8000/docs
```
- Interactive API explorer
- Test endpoints with sample data
- See request/response formats

---

### Method 6: API Queries (Programmatic Access)

#### Check System Status
```bash
curl http://localhost:8000/status | jq

# Output:
{
  "status": "operational",
  "components": {
    "detection_rules_active": 7,
    "detections_total": 42,
    "correlations_total": 0,
    "open_incidents": 0,
    "closed_incidents": 0
  }
}
```

#### View Recent Alerts
```bash
curl "http://localhost:8000/api/v1/alerts?limit=5" | jq

# Shows: Last 5 alerts with full details
```

#### View Events
```bash
curl "http://localhost:8000/api/v1/events?limit=3" | jq

# Shows: Last 3 events ingested
```

#### View Incidents
```bash
curl http://localhost:8000/api/v1/incidents | jq

# Shows: All active incidents
```

#### View Detection Rules
```bash
curl http://localhost:8000/api/v1/detection/rules | jq

# Shows: All 7 detection rules and their configurations
```

#### Get Prometheus Metrics
```bash
curl http://localhost:8000/metrics | head -30

# Shows: Prometheus format metrics
```

---

### Method 7: CLI Commands (Simple Interface)

```bash
# Overall platform status
sentinel status

# Detailed component health
sentinel health

# View active alerts
sentinel alerts --severity critical --limit 10

# View incidents
sentinel incidents --status open

# View detection rules
sentinel detections

# View threat indicators
sentinel iocs

# View events
sentinel events --hostname workstation-01 --hours 24
```

---

## 🔄 Complete Automatic Workflow

### Scenario: Run Everything Automatically

```bash
# Terminal 1: Start everything with auto mode
bash scripts/auto-start.sh
# Choose option 3 (both monitoring and simulations)

# Terminal 2: Watch simulations (optional)
tail -f /tmp/sentinel-simulation.log

# Terminal 3: View backend logs (optional)
docker compose logs -f sentinel-backend

# Browser: Open dashboards
# Grafana: http://localhost:3000
# Kibana: http://localhost:5601
# Prometheus: http://localhost:9090
```

**What happens automatically:**
1. ✅ Platform starts (all 14 services)
2. ✅ Simulations run every 30 seconds
3. ✅ Detection rules fire on generated events
4. ✅ Alerts stored in Elasticsearch
5. ✅ Metrics collected by Prometheus
6. ✅ Dashboards show live data
7. ✅ Logs streamed to console
8. ✅ Everything visible in real-time

---

## 📊 Key Metrics You'll See

### Detection Engine Metrics
- **detection_rules_active**: Number of active rules (should be 7)
- **detections_total**: Cumulative detections made
- **alerts_generated**: Total alerts created

### Alert Metrics
- **alerts_by_severity**: Distribution (critical/high/medium/low)
- **alerts_new**: Unacknowledged alerts
- **alerts_investigated**: Currently under review

### Incident Metrics
- **open_incidents**: Active incidents
- **closed_incidents**: Resolved incidents
- **incident_average_resolution_time**: How long to resolve

### System Metrics
- **cpu_usage**: Container CPU percentage
- **memory_usage**: Container memory usage
- **network_io**: Data in/out
- **container_uptime**: How long running

---

## 🎯 What Happens During Automation

### Every 30 Seconds:
1. **Simulation runs** → Generates synthetic events
2. **Detection engine** → Evaluates events against 7 rules
3. **Matching rules** → Create alerts
4. **Storage** → Alerts saved to Elasticsearch
5. **Metrics** → Counters updated in Prometheus
6. **Visualization** → Dashboards updated
7. **Logs** → Operations logged

### Example Timeline:
```
10:45:05 - Simulation starts (Brute Force scenario)
10:45:05 - 10 events generated
10:45:05 - Detection engine processes events
10:45:05 - Rule "Brute Force" matches 2 events
10:45:06 - 2 alerts created
10:45:06 - Alerts stored in Elasticsearch
10:45:07 - Metrics updated
10:45:08 - Dashboards refresh
10:45:35 - Next simulation starts
```

---

## 🛠️ Troubleshooting Visibility

### Can't see live monitor?
```bash
# Check if scripts are executable
chmod +x scripts/*.sh

# Try running with bash directly
bash scripts/live-monitor.sh
```

### Can't see logs?
```bash
# Check if Docker is running
docker ps

# View all service logs
docker compose logs

# Check specific service
docker compose logs sentinel-backend
```

### Metrics not appearing?
```bash
# Check Prometheus is scraping
curl http://localhost:9090/api/v1/targets

# Query a metric directly
curl 'http://localhost:9090/api/v1/query?query=up'
```

### No alerts showing?
```bash
# Check if backend is running
curl http://localhost:8000/health

# Run a simulation manually
curl -X POST http://localhost:8000/api/v1/simulate/brute-force

# Check alerts were created
curl http://localhost:8000/api/v1/alerts
```

---

## 📈 Performance Expectations

With automatic simulations running every 30 seconds:

- **Alerts/hour**: ~4-6 alerts per hour (from scenarios)
- **Events/hour**: ~120-140 events per hour
- **Processing latency**: <100ms per event
- **Storage**: ~10KB per event (grows over time)
- **CPU impact**: 5-10% average (under 20% peak)
- **Memory**: Stable at 2-3GB total

---

## ✅ Complete Setup Checklist

- [ ] Run `bash scripts/auto-start.sh`
- [ ] Choose monitoring mode (1, 2, 3, or 4)
- [ ] Open browser dashboards (Grafana, Kibana, Prometheus)
- [ ] Watch live monitor or tail logs in terminal
- [ ] See alerts and detections in real-time
- [ ] Query API endpoints manually
- [ ] Observe metrics in Prometheus
- [ ] View events in Kibana

---

## 🎓 Next Steps

1. **Customize**: Modify simulations in `backend/sentinel/simulation/scenarios.py`
2. **Add Rules**: Create new detection rules in `backend/sentinel/detection/engine.py`
3. **Build Dashboards**: Create custom Grafana dashboards
4. **Automate**: Create incident response playbooks
5. **Integrate**: Connect your own event sources

---

**IamZer01 Sentinel – Now Running Automatically!** 🚀
