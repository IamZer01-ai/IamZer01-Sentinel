#!/usr/bin/env python3
"""
IamZer01 Sentinel – Vulnerability Monitoring Exporter
Version 1.0

Exposes vulnerability metrics from CVE feeds and
local vulnerability databases.
"""

import time
import json
import os
from urllib.request import urlopen
from prometheus_client import start_http_server, Gauge, Counter

# ─── Metrics ──────────────────────────────────────────────────
VULN_CRITICAL = Gauge(
    "vuln_critical_count", "Number of critical severity vulnerabilities"
)

VULN_HIGH = Gauge(
    "vuln_high_count", "Number of high severity vulnerabilities"
)

VULN_MEDIUM = Gauge(
    "vuln_medium_count", "Number of medium severity vulnerabilities"
)

VULN_LOW = Gauge(
    "vuln_low_count", "Number of low severity vulnerabilities"
)

VULN_BY_CATEGORY = Gauge(
    "vuln_by_category",
    "Vulnerabilities grouped by category",
    ["category"],
)

VULN_TOTAL = Gauge(
    "vuln_total_count", "Total number of tracked vulnerabilities"
)

VULN_FETCH_ERRORS = Counter(
    "vuln_fetch_errors_total",
    "Total number of errors fetching vulnerability data",
    ["source"],
)

CVE_DB_PATH = os.path.join(os.path.dirname(__file__), "cve_data.json")


def load_local_cve_data():
    """Load local CVE database if available."""
    if os.path.exists(CVE_DB_PATH):
        try:
            with open(CVE_DB_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"vulnerabilities": []}


def fetch_cve_feed():
    """Fetch recent CVEs from NVD API (sample)."""
    try:
        # NVD API 2.0 - last 7 days, limited results
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0?" \
              "pubStartDate=2025-01-01T00:00:00.000&" \
              "pubEndDate=2025-12-31T23:59:59.999&" \
              "resultsPerPage=50"
        req = urlopen(url, timeout=15)
        data = json.loads(req.read().decode("utf-8"))
        return data.get("vulnerabilities", [])
    except Exception as e:
        print(f"[-] CVE fetch error: {e}")
        VULN_FETCH_ERRORS.labels(source="nvd").inc()
        return []


def parse_cves(vulnerabilities):
    """Parse CVE entries and update metrics."""
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    categories = {}

    for vuln in vulnerabilities:
        cve = vuln.get("cve", {})
        metrics = cve.get("metrics", {})

        # Try CVSS v3.1 first, fall back to v3.0, then v2.0
        cvss_data = None
        severity_str = "UNKNOWN"

        if "cvssMetricV31" in metrics:
            cvss_data = metrics["cvssMetricV31"][0]
        elif "cvssMetricV30" in metrics:
            cvss_data = metrics["cvssMetricV30"][0]
        elif "cvssMetricV2" in metrics:
            cvss_data = metrics["cvssMetricV2"][0]

        if cvss_data:
            severity_str = cvss_data.get("baseSeverity", "UNKNOWN").upper()

        # Map severity
        if severity_str == "CRITICAL":
            counts["CRITICAL"] += 1
        elif severity_str == "HIGH":
            counts["HIGH"] += 1
        elif severity_str == "MEDIUM":
            counts["MEDIUM"] += 1
        elif severity_str in ("LOW", "NONE"):
            counts["LOW"] += 1

    return counts


def main():
    start_http_server(8002)
    print("[*] Vulnerability Exporter started on port 8002")

    while True:
        # Fetch from NVD API
        cves = fetch_cve_feed()
        counts = parse_cves(cves)

        # Also load local data
        local_data = load_local_cve_data()
        local_vulns = local_data.get("vulnerabilities", [])
        local_counts = parse_cves(local_vulns)

        # Merge counts
        final_counts = {k: counts.get(k, 0) + local_counts.get(k, 0) for k in counts}

        VULN_CRITICAL.set(final_counts.get("CRITICAL", 0))
        VULN_HIGH.set(final_counts.get("HIGH", 0))
        VULN_MEDIUM.set(final_counts.get("MEDIUM", 0))
        VULN_LOW.set(final_counts.get("LOW", 0))
        VULN_TOTAL.set(sum(final_counts.values()))

        print(f"[+] Vulnerabilities: C={final_counts.get('CRITICAL',0)} H={final_counts.get('HIGH',0)} "
              f"M={final_counts.get('MEDIUM',0)} L={final_counts.get('LOW',0)}")

        time.sleep(300)  # 5 min refresh


if __name__ == "__main__":
    main()
