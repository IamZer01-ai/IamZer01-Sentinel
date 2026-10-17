# Private-first production deployment

## Recommended topology

Use a maintained Linux VPS with Docker Engine and the Docker Compose plugin for the full existing stack. Keep the public GitHub Pages frontend separate. This production Compose file is an **initial private staging configuration**, not a claim that the application is production-ready for public API traffic.

It starts Elasticsearch, FastAPI, Prometheus, InfluxDB, and Grafana on one private Docker bridge. Only FastAPI (127.0.0.1:8000) and Grafana (127.0.0.1:3000) are published, and only on the host loopback interface. Elasticsearch, Prometheus, and InfluxDB have no host-published ports. Do not add a public reverse proxy until API authentication and authorization are implemented and reviewed.

## Before starting

1. Use a supported Linux LTS release and apply security updates.
2. Configure the VPS firewall to allow inbound SSH only from a trusted source where practical. Do not open 3000, 8000, 9090, 9200, 8086, or 5601 to the internet.
3. Install Docker Engine and the Compose plugin from the official Docker documentation.
4. Copy `.env.production.example` to `.env.production` on the server. Replace every placeholder with unique randomly generated secrets; never commit the real file. Restrict its permissions: `chmod 600 .env.production`.
5. Ensure the server has enough memory for Elasticsearch. The configured JVM heap is 1 GiB; allow additional memory for the OS and other containers. A 4 GiB VPS is a constrained lab minimum; 8 GiB or more is a more practical starting point for the combined stack.
6. Review the API before using real telemetry. Current API routes do not implement application-level authentication/authorization, and some POST routes generate simulated events. Loopback binding reduces exposure but is not a substitute for API authentication.

## Stage 1 — validate configuration

From the repository root, run:

```bash
docker compose --env-file .env.production -f docker-compose.production.yml config
```

Resolve any reported missing variables or invalid configuration before proceeding.

## Stage 2 — start the private stack

```bash
docker compose --env-file .env.production -f docker-compose.production.yml up -d --build
docker compose --env-file .env.production -f docker-compose.production.yml ps
docker compose --env-file .env.production -f docker-compose.production.yml logs --tail=100 elasticsearch sentinel-backend
```

Verify the API health check and service logs before loading any real data. Elasticsearch health must be checked rather than assumed. The API health endpoint now returns HTTP 503 if Elasticsearch is unavailable.

## Stage 3 — access dashboards through an SSH tunnel

From your own computer, open an SSH tunnel to the server (replace `YOUR_SERVER` and `YOUR_SSH_USER` with your own values):

```bash
ssh -N -L 3000:127.0.0.1:3000 -L 8000:127.0.0.1:8000 YOUR_SSH_USER@YOUR_SERVER
```

Then visit `http://localhost:3000` for Grafana. The API remains local to the host/tunnel and is not directly available to the public website. Do not expose Grafana by changing the bind address to `0.0.0.0`.

## Stage 4 — security work required before public API access

- Implement and test authentication, role-based authorization, and audit logging for all API routes; protect event ingestion and simulation routes especially.
- Replace the Elasticsearch superuser used in this initial private staging file with a dedicated least-privilege service account.
- Add rate limits, request-size limits, input validation, and safe error responses that do not return internal exception strings.
- Configure HTTPS and a reverse proxy only after authentication works. Restrict CORS to the exact production frontend origin; CORS is not authentication.
- Add a backup/restore test for Elasticsearch, Grafana, InfluxDB, and Prometheus volumes. Confirm retention, disk monitoring, and recovery steps.
- Add a secure event-ingestion source and verify data provenance before describing alerts as live telemetry.

## Stage 5 — connect the public dashboard

Do not put API tokens or passwords in `frontend/config.js`: that file is public to every visitor. The current public frontend should stay in DEMO mode until a safe authenticated integration exists, such as a session-based backend-for-frontend or another reviewed access design.

## Rollback

To stop the private stack without deleting persisted data:

```bash
docker compose --env-file .env.production -f docker-compose.production.yml down
```

Do not use `down -v` unless you deliberately intend to delete the named data volumes. Back up first and test restoration.
