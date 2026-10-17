# Integrations

Adapters planned for this directory:

- `wazuh/`: authenticated Wazuh API client and agent/alert normalization.
- `prometheus/`: verified target health and metric queries.
- `elasticsearch/`: storage/query adapter migration when existing backend dependencies are audited.

Every adapter must expose connection state, last successful check time, and a sanitized error state. Never return credentials to the browser. Keep the existing `backend/sentinel/storage/elasticsearch.py` and current Compose service paths unchanged until migration tests exist.