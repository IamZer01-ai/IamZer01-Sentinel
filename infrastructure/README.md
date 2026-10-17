# Infrastructure migration

Proposed destinations:

- `docker/`: Compose fragments and image build configuration.
- `nginx/`: reverse proxy configuration.
- `grafana/`: dashboard provisioning and dashboards.
- `prometheus/`: scrape configuration and alert rules.

Migration is intentionally staged. The current Compose file references `./config`, `./grafana`, `./nginx`, and `./prometheus`; do not move those paths until all mounts, provisioning paths, scripts, and CI references are updated together and Compose validation passes.