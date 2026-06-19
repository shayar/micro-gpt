# ADR-0001: Local-first by default

## Status

Accepted

## Context

MicroGPT is designed for students, researchers, developers, nonprofits, and small teams that need AI over local project context without sending private data to cloud APIs by default.

## Decision

MicroGPT will run locally by default. Cloud APIs are not required for Phase 1. Local data, model files, vault notes, and MicroLake logs are gitignored.

## Consequences

- Strong privacy position
- Easier offline development
- Slower inference until optimized
- More responsibility for local safety and storage controls
