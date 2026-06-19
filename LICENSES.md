# License Registry

Project license: MIT.

This file tracks core dependencies approved or proposed for the starter. Revalidate exact versions before release.

| Dependency | Purpose | License/status | Phase |
|---|---|---|---|
| Python | Runtime language | PSF License | Core |
| FastAPI | API framework | MIT | Phase 1 |
| Uvicorn | ASGI server | BSD-3-Clause | Phase 1 |
| Pydantic | Validation/settings models | MIT | Phase 1 |
| PyJWT | JWT handling | MIT | Phase 1 |
| pytest | Tests | MIT | Dev |
| HTTPX | Test client dependency | BSD-3-Clause | Dev |
| llama-cpp-python | Optional Python binding for llama.cpp | MIT; optional | Phase 2 optional |
| llama.cpp | Local CPU/GPU inference runtime | MIT; optional runtime backend | Phase 2 optional |

## Model licenses

Model licenses are not inferred from code dependencies. Each model must be recorded in `MODEL_REGISTRY.md` and `models/model_registry.local.json` with exact source, revision, and license validation.

## Rule

Do not add a dependency to core until its license, version, and transitive risk are reviewed.
