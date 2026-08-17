"""
IamZer01 Sentinel – Detection Engine
Implements rule-based detection and alert generation for security events.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
import re
from sentinel.core.models import (
    SecurityEvent,
    DetectionRule,
    Alert,
    AlertStatus,
    Severity,
    EventType,
    IOCType,
)


class RuleConditionMatcher:
    """Evaluates rule conditions against events."""
    
    @staticmethod
    def match_field(event: SecurityEvent, field_path: str, condition: Any) -> bool:
        """Match a single field against a condition."""
        value = RuleConditionMatcher.get_field_value(event, field_path)
        
        if isinstance(condition, dict):
            # Handle operators
            if "equals" in condition:
                return value == condition["equals"]
            elif "contains" in condition:
                if value is None:
                    return False
                return condition["contains"].lower() in str(value).lower()
            elif "regex" in condition:
                if value is None:
                    return False
                return bool(re.search(condition["regex"], str(value)))
            elif "greater_than" in condition:
                return value and value > condition["greater_than"]
            elif "less_than" in condition:
                return value and value < condition["less_than"]
            elif "in" in condition:
                return value in condition["in"]
            elif "not_in" in condition:
                return value not in condition["not_in"]
        else:
            # Simple equality
            return value == condition
        
        return False
    
    @staticmethod
    def get_field_value(event: SecurityEvent, field_path: str) -> Any:
        """Get value from event using dot notation."""
        parts = field_path.split(".")
        value = event
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = getattr(value, part, None)
            
            if value is None:
                return None
        
        return value
    
    @staticmethod
    def evaluate_conditions(event: SecurityEvent, conditions: Dict[str, Any]) -> bool:
        """Evaluate all conditions (AND logic by default)."""
        for field, condition in conditions.items():
            if not RuleConditionMatcher.match_field(event, field, condition):
                return False
        return True


class AggregationWindow:
    """Tracks events within a time window for threshold-based detection."""
    
    def __init__(self, rule_id: str, time_window_seconds: int, threshold: int):
        self.rule_id = rule_id
        self.time_window = timedelta(seconds=time_window_seconds)
        self.threshold = threshold
        self.events: List[SecurityEvent] = []
    
    def add_event(self, event: SecurityEvent) -> bool:
        """Add event and check if threshold is met."""
        now = datetime.utcnow()
        
        # Remove old events outside window
        cutoff = now - self.time_window
        self.events = [e for e in self.events if e.timestamp > cutoff]
        
        # Add new event
        self.events.append(event)
        
        # Check threshold
        return len(self.events) >= self.threshold
    
    def reset(self):
        """Reset the aggregation window."""
        self.events.clear()


class DetectionEngine:
    """
    Core detection engine that evaluates rules against events.
    Generates alerts when rules are matched.
    """
    
    def __init__(self):
        self.rules: Dict[str, DetectionRule] = {}
        self.aggregation_windows: Dict[str, AggregationWindow] = {}
        self.detections_total = 0
    
    def register_rule(self, rule: DetectionRule) -> None:
        """Register a detection rule."""
        if rule.enabled:
            self.rules[rule.rule_id] = rule
    
    def deregister_rule(self, rule_id: str) -> None:
        """Unregister a detection rule."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            # Clean up aggregation window
            if rule_id in self.aggregation_windows:
                del self.aggregation_windows[rule_id]
    
    def evaluate_event(self, event: SecurityEvent) -> List[Alert]:
        """
        Evaluate an event against all active rules.
        Returns list of generated alerts.
        """
        alerts: List[Alert] = []
        
        for rule_id, rule in self.rules.items():
            if not rule.enabled:
                continue
            
            # Check event type match
            if rule.event_type != event.event_type:
                continue
            
            # Evaluate conditions
            if RuleConditionMatcher.evaluate_conditions(event, rule.conditions):
                # Handle threshold-based detection
                if rule.threshold and rule.time_window:
                    alert = self._handle_threshold_detection(event, rule)
                    if alert:
                        alerts.append(alert)
                else:
                    # Immediate detection
                    alert = self._create_alert_from_rule(event, rule)
                    alerts.append(alert)
                
                self.detections_total += 1
        
        return alerts
    
    def _handle_threshold_detection(self, event: SecurityEvent, rule: DetectionRule) -> Optional[Alert]:
        """Handle detection with aggregation."""
        rule_id = rule.rule_id
        
        # Initialize window if needed
        if rule_id not in self.aggregation_windows:
            self.aggregation_windows[rule_id] = AggregationWindow(
                rule_id, rule.time_window, rule.threshold
            )
        
        window = self.aggregation_windows[rule_id]
        
        # Check if threshold met
        if window.add_event(event):
            alert = self._create_alert_from_rule(event, rule)
            alert.event_ids = [e.event_id for e in window.events]
            window.reset()
            return alert
        
        return None
    
    def _create_alert_from_rule(self, event: SecurityEvent, rule: DetectionRule) -> Alert:
        """Create an alert from a matched rule."""
        alert = Alert(
            title=f"[{rule.severity.upper()}] {rule.name}",
            description=rule.description,
            severity=rule.severity,
            status=AlertStatus.NEW,
            event_ids=[event.event_id],
            rule_id=rule.rule_id,
            hostname=event.hostname,
            source_ip=event.source_ip,
            username=event.username,
            mitre_techniques=rule.mitre_techniques,
            iocs=event.iocs,
            recommended_action=self._get_recommended_action(rule.name, event),
        )
        
        return alert
    
    def _get_recommended_action(self, rule_name: str, event: SecurityEvent) -> Optional[str]:
        """Generate recommended action based on rule and event."""
        actions = {
            "Brute Force": f"Block source IP {event.source_ip} if confirmed. Review authentication logs.",
            "Suspicious Process": f"Quarantine process on {event.hostname} if confirmed.",
            "IOC Match": f"Block indicator {event.iocs[0] if event.iocs else 'N/A'} network-wide.",
            "Unusual Login": f"Contact user {event.username} to verify activity.",
            "Excessive Network Activity": f"Review connections from {event.source_ip}.",
        }
        
        for keyword, action in actions.items():
            if keyword.lower() in rule_name.lower():
                return action
        
        return "Review alert evidence and investigate."


