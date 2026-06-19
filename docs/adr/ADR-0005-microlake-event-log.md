# ADR-0005: MicroLake append-only event log

## Status

Accepted

## Decision

Phase 1 records conversations, audit actions, and safety decisions as append-only JSONL files under `data/events`.

## Consequences

- Simple local audit trail
- Easy debugging
- Future migration path to Parquet snapshots and lineage manifests
