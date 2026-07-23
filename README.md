🛡️ IamZer01 Sentinel

> Version 1.0 – Personal SOC Dashboard for Real-Time Security Monitoring, Threat Detection, and Infrastructure Visibility.



    


---

📌 About

IamZer01 Sentinel is a personal Security Operations Center (SOC) platform designed to centralize security monitoring, infrastructure metrics, and threat visibility into a single dashboard.

Version 1 focuses on building a lightweight monitoring stack using Docker, Grafana, Prometheus, Elasticsearch, Kibana, InfluxDB, Telegraf, and custom Python exporters.

This project is intended for learning, experimentation, and building a practical SOC lab.


---

🚀 Features

📊 Grafana Dashboards

📈 Prometheus Monitoring

🚨 Alertmanager Alerts

📡 Telegraf Metrics Collection

📦 InfluxDB Time-Series Storage

🔍 Elasticsearch Logging

📑 Kibana Log Analysis

🔥 Firewall Monitoring Exporter

🛡 Vulnerability Monitoring Exporter

⚔️ MITRE ATT&CK Exporter

🐳 Docker Compose Deployment

📁 Backup Scripts

📋 Health Check Scripts



---

🏗️ Project Structure

IamZer01-Sentinel/
├── config/
├── grafana/
├── prometheus/
├── exporters/
├── scripts/
├── nginx/
├── docs/
├── data/
├── logs/
├── backups/
├── docker-compose.yml
├── .env.example
└── README.md


---

🛠️ Tech Stack

Docker

Docker Compose

Grafana

Prometheus

Alertmanager

Elasticsearch

Kibana

InfluxDB

Telegraf

Python

Nginx



---

⚙️ Installation

Clone the repository:

git clone https://github.com/IamZer01-ai/IamZer01-Sentinel.git
cd IamZer01-Sentinel

Start the platform:

docker compose up -d

Verify running containers:

docker ps


---

🌐 Default Services

Service	URL

Grafana	http://localhost:3000
Prometheus	http://localhost:9090
Alertmanager	http://localhost:9093
Kibana	http://localhost:5601
Elasticsearch	http://localhost:9200
InfluxDB	http://localhost:8086



---

📂 Version 1 Roadmap

✅ Dockerized Monitoring Stack

✅ Grafana Dashboards

✅ Prometheus Metrics

✅ Alert Rules

✅ Python Exporters

✅ Log Collection

✅ Infrastructure Monitoring



---

🔮 Future Roadmap

Version 2 and beyond will expand Sentinel with:

AI Security Assistant

Endpoint Monitoring

Threat Intelligence

Incident Management

User Authentication

Role-Based Access Control

Web Dashboard

Live Asset Discovery

IOC Management

PDF Report Generation

Network Scanner

SIEM Integrations



---

📸 Screenshots

> Screenshots will be added as the dashboard evolves.




---

🤝 Contributing

This repository is currently maintained as a personal cybersecurity learning project. Suggestions, issues, and constructive feedback are welcome.


---

📄 License

This project is licensed under the MIT License.


---

👨‍💻 Author

Jayanth (IamZer01-ai)

GitHub: https://github.com/IamZer01-ai



---

⭐ Project Vision

IamZer01 Sentinel aims to evolve from a personal monitoring dashboard into a modular SOC/XDR platform for learning defensive security, infrastructure monitoring, threat detection, and security operations through hands-on experimentation. 🚀


For Version 1, keep it focused on building a stable, usable SOC monitoring platform. Avoid trying to include every possible feature. Here's a clean architecture:
IamZer01-Sentinel/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── config/
│   ├── prometheus.yml
│   ├── alertmanager.yml
│   ├── telegraf.conf
│   └── .env
│
├── grafana/
│   ├── dashboards/
│   │   ├── overview.json
│   │   ├── firewall.json
│   │   ├── vulnerabilities.json
│   │   └── mitre.json
│   └── provisioning/
│       ├── dashboards/
│       └── datasources/
│
├── prometheus/
│   ├── rules/
│   │   └── soc_alerts.yml
│   └── targets/
│
├── exporters/
│   ├── firewall_exporter.py
│   ├── vuln_exporter.py
│   ├── mitre_exporter.py
│   └── requirements.txt
│
├── scripts/
│   ├── install.sh
│   ├── deploy.sh
│   ├── backup.sh
│   ├── check_services.sh
│   └── check_endpoints.sh
│
├── nginx/
│   └── nginx.conf
│
├── data/
│   ├── prometheus/
│   ├── grafana/
│   ├── influxdb/
│   └── elasticsearch/
│
├── logs/
│
├── docs/
│   ├── installation.md
│   ├── deployment.md
│   └── architecture.md
│
└── backups/



