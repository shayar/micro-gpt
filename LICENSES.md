# License Tracking

MicroGPT is open-source-first. Code, dependencies, model weights, datasets, and generated assets must have clear license tracking before release.

## Project license

| Item | License | Notes |
|---|---|---|
| MicroGPT source code | Apache-2.0 | See `LICENSE`. |

## Runtime and infrastructure dependencies

| Item | Type | License | Notes |
|---|---|---|---|
| FastAPI | Code dependency | MIT | API framework |
| Uvicorn | Code dependency | BSD-3-Clause | ASGI server |
| httpx | Code dependency | BSD-3-Clause | HTTP client |
| python-jose | Code dependency | MIT | JWT handling |
| passlib | Code dependency | BSD-style | Password utilities; MVP currently uses env password comparison |
| llama.cpp | Runtime dependency | MIT | CPU-first model inference runtime |
| Qdrant | Service dependency | Apache-2.0 | Vector database |
| SearXNG | Service dependency | AGPL-3.0-or-later | Metasearch engine; review deployment implications |
| Redis | Service dependency | Review before production | Can be replaced by SQLite KV for local MVP |

## Model tracking

Do not commit model files to GitHub.

| Model | Format | License | Source | Approved for use? | Notes |
|---|---|---|---|---|---|
| TBD | GGUF | TBD | TBD | No | Add before running public demo |

## Dataset tracking

| Dataset | License | Source | Approved for use? | Notes |
|---|---|---|---|---|
| TBD | TBD | TBD | No | Add before evaluation or training |

## Rule

No model, dataset, or dependency should be used in a public release until its license is documented here.
