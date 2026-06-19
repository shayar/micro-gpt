# MicroGPT Local Cognitive Engine

Technical Architecture, System Design, Open-Source Validation, and Phased Delivery Plan

Working Document v0.6 | CPU-First, GPU-Ready | Local-First Privacy | Open-Source Only

Owner: Shayar Shrestha, Interim AI Lead | Generated: June 18, 2026

> Core Thesis: MicroGPT should not be a tiny chatbot. It should be a local-first cognitive engine where a small open model is surrounded by memory, retrieval, graph reasoning, data mining, traditional ML, cache, verification, safety, and observability.

## 1. Executive Summary

MicroGPT should be built as a local-first cognitive engine rather than a small chatbot. The raw language model will be intentionally small and efficient, but the surrounding system will be ambitious: retrieval, memory, graph reasoning, data mining, traditional ML, verification, caching, observability, authentication, safety, and local lakehouse-style storage.

The goal is not to claim that a CPU laptop can match a frontier model's raw parameter-scale intelligence. The goal is to build a system that delivers frontier-style workflows on modest hardware by combining many reliable open-source techniques. MicroGPT should be able to understand a user's local files, project history, decisions, niche interests, research ideas, and personal knowledge vault while keeping data local by default.

The v0.4 plan already established the right backbone: one shared CPU-first platform with inference, search, memory, cache, safety, provenance, evaluation, and secure access/maturity gates. This v0.6 plan expands that into a full technical and architectural system design with an explicit open-source validation policy, a CPU/GPU runtime strategy, a MicroLake storage layer, an Obsidian-inspired vault, MemPalace-inspired long-term memory, Shudhi-inspired cache/debug visibility, a data science engine, a niche evaluator, and deep observability.

## 2. Product Positioning

MicroGPT should be described as an open-source local AI platform for students, researchers, developers, nonprofits, small teams, and technical learners who want AI that understands their own context without sending private data to a cloud provider.

Recommended positioning statement:

MicroGPT is a local-first, CPU-friendly, open-source cognitive engine that combines small open models with memory, search, data mining, graph reasoning, verification, safety, and observability to deliver frontier-style workflows on personal hardware.

The strongest differentiator is system intelligence. MicroGPT does not rely only on the LLM. It routes each task to the cheapest reliable method: rules, SQL, keyword search, vector search, graph traversal, classical ML, numerical optimization, Julia simulations, C++ acceleration, or local language model generation.

## 3. Non-Goals and Honesty Boundaries

MicroGPT should be ambitious, but honest.

Non-goals for v0.1:
- Do not train a frontier-scale foundation model from scratch.
- Do not promise ChatGPT-like speed on CPU.
- Do not ship public access before safety and maturity gates pass.
- Do not commit model weights into the GitHub repository.
- Do not copy code from any project until license and attribution are validated at the exact commit/version.
- Do not rely on closed-source cloud APIs in the default local mode.
- Do not ship audio/vision identity features without consent, provenance, and audit logs.

Honest claim:
MicroGPT competes through local privacy, transparency, open architecture, explainability, task routing, memory, retrieval, evaluation, and CPU/GPU efficiency - not through raw model size alone.

## 4. Design Inspirations

This project should intentionally borrow ideas from engineering disciplines that already solve hard constraints.

From Formula 1 engineering: use telemetry, incremental gains, benchmarks, and fast feedback. Every release should improve a measurable metric such as latency, retrieval precision, citation coverage, cache hit rate, memory recall, or safety bypass rate.

From spacecraft engineering: assume limited compute, offline operation, partial subsystem failure, and the need for safe mode. MicroGPT should keep a small reliable core and degrade gracefully if model inference, web search, GPU, graph search, or embeddings are unavailable.

From old-school programmers: prefer plain files, small modules, deterministic logs, stable interfaces, and profiling before optimization. Use Python for orchestration, C++ for measured hot paths, Julia for numerical/scientific experiments, and PostgreSQL for durable multi-user metadata.

From doctors: use triage, differential diagnosis, evidence hierarchy, safety contraindications, and case notes. MicroGPT should classify requests before answering and should produce uncertainty and citations where needed.

From scientists: build baselines, run experiments, preserve reproducibility, and publish research notes. Every model, retriever, memory strategy, cache policy, and verifier should have an evaluation pathway.

From Databricks/Delta Lake: separate immutable event logs, snapshots, schema enforcement, lineage, and time travel so local AI memory can be reproducible and rollback-friendly.

## 5. Open-Source Validation Policy

