from microgpt.api.config import get_settings
from microgpt.platform.runtime.base import RuntimeAdapter
from microgpt.platform.runtime.errors import RuntimeUnavailableError
from microgpt.platform.runtime.llama_cpp_adapter import cached_llama_runtime
from microgpt.platform.runtime.no_model import NoModelRuntime


def get_runtime() -> RuntimeAdapter:
    settings = get_settings()
    if settings.runtime_mode == "no_model":
        return NoModelRuntime()
    if settings.runtime_mode == "llama_cpp":
        try:
            return cached_llama_runtime()
        except RuntimeUnavailableError as exc:
            if settings.runtime_fallback_enabled:
                return NoModelRuntime(reason=str(exc))
            raise
    return NoModelRuntime(reason=f"Unknown MICROGPT_RUNTIME_MODE={settings.runtime_mode}")
