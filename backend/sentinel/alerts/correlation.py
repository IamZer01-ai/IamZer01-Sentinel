"""
IamZer01 Sentinel – Alert Correlation and Incident Management
Groups related alerts into incidents and manages their lifecycle.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from collections import defaultdict
from sentinel.core.models import (
    Alert,
    AlertStatus,
    Incident,
    IncidentStatus,
    Severity,
)


class AlertCorrelationEngine:
    """
    Correlates alerts to detect attack patterns and group related alerts
    into incidents.
    """
    
    def __init__(self, correlation_window_seconds: int = 3600):
        self.correlation_window = timedelta(seconds=correlation_window_seconds)
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_groups: Dict[str, List[str]] = defaultdict(list)
        self.correlation_total = 0
    
    def add_alert(self, alert: Alert) -> Optional[str]:
        """
        Add alert and find correlated alerts.
        Returns the parent incident ID if correlated, None otherwise.
        """
        self.active_alerts[alert.alert_id] = alert
        
        # Find correlated alerts
        correlated = self._find_correlated_alerts(alert)
        
        if correlated:
            self.correlation_total += 1
            alert.correlated_alerts = correlated
            return self._get_group_id(alert.alert_id, correlated)
        
        return None
    
    def _find_correlated_alerts(self, alert: Alert) -> List[str]:
        """Find alerts that correlate with this alert."""
        correlated = []
        now = datetime.utcnow()
        cutoff = now - self.correlation_window
        
        # Remove old alerts
        expired = [aid for aid, a in self.active_alerts.items() if a.timestamp < cutoff]
        for aid in expired:
            del self.active_alerts[aid]
        
        # Find correlations
        for other_alert_id, other_alert in self.active_alerts.items():
            if other_alert_id == alert.alert_id:
                continue
            
            # Correlation rules
            if self._alerts_correlate(alert, other_alert):
                correlated.append(other_alert_id)
        
        return correlated
    
    def _alerts_correlate(self, alert1: Alert, alert2: Alert) -> bool:
        """Determine if two alerts are correlated."""
        
        # Same host/user correlation
        if alert1.hostname and alert2.hostname and alert1.hostname == alert2.hostname:
            return True
        
        if alert1.username and alert2.username and alert1.username == alert2.username:
            return True
        
        # Same source IP correlation
        if alert1.source_ip and alert2.source_ip and alert1.source_ip == alert2.source_ip:
            return True
        
        # Same IOC correlation
        if alert1.iocs and alert2.iocs:
            if set(alert1.iocs) & set(alert2.iocs):  # Intersection
                return True
        
        # Same MITRE technique correlation
        if alert1.mitre_techniques and alert2.mitre_techniques:
            if set(alert1.mitre_techniques) & set(alert2.mitre_techniques):
                return True
        
        return False
    
    def _get_group_id(self, alert_id: str, correlated_ids: List[str]) -> str:
        """Get or create a group ID for correlated alerts."""
        # Check if any correlated alert already has a group
        for correlated_id in correlated_ids:
            for group_id, alerts in self.alert_groups.items():
                if correlated_id in alerts:
                    if alert_id not in alerts:
                        alerts.append(alert_id)
                    return group_id
        
        # Create new group
        group_id = f"AG-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.alert_groups[group_id] = [alert_id] + correlated_ids
        return group_id
    
    def get_alert_group(self, alert_id: str) -> Optional[List[Alert]]:
        """Get all alerts in a group."""
        for group_id, alert_ids in self.alert_groups.items():
            if alert_id in alert_ids:
                return [self.active_alerts.get(aid) for aid in alert_ids if aid in self.active_alerts]
        return None


class IncidentManager:
    """
    Manages the lifecycle of security incidents, including creation,
    investigation, correlation, and resolution.
    """
    
    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.open_incidents_count = 0
        self.closed_incidents_count = 0
    
    def create_incident_from_alerts(self, alerts: List[Alert], 
                                    title: Optional[str] = None) -> Incident:
        """
        Create an incident from a group of correlated alerts.
        """
        if not alerts:
            raise ValueError("Cannot create incident without alerts")
        
        # Determine severity (highest of all alerts)
        max_severity = max(
            (a.severity for a in alerts),
            key=lambda x: self._severity_score(x),
            default=Severity.MEDIUM
        )
        
        # Collect affected entities
        affected_hosts = set()
        affected_users = set()
        all_iocs = set()
        all_techniques = set()
        event_ids = []
        
        for alert in alerts:
            if alert.hostname:
                affected_hosts.add(alert.hostname)
            if alert.username:
                affected_users.add(alert.username)
            all_iocs.update(alert.iocs)
            all_techniques.update(alert.mitre_techniques)
            event_ids.extend(alert.event_ids)
            alert.parent_incident_id = alert.alert_id  # Placeholder
        
        # Generate title if not provided
        if not title:
            title = self._generate_incident_title(alerts)
        
        # Create incident
        incident = Incident(
            title=title,
            description=f"Incident created from {len(alerts)} correlated alerts",
            severity=max_severity,
            status=IncidentStatus.OPEN,
            alert_ids=[a.alert_id for a in alerts],
            event_ids=event_ids,
            affected_hosts=affected_hosts,
            affected_users=affected_users,
            iocs=all_iocs,
            mitre_techniques=list(all_techniques),
        )
        
        # Store incident
        self.incidents[incident.incident_id] = incident
        self.open_incidents_count += 1
        
        # Link alerts to incident
        for alert in alerts:
            alert.parent_incident_id = incident.incident_id
            alert.status = AlertStatus.INVESTIGATING
        
        return incident
    
    def get_incident(self, incident_id: str) -> Optional[Incident]:
        """Get an incident by ID."""
        return self.incidents.get(incident_id)
    
    def update_incident_status(self, incident_id: str, status: IncidentStatus,
                              summary: Optional[str] = None) -> bool:
        """Update incident status."""
        incident = self.incidents.get(incident_id)
        if not incident:
            return False
        
        incident.status = status
        incident.updated = datetime.utcnow()
        
        if status == IncidentStatus.CLOSED and summary:
            incident.resolution_summary = summary
        
        # Track open/closed
        if status == IncidentStatus.CLOSED:
            self.open_incidents_count -= 1
            self.closed_incidents_count += 1
        
        return True
    
    def add_timeline_entry(self, incident_id: str, entry: Dict) -> bool:
        """Add a timeline entry to an incident."""
        incident = self.incidents.get(incident_id)
        if not incident:
            return False
        
        entry.setdefault("timestamp", datetime.utcnow().isoformat())
        incident.timeline.append(entry)
        incident.updated = datetime.utcnow()
        return True
    
    def add_action(self, incident_id: str, action: Dict) -> bool:
        """Record an action taken on an incident."""
        incident = self.incidents.get(incident_id)
        if not incident:
            return False
        
        action.setdefault("timestamp", datetime.utcnow().isoformat())
        incident.actions_taken.append(action)
        incident.updated = datetime.utcnow()
        return True
    
    def set_investigator(self, incident_id: str, investigator: str) -> bool:
        """Assign an investigator to an incident."""
        incident = self.incidents.get(incident_id)
        if not incident:
            return False
        
        incident.investigator = investigator
        incident.updated = datetime.utcnow()
        return True
    
    def get_open_incidents(self) -> List[Incident]:
        """Get all open incidents."""
        return [i for i in self.incidents.values() if i.status != IncidentStatus.CLOSED]
    
    def get_critical_incidents(self) -> List[Incident]:
        """Get all critical incidents."""
        return [i for i in self.incidents.values() if i.severity == Severity.CRITICAL]
    
    def _severity_score(self, severity: Severity) -> int:
        """Convert severity to numeric score for comparison."""
        scores = {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3,
            Severity.CRITICAL: 4,
        }
        return scores.get(severity, 0)
    
    def _generate_incident_title(self, alerts: List[Alert]) -> str:
        """Generate a descriptive incident title from alerts."""
        # Count alert types
        if len(alerts) == 1:
            return f"Incident: {alerts[0].title}"
        
        # Group by common patterns
        common_keywords = defaultdict(int)
        for alert in alerts:
            words = alert.title.lower().split()
            for word in words:
                if len(word) > 3:
                    common_keywords[word] += 1
        
        if common_keywords:
            top_keyword = max(common_keywords, key=common_keywords.get)
            return f"Multi-Alert Incident: {top_keyword.title()} Activity"
        
        return f"Multi-Alert Incident ({len(alerts)} alerts)"


class AlertDispatcher:
    """
    Routes alerts to appropriate handlers and stakeholders.
    """
    
    def __init__(self):
        self.handlers: Dict[Severity, List[callable]] = defaultdict(list)
        self.alerts_dispatched = 0
    
    def register_handler(self, severity: Severity, handler: callable) -> None:
        """Register a handler for alerts of specific severity."""
        self.handlers[severity].append(handler)
    
    def dispatch_alert(self, alert: Alert) -> None:
        """Dispatch alert to registered handlers."""
        # Call handlers for this severity
        for handler in self.handlers.get(alert.severity, []):
            try:
                handler(alert)
            except Exception as e:
                # Log but don't crash
                print(f"Handler error: {e}")
        
        # Call handlers for all severities
        for handler in self.handlers.get("all", []):
            try:
                handler(alert)
            except Exception as e:
                print(f"Handler error: {e}")
        
        self.alerts_dispatched += 1
