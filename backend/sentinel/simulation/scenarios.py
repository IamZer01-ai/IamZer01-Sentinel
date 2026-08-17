"""
IamZer01 Sentinel – Simulation Engine
Generates synthetic security events for testing and demonstration.
All events are clearly marked as simulated/lab data.
"""

import random
from datetime import datetime, timedelta
from typing import List
from sentinel.core.models import SecurityEvent, EventType, Severity


class SimulationEngine:
    """
    Generates safe, synthetic security events for testing detection rules
    and demonstrating SOC capabilities. All events are marked as lab/simulation.
    """
    
    def __init__(self):
        self.test_usernames = ["alice", "bob", "charlie", "testuser", "admin"]
        self.test_hostnames = ["workstation-01", "workstation-02", "server-01", "server-02", "laptop-01"]
        self.test_ips = [
            "192.168.1.100", "192.168.1.101", "192.168.1.102",
            "10.0.0.50", "10.0.0.51", "10.0.0.52",
        ]
        self.malicious_ips = [
            "203.0.113.10", "203.0.113.20", "203.0.113.30"
        ]
        self.test_processes = [
            "cmd.exe", "powershell.exe", "whoami.exe", "net.exe",
            "svchost.exe", "explorer.exe", "notepad.exe",
        ]
    
    def simulate_brute_force(self) -> List[SecurityEvent]:
        """Simulate a brute force attack."""
        events = []
        source_ip = random.choice(self.test_ips)
        target_host = random.choice(self.test_hostnames)
        target_user = random.choice(self.test_usernames)
        
        base_time = datetime.utcnow()
        for i in range(10):
            event = SecurityEvent(
                event_type=EventType.AUTHENTICATION,
                event_name="Authentication Failure",
                source="test_lab",
                hostname=target_host,
                source_ip=source_ip,
                username=target_user,
                auth_result="failure",
                severity=Severity.MEDIUM,
                environment="lab",
                labels={
                    "scenario": "brute_force",
                    "synthetic": "true",
                },
                timestamp=base_time - timedelta(seconds=30*i),
            )
            events.append(event)
        
        return events
    
    def simulate_suspicious_login(self) -> List[SecurityEvent]:
        """Simulate a suspicious/unusual login."""
        events = []
        unusual_ip = random.choice(self.malicious_ips)
        target_user = random.choice(self.test_usernames)
        target_host = random.choice(self.test_hostnames)
        
        base_time = datetime.utcnow()
        for i in range(3):
            event = SecurityEvent(
                event_type=EventType.AUTHENTICATION,
                event_name="Authentication Failure - Unusual Location",
                source="test_lab",
                hostname=target_host,
                source_ip=unusual_ip,
                username=target_user,
                auth_result="failure",
                severity=Severity.MEDIUM,
                environment="lab",
                labels={
                    "scenario": "suspicious_login",
                    "synthetic": "true",
                    "unusual_location": "true",
                },
                timestamp=base_time - timedelta(seconds=60*i),
            )
            events.append(event)
        
        event = SecurityEvent(
            event_type=EventType.AUTHENTICATION,
            event_name="Successful Login - Unusual Location",
            source="test_lab",
            hostname=target_host,
            source_ip=unusual_ip,
            username=target_user,
            auth_result="success",
            severity=Severity.HIGH,
            risk_score=75.0,
            environment="lab",
            labels={
                "scenario": "suspicious_login",
                "synthetic": "true",
                "unusual_location": "true",
            },
            timestamp=base_time,
        )
        events.append(event)
        
        return events
    
    def simulate_suspicious_process(self) -> List[SecurityEvent]:
        """Simulate execution of suspicious processes."""
        events = []
        target_host = random.choice(self.test_hostnames)
        target_user = random.choice(self.test_usernames)
        
        base_time = datetime.utcnow()
        suspicious_process = random.choice(["cmd.exe", "powershell.exe"])
        
        event = SecurityEvent(
            event_type=EventType.PROCESS,
            event_name="Suspicious Process Execution",
            source="test_lab",
            hostname=target_host,
            username=target_user,
            process_name=suspicious_process,
            process_id=random.randint(1000, 9999),
            process_cmdline=f"{suspicious_process} /c dir c:\\",
            severity=Severity.MEDIUM,
            risk_score=60.0,
            environment="lab",
            labels={
                "scenario": "suspicious_process",
                "synthetic": "true",
            },
            timestamp=base_time,
        )
        events.append(event)
        
        return events
    
    def simulate_ioc_match(self) -> List[SecurityEvent]:
        """Simulate detection of known IOC."""
        events = []
        target_host = random.choice(self.test_hostnames)
        malicious_ip = random.choice(self.malicious_ips)
        
        event = SecurityEvent(
            event_type=EventType.NETWORK,
            event_name="Known IOC Detection",
            source="test_lab",
            hostname=target_host,
            destination_ip=malicious_ip,
            destination_port=443,
            severity=Severity.CRITICAL,
            risk_score=95.0,
            iocs=[malicious_ip],
            environment="lab",
            labels={
                "scenario": "ioc_match",
                "synthetic": "true",
                "ioc_source": "test_data",
            },
            timestamp=datetime.utcnow(),
        )
        events.append(event)
        
        return events
    
    def simulate_network_anomaly(self) -> List[SecurityEvent]:
        """Simulate unusual network activity."""
        events = []
        target_host = random.choice(self.test_hostnames)
        
        base_time = datetime.utcnow()
        for i in range(20):
            target_ip = f"203.0.113.{random.randint(1, 254)}"
            
            event = SecurityEvent(
                event_type=EventType.NETWORK,
                event_name="High Volume Network Activity",
                source="test_lab",
                hostname=target_host,
                destination_ip=target_ip,
                destination_port=random.choice([80, 443, 8080, 3389]),
                protocol="TCP",
                severity=Severity.MEDIUM,
                environment="lab",
                labels={
                    "scenario": "network_anomaly",
                    "synthetic": "true",
                    "volume_test": "true",
                },
                timestamp=base_time - timedelta(seconds=i*3),
            )
            events.append(event)
        
        return events
    
    def simulate_phishing_indicator(self) -> List[SecurityEvent]:
        """Simulate phishing-related event."""
        events = []
        target_user = random.choice(self.test_usernames)
        target_host = random.choice(self.test_hostnames)
        
        event = SecurityEvent(
            event_type=EventType.APPLICATION,
            event_name="Phishing Indicator Detected",
            source="test_lab",
            hostname=target_host,
            username=target_user,
            severity=Severity.HIGH,
            risk_score=70.0,
            environment="lab",
            labels={
                "scenario": "phishing",
                "synthetic": "true",
                "vector": "email",
            },
            event_data={
                "email_domain": "legitimate-looking-domain.test",
                "sender": "no-reply@fake-bank.test",
                "subject": "Urgent: Verify Your Account",
            },
            timestamp=datetime.utcnow(),
        )
        events.append(event)
        
        return events
    
    def generate_all_scenarios(self) -> List[SecurityEvent]:
        """Generate all simulation scenarios."""
        all_events = []
        
        print("[*] Generating Brute Force scenario...")
        all_events.extend(self.simulate_brute_force())
        
        print("[*] Generating Suspicious Login scenario...")
        all_events.extend(self.simulate_suspicious_login())
        
        print("[*] Generating Suspicious Process scenario...")
        all_events.extend(self.simulate_suspicious_process())
        
        print("[*] Generating IOC Match scenario...")
        all_events.extend(self.simulate_ioc_match())
        
        print("[*] Generating Network Anomaly scenario...")
        all_events.extend(self.simulate_network_anomaly())
        
        print("[*] Generating Phishing Indicator scenario...")
        all_events.extend(self.simulate_phishing_indicator())
        
        print(f"[+] Generated {len(all_events)} synthetic events")
        return all_events
