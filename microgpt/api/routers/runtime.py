from fastapi import APIRouter, Depends

from microgpt.api.auth.security import get_current_user
from microgpt.api.config import get_settings
from microgpt.platform.runtime.factory import get_runtime
from microgpt.platform.runtime.model_registry import default_registry

router = APIRouter(prefix="/runtime", tags=["runtime"])


@router.get("/status")
def runtime_status(_: dict = Depends(get_current_user)) -> dict:
    settings = get_settings()
    runtime = get_runtime()
    return {
        "configured_runtime_mode": settings.runtime_mode,
        "active_runtime": runtime.runtime_name,
        "active_model_id": settings.active_model_id or None,
        "model_registry_path": str(settings.model_registry_path),
        "model_dir": str(settings.model_dir),
        "fallback_enabled": settings.runtime_fallback_enabled,
    }


@router.get("/models")
def list_models(_: dict = Depends(get_current_user)) -> list[dict]:
    return default_registry().list()
