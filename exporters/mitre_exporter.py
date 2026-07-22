#!/usr/bin/env python3
"""
IamZer01 Sentinel – MITRE ATT&CK Exporter
Version 1.0

Exposes MITRE ATT&CK framework metrics: technique counts
by tactic, platform coverage, and detection coverage.
"""

import time
import json
import os
from urllib.request import urlopen
from prometheus_client import start_http_server, Gauge, Counter

# ─── Metrics ──────────────────────────────────────────────────
MITRE_TACTIC_COUNT = Gauge(
    "mitre_tactic_techniques",
    "Number of techniques per MITRE ATT&CK tactic",
    ["tactic", "tactic_id"],
)

MITRE_PLATFORM_COUNT = Gauge(
    "mitre_platform_techniques",
    "Number of techniques per platform",
    ["platform"],
)

MITRE_TOTAL_TECHNIQUES = Gauge(
    "mitre_total_techniques",
    "Total number of tracked ATT&CK techniques",
)

MITRE_TOTAL_TACTICS = Gauge(
    "mitre_total_tactics",
    "Total number of tracked ATT&CK tactics",
)

MITRE_COVERAGE_SCORE = Gauge(
    "mitre_coverage_score",
    "Percentage of techniques covered by detection rules",
)

MITRE_FETCH_ERRORS = Counter(
    "mitre_fetch_errors_total",
    "Total errors fetching MITRE ATT&CK data",
    ["source"],
)

# ─── Local cache ─────────────────────────────────────────────
CACHE_FILE = os.path.join(os.path.dirname(__file__), "mitre_cache.json")
STIX_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"


def fetch_mitre_data():
    """Fetch MITRE ATT&CK data from the STIX bundle."""
    try:
        req = urlopen(STIX_URL, timeout=30)
        data = json.loads(req.read().decode("utf-8"))
        return data
    except Exception as e:
        print(f"[-] MITRE fetch error: {e}")
        MITRE_FETCH_ERRORS.labels(source="mitre-stix").inc()
        # Try loading from cache
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {"objects": []}


def parse_mitre_data(stix_data):
    """Parse STIX bundle and extract technique/tactic counts."""
    objects = stix_data.get("objects", [])

    tactics = {}
    techniques_by_tactic = {}
    platforms_count = {}

    for obj in objects:
        # Parse tactics (x-mitre-tactic)
        if obj.get("type") == "x-mitre-tactic":
            name = obj.get("name", "Unknown")
            ext_id = ""
            for ext_ref in obj.get("external_references", []):
                if ext_ref.get("source_name") == "mitre-attack":
                    ext_id = ext_ref.get("external_id", "")
            tactics[name] = {"id": ext_id, "techniques": 0}

        # Parse techniques (attack-pattern)
        if obj.get("type") == "attack-pattern":
            # Get platform coverage
            platforms = obj.get("x_mitre_platforms", [])
            for platform in platforms:
                platforms_count[platform] = platforms_count.get(platform, 0) + 1

            # Get tactic mapping from kill_chain_phases
            for phase in obj.get("kill_chain_phases", []):
                if phase.get("kill_chain_name") == "mitre-attack":
                    tactic_name = phase.get("phase_name", "unknown")
                    if tactic_name not in techniques_by_tactic:
                        techniques_by_tactic[tactic_name] = 0
                    techniques_by_tactic[tactic_name] += 1

    return tactics, techniques_by_tactic, platforms_count


def main():
    start_http_server(8003)
    print("[*] MITRE ATT&CK Exporter started on port 8003")

    # Initial fetch and cache
    data = fetch_mitre_data()
    if data.get("objects"):
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)

    while True:
        data = fetch_mitre_data()
        if data.get("objects"):
            with open(CACHE_FILE, "w") as f:
                json.dump(data, f)

            tactics, techniques_by_tactic, platforms = parse_mitre_data(data)

            # Update tactic metrics
            for tactic_name, tech_count in techniques_by_tactic.items():
                tactic_info = tactics.get(tactic_name, {"id": "unknown"})
                MITRE_TACTIC_COUNT.labels(
                    tactic=tactic_name,
                    tactic_id=tactic_info.get("id", "unknown"),
                ).set(tech_count)

            # Update platform metrics
            for platform, count in platforms.items():
                MITRE_PLATFORM_COUNT.labels(platform=platform).set(count)

            # Total counts
            MITRE_TOTAL_TECHNIQUES.set(sum(techniques_by_tactic.values()))
            MITRE_TOTAL_TACTICS.set(len(techniques_by_tactic))
            MITRE_COVERAGE_SCORE.set(0)  # Placeholder — detection coverage

            print(f"[+] MITRE: {MITRE_TOTAL_TECHNIQUES._value.get()} techniques "
                  f"across {MITRE_TOTAL_TACTICS._value.get()} tactics")

        time.sleep(3600)  # 1 hour refresh


if __name__ == "__main__":
    main()
