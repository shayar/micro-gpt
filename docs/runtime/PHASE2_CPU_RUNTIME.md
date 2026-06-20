# Phase 2 CPU Runtime

Phase 2 adds a runtime boundary so MicroGPT can run without hard-coding a single model backend.

Implemented adapters:

- `no_model`: safe fallback for auth, safety, provenance, and API testing.
- `llama_cpp`: optional `llama-cpp-python` adapter for local GGUF files.

## Phase 2.1 robustness update

This version adds:

- automatic `.env` loading through `python-dotenv`;
- safer `/runtime/status` diagnostics;
- fallback when native llama loading fails;
- model file existence and size reporting;
- `/system/specs` and `/runtime/recommendations` foundations for first-run model selection.

## Recommended Windows install path

```powershell
pip install -e ".[dev]"
pip install --prefer-binary llama-cpp-python==0.3.30 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

Avoid installing `[dev,llama]` first on Windows if `llama-cpp-python` tries to compile from source.

## Runtime status behavior

`GET /runtime/status` should not crash the API. It reports:

- configured runtime mode;
- active runtime;
- fallback reason;
- model registry path;
- active model metadata;
- model file existence and size;
- llama runtime settings.

If native model loading fails, the endpoint returns `active_runtime: no_model` with a detailed `fallback_reason`.

## Known Windows error: 0xc000001d

`Windows Error 0xc000001d` usually means the native llama runtime attempted an illegal CPU instruction. Even if the CPU reports AVX2/FMA, the Python wheel may still be incompatible with the installed Python/Windows/runtime combination.

Short-term mitigation:

- keep `MICROGPT_RUNTIME_FALLBACK_ENABLED=true`;
- use Python 3.12;
- install the CPU wheel from the llama-cpp-python wheel index;
- test standalone llama.cpp.

Future improvement:

- add a `llama_cli` or `llama_server` adapter so MicroGPT can call standalone llama.cpp without relying only on Python native bindings.
