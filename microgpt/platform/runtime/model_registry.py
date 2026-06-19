from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from microgpt.api.config import get_settings


ModelStatus = Literal["candidate", "approved", "blocked", "local_only"]


class ModelSpec(BaseModel):
    model_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    runtime: str = Field(default="llama_cpp")
    path: str = Field(min_length=1)
    license: str = Field(default="unknown")
    source: str = Field(default="local")
    revision: str = Field(default="unknown")
    quantization: str = Field(default="unknown")
    context_length: int = Field(default=2048, ge=1)
    status: ModelStatus = "candidate"
    notes: str = ""

    def resolved_path(self, base_dir: Path | None = None) -> Path:
        raw_path = Path(self.path)
        if raw_path.is_absolute():
            return raw_path
        settings = get_settings()
        base = base_dir or settings.model_dir
        return (base / raw_path).resolve()


class ModelRegistry:
    """Exact-version local model registry.

    The registry is deliberately a plain JSON file so contributors can inspect
    model source, license, revision, quantization, and local path before use.
    """

    def __init__(self, path: Path | None = None) -> None:
        settings = get_settings()
        self.path = path or settings.model_registry_path

    def load(self) -> list[ModelSpec]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        items = raw.get("models", raw if isinstance(raw, list) else [])
        try:
            return [ModelSpec.model_validate(item) for item in items]
        except ValidationError as exc:
            raise ValueError(f"Invalid model registry at {self.path}: {exc}") from exc

    def get(self, model_id: str | None = None) -> ModelSpec | None:
        settings = get_settings()
        target = model_id or settings.active_model_id
        models = self.load()
        if not target and len(models) == 1:
            return models[0]
        for model in models:
            if model.model_id == target:
                return model
        return None

    def list(self) -> list[dict[str, object]]:
        return [model.model_dump() for model in self.load()]


def default_registry() -> ModelRegistry:
    return ModelRegistry()
