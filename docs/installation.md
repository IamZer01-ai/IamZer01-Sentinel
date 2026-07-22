# Installation Guide — IamZer01 Sentinel v1.0

## Prerequisites

- **Docker** >= 24.x + **Docker Compose** >= 2.20
- **Python** 3.10+ (only if running exporters outside Docker)
- **curl**, **jq** for health checks
- Minimum **4 GB RAM** (8 GB recommended)
- **10 GB** free disk

## Quick Start

```bash
# 1. Clone
git clone https://github.com/IamZer01-ai/IamZer01-Sentinel.git
cd IamZer01-Sentinel

# 2. Configure (optional)
cp .env.example .env
# Edit .env with your credentials

# 3. Deploy
chmod +x scripts/*.sh
./scripts/deploy.sh

# 4. Verify
./scripts/check_services.sh
./scripts/check_endpoints.sh
