from functools import lru_cache
import os
from pathlib import Path
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - python-dotenv should be installed, but keep config resilient
    load_dotenv = None

if load_dotenv is not None:
    # Load local .env automatically so contributors do not need shell-specific export commands.
    load_dotenv()


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

    # llama.cpp settings shared by llama_cpp and llama_cli runtimes
    llama_n_ctx: int = Field(default=2048)
    llama_n_threads: int = Field(default_factory=_default_threads)
    llama_n_gpu_layers: int = Field(default=0)
    llama_max_tokens: int = Field(default=128)
    llama_temperature: float = Field(default=0.2)
    llama_top_p: float = Field(default=0.95)
    llama_verbose: bool = Field(default=False)
    llama_stop_tokens: list[str] = Field(default_factory=list)

    # Standalone llama.cpp CLI settings
    llama_cli_path: str = Field(default="llama-cli")
    llama_cli_timeout_seconds: int = Field(default=300)
    llama_cli_extra_args: list[str] = Field(default_factory=list)
    llama_cli_single_turn: bool = Field(default=True)
    llama_cli_suppress_prompt: bool = Field(default=True)
    llama_cli_show_timings: bool = Field(default=False)
    llama_cli_simple_io: bool = Field(default=True)
    llama_cli_log_disable: bool = Field(default=True)
    llama_reasoning: str = Field(default="off")


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
        llama_max_tokens=int(os.getenv("MICROGPT_LLAMA_MAX_TOKENS", "128")),
        llama_temperature=float(os.getenv("MICROGPT_LLAMA_TEMPERATURE", "0.2")),
        llama_top_p=float(os.getenv("MICROGPT_LLAMA_TOP_P", "0.95")),
        llama_verbose=_as_bool(os.getenv("MICROGPT_LLAMA_VERBOSE"), False),
        llama_stop_tokens=_as_list(os.getenv("MICROGPT_LLAMA_STOP_TOKENS")),
        llama_cli_path=os.getenv("MICROGPT_LLAMA_CLI_PATH", "llama-cli"),
        llama_cli_timeout_seconds=int(os.getenv("MICROGPT_LLAMA_CLI_TIMEOUT_SECONDS", "300")),
        llama_cli_extra_args=_as_list(os.getenv("MICROGPT_LLAMA_CLI_EXTRA_ARGS")),
        llama_cli_single_turn=_as_bool(os.getenv("MICROGPT_LLAMA_CLI_SINGLE_TURN"), True),
        llama_cli_suppress_prompt=_as_bool(os.getenv("MICROGPT_LLAMA_CLI_SUPPRESS_PROMPT"), True),
        llama_cli_show_timings=_as_bool(os.getenv("MICROGPT_LLAMA_CLI_SHOW_TIMINGS"), False),
        llama_cli_simple_io=_as_bool(os.getenv("MICROGPT_LLAMA_CLI_SIMPLE_IO"), True),
        llama_cli_log_disable=_as_bool(os.getenv("MICROGPT_LLAMA_CLI_LOG_DISABLE"), True),
        llama_reasoning=os.getenv("MICROGPT_LLAMA_REASONING", "off"),
    )
