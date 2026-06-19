from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from microgpt.api.config import get_settings
from microgpt.platform.documents.identity import DocumentIdentity, fingerprint_file
from microgpt.platform.microlake.events import event_store, utc_now


class DocumentRegistry:
    """Plain JSON document identity registry.

    This is not RAG yet. It is the provenance layer that later lets MicroGPT
    answer: which exact file was used, where was it, did it change, and what
    prior chat context mentions it if the file disappears?
    """

    def __init__(self, path: Path | None = None) -> None:
        settings = get_settings()
        self.path = path or (settings.data_dir / "manifests" / "document_registry.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "updated_at": utc_now(), "documents": {}}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, registry: dict[str, Any]) -> None:
        registry["updated_at"] = utc_now()
        self.path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def register_file(self, path: str | Path) -> DocumentIdentity:
        identity = fingerprint_file(path)
        registry = self._load()
        documents = registry.setdefault("documents", {})
        current = identity.to_dict()
        current["last_seen_at"] = utc_now()
        documents[identity.document_id] = current
        self._save(registry)
        event_store.append(
            "document_events",
            {"action": "document_registered", "document": current},
        )
        return identity

    def list_documents(self) -> list[dict[str, Any]]:
        registry = self._load()
        docs = list(registry.get("documents", {}).values())
        return sorted(docs, key=lambda item: item.get("file_name", ""))

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        registry = self._load()
        return registry.get("documents", {}).get(document_id)

    def reconcile_missing_files(self) -> list[dict[str, Any]]:
        registry = self._load()
        changed: list[dict[str, Any]] = []
        for document_id, document in registry.get("documents", {}).items():
            exists = Path(document["canonical_path"]).exists()
            if bool(document.get("exists", True)) != exists:
                document["exists"] = exists
                document["last_reconciled_at"] = utc_now()
                changed.append(document)
                event_store.append(
                    "document_events",
                    {
                        "action": "document_missing" if not exists else "document_reappeared",
                        "document_id": document_id,
                        "canonical_path": document["canonical_path"],
                    },
                )
        if changed:
            self._save(registry)
        return changed

    def context_from_old_chats(self, document_id: str, limit: int = 25) -> list[dict[str, Any]]:
        """Best-effort retrieval from old chat/event logs when a file is gone.

        Phase 4 will replace this with indexed retrieval. For now, we search the
        append-only MicroLake conversation stream for document_id, path, md5, or sha256.
        """
        document = self.get_document(document_id)
        if not document:
            return []
        needles = {
            document_id,
            str(document.get("canonical_path", "")),
            str(document.get("path", "")),
            str(document.get("md5", "")),
            str(document.get("sha256", "")),
            str(document.get("file_name", "")),
        }
        needles = {item for item in needles if item}
        hits: list[dict[str, Any]] = []
        for event in event_store.read_stream("conversations", limit=1000):
            payload = event.get("payload", {})
            raw = json.dumps(payload, ensure_ascii=False)
            if any(needle in raw for needle in needles):
                hits.append(event)
        return hits[-limit:]


def default_document_registry() -> DocumentRegistry:
    return DocumentRegistry()
