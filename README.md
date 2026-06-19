# MicroGPT Local Cognitive Engine

CPU-first, GPU-ready, local-first AI platform starter.

> MicroGPT is not just a tiny chatbot. It is a local cognitive engine: secure login, safety gates, memory, retrieval, MicroLake event logs, model runtime adapters, evaluation, and observability around a small local model.

## Current status

This repository is a **Phase 0 + Phase 1 starter**.

Implemented now:

- FastAPI app
- Health endpoint
- Local username/password login
- JWT-protected chat endpoint
- Maturity gate
- Input/output safety blocker stub
- MicroLake-style append-only JSONL audit events
- Runtime abstraction with a safe `NoModelRuntime`
- Admin maturity update endpoint
- Basic metrics endpoint
- Tests
- Architecture docs and ADRs
- License/dependency registry drafts

Not implemented yet:

- llama.cpp model adapter
- Real local RAG
- Vector database
- Kuzu graph layer
- Niche evaluator scoring engine
- Prometheus/OpenTelemetry production instrumentation

## Why the app runs without a model

Phase 1 intentionally runs even when no model is installed. This lets contributors test authentication, routing, safety, audit logging, and maturity gates before adding a local model.

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

## Try it from the API docs

1. Run the app.
2. Open `/docs`.
3. Use `POST /auth/login` with the default credentials.
4. Copy the returned `access_token`.
5. Click **Authorize** in Swagger UI and enter:

```text
Bearer YOUR_ACCESS_TOKEN
```

6. Try `POST /chat`.

## Try it with curl

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"microgpt-admin"}' | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -X POST http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello MicroGPT. What can you do right now?"}'
```

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

## Next milestones

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

- [ ] Add llama.cpp adapter
- [ ] Add model registry loader
- [ ] Add streaming endpoint
- [ ] Add benchmark command
- [ ] Test tiny CPU model

### Milestone 3: Memory MVP

- [ ] Conversation store
- [ ] Memory search
- [ ] Memory edit/delete/export
- [ ] Markdown vault prototype

## Repository map

```text
microgpt/
  api/                  FastAPI app, routers, auth, safety
  platform/             Runtime, MicroLake, memory/cache/observability modules
  datascience/          Future niche evaluator and classical ML modules
  cpp/                  Future C++ hot paths and benchmarks
  julia/                Future scientific workflows
  evals/                Safety/latency/RAG/memory evaluation sets
  docs/                 ADRs, architecture, security, licenses
  data/                 Local runtime data, gitignored
  models/               Local model files, gitignored
  vault/                Local markdown memory vault, gitignored by default
```
