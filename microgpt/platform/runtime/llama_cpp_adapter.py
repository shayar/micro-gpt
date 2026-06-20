from __future__ import annotations

from functools import lru_cache
from typing import Iterator

from microgpt.api.config import get_settings
from microgpt.platform.runtime.base import GenerationResult, RuntimeAdapter
from microgpt.platform.runtime.errors import RuntimeUnavailableError
from microgpt.platform.runtime.model_registry import ModelRegistry, ModelSpec


def _friendly_llama_error(exc: Exception) -> str:
    message = str(exc)
    text = f"{exc.__class__.__name__}: {message}"
    if "0xc000001d" in message or "-1073741795" in message:
        return (
            "llama-cpp-python failed while loading the GGUF model with Windows error 0xc000001d "
            "(illegal CPU instruction). Your machine may support AVX2/FMA, but the installed native wheel "
            "can still be incompatible with your Windows/Python/runtime combination. Try a CPU-safe rebuild "
            "with GGML_NATIVE=OFF, or use the standalone llama.cpp CLI/server adapter. Raw error: "
            f"{text}"
        )
    if "nmake" in message or "CMAKE_C_COMPILER" in message or "CMAKE_CXX_COMPILER" in message:
        return (
            "llama-cpp-python tried to build from source but Windows C++ build tools were not available. "
            "Use Python 3.12 with a prebuilt CPU wheel, or install Visual Studio Build Tools with Desktop "
            f"development with C++. Raw error: {text}"
        )
    return f"llama-cpp-python could not load the configured model. Raw error: {text}"


class LlamaCppRuntime(RuntimeAdapter):
    """CPU-first llama.cpp adapter through llama-cpp-python.

    The dependency is optional and imported lazily so the default project remains
    light and runnable without a compiler or model file.
    """

    def __init__(self, model: ModelSpec) -> None:
        settings = get_settings()
        self.model = model
        model_path = model.resolved_path(settings.model_dir)
        if not model_path.exists():
            raise RuntimeUnavailableError(
                f"Model file not found: {model_path}. Add a GGUF model locally or update the registry."
            )

        try:
            from llama_cpp import Llama
        except Exception as exc:  # pragma: no cover - optional dependency path
            raise RuntimeUnavailableError(
                "llama-cpp-python is not installed in this environment. "
                "Install a compatible CPU wheel or keep MICROGPT_RUNTIME_MODE=no_model."
            ) from exc

        try:
            self._llm = Llama(
                model_path=str(model_path),
                n_ctx=settings.llama_n_ctx,
                n_threads=settings.llama_n_threads,
                n_gpu_layers=settings.llama_n_gpu_layers,
                verbose=settings.llama_verbose,
            )
        except Exception as exc:  # pragma: no cover - depends on native runtime/hardware
            raise RuntimeUnavailableError(_friendly_llama_error(exc)) from exc

    @property
    def runtime_name(self) -> str:
        return "llama_cpp"

    def generate(self, prompt: str, max_tokens: int | None = None) -> GenerationResult:
        settings = get_settings()
        token_limit = max_tokens or settings.llama_max_tokens
        response = self._llm(
            prompt,
            max_tokens=token_limit,
            temperature=settings.llama_temperature,
            top_p=settings.llama_top_p,
            stop=settings.llama_stop_tokens or None,
        )
        choice = response.get("choices", [{}])[0]
        text = choice.get("text", "")
        usage = response.get("usage", {})
        return GenerationResult(
            text=text.strip(),
            model_id=self.model.model_id,
            tokens_generated=int(usage.get("completion_tokens", len(text.split()))),
            prompt_tokens=int(usage.get("prompt_tokens", len(prompt.split()))),
            runtime=self.runtime_name,
            metadata={
                "model_name": self.model.name,
                "quantization": self.model.quantization,
                "context_length": self.model.context_length,
                "license": self.model.license,
            },
        )

    def stream_generate(self, prompt: str, max_tokens: int | None = None) -> Iterator[str]:
        settings = get_settings()
        token_limit = max_tokens or settings.llama_max_tokens
        stream = self._llm(
            prompt,
            max_tokens=token_limit,
            temperature=settings.llama_temperature,
            top_p=settings.llama_top_p,
            stop=settings.llama_stop_tokens or None,
            stream=True,
        )
        for chunk in stream:
            choice = chunk.get("choices", [{}])[0]
            text = choice.get("text", "")
            if text:
                yield text


@lru_cache(maxsize=1)
def cached_llama_runtime() -> LlamaCppRuntime:
    settings = get_settings()
    model = ModelRegistry(settings.model_registry_path).get(settings.active_model_id or None)
    if model is None:
        raise RuntimeUnavailableError(
            f"No active model found. Set MICROGPT_ACTIVE_MODEL_ID or add one model to {settings.model_registry_path}."
        )
    if model.runtime != "llama_cpp":
        raise RuntimeUnavailableError(f"Active model runtime is {model.runtime}, not llama_cpp.")
    if model.status not in {"approved", "local_only", "candidate"}:
        raise RuntimeUnavailableError(f"Model {model.model_id} is not allowed: status={model.status}.")
    return LlamaCppRuntime(model)
