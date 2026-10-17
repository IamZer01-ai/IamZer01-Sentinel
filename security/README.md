# Security modules

Target modules for the Sentinel v2 migration:

- `rules/`: versioned detection rules with IDs, severity rationale, false-positive guidance, and test fixtures.
- `ioc/`: IOC parsing, normalization, validation, and optional enrichment providers.
- `mitre/`: ATT&CK technique metadata and mapping validation.
- `yara/`: safe, isolated scanning workflow and rule validation.

Do not execute uploaded files. Treat PCAPs, IOC feeds, event fields, and YARA files as untrusted input. Preserve source references and analyst audit records.