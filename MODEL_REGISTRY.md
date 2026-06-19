# Model Registry

MicroGPT does **not** commit model weights to Git.

Phase 2 adds a local JSON model registry. Use:

```text
models/model_registry.example.json
```

Copy it to:

```text
models/model_registry.local.json
```

Then update the exact model path, source URL, license, revision, quantization, and status.

## Required fields

| Field | Meaning |
|---|---|
| `model_id` | Stable local ID used by MicroGPT |
| `name` | Human-readable model name |
| `runtime` | Runtime adapter, usually `llama_cpp` |
| `path` | Local GGUF path relative to `MICROGPT_MODEL_DIR` or absolute path |
| `license` | Exact model license after validation |
| `source` | Upstream model card/repository URL |
| `revision` | Exact model revision/commit/tag |
| `quantization` | Example: Q4_K_M, Q5_K_M, Q8_0 |
| `context_length` | Claimed/supported context window |
| `status` | `candidate`, `approved`, `blocked`, or `local_only` |
| `notes` | Validation and benchmark notes |

## Starter candidate

The starter includes an example for Qwen3 0.6B GGUF because it is a practical tiny CPU candidate. Treat it as a **candidate**, not automatically approved. Revalidate the exact model card, license, and revision before any release.

## Policy

- Do not commit GGUF, SafeTensors, PyTorch, ONNX, or other model weight files.
- Do not use a model in public releases until license and attribution are recorded.
- Keep benchmarks in `data/events/benchmark_runs.jsonl` or a future evaluation report.
