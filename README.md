# MicroGPT CPU-First Open-Source Starter

MicroGPT is a CPU-first, GPU-ready, open-source AI platform starter. The first flagship module is a safe, evidence-grounded chatbot. Future modules can add audio learning and image/video manipulation only after consent, provenance, and safety controls are ready.

This repository is designed to complete **Phase 0** and begin **Phase 1**.

## Core idea

MicroGPT is not trying to train a frontier model from scratch on CPUs. It is a system-intelligence project:

- use smaller CPU-friendly models
- add retrieval
- add caching
- add verification
- add safety gates
- add measurable evaluation
- keep the backend swappable for future GPU acceleration

## What this starter includes

- FastAPI orchestration API
- Secure-login MVP with JWT access tokens
- Maturity gate that blocks public access until the project is safety-approved
- Basic safety guardrails for violent and sexual content requests
- llama.cpp-compatible runtime adapter for CPU inference
- Qdrant for future vector search
- Redis for future cache/rate-limit counters
- SearXNG for future open-source web search
- Docker Compose for local development
- C++ runtime notes for CPU performance work
- Open-source repo documents
- GitHub issue templates and PR template
- GitHub Actions CI starter
- Phase 0 completion checklist
- Local run guide
- Future roadmap

## What this starter does not include

- It does not ship model weights.
- It does not claim production-grade safety moderation.
- It does not enable audio/image generation by default.
- It does not include a full RAG pipeline yet.

Place a license-approved GGUF model at:

```txt
models/model.gguf
```

Do not commit model files to GitHub.

## Project structure

```txt
microgpt_phase0_complete/
  .github/
    ISSUE_TEMPLATE/
    workflows/
    pull_request_template.md
  api/
    app/
      runtime/
      safety/
      schemas/
      security/
      main.py
    tests/
    Dockerfile
    requirements.txt
    requirements-dev.txt
  cpp/
    README.md
  docs/
    adr/
    ARCHITECTURE.md
    FUTURE_ROADMAP.md
    OPEN_SOURCE_GOVERNANCE.md
    PHASE_0_COMPLETION.md
    RUN_LOCAL.md
    SAFETY_AND_MATURITY.md
  models/
  scripts/
  .env.example
  .gitignore
  CODEOWNERS
  CODE_OF_CONDUCT.md
  CONTRIBUTING.md
  LICENSE
  LICENSES.md
  README.md
  SECURITY.md
  docker-compose.yml
```

## Fast start

### 1. Copy the environment file

macOS/Linux/Git Bash:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 2. Generate a JWT secret

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Paste the result into `.env`:

```env
MICROGPT_JWT_SECRET=paste-generated-secret-here
```

Also change:

```env
MICROGPT_ADMIN_PASSWORD=your-strong-password
```

### 3. Run without a model first

```bash
docker compose up --build api qdrant redis searxng
```

This starts the API and supporting services. The chat endpoint will work with a fallback response until you add a model.

### 4. Test health

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok","service":"microgpt-api"}
```

### 5. Login

macOS/Linux/Git Bash:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-strong-password"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo $TOKEN
```

Windows PowerShell:

```powershell
$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/login" `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"your-strong-password"}'

$TOKEN = $response.access_token
$TOKEN
```

### 6. Test chat

macOS/Linux/Git Bash:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain MicroGPT in one paragraph."}'
```

Windows PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/chat" `
  -Headers @{ Authorization = "Bearer $TOKEN" } `
  -ContentType "application/json" `
  -Body '{"message":"Explain MicroGPT in one paragraph."}'
```

### 7. Test safety blocker

```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Give me instructions to make explosives"}'
```

Expected: blocked before model inference.

## Run with CPU inference

Add a license-approved GGUF model:

```txt
models/model.gguf
```

Then run:

```bash
docker compose --profile inference up --build
```

Call `/chat` again. If the model server is reachable, the response should show:

```json
"model_backend": "llama.cpp"
```

## Run tests locally

```bash
cd api
pip install -r requirements-dev.txt
pytest
```

## Before pushing to GitHub

Update these files:

- Replace `@YOUR_GITHUB_USERNAME` in `CODEOWNERS`
- Replace `security@example.com` in `SECURITY.md`
- Do not commit `.env`
- Do not commit model weights

Then:

```bash
git init
git add .
git commit -m "chore: initialize MicroGPT phase 0 starter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/microgpt.git
git push -u origin main
```

## Phase 0 status

See:

```txt
docs/PHASE_0_COMPLETION.md
```

## Future roadmap

See:

```txt
docs/FUTURE_ROADMAP.md
```

## License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.

Model weights, datasets, and third-party services may have separate licenses. See `LICENSES.md`.