Every dependency must pass an open-source validation gate before being used in the core repository. Validation means checking the exact source repository, license file, model card, dataset card, and transitive dependency risks. A project being popular or described as open-source in a README is not enough.

Policy rules:
1. Prefer OSI-approved licenses for core dependencies: MIT, Apache-2.0, BSD-2/3-Clause, PostgreSQL License, PSF License, and public domain components.
2. Allow copyleft tools such as AGPL only when they are isolated as optional services and their obligations are understood.
3. Avoid source-available or custom licenses in the core unless leadership/legal approval is recorded.
4. Do not copy code from repositories with no visible license. Ideas may be used, but code must not be copied.
5. For model weights, validate the exact model card and license at the specific revision. Open-weight does not always mean open-source or commercially unrestricted.
6. Maintain LICENSES.md, MODEL_REGISTRY.md, DATASET_REGISTRY.md, and NOTICE files before any public release.
7. Run license scanning in CI, and block PRs that introduce unknown or incompatible licenses.

### 5.1 Validated Stack Snapshot

| Component | Role | Validated license/status | Decision |
|---|---|---|---|

| Python | Core orchestration, API, ML workflows | PSF License | Approved core |

| C++ | Inference runtime, tokenization, CPU hot paths | Language has no license; use validated compilers/libs | Approved core with dependency validation |

| Julia | Scientific computing, optimization, simulations | MIT | Approved research/core optional |

| PostgreSQL | Durable metadata, users, audit, pgvector option | PostgreSQL License | Approved core for server mode |

| FastAPI | Python API/orchestration | MIT | Approved core |

| Strawberry GraphQL | Graph/vault explorer API | MIT | Approved optional |

| Keycloak | Team/server IAM | Apache-2.0 | Approved optional/server mode |

| llama.cpp | Local CPU/GPU LLM inference | MIT | Approved core runtime |

| bitnet.cpp | 1.58-bit inference research | MIT | Approved research runtime |

| Qwen3 small models | Tiny/standard model candidates | Apache-2.0 per Qwen3 blog | Candidate; validate exact model card |

| SmolLM3/Smol models | Small local model candidate | Apache-2.0 in repo | Candidate; validate exact model card |

| OLMo/OLMo 2 | Fully open research baseline | Apache-2.0 | Candidate; validate exact model card |

| SQLite | Local metadata, FTS5, single-user mode | Public domain | Approved core |

| Qdrant | Vector search | Apache-2.0 | Approved core/optional local service |

| Kuzu | Embedded graph DB | MIT | Approved graph layer |

| DuckDB | Local analytics | MIT | Approved data science layer |

| Polars | DataFrame engine | MIT | Approved data science layer |

| scikit-learn | Classical ML/data mining | BSD-3-Clause | Approved data science layer |

| Valkey | Cache, queue, rate limits | BSD | Approved Redis-compatible choice |

| SearXNG | Optional metasearch | AGPL-3.0 | Optional isolated service; review obligations |

| OpenTelemetry | Traces, metrics, logs | Apache-2.0 ecosystem | Approved observability |

| Prometheus | Metrics store | Apache-2.0 | Approved observability |

| Grafana OSS | Dashboards | AGPLv3 | Optional; understand AGPL obligations |

| DCGM Exporter | NVIDIA GPU metrics | Apache-2.0 | Approved GPU monitoring optional |

| Delta Lake | Lakehouse inspiration / future compatibility | Apache-2.0 | Approved optional/future |

| Apache Iceberg | Open table format option | Apache-2.0 | Approved optional/future |

| Apache Parquet | Columnar table files | Apache-2.0 | Approved MicroLake table format |

| MemPalace | Local-first memory inspiration or dependency | MIT | Approved candidate; validate exact version |

| Shudhi | Cache inspector inspiration | No visible license in fetched listing | Do not copy code until license confirmed |

| Open WebUI | UI inspiration | Current mixed/custom terms | Inspiration only; avoid dependency for core |



## 6. High-Level Architecture

MicroGPT is a modular local platform. Each product feature calls stable interfaces rather than talking directly to one model, database, or search engine. This keeps the system CPU-first today, GPU-ready later, and replaceable when better open-source tools appear.

