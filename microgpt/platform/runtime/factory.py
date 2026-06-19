from microgpt.api.config import get_settings
from microgpt.platform.runtime.base import RuntimeAdapter
from microgpt.platform.runtime.no_model import NoModelRuntime


def get_runtime() -> RuntimeAdapter:
    settings = get_settings()
    if settings.runtime_mode == "no_model":
        return NoModelRuntime()
    # Future: llama.cpp / bitnet.cpp adapters.
    return NoModelRuntime()
