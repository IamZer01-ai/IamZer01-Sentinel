# Sentinel SOC console preview

This directory contains the first responsive console scaffold for the v2 redesign.

## Preview locally

Open `index.html` in a browser, or serve the repository root with any static HTTP server and visit `/frontend/`.

## Current capabilities

- Responsive SOC overview layout for desktop and mobile.
- Clearly labelled demo mode and unverified source health.
- Client-side search and severity filtering for sample alerts.
- Local JSON export of the sample snapshot.
- Navigation placeholders for future incident, asset and investigation modules.

## Important limitations

This preview is not connected to FastAPI or live Wazuh, Prometheus, or Elasticsearch telemetry. Alert records are static demo fixtures. Do not use it as an operational security monitoring system or expose sensitive production information through it.

## Next integration work

1. Define and validate normalized event and health response schemas in the FastAPI backend.
2. Add a same-origin API client and loading, stale-data, unauthorized, and unavailable states.
3. Connect panels to authenticated backend endpoints; never expose integration credentials in browser code.
4. Add frontend tests and accessibility checks.
