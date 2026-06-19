from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationResult:
    text: str
    model_id: str
    tokens_generated: int = 0


class RuntimeAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> GenerationResult:
        raise NotImplementedError

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embedding is not implemented yet")

    def classify(self, text: str) -> str:
        raise NotImplementedError("Classification is not implemented yet")
