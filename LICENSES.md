# Dependency License Registry

This file tracks dependencies approved for the starter. Revalidate exact versions before public release.

| Dependency | Purpose | License status | Decision |
|---|---|---|---|
| Python | Runtime language | PSF License | Approved |
| FastAPI | API framework | MIT | Approved |
| Uvicorn | ASGI server | BSD-3-Clause | Approved |
| Pydantic | Data validation | MIT | Approved |
| PyJWT | JWT tokens | MIT | Approved |
| pytest | Development tests | MIT | Dev-only approved |
| HTTPX | TestClient dependency / dev testing | BSD-3-Clause | Dev-only approved |

## Rules

1. Do not add a dependency without recording its license here.
2. Do not copy code from projects with no visible license.
3. Treat source-available/custom licenses as blocked until reviewed.
4. For model weights, validate the exact model card and revision in `MODEL_REGISTRY.md`.
