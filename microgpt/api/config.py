from functools import lru_cache
import os
from pathlib import Path
from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default="MicroGPT Local Cognitive Engine")
    public_access: bool = Field(default=False)
    maturity_level: str = Field(default="research")
    data_dir: Path = Field(default=Path("./data"))
    jwt_secret: str = Field(default="change-this-local-dev-secret-32bytes-min")
    jwt_algorithm: str = Field(default="HS256")
    token_expire_minutes: int = Field(default=1440)
    admin_username: str = Field(default="admin")
    admin_password: str = Field(default="microgpt-admin")
    runtime_mode: str = Field(default="no_model")


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("MICROGPT_APP_NAME", "MicroGPT Local Cognitive Engine"),
        public_access=_as_bool(os.getenv("MICROGPT_PUBLIC_ACCESS"), False),
        maturity_level=os.getenv("MICROGPT_MATURITY_LEVEL", "research"),
        data_dir=Path(os.getenv("MICROGPT_DATA_DIR", "./data")),
        jwt_secret=os.getenv("MICROGPT_JWT_SECRET", "change-this-local-dev-secret-32bytes-min"),
        jwt_algorithm=os.getenv("MICROGPT_JWT_ALGORITHM", "HS256"),
        token_expire_minutes=int(os.getenv("MICROGPT_TOKEN_EXPIRE_MINUTES", "1440")),
        admin_username=os.getenv("MICROGPT_ADMIN_USERNAME", "admin"),
        admin_password=os.getenv("MICROGPT_ADMIN_PASSWORD", "microgpt-admin"),
        runtime_mode=os.getenv("MICROGPT_RUNTIME_MODE", "no_model"),
    )
