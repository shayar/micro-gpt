# MicroGPT Local Cognitive Engine

CPU-first, GPU-ready, local-first AI platform starter.

> MicroGPT is not just a tiny chatbot. It is a local cognitive engine: secure login, safety gates, model runtime adapters, memory/retrieval foundations, MicroLake event logs, evaluation, and observability around small local models.

## Current status

This repository is a **Phase 0 + Phase 1 + Phase 2 starter**.

Implemented now:

- FastAPI app
- Health endpoint
- Local username/password login
- JWT-protected chat endpoint
- Maturity gate
- Input/output safety blocker stub
- MicroLake-style append-only JSONL audit events
- Runtime abstraction with safe `NoModelRuntime`
- Optional `llama_cpp` runtime adapter through `llama-cpp-python`
- Local JSON model registry
- Streaming chat endpoint
- Runtime benchmark script
- Document identity/provenance registry with MD5 + SHA-256
- Deleted/moved file reconciliation foundation
- Admin maturity update endpoint
- Basic metrics endpoint
- Tests
- Architecture docs and ADRs
- License/dependency registry drafts

Not implemented yet:

- Full local RAG
- Vector database
- Kuzu graph layer
- Niche evaluator scoring engine
- Prometheus/OpenTelemetry production instrumentation
- Production-grade safety classifier

## Why the app still runs without a model

Phase 2 keeps the default runtime as `no_model`. This lets contributors test authentication, routing, safety, streaming, audit logging, document identity, and maturity gates before installing a local GGUF model.

## Requirements

- Python 3.11+
- Git
- Windows PowerShell, macOS Terminal, or Linux shell

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
copy .env.example .env
python scripts/init_dev.py
uvicorn microgpt.api.main:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
python scripts/init_dev.py
uvicorn microgpt.api.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Default local login

Development-only default:

```text
username: admin
password: microgpt-admin
```

Change it in `.env` before sharing the repo or deploying anywhere.

## Try chat from the API docs

1. Run the app.
2. Open `/docs`.
3. Use `POST /auth/login` with the default credentials.
4. Copy the returned `access_token`.
5. Click **Authorize** in Swagger UI and enter:

```text
Bearer YOUR_ACCESS_TOKEN
```

6. Try `POST /chat`.

## Try streaming chat

Use `POST /chat/stream` in Swagger UI or with curl:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"microgpt-admin"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -N -X POST http://127.0.0.1:8000/chat/stream \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello MicroGPT. Stream a short answer."}'
```

## Phase 2: run a local CPU model with llama.cpp

The default mode is still safe fallback:

```env
MICROGPT_RUNTIME_MODE=no_model
```

To use a local GGUF model:

```bash
pip install -e ".[dev,llama]"
cp models/model_registry.example.json models/model_registry.local.json
```

Then edit `.env`:

```env
MICROGPT_RUNTIME_MODE=llama_cpp
MICROGPT_MODEL_REGISTRY_PATH=./models/model_registry.local.json
MICROGPT_ACTIVE_MODEL_ID=qwen3-0.6b-gguf-local
MICROGPT_LLAMA_N_THREADS=4
MICROGPT_LLAMA_N_GPU_LAYERS=0
```

Put your GGUF file in `models/` and update `models/model_registry.local.json` so `path` matches your local file.

Important: model weights are local only and gitignored.

## Benchmark the runtime

```bash
python scripts/benchmark_runtime.py --prompt "Explain MicroGPT in one short paragraph." --runs 3 --max-tokens 128
```

Results are appended to:

```text
data/events/benchmark_runs.jsonl
```

## Document identity / provenance foundation

This is your file-management idea implemented as a foundation before full RAG.

Register a file:

```bash
python scripts/check_documents.py README.md
```

Or through the API:

```text
POST /documents/register
```

The registry stores:

- original path
- canonical path/location
- filename
- extension
- size
- modified timestamp
- MD5
- SHA-256
- stable `document_id`
- exists/missing status

Check deleted or moved files:

```bash
python scripts/check_documents.py --reconcile
```

Later, Phase 4 RAG will use this to answer: **which exact document was used, did it change, and what old chat context can still help if the file disappeared?**

## Runtime endpoints

- `GET /runtime/status`
- `GET /runtime/models`

## Document endpoints

- `POST /documents/register`
- `GET /documents`
- `POST /documents/reconcile`
- `GET /documents/{document_id}/context`

## Test

```bash
pytest
```

## Important security note

This is a local development skeleton. It is not production-ready. Before any public use, complete:

- Strong password policy
- Secret rotation
- Real user database
- Rate limiting
- Strong safety classifier
- Prompt-injection tests
- Full audit review
- Dependency license scanning
- Evaluation report

## Milestones

### Milestone 1: Secure local skeleton

- [x] FastAPI app
- [x] Health route
- [x] Local login
- [x] JWT-protected chat endpoint
- [x] Maturity gate
- [x] Safety blocker stub
- [x] Local audit log
- [x] App runs without model installed

### Milestone 2: CPU runtime

- [x] Add llama.cpp adapter
- [x] Add model registry loader
- [x] Add streaming endpoint
- [x] Add benchmark command
- [x] Keep safe fallback when model is missing
- [ ] Download and validate one tiny CPU model locally
- [ ] Benchmark tiny model on target laptops

### Provenance improvement added early

- [x] Document identity registry
- [x] MD5 + SHA-256 file fingerprints
- [x] File location/canonical path tracking
- [x] Deleted/moved file reconciliation
- [x] Best-effort context recovery from old conversation logs

### Milestone 3: Memory MVP

- [ ] Conversation store
- [ ] Memory search
- [ ] Memory edit/delete/export
- [ ] Markdown vault prototype

### Milestone 4: Local RAG MVP

- [ ] File ingest
- [ ] Chunking
- [ ] SQLite FTS5
- [ ] Qdrant
- [ ] Citations
- [ ] Verifier

## Repository map

```text
microgpt/
  api/                  FastAPI app, routers, auth, safety
  platform/             Runtime, documents, MicroLake, memory/cache/observability modules
  datascience/          Future niche evaluator and classical ML modules
  cpp/                  Future C++ hot paths and benchmarks
  julia/                Future scientific workflows
  evals/                Safety/latency/RAG/memory evaluation sets
  docs/                 ADRs, architecture, runtime, provenance, security, licenses
  data/                 Local runtime data, gitignored
  models/               Local model files, gitignored except example registry
  vault/                Local markdown memory vault, gitignored by default
```