For a professional, scalable SOC Dashboard (IamZer01-Sentinel), I'd recommend the following architecture. It separates infrastructure, monitoring, detection, exporters, integrations, and future AI features cleanly.
IamZer01-Sentinel/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── config/
│   ├── .env
│   ├── app.yml
│   ├── prometheus.yml
│   ├── alertmanager.yml
│   └── telegraf.conf
│
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.frontend
│   └── Dockerfile.exporters
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── package.json
│
├── backend/
│   ├── src/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── alerts/
│   │   ├── endpoints/
│   │   ├── incidents/
│   │   ├── vulnerabilities/
│   │   ├── mitre/
│   │   ├── threatintel/
│   │   ├── websocket/
│   │   ├── ai/
│   │   ├── reports/
│   │   ├── users/
│   │   └── common/
│   ├── prisma/
│   └── package.json
│
├── exporters/
│   ├── firewall_exporter.py
│   ├── vuln_exporter.py
│   ├── mitre_exporter.py
│   ├── endpoint_exporter.py
│   ├── network_exporter.py
│   ├── windows_exporter.py
│   ├── linux_exporter.py
│   └── requirements.txt
│
├── prometheus/
│   ├── prometheus.yml
│   ├── rules/
│   │   ├── soc_alerts.yml
│   │   ├── endpoint_alerts.yml
│   │   └── network_alerts.yml
│   └── targets/
│
├── grafana/
│   ├── dashboards/
│   │   ├── executive.json
│   │   ├── soc-overview.json
│   │   ├── firewall.json
│   │   ├── mitre.json
│   │   ├── endpoint.json
│   │   ├── vulnerability.json
│   │   ├── threat-intelligence.json
│   │   └── incidents.json
│   │
│   └── provisioning/
│       ├── dashboards/
│       └── datasources/
│
├── elasticsearch/
│
├── kibana/
│
├── influxdb/
│
├── telegraf/
│
├── nginx/
│   ├── nginx.conf
│   └── ssl/
│
├── scripts/
│   ├── install.sh
│   ├── deploy.sh
│   ├── backup.sh
│   ├── restore.sh
│   ├── update.sh
│   ├── check_services.sh
│   ├── check_endpoints.sh
│   └── firewall_geo_enrich.py
│
├── monitoring/
│   ├── syslog/
│   ├── snmp/
│   ├── netflow/
│   ├── zeek/
│   └── suricata/
│
├── threat-intel/
│   ├── abuseipdb/
│   ├── virustotal/
│   ├── alienvault/
│   ├── cve/
│   └── feeds/
│
├── integrations/
│   ├── slack/
│   ├── discord/
│   ├── email/
│   ├── teams/
│   └── webhook/
│
├── reports/
│   ├── pdf/
│   ├── csv/
│   └── html/
│
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── api.md
│   └── screenshots/
│
├── logs/
│
├── backups/
│
├── data/
│   ├── prometheus/
│   ├── influxdb/
│   ├── elasticsearch/
│   └── grafana/
│
└── tests/
    ├── unit/
    ├── integration/
    └── api/

Endpoints
      │
      ▼
Exporters (Python)
      │
      ▼
Prometheus ─────────── Alertmanager
      │                      │
      │                      ▼
      │                Email / Discord / Slack
      │
      ▼
Grafana Dashboards
      │
      ▼
NestJS Backend API
      │
      ├── AI Assistant
      ├── Incident Response
      ├── Threat Intelligence
      ├── MITRE ATT&CK
      ├── Vulnerability Management
      ├── Reports
      └── Authentication
      │
      ▼
Next.js Frontend

Here is a complete, production-ready `README.md` for **IamZer01 Sentinel**. You can copy and paste this directly into your GitHub repository.

---

