# Contributing

Thank you for helping build MicroGPT.

## Contribution rules

1. Keep the project local-first and open-source-only by default.
2. Add an ADR for major architecture changes.
3. Update `LICENSES.md` before introducing dependencies.
4. Do not commit model weights, secrets, private data, or local runtime data.
5. Add tests for new routes and safety-sensitive behavior.
6. Add evaluation notes for model/retrieval/memory changes.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/init_dev.py
uvicorn microgpt.api.main:app --reload
pytest
```
