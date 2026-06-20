# ADR-0008: Add standalone llama.cpp CLI runtime adapter

## Status
Accepted for Phase 2.2.

## Context
The Python `llama-cpp-python` adapter is useful, but Windows native wheels can fail on some machines even when the CPU supports AVX2/FMA. In local testing, standalone `llama-cli` successfully loaded and generated from the same GGUF model where the Python binding failed with Windows error `0xc000001d`.

## Decision
MicroGPT supports a second CPU runtime mode:

```env
MICROGPT_RUNTIME_MODE=llama_cli
MICROGPT_LLAMA_CLI_PATH=llama-cli
```

The `llama_cli` adapter calls the installed standalone `llama-cli` binary as a subprocess. This keeps MicroGPT usable on machines where the Python binding is incompatible.

## Consequences
- Windows users can run local GGUF inference without compiling `llama-cpp-python`.
- Streaming is initially whole-response streaming through the subprocess adapter.
- A future `llama_server` adapter can provide more efficient persistent model loading and true token streaming.