```markdown
# 🛡️ IamZer01 Sentinel — Personal Security Operations Center (SOC)

[![Docker](https://img.shields.io/badge/Docker-24.0+-0db7ed?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Grafana](https://img.shields.io/badge/Grafana-11.3-F46800?style=flat&logo=grafana&logoColor=white)](https://grafana.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.55-E6522C?style=flat&logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.15-005571?style=flat&logo=elasticsearch&logoColor=white)](https://www.elastic.co/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**IamZer01 Sentinel** is a full-stack, lightweight Security Operations Center (SOC) platform designed for real-time security monitoring, threat visibility, system telemetry, and incident response prototyping. Built with containerized microservices, custom threat exporters, and a unified command interface.

---

## 📌 Features

* **Centralized Command Portal (V2):** Dark-themed, high-density interface displaying real-time service health, active alerts, vulnerability posture, and single-click access to all tools.
* **Infrastructure Telemetry:** Metrics collection via Prometheus, Node Exporter, and cAdvisor (CPU, Memory, Disk, Network, Container stats).
* **Custom Security Exporters:**
  * **Firewall Exporter:** Tracks active rules, open ports, connection states, and blocked traffic.
  * **Vulnerability Exporter:** Ingests NVD feeds to track CVE metrics across Critical, High, Medium, and Low severities.
  * **MITRE ATT&CK Exporter:** Parses STIX bundles to track coverage across 14 tactics and 500+ techniques.
* **Log Analytics & SIEM Core:** Elasticsearch + Kibana pipeline for log aggregation and interactive query analysis.
* **Alerting Engine:** Prometheus rules connected to Alertmanager for real-time notification routing.
* **Grafana Dashboards:** Pre-provisioned dashboards for SOC Overview, Firewall Analytics, CVE Tracking, and MITRE Mapping.

---

## 🏗️ Architecture Stack


```

```
                           ┌─────────────────────────┐
                           │     SOC Portal (V2)     │
                           │   (Flask UI - Port 80)  │
                           └────────────┬────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
  ┌────────┴────────┐          ┌────────┴────────┐          ┌────────┴────────┐
  │     Grafana     │          │   Prometheus    │          │     Kibana      │
  │   (Port 3000)   │          │   (Port 9090)   │          │   (Port 5601)   │
  └────────┬────────┘          └────────┬────────┘          └────────┬────────┘
           │                            │                            │

```

┌─────────────┴─────────────┐              │              ┌─────────────┴─────────────┐
│    Provisioned Dashboards │              │              │       Elasticsearch       │
└───────────────────────────┘              │              └─────────────┬─────────────┘
│                            │
┌─────────────────────────────────────┼────────────────────────────┘
│                                     │
┌─────┴──────────────────┐      ┌───────────┴────────────┐      ┌─────────────────────────┐
│   Custom Exporters     │      │   System Collectors    │      │    Time-Series Store    │
├────────────────────────┤      ├────────────────────────┤      ├─────────────────────────┤
│ • Firewall Exporter    │      │ • Node Exporter (9100) │      │ • InfluxDB (8086)       │
│ • Vulnerability Exp.   │      │ • cAdvisor (8080)      │      │ • Telegraf (Agent)      │
│ • MITRE ATT&CK Exp.    │      │ • Alertmanager (9093)  │      └─────────────────────────┘
└────────────────────────┘      └────────────────────────┘

```

---

## 📂 Directory Structure


```

IamZer01-Sentinel/
├── config/                  # Configuration files
│   ├── .env                 # Environment variables & credentials
│   ├── alertmanager.yml     # Alertmanager routing rules
│   ├── prometheus.yml       # Prometheus scrape configurations
│   └── telegraf.conf        # Telegraf system metrics config
├── scripts/                 # Operational & health check scripts
│   ├── check_services.sh    # Service container status checker
│   └── check_endpoints.sh   # Exporter metric validation script
├── exporters/               # Custom Python Prometheus exporters
│   ├── firewall/            # Firewall & socket telemetry exporter
│   ├── vulnerability/       # CVE feed exporter
│   └── mitre/               # MITRE ATT&CK framework exporter
├── grafana/                 # Grafana provisioning
│   ├── dashboards/          # Pre-built JSON dashboard definitions
│   └── provisioning/        # Auto-loader YAML configurations
├── portal/                  # SOC Portal UI (Flask / Bootstrap)
│   ├── app.py               # Main Portal API & backend router
│   ├── Dockerfile           # Portal container spec
│   └── templates/           # System Command UI (index.html)
├── nginx/                   # Reverse proxy configuration
│   └── nginx.conf           # Unified path routing & security headers
├── docker-compose.yml       # Primary orchestration stack definition
└── README.md

