# Contributing to MicroGPT

Thank you for your interest in contributing to MicroGPT.

MicroGPT is a CPU-first, open-source AI platform focused on safe, evidence-grounded AI applications. The first product module is an evidence-cited chatbot. Audio and vision modules will be added only behind consent, provenance, and safety controls.

## Project principles

- CPU-first, GPU-ready
- Open-source-first tooling
- Safety as architecture, not an afterthought
- Evidence before generation
- Measurable quality before release
- Small pull requests with clear ownership

## Development setup

1. Fork the repository.
2. Clone your fork.
3. Copy the environment file:

```bash
cp .env.example .env
```

4. Update secrets in `.env`.
5. Start the local stack:

```bash
docker compose up --build api qdrant redis searxng
```

6. Run tests:

```bash
cd api
pip install -r requirements-dev.txt
pytest
```

## Pull request rules

Before opening a PR, make sure:

- Code runs locally.
- Tests pass.
- New behavior is documented.
- Safety-sensitive changes include a safety note.
- Model, dataset, or dependency license changes are added to `LICENSES.md`.
- Large model files are not committed.

## Definition of done

A PR is done only when:

- The feature works locally.
- Tests are added or updated.
- Documentation is updated.
- Safety impact is considered.
- The PR is reviewed by the relevant owner.

## Safety-sensitive areas

Changes to the following areas require careful review:

- Authentication
- Safety policy
- Maturity gate
- Model inference
- Web search
- Retrieval
- Audio generation
- Image/video generation
- Consent or provenance logic

## Commit style

Use clear commit messages:

```txt
feat: add maturity gate
fix: block unsafe prompt before inference
docs: add CPU-first architecture ADR
test: add safety policy tests
```

## DCO signoff

By contributing, you confirm that you have the right to submit your contribution to this project.

Use signed-off commits:

```bash
git commit -s -m "feat: add retrieval adapter"
```
