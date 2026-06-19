from fastapi import HTTPException, status

from microgpt.api.config import get_settings

ALLOWED_LEVELS = {"research", "internal_alpha", "private_beta", "public"}


def enforce_maturity_gate() -> None:
    settings = get_settings()
    if settings.public_access and settings.maturity_level != "public":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public access is disabled until maturity level is public",
        )
    if settings.maturity_level not in ALLOWED_LEVELS:
        raise HTTPException(status_code=500, detail="Invalid maturity level configuration")
