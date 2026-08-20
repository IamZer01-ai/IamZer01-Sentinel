"""
IamZer01 Sentinel – FastAPI Backend Service
REST API for the Sentinel SOC platform.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
import logging

# Import Sentinel components
from sentinel.core.models import (
    SecurityEvent,
    Alert,
    Incident,
    Severity,
    IOC,
    EventType,
)
from sentinel.detection.engine import DetectionEngine, create_builtin_rules
from sentinel.alerts.correlation import AlertCorrelationEngine, IncidentManager, AlertDispatcher
from sentinel.storage.elasticsearch import ElasticsearchBackend
from sentinel.simulation.scenarios import SimulationEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="IamZer01 Sentinel API",
    description="Personal SOC Platform API",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Sentinel components
detection_engine = DetectionEngine()
correlation_engine = AlertCorrelationEngine()
incident_manager = IncidentManager()
dispatcher = AlertDispatcher()
es_backend = ElasticsearchBackend()
simulation_engine = SimulationEngine()

# Register built-in rules
for rule in create_builtin_rules():
    detection_engine.register_rule(rule)

logger.info(f"Loaded {len(detection_engine.rules)} detection rules")


# ─────────────────────────────────────────────────────────────
# Health and Status Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "detection_engine": "healthy",
            "correlation_engine": "healthy",
            "incident_manager": "healthy",
            "elasticsearch": "healthy",
        }
    }


@app.get("/status")
async def get_status():
    """Get overall Sentinel status."""
    return {
        "status": "operational",
        "version": "1.0.0",
        "components": {
            "detection_rules_active": len(detection_engine.rules),
            "detections_total": detection_engine.detections_total,
            "correlations_total": correlation_engine.correlation_total,
            "open_incidents": incident_manager.open_incidents_count,
            "closed_incidents": incident_manager.closed_incidents_count,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────────────────────────
# Event Processing Endpoints
# ─────────────────────────────────────────────────────────────

@app.post("/api/v1/events")
async def ingest_event(event: SecurityEvent):
    """Ingest a security event and run detection."""
    try:
        # Store event
        es_backend.store_event(event)
        logger.info(f"Stored event: {event.event_id}")
        
        # Run detection
        alerts = detection_engine.evaluate_event(event)
        logger.info(f"Generated {len(alerts)} alerts from event")
        
        # Correlate alerts and create incidents
        for alert in alerts:
            correlated = correlation_engine.add_alert(alert)
            if correlated:
                logger.info(f"Alert {alert.alert_id} correlated with group {correlated}")
            
            es_backend.store_alert(alert)
        
        return {
            "event_id": event.event_id,
            "alerts_generated": len(alerts),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error ingesting event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/events")
async def search_events(
    hostname: Optional[str] = None,
    username: Optional[str] = None,
    hours: int = Query(24, ge=1, le=168),
    limit: int = Query(100, ge=1, le=1000),
):
    """Search for events."""
    try:
        if hostname:
            events = es_backend.get_events_by_host(hostname, hours)
        elif username:
            events = es_backend.get_events_by_user(username, hours)
        else:
            events = es_backend.get_recent_events(hours)
        
        return {
            "count": len(events),
            "events": events[:limit],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error searching events: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Alert Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/api/v1/alerts")
async def get_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    hours: int = Query(24, ge=1, le=168),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get alerts."""
    try:
        alerts = es_backend.get_recent_alerts(hours)
        
        # Filter if needed
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        if status:
            alerts = [a for a in alerts if a.get("status") == status]
        
        return {
            "count": len(alerts),
            "alerts": alerts[:limit],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/alerts/critical")
async def get_critical_alerts(limit: int = Query(50, ge=1, le=1000)):
    """Get critical alerts."""
    try:
        alerts = es_backend.get_critical_alerts()
        return {
            "count": len(alerts),
            "alerts": alerts[:limit],
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error getting critical alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Incident Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/api/v1/incidents")
async def get_incidents():
    """Get all incidents."""
    incidents = incident_manager.get_open_incidents()
    return {
        "count": len(incidents),
        "incidents": [i.model_dump() for i in incidents],
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/incidents/critical")
async def get_critical_incidents():
    """Get critical incidents."""
    incidents = incident_manager.get_critical_incidents()
    return {
        "count": len(incidents),
        "incidents": [i.model_dump() for i in incidents],
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """Get a specific incident."""
    incident = incident_manager.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident.model_dump()


# ─────────────────────────────────────────────────────────────
# Detection Engine Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/api/v1/detection/rules")
async def get_detection_rules():
    """Get all active detection rules."""
    rules = []
    for rule_id, rule in detection_engine.rules.items():
        rules.append({
            "rule_id": rule_id,
            "name": rule.name,
            "enabled": rule.enabled,
            "severity": rule.severity,
            "mitre_techniques": rule.mitre_techniques,
        })
    return {
        "count": len(rules),
        "rules": rules,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────────────────────────
# Simulation Endpoints
# ─────────────────────────────────────────────────────────────

@app.post("/api/v1/simulate/brute-force")
async def simulate_brute_force():
    """Generate brute force simulation events."""
    try:
        events = simulation_engine.simulate_brute_force()
        
        # Ingest simulated events
        for event in events:
            alerts = detection_engine.evaluate_event(event)
            for alert in alerts:
                es_backend.store_alert(alert)
        
        return {
            "scenario": "brute_force",
            "events_generated": len(events),
            "alerts_generated": sum(len(detection_engine.evaluate_event(e)) for e in events),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/simulate/suspicious-login")
async def simulate_suspicious_login():
    """Generate suspicious login simulation events."""
    try:
        events = simulation_engine.simulate_suspicious_login()
        
        for event in events:
            es_backend.store_event(event)
        
        return {
            "scenario": "suspicious_login",
            "events_generated": len(events),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/simulate/all-scenarios")
async def simulate_all_scenarios():
    """Generate all simulation scenarios."""
    try:
        events = simulation_engine.generate_all_scenarios()
        
        total_alerts = 0
        for event in events:
            es_backend.store_event(event)
            alerts = detection_engine.evaluate_event(event)
            for alert in alerts:
                es_backend.store_alert(alert)
            total_alerts += len(alerts)
        
        return {
            "scenarios": "all",
            "events_generated": len(events),
            "alerts_generated": total_alerts,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Metrics Endpoint
# ─────────────────────────────────────────────────────────────

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    try:
        alert_severity = es_backend.count_alerts_by_severity(hours=24)
        
        output = []
        output.append(f"# HELP sentinel_detections_total Total number of detections")
        output.append(f"# TYPE sentinel_detections_total counter")
        output.append(f"sentinel_detections_total {detection_engine.detections_total}")
        
        output.append(f"# HELP sentinel_correlations_total Total number of correlations")
        output.append(f"# TYPE sentinel_correlations_total counter")
        output.append(f"sentinel_correlations_total {correlation_engine.correlation_total}")
        
        output.append(f"# HELP sentinel_open_incidents Number of open incidents")
        output.append(f"# TYPE sentinel_open_incidents gauge")
        output.append(f"sentinel_open_incidents {incident_manager.open_incidents_count}")
        
        output.append(f"# HELP sentinel_alerts_by_severity Count of alerts by severity")
        output.append(f"# TYPE sentinel_alerts_by_severity gauge")
        for severity, count in alert_severity.items():
            output.append(f'sentinel_alerts_by_severity{{severity="{severity}"}} {count}')
        
        return "\n".join(output)
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        return ""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
