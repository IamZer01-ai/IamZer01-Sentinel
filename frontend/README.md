# Sentinel frontend

Static SOC console for the IamZer01 Sentinel project.

## Preview and deployment status

The GitHub Pages site is a public **demo frontend**. It uses labelled sample fixtures by default; it does not claim to receive live Wazuh, Prometheus, or Elasticsearch telemetry.

## Configure a backend API

Edit `config.js` and set `apiBase` to the base URL of a separately hosted Sentinel API, for example:

```js
window.SENTINEL_CONFIG = {
  apiBase: "https://your-api-host.example"
};
```

The console will request `/api/v1/alerts?hours=24&limit=100` from that origin. The API must permit CORS requests from the exact GitHub Pages origin.

**Do not put API keys, passwords, or other secrets in this file.** It is downloaded by every visitor. Do not point the public dashboard at real security telemetry until the API has authentication, authorization, rate limiting, and appropriately restricted data access. The current backend still needs a security-hardening pass before public exposure.

An empty `apiBase` keeps the console in demo mode and avoids making a misleading same-origin API request to GitHub Pages.

## Local preview

From the repository root:

```bash
python -m http.server 8088
```

Open `http://localhost:8088/frontend/`. The frontend remains in demo mode until you set `apiBase` in `config.js`.

## UI behavior

- Search and severity filtering work against the active alert list.
- JSON snapshot export is available.
- KPI cards and charts are illustrative and are not automatically derived from the API response.
- The interface labels API alert data separately from verified upstream telemetry.
