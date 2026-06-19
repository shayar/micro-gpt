from fastapi import APIRouter

from microgpt.api.config import get_settings
from microgpt.api.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        maturity_level=settings.maturity_level,
        public_access=settings.public_access,
        runtime_mode=settings.runtime_mode,
    )
