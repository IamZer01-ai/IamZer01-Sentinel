"""
IamZer01 Sentinel – Elasticsearch Integration
Stores and queries security events, alerts, and incidents.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
from sentinel.core.models import SecurityEvent, Alert, Incident
import json


class ElasticsearchBackend:
    """Elasticsearch backend for storing and retrieving security data."""
    
    def __init__(self, hosts: List[str] = None):
        """Initialize Elasticsearch client."""
        if hosts is None:
            hosts = ["http://elasticsearch:9200"]
        
        self.client = Elasticsearch(hosts)
        self.events_index = "sentinel-events"
        self.alerts_index = "sentinel-alerts"
        self.incidents_index = "sentinel-incidents"
        
        # Create indices if needed
        self._initialize_indices()
    
    def _initialize_indices(self) -> None:
        """Create indices with proper mappings."""
        
        # Events index
        if not self.client.indices.exists(index=self.events_index):
            self.client.indices.create(
                index=self.events_index,
                body={
                    "mappings": {
                        "properties": {
                            "event_id": {"type": "keyword"},
                            "timestamp": {"type": "date"},
                            "event_type": {"type": "keyword"},
                            "hostname": {"type": "keyword"},
                            "source_ip": {"type": "ip"},
                            "destination_ip": {"type": "ip"},
                            "username": {"type": "keyword"},
                            "severity": {"type": "keyword"},
                            "risk_score": {"type": "float"},
                            "iocs": {"type": "keyword"},
                            "mitre_techniques": {"type": "keyword"},
                        }
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                    }
                }
            )
        
        # Alerts index
        if not self.client.indices.exists(index=self.alerts_index):
            self.client.indices.create(
                index=self.alerts_index,
                body={
                    "mappings": {
                        "properties": {
                            "alert_id": {"type": "keyword"},
                            "timestamp": {"type": "date"},
                            "severity": {"type": "keyword"},
                            "status": {"type": "keyword"},
                            "hostname": {"type": "keyword"},
                            "username": {"type": "keyword"},
                            "source_ip": {"type": "ip"},
                        }
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                    }
                }
            )
        
        # Incidents index
        if not self.client.indices.exists(index=self.incidents_index):
            self.client.indices.create(
                index=self.incidents_index,
                body={
                    "mappings": {
                        "properties": {
                            "incident_id": {"type": "keyword"},
                            "created": {"type": "date"},
                            "severity": {"type": "keyword"},
                            "status": {"type": "keyword"},
                        }
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                    }
                }
            )
    
    def store_event(self, event: SecurityEvent) -> bool:
        """Store a security event."""
        try:
            self.client.index(
                index=self.events_index,
                id=event.event_id,
                body=json.loads(event.model_dump_json()),
            )
            return True
        except Exception as e:
            print(f"Error storing event: {e}")
            return False
    
    def store_alert(self, alert: Alert) -> bool:
        """Store an alert."""
        try:
            self.client.index(
                index=self.alerts_index,
                id=alert.alert_id,
                body=json.loads(alert.model_dump_json()),
            )
            return True
        except Exception as e:
            print(f"Error storing alert: {e}")
            return False
    
    def store_incident(self, incident: Incident) -> bool:
        """Store an incident."""
        try:
            self.client.index(
                index=self.incidents_index,
                id=incident.incident_id,
                body=json.loads(incident.model_dump_json()),
            )
            return True
        except Exception as e:
            print(f"Error storing incident: {e}")
            return False
    
    def search_events(self, query: Dict[str, Any], size: int = 100) -> List[Dict]:
        """Search for events."""
        try:
            result = self.client.search(
                index=self.events_index,
                body=query,
                size=size,
            )
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception as e:
            print(f"Error searching events: {e}")
            return []
    
    def search_alerts(self, query: Dict[str, Any], size: int = 100) -> List[Dict]:
        """Search for alerts."""
        try:
            result = self.client.search(
                index=self.alerts_index,
                body=query,
                size=size,
            )
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception as e:
            print(f"Error searching alerts: {e}")
            return []
    
    def get_recent_events(self, hours: int = 24) -> List[Dict]:
        """Get recent events."""
        query = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": f"now-{hours}h"
                    }
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}]
        }
        return self.search_events(query, size=1000)
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recent alerts."""
        query = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": f"now-{hours}h"
                    }
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}]
        }
        return self.search_alerts(query, size=1000)
    
    def get_events_by_host(self, hostname: str, hours: int = 24) -> List[Dict]:
        """Get events from a specific host."""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"hostname": hostname}},
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}}
                    ]
                }
            }
        }
        return self.search_events(query, size=1000)
    
    def get_events_by_user(self, username: str, hours: int = 24) -> List[Dict]:
        """Get events from a specific user."""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"username": username}},
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}}
                    ]
                }
            }
        }
        return self.search_events(query, size=1000)
    
    def get_critical_alerts(self) -> List[Dict]:
        """Get all critical alerts."""
        query = {
            "query": {
                "term": {"severity": "critical"}
            },
            "sort": [{"timestamp": {"order": "desc"}}]
        }
        return self.search_alerts(query, size=100)
    
    def count_alerts_by_severity(self, hours: int = 24) -> Dict[str, int]:
        """Count alerts by severity."""
        query = {
            "query": {
                "range": {
                    "timestamp": {"gte": f"now-{hours}h"}
                }
            },
            "aggs": {
                "by_severity": {
                    "terms": {"field": "severity", "size": 10}
                }
            }
        }
        
        try:
            result = self.client.search(index=self.alerts_index, body=query)
            counts = {}
            for bucket in result["aggregations"]["by_severity"]["buckets"]:
                counts[bucket["key"]] = bucket["doc_count"]
            return counts
        except Exception as e:
            print(f"Error counting alerts: {e}")
            return {}
