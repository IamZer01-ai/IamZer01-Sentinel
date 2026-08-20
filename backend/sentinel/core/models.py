"""
IamZer01 Sentinel – Core Data Models
Defines the fundamental data structures for events, alerts, incidents, and IOCs.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class Severity(str, Enum):
    """Alert and incident severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    """Types of security events."""
    AUTHENTICATION = "authentication"
    NETWORK = "network"
    PROCESS = "process"
    FILE = "file"
    REGISTRY = "registry"
    SYSTEM = "system"
    FIREWALL = "firewall"
    APPLICATION = "application"
    THREAT = "threat"


class AlertStatus(str, Enum):
    """Alert status throughout its lifecycle."""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class IncidentStatus(str, Enum):
    """Incident lifecycle status."""
    OPEN = "open"
    TRIAGE = "triage"
    INVESTIGATING = "investigating"
    CONTAINMENT = "containment"
    RESOLUTION = "resolution"
    CLOSED = "closed"


class IOCType(str, Enum):
    """Types of Indicators of Compromise."""
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    PROCESS_NAME = "process_name"
    REGISTRY_KEY = "registry_key"
    FILENAME = "filename"


# ─────────────────────────────────────────────────────────────
# Core Security Event Model
# ─────────────────────────────────────────────────────────────

class SecurityEvent(BaseModel):
    """Normalized security event schema."""
    
    # Identifiers
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique event ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    
    # Event classification
    event_type: EventType = Field(..., description="Type of event")
    event_name: str = Field(..., description="Human-readable event name")
    source: str = Field(..., description="Event source (system, application, etc)")
    
    # Host information
    hostname: Optional[str] = Field(None, description="Hostname where event occurred")
    host_ip: Optional[str] = Field(None, description="IP address of host")
    
    # Network information
    source_ip: Optional[str] = Field(None, description="Source IP address")
    source_port: Optional[int] = Field(None, description="Source port")
    destination_ip: Optional[str] = Field(None, description="Destination IP address")
    destination_port: Optional[int] = Field(None, description="Destination port")
    protocol: Optional[str] = Field(None, description="Network protocol (TCP, UDP, etc)")
    
    # User and authentication
    username: Optional[str] = Field(None, description="Username associated with event")
    user_domain: Optional[str] = Field(None, description="User domain/realm")
    auth_result: Optional[str] = Field(None, description="Authentication result (success, failure)")
    
    # Process information
    process_name: Optional[str] = Field(None, description="Process name")
    process_id: Optional[int] = Field(None, description="Process ID")
    process_parent_id: Optional[int] = Field(None, description="Parent process ID")
    process_path: Optional[str] = Field(None, description="Full process path")
    process_cmdline: Optional[str] = Field(None, description="Process command line")
    
    # File and system activity
    file_path: Optional[str] = Field(None, description="File path")
    file_hash: Optional[str] = Field(None, description="File hash (MD5, SHA1, SHA256)")
    registry_key: Optional[str] = Field(None, description="Registry key path")
    
    # Security context
    severity: Optional[Severity] = Field(None, description="Event severity")
    risk_score: Optional[float] = Field(None, ge=0, le=100, description="Risk score 0-100")
    
    # Detection and enrichment
    detection_rule: Optional[str] = Field(None, description="Detection rule that matched")
    iocs: List[str] = Field(default_factory=list, description="Indicators of Compromise matched")
    mitre_techniques: List[str] = Field(default_factory=list, description="MITRE ATT&CK techniques")
    
    # Raw and metadata
    raw_event: Optional[str] = Field(None, description="Raw event data")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Additional event data")
    labels: Dict[str, str] = Field(default_factory=dict, description="Custom labels")
    
    # Environment
    environment: str = Field(default="production", description="Environment (production, lab, test)")
    
    class Config:
        use_enum_values = True


# ─────────────────────────────────────────────────────────────
# Detection and Alert Models
# ─────────────────────────────────────────────────────────────

class DetectionRule(BaseModel):
    """A security detection rule."""
    
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(...)
    enabled: bool = Field(default=True)
    severity: Severity = Field(...)
    
    # Detection logic
    event_type: EventType = Field(...)
    conditions: Dict[str, Any] = Field(..., description="Conditions to match")
    threshold: Optional[int] = Field(None, description="Number of events to trigger")
    time_window: Optional[int] = Field(None, description="Time window in seconds")
    
    # Metadata
    mitre_techniques: List[str] = Field(default_factory=list)
    false_positive_rate: Optional[float] = Field(None, description="Known FP rate 0-100")
    author: str = Field(default="Sentinel")
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


