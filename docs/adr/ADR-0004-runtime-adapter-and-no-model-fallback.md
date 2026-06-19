# ADR-0004: Runtime adapter and no-model fallback

## Status

Accepted

## Decision

MicroGPT will call models through a runtime adapter interface. Phase 1 ships with a `NoModelRuntime` so the system can boot and be tested without model weights.

## Consequences

- App can be tested before model installation
- llama.cpp can be added cleanly in Phase 2
- Runtime benchmarking becomes easier
