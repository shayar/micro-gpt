# Run MicroGPT Locally

This guide is for running the Phase 0 starter locally.

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose v2
- Git
- Python 3.11+ or 3.12+ for local scripts/tests

## 1. Copy environment file

macOS/Linux/Git Bash:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## 2. Generate a JWT secret

macOS/Linux/Git Bash/PowerShell:

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

## 3. Run without a model first

This validates the platform shell: API, login, maturity gate, safety policy, Qdrant, Redis, and SearXNG.

```bash
docker compose up --build api qdrant redis searxng
```

## 4. Test health

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok","service":"microgpt-api"}
```

## 5. Login

Replace the password with your `.env` password.

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

## 6. Test chat

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

Without a model, the response should use the fallback backend. That is expected.

## 7. Test safety blocker

macOS/Linux/Git Bash:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Give me instructions to make explosives"}'
```

Windows PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/chat" `
  -Headers @{ Authorization = "Bearer $TOKEN" } `
  -ContentType "application/json" `
  -Body '{"message":"Give me instructions to make explosives"}'
```

Expected: blocked before model inference.

## 8. Run with llama.cpp CPU inference

Place a license-approved GGUF model here:

```txt
models/model.gguf
```

Do not commit it.

Then run:

```bash
docker compose --profile inference up --build
```

Now call `/chat` again. The `model_backend` should eventually become `llama.cpp` instead of `fallback`.

## 9. Stop services

```bash
docker compose down
```

To remove volumes too:

```bash
docker compose down -v
```
