from fastapi import APIRouter, Depends

from microgpt.api.auth.security import require_admin
from microgpt.platform.microlake.events import event_store

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def metrics(_: dict = Depends(require_admin)) -> dict:
    # Placeholder metrics endpoint. Phase 8 can replace/augment this with Prometheus.
    return {
        "audit_events_last_100": len(event_store.read_stream("audit_events", limit=100)),
        "safety_events_last_100": len(event_store.read_stream("safety_events", limit=100)),
        "conversation_events_last_100": len(event_store.read_stream("conversations", limit=100)),
        "document_events_last_100": len(event_store.read_stream("document_events", limit=100)),
    }