The platform has nine layers:
1. Interface Layer: chat, vault, graph explorer, niche evaluator, admin dashboard, monitoring dashboard.
2. Access and Safety Layer: local login, optional Keycloak, maturity gates, RBAC, content safety, audit logs.
3. Orchestration Layer: FastAPI, optional GraphQL, planner/router, task queue, tool registry.
4. Runtime Layer: llama.cpp, BitNet research runtime, CPU/GPU adapters, model registry.
5. Knowledge Layer: local memory, local documents, keyword search, vector search, graph search, citations.
6. Data Science Layer: DuckDB, Polars, scikit-learn, clustering, anomaly detection, scoring, forecasting.
7. MicroLake Storage Layer: append-only event logs, Parquet tables, snapshots, lineage, rollback.
8. Observability Layer: OpenTelemetry, Prometheus, Grafana-compatible dashboards, CPU/GPU metrics, LLM quality metrics.
9. Governance Layer: licensing, evaluations, release gates, CODEOWNERS, security policy, contributor workflow.

### 6.1 System Diagram
```text
MicroGPT Local Cognitive Engine
|
+-- Interface Layer
|   +-- Chat UI
|   +-- Obsidian-style Vault
|   +-- Graph Explorer
|   +-- Niche Evaluator
|   +-- Admin/Safety Dashboard
|   +-- Monitoring Dashboard
|
+-- Access + Safety Layer
|   +-- Local Auth / JWT
|   +-- Optional Keycloak
|   +-- Maturity Gate
|   +-- RBAC
|   +-- Input/Output Safety
|   +-- Audit Log
|
+-- Orchestration Layer
|   +-- FastAPI REST
|   +-- Optional Strawberry GraphQL
|   +-- Planner / Router
|   +-- Tool Registry
|   +-- Job Queue
|
+-- Intelligence Layer
|   +-- llama.cpp Local LLM Runtime
|   +-- BitNet Research Runtime
|   +-- Embeddings + Reranker
|   +-- Verifier / Critic
|   +-- Traditional ML + Data Mining
|   +-- Rules / Symbolic Checks
|
+-- Knowledge Layer
|   +-- PostgreSQL / SQLite Metadata
|   +-- SQLite FTS5 Keyword Search
|   +-- Qdrant Vector Store
|   +-- Kuzu Knowledge Graph
|   +-- Markdown Vault
|   +-- Citation Index
|
+-- MicroLake Layer
|   +-- JSONL Event Logs
|   +-- Parquet Tables
|   +-- Snapshots + Manifests
|   +-- Lineage + Rollback
|
+-- Observability Layer
    +-- OpenTelemetry
    +-- Prometheus
    +-- Grafana-compatible Dashboards
    +-- DCGM Exporter for GPU mode
```

## 7. Core Request Flow

A normal MicroGPT request should not go directly to the LLM. It should go through a router that decides the best path.

Flow:
1. Authenticate user and enforce maturity gate.
2. Create request ID and audit record.
3. Run input safety classifier and prompt-injection checks.
4. Classify task type: simple chat, factual question, local document question, memory question, niche evaluation, data analysis, coding task, research task, unsafe task, or system action.
5. Check cache using task type, source fingerprints, memory version, model version, and TTL.
6. Retrieve relevant context from memory, vault, local documents, keyword index, vector index, graph, or optional web search.
7. Run deterministic/data-science tools where they are better than the LLM.
8. Generate draft answer with local model only after context is prepared.
9. Run verifier/critic: citation coverage, unsupported claims, contradiction, unsafe content, stale-memory risk.
10. Return final answer with citations, confidence, and trace summary.
11. Write event, memory candidates, retrieval traces, metrics, and safety decisions to MicroLake.

### 7.1 Request Flow Diagram
```text
User Request
   |
   v
Auth + Maturity Gate
   |
   v
Input Safety + Prompt Injection Check
   |
   v
Task Router
   |--------------------|--------------------|-------------------|
   v                    v                    v                   v
Memory Search       Local RAG            Data Science        Unsafe Refusal
   |                    |                    |                   |
   v                    v                    v                   |
Hybrid Retrieve     FTS + Vector + Graph  DuckDB/Polars/ML     |
   |                    |                    |                   |
   +----------+---------+---------+----------+                   |
              v                   v                              |
          Context Builder     Tool Results                        |
              |                   |                              |
              +---------+---------+                              |
                        v                                        |
                 Local LLM Generate                              |
                        |                                        |
                        v                                        |
               Verifier + Safety Output Check                    |
                        |                                        |
                        v                                        v
             Final Answer + Citations + Trace              Audit + Regression
```

## 8. Task Router Design

The task router is the core mechanism that lets a small model behave like a bigger system. It decides when not to use the LLM.

