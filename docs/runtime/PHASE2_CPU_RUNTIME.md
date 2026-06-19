# Phase 2: CPU Runtime

Phase 2 adds the foundation for local CPU inference while keeping the project runnable without a model.

## Modes

### `no_model`
Default. Used for auth, safety, provenance, streaming, and audit testing.

```env
MICROGPT_RUNTIME_MODE=no_model
```

### `llama_cpp`
Uses the optional `llama-cpp-python` adapter to load a local GGUF model.

```env
MICROGPT_RUNTIME_MODE=llama_cpp
MICROGPT_MODEL_REGISTRY_PATH=./models/model_registry.local.json
MICROGPT_ACTIVE_MODEL_ID=qwen3-0.6b-gguf-local
```

Install optional dependency:

```bash
pip install -e ".[dev,llama]"
```

Copy the example registry:

```bash
cp models/model_registry.example.json models/model_registry.local.json
```

Then update the local model path and exact revision/license validation notes.

## Benchmark

```bash
python scripts/benchmark_runtime.py --prompt "Explain MicroGPT" --runs 3 --max-tokens 128
```

Benchmark results are appended to `data/events/benchmark_runs.jsonl`.

## Streaming

Use `POST /chat/stream` from Swagger UI or curl. The endpoint streams plain text chunks.
