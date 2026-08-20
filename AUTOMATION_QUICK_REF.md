# 🚀 IamZer01 Sentinel – Automatic Execution Quick Reference

## ONE-COMMAND STARTUP

```bash
cd /workspaces/IamZer01-Sentinel && bash scripts/auto-start.sh
```

Then choose:
- **Option 1** → Live monitor (real-time dashboard)
- **Option 2** → Auto simulations (background)
- **Option 3** → Both (recommended)
- **Option 4** → Manual (for advanced users)

---

## VIEW EXECUTION (5 Ways)

### 🖥️ Live Dashboard (Recommended - Auto-Refreshes Every 5 Seconds)
```bash
bash scripts/live-monitor.sh
```
**Shows:** Health, stats, recent alerts, events, services
**Stop:** `Ctrl+C`

### 🎬 Automated Simulations (Runs Every 30 Seconds in Background)
```bash
bash scripts/auto-simulate.sh
```
**Watch it:** `tail -f /tmp/sentinel-simulation.log`
**Stop:** `Ctrl+C`

### 📝 Backend Logs (Real Processing)
```bash
docker compose logs -f sentinel-backend
```
**Stop:** `Ctrl+C`

### 🌐 Web Dashboards (Open in Browser)
| Dashboard | URL |
|-----------|-----|
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Kibana | http://localhost:5601 |
| API Docs | http://localhost:8000/docs |

### 🔌 API Queries (Terminal)
```bash
# Check status
curl http://localhost:8000/status | jq

# View alerts
curl http://localhost:8000/api/v1/alerts | jq

# View events
curl http://localhost:8000/api/v1/events | jq

# View incidents
curl http://localhost:8000/api/v1/incidents | jq
```

---

## WHAT HAPPENS AUTOMATICALLY

```
Every 30 Seconds:
┌─────────────────────────────────────────┐
│ 1. Simulation generates events          │
│ 2. Detection engine processes them      │
│ 3. Rules match & create alerts          │
│ 4. Alerts stored in Elasticsearch       │
│ 5. Metrics updated in Prometheus        │
│ 6. Dashboards refresh                   │
│ 7. Logs show everything                 │
└─────────────────────────────────────────┘
```

---

## REAL-TIME EXECUTION EXAMPLE

### Before (Empty Platform)
```
Detections: 0
Alerts: 0
Incidents: 0
```

### Simulation Runs
```
$ curl -X POST http://localhost:8000/api/v1/simulate/brute-force
{
  "scenario": "brute_force",
  "events_generated": 10,
  "alerts_generated": 2,
  "timestamp": "2026-08-17T10:45:23"
}
```

### After (Instantly Updated)
```
Detections: 20
Alerts: 2
Incidents: 0  (correlating...)
```

---

## AUTOMATION WORKFLOW (Complete)

```bash
# Terminal 1: Start everything
bash scripts/auto-start.sh
# Choose: Option 3 (both monitoring and simulations)

# Terminal 2 (optional): Watch simulations
tail -f /tmp/sentinel-simulation.log

# Terminal 3 (optional): Watch backend logs
docker compose logs -f sentinel-backend

# Browser: Open dashboards
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
# Kibana: http://localhost:5601
```

---

## KEY COMMANDS SUMMARY

| Task | Command |
|------|---------|
| **Start Everything** | `bash scripts/auto-start.sh` |
| **Live Monitor** | `bash scripts/live-monitor.sh` |
| **Auto Simulations** | `bash scripts/auto-simulate.sh` |
| **Backend Logs** | `docker compose logs -f sentinel-backend` |
| **All Logs** | `docker compose logs -f` |
| **Check Status** | `curl http://localhost:8000/status \| jq` |
| **View Alerts** | `curl http://localhost:8000/api/v1/alerts \| jq` |
| **Stop Services** | `docker compose down` |
| **View Simulation Log** | `tail -f /tmp/sentinel-simulation.log` |

---

## DEMO: What You'll See

### Before Running Simulation
```
Platform Status:
  Detection Rules: 7 active
  Detections Made: 40
  Alerts: 4
  Incidents: 0
```

### Run Simulation
```bash
curl -X POST http://localhost:8000/api/v1/simulate/brute-force
```