Task routes:
- Simple chat: local LLM with short context.
- Factual answer: hybrid retrieval + citations + verifier.
- Local document answer: document index + citation formatter.
- Personal/project memory: MemPalace-style memory + vault + graph.
- Niche evaluation: retrieval + data mining + scoring model + LLM explanation.
- Data analysis: DuckDB/Polars/scikit-learn first; LLM explains results after computation.
- Code understanding: static analysis + file graph + local RAG + LLM summary.
- Research synthesis: RAPTOR/GraphRAG-style retrieval + evidence hierarchy + verifier.
- Unsafe request: safety refusal or safe redirect.
- Heavy task: estimate cost/latency and ask user before continuing.

The router should be measurable. Every decision should be logged with route, confidence, reason, latency, and success/failure result.

## 9. Runtime and Model Strategy

MicroGPT should support multiple model runtimes behind stable interfaces. The runtime API should expose generate(), embed(), rerank(), classify(), transcribe(), synthesize(), and edit_image() even before all implementations are complete.

Primary runtime:
- llama.cpp for local CPU-first inference using GGUF models.

Research runtime:
- bitnet.cpp for 1.58-bit CPU/GPU inference experiments.

Optional adapter:
- Ollama can be supported as an adapter because it is MIT licensed, but MicroGPT should not depend on it as the core runtime.

Model registry categories:
- Tiny mode: Qwen3-0.6B or similar for weak laptops.
- Standard CPU mode: Qwen3-1.7B, SmolLM3-3B, or OLMo small variants.
- Strong local mode: 4B-8B quantized models where hardware allows.
- Research mode: BitNet b1.58 models, Mamba/RWKV-style models, and emerging CPU-efficient architectures.

Do not hard-code one model. The model registry should record model name, source, license, revision, quantization, RAM target, expected tokens/sec, context length, allowed use, and benchmark results.

## 10. Memory and Knowledge Vault

MicroGPT memory should be local-first, inspectable, and reversible. Inspired by MemPalace, the first principle is verbatim memory: store original snippets/events with metadata instead of relying only on summaries.

Memory record fields:
- memory_id
- user_id
- project_id
- memory_type: user, project, file, task, research, person, decision, failed_attempt
- raw_text
- source_type: chat, file, note, web, code, eval, system
- source_ref
- timestamp
- confidence
- visibility: private, project, shared
- expiry_policy
- vector_id
- graph_node_id
- deleted_at

Memory operations:
- remember
- search
- cite
- update
- delete
- export
- mark stale
- link to project/person/topic
- convert failure into regression test

Vault design:
- Store human-readable Markdown notes under /vault.
- Use links like [[MicroGPT Runtime]], [[Niche Evaluator]], and [[Safety Gate]].
- Maintain backlinks and graph relationships.
- Keep AI memory visible so users can correct it.

## 11. MicroLake: Local Lakehouse-Inspired Storage

MicroLake is the storage discipline for MicroGPT. It is inspired by Delta Lake and modern lakehouse ideas, but intentionally small enough to run on a laptop.

Design goals:
- Append-only history for auditability.
- Snapshot versions for rollback.
- Schema validation for memory, documents, evaluations, and safety logs.
- Lineage from answer back to documents, chunks, model version, prompt, and memory state.
- Reproducibility for benchmark and answer traces.

Recommended local layout:
/data
  /events
    conversations.jsonl
    memory_events.jsonl
    tool_calls.jsonl
    safety_events.jsonl
    eval_events.jsonl
  /tables
    documents.parquet
    chunks.parquet
    citations.parquet
    memories.parquet
    eval_results.parquet
    benchmark_runs.parquet
  /snapshots
    snapshot_000001.json
    snapshot_000002.json
  /indexes
    sqlite_fts.db
    qdrant/
    kuzu/
  /manifests
    model_registry.json
    license_registry.json
    dataset_registry.json
    lineage.json

MicroLake features for v0.1:
- append event
- validate schema
- create snapshot
- restore snapshot
- record lineage
- reproduce answer trace

Future features:
- Delta Lake or Apache Iceberg compatibility for larger deployments.
- PostgreSQL-backed metadata catalog.
- Local object store or MinIO-compatible mode if license obligations are accepted.

## 12. Data Science and Data Mining Engine

MicroGPT should not use an LLM for everything. A strong local AI system should use traditional approaches when they are cheaper, more accurate, or more explainable.

