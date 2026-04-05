# API

## Purpose

The API exposes the platform as a governed analytical service surface rather than a demo-only backend.

## Main Endpoint Groups

- `/health`
- `/snapshot`
- `/metrics`
- `/metrics/history`
- `/metrics/domain-history`
- `/metrics/project-history`
- `/insights`
- `/genai`
- `/change-drivers`
- `/repositories`
- `/quality/status`
- `/catalog/datasets`
- `/catalog/glossary`
- `/catalog/metrics`
- `/governance/runtime-config`
- `/governance/policy-checks`
- `/governance/analytics-engineering`

## Security

Protected endpoints require API key or JWT mode depending on runtime configuration.
