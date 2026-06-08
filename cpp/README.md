# C++ Runtime Policy

MicroGPT should not rewrite the LLM engine from scratch. The CPU inference layer should rely on proven open-source C/C++ runtimes first, especially llama.cpp.

Use C++ when it improves CPU-bound performance or deployment simplicity:

- llama.cpp model serving and quantized GGUF inference
- high-throughput text chunking or tokenization experiments
- CPU benchmarking utilities
- native extensions only after Python becomes a measurable bottleneck

Avoid C++ for early product orchestration:

- authentication
- safety policy routing
- API endpoints
- documentation tooling
- evaluation scripts

The preferred architecture is Python/FastAPI for orchestration and C/C++ behind stable runtime interfaces for inference and performance-critical components.
