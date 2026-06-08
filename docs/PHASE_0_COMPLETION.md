# Phase 0 Completion Checklist

Phase 0 creates the repo foundation before the team starts building features.

## Completed in this starter

- [x] CPU-first project structure
- [x] FastAPI API skeleton
- [x] JWT login endpoint
- [x] Chat endpoint protected by login
- [x] Maturity gate
- [x] Basic safety blocker for violent and sexual content requests
- [x] llama.cpp-compatible runtime adapter
- [x] Docker Compose for API, Qdrant, Redis, SearXNG, and optional llama.cpp
- [x] README with setup and run instructions
- [x] Apache-2.0 project license
- [x] License tracking document
- [x] Contributing guide
- [x] Code of conduct
- [x] Security policy
- [x] CODEOWNERS template
- [x] GitHub issue templates
- [x] GitHub PR template
- [x] GitHub Actions CI starter
- [x] ADR 0001: CPU-first open-source platform
- [x] ADR 0002: secure login and maturity gate

## You must update before publishing

- [ ] Replace `@YOUR_GITHUB_USERNAME` in `CODEOWNERS`
- [ ] Replace `security@example.com` in `SECURITY.md`
- [ ] Set a strong `MICROGPT_JWT_SECRET` in local `.env`
- [ ] Set a strong `MICROGPT_ADMIN_PASSWORD` in local `.env`
- [ ] Confirm model license before placing any GGUF model in `models/`

## Phase 0 exit criteria

Phase 0 is complete when:

- The repo is pushed to GitHub.
- Open-source governance docs exist.
- Contributors know how to run the project.
- Login works.
- Chat requires login.
- Maturity gate exists.
- Violent/sexual unsafe prompts are blocked before model inference.
- Model files and secrets are excluded from Git.

## Phase 1 next objective

Phase 1 should connect real CPU inference and begin retrieval:

- Add a license-approved GGUF model.
- Start llama.cpp through Docker Compose.
- Add local document ingestion.
- Add SQLite FTS5 keyword search.
- Add Qdrant vector indexing.
- Add SearXNG web search adapter.
- Add citations and retrieval traces.
