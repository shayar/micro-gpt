import os

from fastapi import APIRouter, Depends

from microgpt.api.auth.security import require_admin
from microgpt.api.config import get_settings
from microgpt.api.schemas.common import MaturityRequest
from microgpt.platform.microlake.events import event_store

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/maturity")
def set_maturity(request: MaturityRequest, user: dict = Depends(require_admin)) -> dict:
    # Phase 1 uses environment-backed settings, so this update is recorded and
    # reflected in-process. Restarting the app should use .env or deployment config.
    os.environ["MICROGPT_MATURITY_LEVEL"] = request.level
    get_settings.cache_clear()
    event_store.append(
        "audit_events",
        {
            "action": "maturity_updated",
            "username": user["username"],
            "level": request.level,
        },
    )
    return {"status": "ok", "maturity_level": request.level}
