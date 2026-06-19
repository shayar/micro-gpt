from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from microgpt.api.config import get_settings


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MicroLakeEventStore:
    """Small append-only JSONL event store for Phase 1.

    This is intentionally boring and inspectable. Later phases can add Parquet,
    snapshots, lineage manifests, and rollback.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        settings = get_settings()
        self.data_dir = data_dir or settings.data_dir
        self.events_dir = self.data_dir / "events"
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def append(self, stream: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "event_id": str(uuid4()),
            "stream": stream,
            "timestamp": utc_now(),
            "payload": payload,
        }
        path = self.events_dir / f"{stream}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event

    def read_stream(self, stream: str, limit: int = 100) -> list[dict[str, Any]]:
        path = self.events_dir / f"{stream}.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]


event_store = MicroLakeEventStore()
