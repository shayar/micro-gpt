from __future__ import annotations

from microgpt.platform.runtime.base import GenerationResult, RuntimeAdapter


class NoModelRuntime(RuntimeAdapter):
    """Safe fallback runtime.

    The app can boot, authenticate users, audit requests, and test routing before
    any GGUF model is downloaded. This is essential for Phase 1.
    """

    model_id = "no-model-phase1"

    def generate(self, prompt: str) -> GenerationResult:
        return GenerationResult(
            model_id=self.model_id,
            text=(
                "MicroGPT Phase 1 is running without a local model installed. "
                "Auth, maturity gate, safety checks, routing, and MicroLake audit logs are active. "
                "Next step: add the llama.cpp adapter and a validated GGUF model."
            ),
            tokens_generated=0,
        )
