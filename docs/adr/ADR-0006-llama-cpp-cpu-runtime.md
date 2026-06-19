# ADR-0006: llama.cpp CPU Runtime Adapter

## Status
Accepted for Phase 2 starter.

## Context
MicroGPT is CPU-first and GPU-ready. The runtime layer must support local inference without making the whole app dependent on one model, one vendor, or one machine type.

## Decision
Use a runtime adapter interface with `NoModelRuntime` as the default and an optional `llama_cpp` adapter through `llama-cpp-python`.

The project must:

- Keep `llama-cpp-python` optional.
- Load it lazily only when `MICROGPT_RUNTIME_MODE=llama_cpp`.
- Keep model files out of Git.
- Use a local JSON model registry to track model path, source, license, revision, quantization, context length, and approval status.
- Fall back safely to `NoModelRuntime` unless strict runtime mode is requested.

## Consequences
The app remains easy to run for new contributors while still giving power users a real local CPU inference path.
