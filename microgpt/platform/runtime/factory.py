from microgpt.api.config import get_settings
from microgpt.platform.runtime.base import RuntimeAdapter
from microgpt.platform.runtime.errors import RuntimeUnavailableError
from microgpt.platform.runtime.llama_cpp_adapter import cached_llama_runtime
from microgpt.platform.runtime.llama_cli_adapter import cached_llama_cli_runtime
from microgpt.platform.runtime.no_model import NoModelRuntime


def get_runtime() -> RuntimeAdapter:
    """Return the configured runtime, falling back safely when enabled.

    Phase 2 should never take down the API because a native llama runtime or GGUF file
    is incompatible. The fallback keeps auth, safety, provenance, and docs testable.
    """
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
        except Exception as exc:  # Defensive guard for native runtime errors.
            if settings.runtime_fallback_enabled:
                return NoModelRuntime(reason=f"Unexpected runtime error: {exc.__class__.__name__}: {exc}")
            raise RuntimeUnavailableError(f"Unexpected runtime error: {exc.__class__.__name__}: {exc}") from exc
    if settings.runtime_mode == "llama_cli":
        try:
            return cached_llama_cli_runtime()
        except RuntimeUnavailableError as exc:
            if settings.runtime_fallback_enabled:
                return NoModelRuntime(reason=str(exc))
            raise
        except Exception as exc:  # Defensive guard for subprocess/runtime errors.
            if settings.runtime_fallback_enabled:
                return NoModelRuntime(reason=f"Unexpected llama-cli runtime error: {exc.__class__.__name__}: {exc}")
            raise RuntimeUnavailableError(
                f"Unexpected llama-cli runtime error: {exc.__class__.__name__}: {exc}"
            ) from exc
    return NoModelRuntime(reason=f"Unknown MICROGPT_RUNTIME_MODE={settings.runtime_mode}")