Core algorithms:
- TF-IDF and BM25 for exact matching.
- KMeans, HDBSCAN, and hierarchical clustering for topic discovery.
- UMAP/PCA for visualization and dimensionality reduction.
- Classification and regression via scikit-learn.
- Time-series anomaly detection for user habits, study patterns, or system behavior.
- Rule-based scoring for niche evaluation and safety gating.
- Graph algorithms for centrality, community detection, and relationship discovery.
- Statistical tests for evaluating whether changes improved the system.

Languages:
- Python: orchestration, ML, API, data workflows.
- C++: inference runtime, tokenization, low-level hot paths, SIMD-friendly operations.
- Julia: numerical experiments, optimization, scientific workflows, simulation research.
- SQL/PostgreSQL: metadata, user state, audit logs, memory, and analytics views.

## 13. Niche Evaluator Product Module

The niche evaluator is a flagship feature for students and researchers. A student should be able to enter a niche such as AI for agriculture in Nepal, AI-powered accessibility tools, local-language education, medical scheduling, or climate-risk mapping, and MicroGPT should evaluate feasibility rather than giving a shallow answer.

Pipeline:
1. Intake: ask goal, audience, skills, location, time, budget, hardware, and desired output.
2. Local context: search user's notes, projects, resume, coursework, and prior ideas.
3. Optional web research: use SearXNG only when enabled.
4. Topic mining: cluster related terms, papers, products, tools, datasets, and open-source repos.
5. Feasibility scoring: technical difficulty, data availability, local impact, competition, monetization/research potential, MVP path, safety risk.
6. Roadmap generation: 2-week MVP, 1-month prototype, 3-month open-source track.
7. Evidence report: citations, assumptions, risks, suggested datasets/tools, and evaluation metrics.
8. Memory writeback: store the niche, reasoning, selected roadmap, and future tasks.

Example score dimensions:
- Technical feasibility
- Dataset availability
- Local/community impact
- Novelty
- Competition
- MVP difficulty
- Research potential
- Career/project value
- Safety/regulatory risk

## 14. Retrieval and Graph Architecture

MicroGPT should use hybrid retrieval:
- SQLite FTS5 for keyword/BM25-style retrieval.
- Qdrant for dense semantic vector search.
- Reranker for final ordering.
- Kuzu graph for relationships among projects, people, documents, decisions, topics, claims, tools, and experiments.

Knowledge graph entities:
- Person
- Project
- Document
- Chunk
- Claim
- Topic
- Tool
- Model
- Memory
- Dataset
- Decision
- Experiment
- Evaluation

Relationships:
- WORKED_ON
- MENTIONS
- SUPPORTS
- CONTRADICTS
- DERIVED_FROM
- CITES
- SIMILAR_TO
- PART_OF
- FAILED_BECAUSE
- IMPROVED_BY

Retrieval flow:
1. Query rewrite and intent classification.
2. Keyword retrieval.
3. Vector retrieval.
4. Graph expansion for related entities.
5. Reciprocal rank fusion.
6. Reranking.
7. Context packing with citations.
8. Verifier checks source support.

## 15. Authentication, Access Control, and Maturity Gates

Secure access is not optional. The v0.4 draft already includes manager requirements for secure login, maturity gates, violent/sexual content blocking, audit logs, and no public release until safety gates pass.

Local mode:
- Local username/password.
- JWT or signed local sessions.
- Admin-only settings.
- Login required for generation endpoints.
- Local audit log.

Team/server mode:
- Keycloak for identity and access management.
- PostgreSQL for users/sessions/audit metadata.
- Roles: Admin, Maintainer, Contributor, Tester, Viewer.
- Fine-grained permissions for models, tools, memory, web search, uploads, audio, vision, and exports.

Maturity levels:
- Research: core team only.
- Internal alpha: authenticated contributors only.
- Private beta: approved testers only.
- Public: only after safety, evaluation, license, and release gates pass.

Default setting:
MICROGPT_PUBLIC_ACCESS=false

## 16. Safety and Responsible Release

Safety must be a platform layer, not a late middleware patch.

Required controls:
- Input safety classifier.
- Output safety classifier.
- Prompt-injection detection.
- Tool permission boundaries.
- Source trust scoring.
- Refusal and safe-completion policy.
- Audit logs for blocked attempts.
- Regression tests for known bypasses.
- Consent and provenance gates for audio/vision.
- No public access until maturity gate is approved.

Blocked v0.1 categories:
- Violent or weaponized instructions.
- Explicit sexual content generation.
- Non-consensual sexual media.
- Sexualized minor content.
- Voice impersonation without consent.
- Identity manipulation likely to mislead without provenance.
- Attempts to reveal secrets or override system/safety rules.

