# IamZer01 Sentinel — Platform v2 redesign

## Goals

- Deliver a clear, responsive SOC console focused on triage and investigation.
- Preserve the current FastAPI detection engine, exporters, Grafana dashboards, Prometheus rules, Nginx configuration and Docker Compose deployment until each migration is verified.
- Distinguish demo/sample data from telemetry actually retrieved from a connected source.
- Normalize events before correlation, assign explainable severity, and preserve event provenance.
- Keep credentials server-side and deny access by default for protected endpoints.

## Target layout

```text
frontend/                 # SOC console, pages, components, API client, styles
backend/sentinel/          # existing FastAPI app and detection package
integrations/              # Wazuh, Prometheus, Elasticsearch adapters
security/                  # IOC enrichment, ATT&CK mappings, rule packs, YARA workflow
infrastructure/
  docker/                  # container build assets
  nginx/                   # reverse proxy configuration
  grafana/                 # dashboards and provisioning
  prometheus/               # scrape config and alert rules
config/                    # non-secret configuration templates only
scripts/                   # setup, migration, validation and maintenance tools
tests/                     # unit, API, integration and frontend checks
docs/                      # architecture, deployment, operations and runbooks
.github/workflows/          # CI and security checks
```

## Migration strategy

1. Add the new console and architecture docs on a feature branch.
2. Map every current path referenced by Docker Compose, Dockerfiles, CI workflows, Nginx, Grafana provisioning, Prometheus, scripts and Python imports.
3. Move configuration directories in small commits, updating every dependent path and validating Compose configuration after each move.
4. Add normalized event schemas and source adapters with explicit connection state, freshness timestamps and source error reporting.
5. Connect dashboard panels to backend APIs; demo fixtures must be labelled `DEMO` and never imply a live sensor is healthy.
6. Add automated tests, secret scanning and deployment instructions; open a pull request for review before merging to `main`.

## Event identification model

Each normalized event should carry `event_id`, `timestamp`, `source`, `source_status`, `asset`, `source_ip`, `destination_ip`, `category`, `severity`, `confidence`, `rule_id`, `mitre_techniques`, `evidence`, and `raw_reference` where available. Missing values must remain unknown rather than being fabricated. Severity must be explainable from rule matches and context. Correlation should retain links to source events and avoid treating a single alert as confirmed compromise without supporting evidence.

## Security requirements

- Never commit live `.env` files, passwords, API tokens, private keys, or production event dumps.
- Use `.env.example` for placeholders and validate required environment variables at startup.
- Protect the dashboard and APIs with server-side authentication and authorization before exposing them beyond localhost or a trusted private network.
- Do not put Wazuh/Elasticsearch credentials in browser JavaScript.
- Restrict CORS, rate-limit sensitive routes, validate inputs, and avoid returning raw secrets or stack traces.
- Bind monitoring services to private interfaces by default and review exposed ports before deployment.
- Use least-privilege credentials and rotate any credential that may have been exposed.

## Acceptance checks

- Existing Compose services and volume mounts resolve after path changes.
- Backend health and source health are separate statuses.
- The UI remains usable on mobile and desktop, with accessible focus states and readable contrast.
- Demo fixtures are visibly marked; disconnected integrations display `Not connected` or `Unknown`, not green/healthy.
- Tests and security checks pass before the branch is merged.

## Current status

The redesign branch is a safe staging area. Existing production configuration is not moved or deleted until path dependencies are checked. The initial frontend is a standalone console scaffold and uses clearly labelled demo fixtures; it is not yet wired to live telemetry.