### Instantly After (Within 1-2 Seconds)
```
Platform Status:
  Detection Rules: 7 active
  Detections Made: 60 (+20 new)
  Alerts: 6 (+2 new)
  Incidents: 0
```

---

## WHAT GETS AUTOMATED

✅ Event generation (security scenarios)
✅ Detection rule evaluation
✅ Alert generation
✅ Alert storage
✅ Metrics collection
✅ Dashboard updates
✅ Logging
✅ Health checks
✅ Service monitoring

---

## OUTPUT LOCATIONS

| What | Where | Command |
|------|-------|---------|
| **Live Dashboard** | Terminal | `bash scripts/live-monitor.sh` |
| **Simulation Log** | File | `tail -f /tmp/sentinel-simulation.log` |
| **Backend Logs** | Terminal | `docker compose logs -f sentinel-backend` |
| **Alerts** | API | `curl http://localhost:8000/api/v1/alerts` |
| **Events** | Elasticsearch/API | `curl http://localhost:8000/api/v1/events` |
| **Dashboards** | Browser | http://localhost:3000 (Grafana) |
| **Metrics** | Browser | http://localhost:9090 (Prometheus) |
| **Logs** | Browser | http://localhost:5601 (Kibana) |

---

## AUTO-START FLOW

```
1. Run: bash scripts/auto-start.sh
   ↓
2. Starts 14 Docker services
   ↓
3. Verifies health (wait ~10s)
   ↓
4. Shows access points & options
   ↓
5. You choose monitoring mode
   ├─ Option 1: Live monitor in terminal
   ├─ Option 2: Background simulations
   ├─ Option 3: Both (recommended)
   └─ Option 4: Manual mode
   ↓
6. Platform runs automatically
   ↓
7. Everything visible in real-time
```

---

## MONITORING MODES EXPLAINED

### Mode 1: Live Dashboard
- Real-time metrics (refresh every 5s)
- One terminal showing everything
- Best for: Watching platform activity

### Mode 2: Background Simulations
- Runs in background
- Log file updates with events
- Best for: Continuous testing while working

### Mode 3: Both (Recommended)
- Live dashboard + background simulations
- Complete visibility + continuous testing
- Best for: Complete automation & monitoring

### Mode 4: Manual
- You run commands as needed
- Full control
- Best for: Advanced users

---

## QUICK TEST

```bash
# 1. Open terminal
bash scripts/live-monitor.sh

# 2. In another terminal, run:
curl -X POST http://localhost:8000/api/v1/simulate/brute-force

# 3. Watch the live monitor update with:
#    - Detections increased
#    - Alerts appeared
#    - Events shown
```

---

## TROUBLESHOOTING

### Can't see live monitor?
```bash
chmod +x scripts/live-monitor.sh
bash scripts/live-monitor.sh
```

### Simulations not running?
```bash
# Check if backend is ready
curl http://localhost:8000/health

# Run simulation manually
curl -X POST http://localhost:8000/api/v1/simulate/brute-force
```

### No logs appearing?
```bash
# Check Docker is running
docker ps

# View service logs
docker compose logs -f
```

---

## COMPLETE DOCUMENTATION

- **AUTOMATION_GUIDE.md** – Detailed automation guide
- **QUICK_START.md** – Getting started
- **IMPLEMENTATION.md** – Architecture details
- **README.md** – Feature overview

---

## ONE-LINER COMMANDS

```bash
# Run everything automatically
bash scripts/auto-start.sh

# Watch platform activity live
bash scripts/live-monitor.sh

# Run continuous simulations
bash scripts/auto-simulate.sh

# Check what's happening (API)
curl http://localhost:8000/status | jq

# View recent alerts
curl http://localhost:8000/api/v1/alerts | jq '.alerts[] | {title, severity}'

# View events count
curl http://localhost:8000/api/v1/events | jq '.count'

# Run single simulation
curl -X POST http://localhost:8000/api/v1/simulate/brute-force | jq

# View all detection rules
curl http://localhost:8000/api/v1/detection/rules | jq

# View open incidents
curl http://localhost:8000/api/v1/incidents | jq '.incidents[] | {title, status}'
```

---

**IamZer01 Sentinel – Ready to Run Automatically!** 🚀
