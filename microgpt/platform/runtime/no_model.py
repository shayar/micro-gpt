from __future__ import annotations

from typing import Iterator

from microgpt.platform.runtime.base import GenerationResult, RuntimeAdapter


class NoModelRuntime(RuntimeAdapter):
    """Safe fallback runtime used before a GGUF model is installed."""

    def __init__(self, reason: str | None = None) -> None:
        self.reason = reason

    @property
    def runtime_name(self) -> str:
        return "no_model"

    def generate(self, prompt: str, max_tokens: int | None = None) -> GenerationResult:
        details = ""
        if self.reason:
            details = f" Runtime fallback reason: {self.reason}"
        text = (
            "MicroGPT Phase 2 runtime is ready, but no local GGUF model is currently loaded. "
            "You can keep testing auth, safety, provenance, streaming, and audit logs. "
            "Set MICROGPT_RUNTIME_MODE=llama_cli or llama_cpp and configure a model registry entry to use CPU inference."
            f"{details}"
        )
        return GenerationResult(
            text=text,
            model_id="no-model-phase2",
            tokens_generated=len(text.split()),
            prompt_tokens=len(prompt.split()),
            runtime=self.runtime_name,
            fallback_used=self.reason is not None,
            metadata={"max_tokens_requested": max_tokens},
        )

    def stream_generate(self, prompt: str, max_tokens: int | None = None) -> Iterator[str]:
        result = self.generate(prompt, max_tokens=max_tokens)
        words = result.text.split(" ")
        for index, word in enumerate(words):
            suffix = " " if index < len(words) - 1 else ""
            yield word + suffix