Every safety decision should include request_id, user_id, category, route, model version, release version, and review status.

## 17. Observability and Monitoring

MicroGPT should treat observability like an F1 pit wall. The team should see model speed, retrieval behavior, cache behavior, memory behavior, CPU/GPU usage, safety blocks, and quality metrics.

Metrics:
- LLM: tokens/sec, time to first token, total latency, context tokens, generation tokens, model ID.
- Retrieval: recall@k, precision@k, source count, reranker score, citation coverage.
- Memory: memory hit rate, stale memory, conflict rate, delete/edit counts.
- Cache: hit rate, TTL, invalidations, stale-cache incidents.
- System: CPU, RAM, disk I/O, queue depth.
- GPU optional: utilization, VRAM, power, temperature via DCGM exporter.
- Safety: blocked requests, bypass attempts, categories, post-generation rejections.
- Product: task success rate, failed routes, user feedback, repeated questions.

Stack:
- OpenTelemetry for traces/logs/metrics instrumentation.
- Prometheus for time-series metrics.
- Grafana-compatible dashboards, with awareness that Grafana OSS is AGPLv3.
- DCGM Exporter for NVIDIA GPU metrics in GPU mode.

## 18. API Design

Use REST for operational actions and GraphQL for exploratory graph/vault queries.

REST endpoints:
- POST /auth/login
- POST /auth/logout
- GET /health
- GET /metrics
- POST /chat
- POST /generate
- POST /ingest/file
- GET /documents
- GET /documents/{id}
- POST /memory
- GET /memory/search
- PATCH /memory/{id}
- DELETE /memory/{id}
- GET /cache/keys
- GET /cache/{key}
- DELETE /cache/{key}
- POST /niche/evaluate
- GET /evals/runs
- POST /admin/maturity

GraphQL use cases:
- Explore project graph.
- Query related memories/documents/decisions.
- Render graph explorer.
- Ask questions like: which decisions affected runtime design? Which documents support a claim? Which failed attempts should not be repeated?

Example GraphQL query:
query {
  project(name: "MicroGPT") {
    decisions { title date rationale }
    relatedDocuments { title citationCount }
    memories { text confidence sourceRef }
  }
}

## 19. Repository Structure

/microgpt
  /apps
    /web                    # React/Next or simple local UI
    /desktop                # optional future desktop wrapper
  /api
    /routers                # FastAPI routers
    /auth
    /safety
    /settings
    /schemas
  /platform
    /runtime                # generate/embed/rerank/classify interfaces
    /inference              # llama.cpp, bitnet, model registry
    /retrieval              # FTS, Qdrant, reranker, fusion
    /memory                 # memory engine and vault integration
    /graph                  # Kuzu graph adapters
    /microlake              # event log, snapshots, lineage
    /cache                  # answer/retrieval/model cache and inspector
    /observability          # OTEL, Prometheus, dashboards
  /datascience
    /features
    /clustering
    /niche_evaluator
    /scoring
    /experiments
  /cpp
    /benchmarks
    /tokenization
    /hotpaths
  /julia
    /optimization
    /simulation
    /scientific_workflows
  /evals
    /golden_questions
    /rag
    /memory
    /safety
    /latency
  /docs
    /adr
    /architecture
    /research
    /security
    /licenses
  /models                  # local only, gitignored
  /data                    # local only, gitignored
  docker-compose.yml
  LICENSES.md
  MODEL_REGISTRY.md
  DATASET_REGISTRY.md
  NOTICE
  README.md

## 20. Phased Delivery Plan

Phase 0 - Architecture and license lock:
- Finalize this document.
- Create LICENSES.md and dependency approval workflow.
- Create ADRs for local-first, llama.cpp, PostgreSQL/SQLite, MicroLake, memory design, and safety gates.
- Open GitHub milestones and issues.

Phase 1 - Secure local skeleton:
- FastAPI app, login, maturity gate, health, settings, audit log, safety blocker, local data folder.
- App must run even without a model installed.

Phase 2 - CPU model runtime:
- llama.cpp adapter, model registry, streaming, benchmark script, fallback behavior.
- Test at least one tiny and one stronger CPU model.

Phase 3 - Memory and vault:
- Conversation store, memory write policy, search, edit/delete/export, Markdown vault, backlinks.

Phase 4 - Local RAG:
- Document ingestion, chunking, SQLite FTS5, Qdrant, hybrid retrieval, reranking, citations, verifier.

Phase 5 - MicroLake:
- JSONL event logs, Parquet tables, snapshots, restore, lineage, reproducibility.

