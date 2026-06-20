# MicroGPT Local Cognitive Engine

CPU-first, GPU-ready, local-first AI platform starter.

> MicroGPT is not just a tiny chatbot. It is a local cognitive engine: secure login, safety gates, model runtime adapters, memory/retrieval foundations, MicroLake event logs, evaluation, and observability around small local models.

## Current status

This repository is a **Phase 0 + Phase 1 + Phase 2.3 robust starter**.

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
- Automatic `.env` loading with `python-dotenv`
- Runtime status diagnostics that do not crash when native llama loading fails
- Hardware/specs endpoint for first-run model recommendations
- Local JSON model registry
- Streaming chat endpoint
- Phase 2.3 llama-cli output cleanup and prompt wrapper
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

## Phase 2.1/2.3: run a local CPU model with llama.cpp

The default mode is still safe fallback:

```env
MICROGPT_RUNTIME_MODE=no_model
```

To use a local GGUF model:

Recommended install path on Windows:

```bash
pip install -e ".[dev]"
pip install --prefer-binary llama-cpp-python==0.3.30 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
cp models/model_registry.example.json models/model_registry.local.json
```

You can still use `pip install -e ".[dev,llama]"` on machines where the wheel/build works, but the separated install makes Windows troubleshooting easier.

Then edit `.env`:

```env
MICROGPT_RUNTIME_MODE=llama_cpp
MICROGPT_MODEL_REGISTRY_PATH=./models/model_registry.local.json
MICROGPT_ACTIVE_MODEL_ID=qwen3-0.6b-gguf-local
MICROGPT_LLAMA_N_THREADS=4
MICROGPT_LLAMA_N_GPU_LAYERS=0
```

Recommended local layout:

```text
models/
  local/
    Qwen_Qwen3-0.6B-Q4_K_M.gguf
  model_registry.local.json
```

Update `models/model_registry.local.json` so the model path is `local/Qwen_Qwen3-0.6B-Q4_K_M.gguf`.

Important: model weights are local only and gitignored.


## Phase 2.3: llama-cli output cleanup

The Windows-friendly `llama_cli` adapter now wraps the raw user prompt with a small MicroGPT instruction prompt and cleans common `llama-cli` console noise from API responses, including:

- `Loading model...`
- `Exiting...`
- llama.cpp banner/menu text
- timing footer lines
- visible Qwen thinking blocks like `[Start thinking]`

For local CPU testing, use short prompts first:

```json
{
  "message": "Explain math to a 10-year-old in 3 short sentences.",
  "max_tokens": 64
}
```

`/chat/stream` is clean but intentionally conservative for `llama_cli`: it buffers the short-lived CLI process, cleans the answer, then yields the text in chunks. A future `llama_server` adapter should provide true token streaming with the model kept warm between requests.

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

## Runtime and system endpoints

- `GET /runtime/status` — shows configured runtime, fallback reason, model path, file existence, and llama settings
- `GET /runtime/models` — lists registry entries
- `GET /runtime/recommendations` — recommends a model tier from local specs
- `GET /system/specs` — reports CPU/Python/OS/disk info for first-run onboarding

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
- [x] Keep safe fallback when native llama loading fails
- [x] Add runtime diagnostics and first-run specs endpoint
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


## Windows llama-cpp troubleshooting

If `/runtime/status` reports a fallback reason containing `Windows error 0xc000001d`, the API is working but the native llama runtime failed during model load. This can happen even when the CPU reports AVX2/FMA because the installed wheel may be incompatible with the exact Windows/Python/runtime combination.

Try these in order:

1. Use Python 3.12, not 3.14.
2. Install the CPU wheel separately:

```powershell
pip uninstall -y llama-cpp-python
pip install --no-cache-dir --prefer-binary llama-cpp-python==0.3.30 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

3. If it still fails, keep `MICROGPT_RUNTIME_FALLBACK_ENABLED=true` so the app remains usable, and test standalone llama.cpp.
4. Later we should add a `llama_cli` / `llama_server` adapter for Windows-friendly execution outside Python native bindings.

The app should no longer crash on `/runtime/status`; it should report the fallback reason and keep running.

---

## Phase 2.2 Update: Standalone llama.cpp CLI Runtime

This build adds a Windows-friendly runtime mode that calls the standalone `llama-cli` binary instead of using `llama-cpp-python`.

Use this mode when:

- `llama-cli` works in the terminal.
- `llama-cpp-python` fails with native Windows errors such as `0xc000001d`.
- You want to test GGUF inference without compiling Python native extensions.

### 1. Confirm standalone llama.cpp works

```powershell
llama-cli -m models\local\Qwen_Qwen3-0.6B-Q4_K_M.gguf -p "Explain AI to a kid." -n 128
```

### 2. Configure MicroGPT for llama-cli

Copy the example files:

```powershell
copy .env.example .env
copy models\model_registry.example.json models\model_registry.local.json
```

Edit `.env`:

```env
MICROGPT_RUNTIME_MODE=llama_cli
MICROGPT_ACTIVE_MODEL_ID=qwen3-0.6b-q4-k-m-local
MICROGPT_LLAMA_CLI_PATH=llama-cli
MICROGPT_LLAMA_N_THREADS=4
MICROGPT_LLAMA_MAX_TOKENS=128
MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS=300
```

If `llama-cli` is not available from PATH, set the full executable path:

```env
MICROGPT_LLAMA_CLI_PATH=C:/path/to/llama-cli.exe
```

### 3. Run the API

```powershell
uvicorn microgpt.api.main:app --reload
```

### 4. Test in Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

1. `POST /auth/login`
2. Authorize with the returned token
3. `GET /runtime/status`
4. `POST /chat`
5. `POST /chat/stream`

Expected runtime fields:

```json
{
  "configured_runtime_mode": "llama_cli",
  "active_runtime": "llama_cli"
}
```


### 5. Timeout and streaming behavior

Phase 2.2 changes the `llama_cli` adapter from `subprocess.run(...)` to `subprocess.Popen(...)`, so `/chat/stream` can stream chunks from `llama-cli` instead of waiting for the whole response first.

If a request still times out, start with fewer tokens:

```json
{
  "message": "Explain AI to a kid.",
  "max_tokens": 64
}
```

Then increase this only if needed:

```env
MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS=600
```

For weak CPU laptops, `MICROGPT_LLAMA_N_CTX=1024` can also reduce load.

### Runtime modes now supported

| Mode | Use case |
|---|---|
| `no_model` | Safe fallback and platform testing |
| `llama_cli` | Standalone llama.cpp binary, recommended Windows-first path |
| `llama_cpp` | Python binding through `llama-cpp-python`, optional |