# ─────────────────────────────────────────────────────────────
# Built-in Detection Rules
# ─────────────────────────────────────────────────────────────

def create_builtin_rules() -> List[DetectionRule]:
    """Create a set of common detection rules."""
    
    rules = [
        # Brute Force Detection
        DetectionRule(
            name="Brute Force - Multiple Failed Logins",
            description="Detects multiple failed authentication attempts from same source",
            severity=Severity.HIGH,
            event_type=EventType.AUTHENTICATION,
            conditions={
                "auth_result": "failure",
            },
            threshold=5,
            time_window=300,  # 5 minutes
            mitre_techniques=["T1110"],  # Brute Force
        ),
        
        # Suspicious Process
        DetectionRule(
            name="Suspicious Process Execution",
            description="Detects execution of suspicious processes",
            severity=Severity.MEDIUM,
            event_type=EventType.PROCESS,
            conditions={
                "process_name": {"in": ["cmd.exe", "powershell.exe", "whoami.exe", "net.exe"]},
            },
            mitre_techniques=["T1059"],  # Command and Scripting Interpreter
        ),
        
        # Unusual Login Time
        DetectionRule(
            name="Unusual Login Time",
            description="Detects login attempts at unusual hours",
            severity=Severity.MEDIUM,
            event_type=EventType.AUTHENTICATION,
            conditions={
                "auth_result": "success",
            },
            mitre_techniques=["T1021"],  # Remote Services
        ),
        
        # IOC Match
        DetectionRule(
            name="Known IOC Detection",
            description="Detects connections to known malicious IPs or domains",
            severity=Severity.CRITICAL,
            event_type=EventType.NETWORK,
            conditions={
                "destination_ip": {"regex": ".*"},  # Will be enhanced by IOC matcher
            },
            mitre_techniques=["T1071"],  # Application Layer Protocol
        ),
        
        # Excessive Network Activity
        DetectionRule(
            name="Excessive Network Activity",
            description="Detects host with unusually high network activity",
            severity=Severity.MEDIUM,
            event_type=EventType.NETWORK,
            conditions={
                "protocol": {"in": ["TCP", "UDP"]},
            },
            threshold=100,
            time_window=60,
            mitre_techniques=["T1041"],  # Exfiltration Over C2 Channel
        ),
        
        # Firewall Block
        DetectionRule(
            name="Firewall Block - Suspicious Traffic",
            description="Detects firewall blocks of suspicious traffic",
            severity=Severity.LOW,
            event_type=EventType.FIREWALL,
            conditions={
                "event_type": {"equals": "firewall"},
            },
        ),
        
        # Privilege Escalation Attempt
        DetectionRule(
            name="Privilege Escalation Attempt",
            description="Detects attempts to escalate privileges",
            severity=Severity.HIGH,
            event_type=EventType.PROCESS,
            conditions={
                "process_name": {"contains": "sudo"},
            },
            mitre_techniques=["T1548"],  # Abuse Elevation Control Mechanism
        ),
    ]
    
    return rules