Phase 6 - Niche evaluator:
- Intake form, clustering, scoring, roadmap, evidence report, export.

Phase 7 - Graph intelligence:
- Kuzu schema, graph extraction, GraphQL query layer, graph explorer.

Phase 8 - Observability and performance lab:
- OpenTelemetry, Prometheus, dashboards, CPU/GPU metrics, quality dashboard, regression dashboard.

Phase 9 - Audio/vision research gates:
- Only after core safety, consent, provenance, and monitoring are stable.

## 21. Evaluation Strategy

Evaluation must be treated as a product feature.

Core metrics:
- Retrieval precision@5
- Retrieval recall@5
- Citation coverage
- Faithfulness
- Answer relevance
- Unsupported claim rate
- Memory recall accuracy
- Cache hit rate
- Safety bypass rate
- P50/P95 latency
- Tokens per second
- RAM footprint
- CPU utilization
- GPU utilization when applicable

Evaluation sets:
- Local project questions.
- Uploaded document questions.
- Memory questions.
- Niche evaluation tasks.
- Data analysis tasks.
- Coding/codebase questions.
- Safety red-team prompts.
- Freshness-sensitive questions where web search is enabled.

Release rule:
No evaluation report, no release.

## 22. Initial GitHub Milestones

Milestone 0: Repo foundation and licensing
- README.md
- CONTRIBUTING.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- CODEOWNERS
- LICENSES.md
- MODEL_REGISTRY.md
- issue templates
- PR template

Milestone 1: Secure local skeleton
- FastAPI health route
- local login
- maturity gate
- audit log
- safety stub
- local settings

Milestone 2: CPU runtime
- llama.cpp adapter
- streaming chat endpoint
- model registry
- benchmark command

Milestone 3: Memory MVP
- conversation store
- memory search
- memory edit/delete/export
- Markdown vault prototype

Milestone 4: Local RAG MVP
- file ingest
- chunking
- SQLite FTS5
- Qdrant
- citations
- verifier

Milestone 5: MicroLake MVP
- event log
- Parquet tables
- snapshot/restore
- lineage viewer

Milestone 6: Niche evaluator MVP
- intake form
- topic mining
- scoring
- roadmap report

Milestone 7: Observability MVP
- OpenTelemetry traces
- Prometheus metrics
- dashboard JSON
- safety and latency reports

## 23. Architecture Decision Records to Create

ADR-0001: Local-first by default.
ADR-0002: Open-source-only dependency gate.
ADR-0003: Python orchestration, C++ hot paths, Julia research, PostgreSQL durable state.
ADR-0004: llama.cpp as first runtime adapter.
ADR-0005: Model registry instead of hard-coded model.
ADR-0006: MemPalace-inspired memory, verbatim-first storage.
ADR-0007: Shudhi-inspired cache inspector, no code copy until license is validated.
ADR-0008: MicroLake event-sourced local storage.
ADR-0009: REST for operations, GraphQL for graph/vault exploration.
ADR-0010: Secure login and maturity gates before generation.
ADR-0011: Safety as architecture.
ADR-0012: Observability as release requirement.

## 24. Risks and Mitigations

Risk: CPU latency is too slow.
Mitigation: stream tokens, use tiny/standard/power-user model tiers, cache stable answers, route deterministic tasks away from LLM, and keep GPU adapter ready.

Risk: small model gives weak reasoning.
Mitigation: retrieval, graph context, decomposition, verifier, citations, data mining, and eval-driven prompt/routing improvements.

Risk: memory stores wrong facts.
Mitigation: confidence scores, expiry, user-visible memory, delete/edit/export, stale marking, and conflict detection.

Risk: licensing mistake.
Mitigation: license gate, exact-version validation, NOTICE file, no-code-copy rule for unlicensed repos, CI license scanning.

Risk: project becomes too broad.
Mitigation: keep v0.1 focused on secure local skeleton, CPU runtime, memory, local RAG, MicroLake, and observability. Audio/vision wait.

Risk: open-source contributors create inconsistent architecture.
Mitigation: CODEOWNERS, ADRs, module boundaries, PR templates, tests, eval reports, and release gates.

Risk: safety bypass.
Mitigation: input/output safety, tool permission boundaries, red-team prompts, audit logs, and regression tests.

## 25. Recommended v0.1 Promise

Do not promise that MicroGPT beats ChatGPT. Promise something stronger and more believable:

