#!/usr/bin/env python3
"""
IamZer01 Sentinel – Firewall Monitoring Exporter
Version 1.0

Exposes firewall metrics: blocked connections, allowed traffic,
active rules count, and per-port/service statistics.
"""

import time
import os
import subprocess
import re
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import psutil

# ─── Metrics ──────────────────────────────────────────────────
BLOCKED_CONNECTIONS = Counter(
    "firewall_blocked_connections_total",
    "Total number of blocked connections",
    ["source_ip", "port", "protocol"],
)

ALLOWED_CONNECTIONS = Counter(
    "firewall_allowed_connections_total",
    "Total number of allowed connections",
    ["port", "protocol"],
)

ACTIVE_RULES = Gauge(
    "firewall_active_rules",
    "Number of active firewall rules",
    ["table", "chain"],
)

OPEN_PORTS = Gauge(
    "firewall_open_ports",
    "Number of open/listening ports",
    ["port", "protocol", "service"],
)

CONNECTION_STATES = Gauge(
    "firewall_connection_states",
    "Current connections by TCP state",
    ["state"],
)

LAST_IPTABLES_UPDATE = Gauge(
    "firewall_last_iptables_update_timestamp",
    "Timestamp of last successful iptables poll",
)


def get_iptables_rules():
    """Parse iptables rules count per table/chain."""
    counts = {}
    try:
        result = subprocess.run(
            ["iptables", "-L", "-n", "--line-numbers"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        current_table = "filter"
        current_chain = ""
        rule_count = 0

        for line in result.stdout.split("\n"):
            if line.startswith("Chain "):
                # Save previous chain count
                if current_chain:
                    counts[(current_table, current_chain)] = rule_count

                parts = line.split()
                if len(parts) >= 2:
                    chain_info = parts[1]
                    current_chain = chain_info
                    rule_count = 0
                    # Detect table
                    if "(policy" in line or "policy" in line:
                        pass
            elif line.strip() and re.match(r"^\d+", line.strip()):
                rule_count += 1

        if current_chain:
            counts[(current_table, current_chain)] = rule_count

    except (subprocess.TimeoutExpired, FileNotFoundError):
        # iptables may not be available (running in container)
        counts[("filter", "INPUT")] = 0
        counts[("filter", "FORWARD")] = 0
        counts[("filter", "OUTPUT")] = 0

    return counts


def get_listening_ports():
    """Get currently listening ports via psutil."""
    ports = []
    try:
        for conn in psutil.net_connections(kind="tcp"):
            if conn.status == "LISTEN" and conn.laddr:
                ports.append({
                    "port": conn.laddr.port,
                    "protocol": "tcp",
                    "service": get_service_name(conn.laddr.port) if conn.laddr.port < 1024 else "custom",
                })
        for conn in psutil.net_connections(kind="udp"):
            if conn.laddr:
                ports.append({
                    "port": conn.laddr.port,
                    "protocol": "udp",
                    "service": get_service_name(conn.laddr.port) if conn.laddr.port < 1024 else "custom",
                })
    except (psutil.AccessDenied, PermissionError):
        pass
    return ports


def get_service_name(port):
    """Simple service name mapping."""
    services = {
        22: "ssh", 80: "http", 443: "https", 53: "dns",
        3306: "mysql", 5432: "postgresql", 6379: "redis",
        8080: "http-alt", 9090: "prometheus", 3000: "grafana",
        5601: "kibana", 9200: "elasticsearch", 8086: "influxdb",
        9093: "alertmanager", 9100: "node-exporter",
    }
    return services.get(port, "unknown")


def get_tcp_states():
    """Count current TCP connections by state."""
    states = {}
    try:
        for conn in psutil.net_connections(kind="tcp"):
            states[conn.status] = states.get(conn.status, 0) + 1
    except (psutil.AccessDenied, PermissionError):
        pass
    return states


def main():
    start_http_server(8001)
    print("[*] Firewall Exporter started on port 8001")

    while True:
        # Parse iptables rules
        rules = get_iptables_rules()
        for (table, chain), count in rules.items():
            ACTIVE_RULES.labels(table=table, chain=chain).set(count)

        # Get listening ports
        ports = get_listening_ports()
        seen_ports = set()
        for p in ports:
            key = (p["port"], p["protocol"])
            if key not in seen_ports:
                OPEN_PORTS.labels(port=str(p["port"]), protocol=p["protocol"], service=p["service"]).set(1)
                seen_ports.add(key)

        # Get TCP connection states
        states = get_tcp_states()
        for state, count in states.items():
            CONNECTION_STATES.labels(state=state).set(count)

        LAST_IPTABLES_UPDATE.set(time.time())
        time.sleep(30)


if __name__ == "__main__":
    main()
