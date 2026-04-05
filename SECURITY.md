# Security

## Scope

This repository is a public portfolio platform and demonstration scaffold.
It is not intended to process real customer production data in its current root-level sample mode.

## Security Posture

- protected API endpoints require API key or JWT mode
- secrets are not rendered in runtime summaries
- external GenAI providers are optional and disabled by default
- the current root sample dataset does not require personal data

## Reporting

If you identify a security issue:

1. do not open a public issue with exploit details
2. report it privately through GitHub security reporting if enabled, or contact the repository owner directly
3. include reproduction steps, impact, and recommended remediation if possible

## Sensitive Data Handling

Do not commit:

- credentials
- tokens
- private datasets
- customer records
- generated artifacts that contain personal data