MicroGPT v0.1 is a local-first, CPU-friendly open-source AI platform that can run a small local model, remember approved conversations, search local files, cite evidence, inspect/delete memory and cache, enforce login and safety gates, and report its own performance through evaluation and observability.

That is a serious open-source foundation. Once this is stable, the team can add more model backends, data science modules, niche evaluators, graph intelligence, and later audio/vision modules.

## 26. References and Validation Sources

1. **Python Software Foundation License FAQ** — PSF License; permissive use of Python in open and non-open applications. https://wiki.python.org/moin/PythonSoftwareFoundationLicenseFaq

2. **Julia Language official site / license** — Julia is open source and made available under MIT license. https://julialang.org/

3. **PostgreSQL License** — PostgreSQL is released under the PostgreSQL License, a liberal open-source license similar to BSD/MIT. https://www.postgresql.org/about/licence/

4. **FastAPI GitHub** — FastAPI is licensed under MIT. https://github.com/fastapi/fastapi

5. **llama.cpp GitHub** — llama.cpp enables local inference across hardware and is MIT licensed. https://github.com/ggml-org/llama.cpp

6. **Microsoft BitNet GitHub** — bitnet.cpp is MIT licensed and targets 1.58-bit CPU/GPU inference. https://github.com/microsoft/BitNet

7. **Qwen3 official blog** — Qwen3 dense models include 0.6B/1.7B/4B/8B/14B/32B open-weight models under Apache 2.0. https://qwen.ai/blog?id=qwen3

8. **Hugging Face SmolLM repository** — Smol models project states an Apache-2.0 license; exact model card/version must be rechecked. https://github.com/huggingface/smollm

9. **Ai2 OLMo** — OLMo aims for a fully open model flow. https://allenai.org/olmo

10. **Ai2 OLMo GitHub** — OLMo code is Apache-2.0 licensed. https://github.com/allenai/OLMo

11. **Qdrant GitHub** — Qdrant is licensed under Apache License 2.0. https://github.com/qdrant/qdrant

12. **SQLite Copyright** — SQLite is in the public domain and does not require a license. https://sqlite.org/copyright.html

13. **DuckDB official site** — DuckDB is released under MIT license. https://duckdb.org/

14. **Polars official site** — Polars is open source and MIT licensed. https://pola.rs/

15. **scikit-learn PyPI** — scikit-learn is distributed under the 3-Clause BSD license. https://pypi.org/project/scikit-learn/

16. **Kuzu GitHub** — Kuzu is MIT licensed and provides embedded graph database features. https://github.com/kuzudb/kuzu

17. **SearXNG GitHub** — SearXNG is AGPL-3.0 and aggregates search results without tracking/profiling users. https://github.com/searxng/searxng

18. **Valkey official site** — Valkey is an open-source BSD key/value datastore. https://valkey.io/

19. **OpenTelemetry official site** — OpenTelemetry is an open-source observability framework for traces, metrics, and logs. https://opentelemetry.io/

20. **Prometheus official site** — Prometheus is 100% open source under Apache 2.0. https://prometheus.io/

21. **Grafana licensing** — Grafana core open-source projects moved to AGPLv3. https://grafana.com/licensing/

22. **NVIDIA DCGM Exporter GitHub** — dcgm-exporter is Apache-2.0 licensed and exposes GPU metrics for Prometheus. https://github.com/NVIDIA/dcgm-exporter

23. **Keycloak GitHub** — Keycloak is Apache-2.0 licensed open-source identity and access management. https://github.com/keycloak/keycloak

24. **Strawberry GraphQL GitHub** — Strawberry GraphQL is MIT licensed. https://github.com/strawberry-graphql/strawberry

25. **Delta Lake GitHub** — Delta Lake is Apache-2.0 licensed open-source lakehouse storage framework. https://github.com/delta-io/delta

26. **Apache Iceberg official site** — Apache Iceberg is licensed under Apache License 2.0. https://iceberg.apache.org/

27. **Apache Parquet official site** — Apache Parquet is an open-source columnar data file format. https://parquet.apache.org/

28. **MemPalace GitHub** — MemPalace is MIT licensed, local-first memory with verbatim storage and pluggable backend. https://github.com/MemPalace/mempalace

29. **Shudhi GitHub** — Shudhi provides cache visibility/inspection/invalidation via sidecar; no visible LICENSE file in fetched repo listing, so use inspiration only until validated. https://github.com/nammayatri/shudhi

30. **Open WebUI GitHub** — Current codebase has multiple licensing terms and an Open WebUI License with branding requirements; use inspiration only unless exact license is approved. https://github.com/open-webui/open-webui
