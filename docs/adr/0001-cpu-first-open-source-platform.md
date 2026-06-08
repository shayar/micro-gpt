# ADR 0001: CPU-First Open-Source Platform

## Status

Accepted

## Context

MicroGPT should be accessible to students, volunteers, nonprofits, and low-budget teams. The project should not depend on expensive GPU infrastructure for the first working prototype.

The project also needs to support future GPU acceleration without rewriting the product layer.

## Decision

MicroGPT will be built as a CPU-first, GPU-ready open-source platform.

The first inference backend will use llama.cpp-compatible local serving with quantized GGUF models. Product modules will call stable runtime interfaces such as:

- `generate()`
- `embed()`
- `rerank()`
- `search_web()`
- `search_corpus()`

## Consequences

Benefits:

- Lower setup cost
- Easier local development
- Better fit for open-source contributors
- Clear path to CPU benchmarking
- Backend can later be swapped for GPU inference

Tradeoffs:

- Slower inference than GPU systems
- Smaller models may require stronger retrieval and verification
- Latency must be measured honestly

## Follow-up work

- Add CPU benchmark script
- Compare small GGUF models
- Add retrieval before generation
- Track latency and memory usage