class Alert(BaseModel):
    """A security alert generated from an event or rule match."""
    
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Alert content
    title: str = Field(...)
    description: str = Field(...)
    severity: Severity = Field(...)
    status: AlertStatus = Field(default=AlertStatus.NEW)
    
    # Related event and rule
    event_ids: List[str] = Field(default_factory=list, description="Related event IDs")
    rule_id: Optional[str] = Field(None)
    
    # Context
    hostname: Optional[str] = Field(None)
    source_ip: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    
    # Technical details
    mitre_techniques: List[str] = Field(default_factory=list)
    iocs: List[str] = Field(default_factory=list)
    
    # Investigation
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_action: Optional[str] = Field(None)
    
    # Correlation
    correlated_alerts: List[str] = Field(default_factory=list, description="Related alert IDs")
    parent_incident_id: Optional[str] = Field(None)
    
    # Lifecycle
    acknowledged_at: Optional[datetime] = Field(None)
    resolved_at: Optional[datetime] = Field(None)
    investigation_notes: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


# ─────────────────────────────────────────────────────────────
# Incident Models
# ─────────────────────────────────────────────────────────────

class Incident(BaseModel):
    """A security incident aggregating multiple alerts."""
    
    incident_id: str = Field(default_factory=lambda: f"IR-{uuid.uuid4().hex[:8].upper()}")
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    
    # Incident details
    title: str = Field(...)
    description: str = Field(default="")
    severity: Severity = Field(...)
    status: IncidentStatus = Field(default=IncidentStatus.OPEN)
    
    # Related entities
    alert_ids: List[str] = Field(default_factory=list)
    event_ids: List[str] = Field(default_factory=list)
    affected_hosts: Set[str] = Field(default_factory=set)
    affected_users: Set[str] = Field(default_factory=set)
    iocs: Set[str] = Field(default_factory=set)
    
    # Analysis
    mitre_techniques: List[str] = Field(default_factory=list)
    root_cause: Optional[str] = Field(None)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Resolution
    resolution_summary: Optional[str] = Field(None)
    lessons_learned: Optional[str] = Field(None)
    
    # Metadata
    reporter: str = Field(default="system")
    investigator: Optional[str] = Field(None)
    
    class Config:
        use_enum_values = True


# ─────────────────────────────────────────────────────────────
# Threat Intelligence Models
# ─────────────────────────────────────────────────────────────

class IOC(BaseModel):
    """An Indicator of Compromise."""
    
    ioc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ioc_type: IOCType = Field(...)
    ioc_value: str = Field(..., description="The actual indicator value")
    
    # Context
    severity: Severity = Field(default=Severity.MEDIUM)
    source: str = Field(..., description="Source of the IOC")
    confidence: int = Field(default=80, ge=0, le=100)
    description: Optional[str] = Field(None)
    
    # Tracking
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    expiration: Optional[datetime] = Field(None)
    
    # Related
    mitre_techniques: List[str] = Field(default_factory=list)
    campaign: Optional[str] = Field(None)
    threat_actor: Optional[str] = Field(None)
    
    # Tags
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class ThreatIntel(BaseModel):
    """Threat intelligence enrichment data."""
    
    intel_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Subject
    indicator: str = Field(...)
    indicator_type: str = Field(...)
    
    # Enrichment data
    is_malicious: bool = Field(default=False)
    threat_level: Optional[Severity] = Field(None)
    reputation_score: Optional[float] = Field(None, ge=0, le=100)
    
    # Details
    threat_actors: List[str] = Field(default_factory=list)
    malware_families: List[str] = Field(default_factory=list)
    campaigns: List[str] = Field(default_factory=list)
    
    # Sources
    sources: List[str] = Field(default_factory=list)
    report_links: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


# ─────────────────────────────────────────────────────────────
# Pipeline Status and Health Models
# ─────────────────────────────────────────────────────────────

class PipelineHealth(BaseModel):
    """Health status of Sentinel components."""
    
    component: str = Field(...)
    status: str = Field(...)  # "healthy", "degraded", "unhealthy"
    last_update: datetime = Field(default_factory=datetime.utcnow)
    
    # Metrics
    events_processed: int = Field(default=0)
    errors: int = Field(default=0)
    latency_ms: Optional[float] = Field(None)
    
    # Details
    message: Optional[str] = Field(None)
    details: Dict[str, Any] = Field(default_factory=dict)
