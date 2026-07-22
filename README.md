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

# SOC-Dashboard
SOC Dashboard for internal use
token: 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