```

---

## 🚀 Quick Start Guide

### Prerequisites
* **Docker Engine** v24.0+ & **Docker Compose** v2.0+
* Minimum **4 GB RAM** and **2 vCPUs** (GitHub Codespaces or VPS)

---

### Step 1: Clone & Configure

```bash
# Clone the repository
git clone [https://github.com/IamZer01-ai/IamZer01-Sentinel.git](https://github.com/IamZer01-ai/IamZer01-Sentinel.git)
cd IamZer01-Sentinel

# Set executable permissions
chmod +x scripts/*.sh

# Initialize environment configuration
cp .env.example config/.env

```

---

### Step 2: System Pre-requisites

Set the host virtual memory limit required for Elasticsearch:

```bash
sudo sysctl -w vm.max_map_count=262144

# Make setting persistent across reboots
sudo sh -c 'echo "vm.max_map_count=262144" >> /etc/sysctl.conf'

```

---

### Step 3: Build & Deploy Services

```bash
# Create required data directory structures
mkdir -p data/{prometheus,grafana,influxdb,elasticsearch} logs backups

# Pull standard upstream container images
docker compose pull

# Build custom exporters and the SOC Portal
docker compose build

# Launch the entire stack in detached mode
docker compose up -d

```

---

### Step 4: Provision Grafana Dashboards

Copy the dashboard JSON definitions into the active Grafana volume and trigger provisioning:

```bash
docker compose cp grafana/dashboards/overview.json grafana:/var/lib/grafana/dashboards/
docker compose cp grafana/dashboards/firewall.json grafana:/var/lib/grafana/dashboards/
docker compose cp grafana/dashboards/vulnerabilities.json grafana:/var/lib/grafana/dashboards/
docker compose cp grafana/dashboards/mitre.json grafana:/var/lib/grafana/dashboards/

# Fix permissions and restart Grafana
docker compose exec grafana chown -R grafana:root /var/lib/grafana/dashboards/
docker compose restart grafana

```

---

## 🔗 Default Access Ports

| Service | Internal Port | External Route / Port | Default Credentials |
| --- | --- | --- | --- |
| **SOC Portal UI** | `5050` | `http://localhost:80` | Public / Unauthenticated |
| **Grafana** | `3000` | `http://localhost:3000` | `admin` / `admin` |
| **Prometheus** | `9090` | `http://localhost:9090` | None |
| **Kibana** | `5601` | `http://localhost:5601` | None |
| **Alertmanager** | `9093` | `http://localhost:9093` | None |
| **Elasticsearch** | `9200` | `http://localhost:9200` | None |
| **InfluxDB** | `8086` | `http://localhost:8086` | `admin` / `admin123` |

---

## 📊 Pre-built Dashboards

1. **SOC Overview (`sentinel-overview`):** Uptime metrics, CPU/Memory gauges, disk trends, active alert tables, and service states.
2. **Firewall Monitoring (`sentinel-firewall`):** Blocked vs. allowed connection ratios, TCP state breakdowns, open socket counts, and iptables rule tracking.
3. **Vulnerability Tracking (`sentinel-vuln`):** Critical/High/Medium/Low CVE gauges, vulnerability category breakdown, and historical trends.
4. **MITRE ATT&CK Matrix (`sentinel-mitre`):** Coverage percentage, tactics tracker, technique count by platform, and interactive tactic mapping.

---

## 🌐 Remote Access via Cloudflare Tunnel (Optional)

To expose your SOC dashboard securely to the internet without opening router ports:

```bash
# Install cloudflared
curl -L [https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared

# Authenticate Cloudflare account
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create sentinel-soc

# Route domain and start service
cloudflared tunnel route dns sentinel-soc soc.yourdomain.com
cloudflared service install

```

---

## 📱 Mobile Access (PWA Integration)

The SOC Portal supports Progressive Web App (PWA) installation:

1. Access the portal URL (`http://your-server-ip`) on Chrome (Android/Desktop) or Safari (iOS).
2. Tap **Share** or the browser menu **(⋮)**.
3. Select **"Add to Home Screen"**.
4. Sentinel will now function as a native, standalone mobile application.

---

## 🛠️ Verification & Diagnostic Commands

```bash
# Check running container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Run automated service health check script
./scripts/check_services.sh

# Validate custom exporter metrics stream
./scripts/check_endpoints.sh

```

---

## 📄 License

This project is open-source software licensed under the [MIT License](https://www.google.com/search?q=LICENSE).

```

```
# SOC-Dashboard
SOC Dashboard for internal use
token: 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
