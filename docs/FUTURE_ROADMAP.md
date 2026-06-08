# Future Roadmap

This file explains where MicroGPT goes after Phase 0.

## Phase 1: Platform Skeleton

Goal: prove the shared platform can run locally on CPU.

Planned work:

- llama.cpp CPU inference with a license-approved GGUF model
- `/generate` runtime adapter cleanup
- `/embed` interface
- SearXNG search adapter
- Local document ingestion
- SQLite FTS5 keyword search
- Qdrant vector search
- Cache abstraction
- OpenTelemetry/Prometheus placeholders

Exit criteria:

- Developer can run Docker Compose locally.
- Developer can log in.
- API can call the local model backend.
- API can retrieve docs/search results.
- API can generate a basic answer.

## Phase 2: Chatbot MVP

Goal: evidence-cited chatbot demo.

Planned work:

- classify -> cache -> retrieve -> web if needed -> draft -> verify -> cite
- citation formatting
- source preview
- simple UI
- fixed evaluation question set
- hallucination and unsupported-claim checks

## Phase 3: Retrieval and Memory Hardening

Goal: measurable quality improvement.

Planned work:

- retrieval precision metrics
- citation coverage metrics
- answer faithfulness checks
- cache hit-rate tracking
- failure traces
- regression question set

## Phase 4: Audio Learning MVP

Goal: safe audio ingestion and transcription first.

Planned work:

- consent schema
- audio validation
- VAD/noise trimming
- whisper.cpp transcription
- audit logs
- provenance records

No voice cloning or speaker synthesis should ship without consent and safety review.

## Phase 5: Image/Vision MVP

Goal: safe image editing first.

Planned work:

- OpenCV image transformation
- image provenance records
- safety checks before output download
- diffusion/inpainting research behind gate

## Phase 6: Research and v0.2 Planning

Goal: benchmark before adopting research ideas.

Research tracks:

- CPU-efficient inference
- hybrid retrieval
- RAPTOR/clustering memory
- GraphRAG
- verifier/critic pass
- evaluation loop
