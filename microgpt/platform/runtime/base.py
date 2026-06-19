from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator


@dataclass(frozen=True)
class GenerationResult:
    text: str
    model_id: str
    tokens_generated: int = 0
    prompt_tokens: int = 0
    runtime: str = "unknown"
    fallback_used: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


class RuntimeAdapter(ABC):
    @property
    @abstractmethod
    def runtime_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int | None = None) -> GenerationResult:
        raise NotImplementedError

    def stream_generate(self, prompt: str, max_tokens: int | None = None) -> Iterator[str]:
        result = self.generate(prompt, max_tokens=max_tokens)
        yield result.text

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embedding is not implemented yet")

    def classify(self, text: str) -> str:
        raise NotImplementedError("Classification is not implemented yet")
