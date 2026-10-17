# Test strategy

Planned test layers:

- `unit/`: normalized event validation, rule matching, severity logic, and correlation behavior.
- `api/`: FastAPI request/response contracts, query validation, error redaction, and authorization behavior.
- `integration/`: Elasticsearch and monitoring adapter tests using disposable test services or mocks.
- `frontend/`: browser-level smoke tests for responsive layout, alert filtering, API-unavailable fallback, and XSS-safe rendering.

Do not use real credentials or production telemetry in fixtures. Test fixtures should be synthetic and visibly marked.