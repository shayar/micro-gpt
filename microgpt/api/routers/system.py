from fastapi import APIRouter, Depends

from microgpt.api.auth.security import get_current_user
from microgpt.platform.system.specs import collect_system_specs

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/specs")
def system_specs(_: dict = Depends(get_current_user)) -> dict:
    return collect_system_specs()
