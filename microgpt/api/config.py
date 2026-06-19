from functools import lru_cache
import os
from pathlib import Path
from pydantic import BaseModel, Field


def _default_threads() -> int:
    cpu_count = os.cpu_count() or 2
    return max(1, cpu_count - 1)


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

    # Runtime settings
    runtime_mode: str = Field(default="no_model")
    runtime_fallback_enabled: bool = Field(default=True)
    model_dir: Path = Field(default=Path("./models"))
    model_registry_path: Path = Field(default=Path("./models/model_registry.local.json"))
    active_model_id: str = Field(default="")

    # llama.cpp settings
    llama_n_ctx: int = Field(default=2048)
    llama_n_threads: int = Field(default_factory=_default_threads)
    llama_n_gpu_layers: int = Field(default=0)
    llama_max_tokens: int = Field(default=256)
    llama_temperature: float = Field(default=0.2)
    llama_top_p: float = Field(default=0.95)
    llama_verbose: bool = Field(default=False)
    llama_stop_tokens: list[str] = Field(default_factory=list)


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


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
        runtime_fallback_enabled=_as_bool(os.getenv("MICROGPT_RUNTIME_FALLBACK_ENABLED"), True),
        model_dir=Path(os.getenv("MICROGPT_MODEL_DIR", "./models")),
        model_registry_path=Path(
            os.getenv("MICROGPT_MODEL_REGISTRY_PATH", "./models/model_registry.local.json")
        ),
        active_model_id=os.getenv("MICROGPT_ACTIVE_MODEL_ID", ""),
        llama_n_ctx=int(os.getenv("MICROGPT_LLAMA_N_CTX", "2048")),
        llama_n_threads=int(os.getenv("MICROGPT_LLAMA_N_THREADS", str(_default_threads()))),
        llama_n_gpu_layers=int(os.getenv("MICROGPT_LLAMA_N_GPU_LAYERS", "0")),
        llama_max_tokens=int(os.getenv("MICROGPT_LLAMA_MAX_TOKENS", "256")),
        llama_temperature=float(os.getenv("MICROGPT_LLAMA_TEMPERATURE", "0.2")),
        llama_top_p=float(os.getenv("MICROGPT_LLAMA_TOP_P", "0.95")),
        llama_verbose=_as_bool(os.getenv("MICROGPT_LLAMA_VERBOSE"), False),
        llama_stop_tokens=_as_list(os.getenv("MICROGPT_LLAMA_STOP_TOKENS")),
    )
