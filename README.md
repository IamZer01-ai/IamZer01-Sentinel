# IamZer01 Sentinel

**A personal Security Operations Center (SOC) lab for event normalization, rule-based detection, alert correlation, and investigation workflows.**

> **Status:** v2 redesign is under review. The new frontend includes sample fixtures and an optional same-origin API alert feed. It is not a verified production SOC and does not imply live Wazuh telemetry.

## Current capabilities

- FastAPI service and normalized event / alert / incident models in `backend/sentinel/`.
- Rule-based detection engine, alert correlation, incident manager, and simulation scenarios.
- Elasticsearch storage adapter and Prometheus metrics endpoint.
- Existing Docker Compose stack with Grafana, Prometheus, Elasticsearch, Kibana, exporters, and Nginx.
- New responsive SOC console in `frontend/` with alert search, severity filtering, and JSON snapshot export.
- Frontend CI validation and a GitHub Pages deployment workflow, intended to run after the changes are merged to `main` and Pages is configured for GitHub Actions.

## Quick start — frontend preview

Open `frontend/index.html` in a browser, or run a static HTTP server from the repository root:

```bash
python -m http.server 8088
```

Then open `http://localhost:8088/frontend/`.

The console starts with labelled demo fixtures. It tries to request `/api/v1/alerts` from the same origin; when that endpoint is unavailable, it falls back to demo data. A successful alert API response does not prove that Wazuh, Prometheus, or Elasticsearch is connected. The chart and KPI cards remain illustrative until they are wired to verified backend data.

## Backend development

The backend is packaged in `backend/`. Review `backend/requirements.txt`, `backend/Dockerfile`, and `docker-compose.yml` before starting services. Copy the safe placeholder template to a local `.env` and set unique credentials for every service. Do not commit `.env`, tokens, private keys, production logs, or customer telemetry.

API endpoints currently include:

- `GET /health` and `GET /status`
- `GET /api/v1/events` and `POST /api/v1/events`
- `GET /api/v1/alerts` and `GET /api/v1/alerts/critical`
- `GET /api/v1/incidents`
- `GET /api/v1/detection/rules`
- `GET /metrics`

These endpoints are part of an active development codebase. Confirm backend dependencies, data-store connectivity, and access controls before exposing them to a network.

## Target architecture

```text
frontend/                 # SOC console, UI assets, API client
backend/sentinel/         # FastAPI, data models, detection, correlation, storage
integrations/             # planned Wazuh / Prometheus / Elasticsearch adapters
security/                 # planned IOC enrichment, ATT&CK mapping, rule packs
infrastructure/           # planned organized Docker / Nginx / Grafana / Prometheus assets
config/                   # non-secret templates only
exporters/                # existing custom Prometheus exporters
scripts/                  # existing maintenance and health-check scripts
tests/                    # automated unit, API, and integration tests
docs/                     # installation, architecture, migration, and runbooks
.github/workflows/        # CI and site deployment workflows
```

Existing configuration directories will only be moved after every Docker Compose, Nginx, Grafana provisioning, Prometheus, script, and Python import reference has been audited.

## Security notes

- Never deploy with default credentials. The Compose file and existing integrations still need a full security hardening pass.
- The legacy tracked `config/.env` was removed on the redesign branch, but previous Git commits can still contain those values. Rotate any credential that was ever used and consider history cleanup before publishing a production-ready repository.
- Existing API routes currently lack a complete authentication and authorization layer. Keep the backend and monitoring ports private; do not expose them directly to the public internet.
- Elasticsearch is configured without built-in security in the current Compose file. Do not use that configuration for an untrusted network.
- A healthy application process is not the same as a healthy data source. Report unknown or disconnected upstream systems explicitly.

## Validation status

The frontend JavaScript syntax and required file checks are configured in `.github/workflows/sentinel-site.yml`. Runtime browser tests, backend tests, Compose validation, live integrations, authentication, and deployment must still be run and reviewed before production use.

## Contributing

Use a feature branch and pull request. Preserve existing functionality while migrating folders, add tests for changed behavior, and document any new integration's permissions and secret requirements.
