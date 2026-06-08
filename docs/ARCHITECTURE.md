# MicroGPT Phase 1 Architecture

```text
User/UI
  |
  v
FastAPI API
  |-- Auth / JWT login
  |-- Maturity gate
  |-- Safety policy
  |-- Runtime adapter
  |-- Search/retrieval adapters
  |
  +--> llama.cpp server for CPU inference
  +--> Qdrant for vector search
  +--> SearXNG for web search
  +--> Redis for cache/rate limits
```

## Design rule

Product modules should call stable interfaces such as `generate()`, `embed()`, `search_web()`, and `search_corpus()`. They should not know whether inference is running on CPU llama.cpp, OpenVINO, vLLM, or a later GPU backend.
