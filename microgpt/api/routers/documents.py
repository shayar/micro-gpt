from fastapi import APIRouter, Depends, HTTPException, status

from microgpt.api.auth.security import get_current_user
from microgpt.api.schemas.common import (
    DocumentContextResponse,
    DocumentIdentityResponse,
    DocumentRegisterRequest,
)
from microgpt.platform.documents.registry import default_document_registry

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/register", response_model=DocumentIdentityResponse)
def register_document(
    request: DocumentRegisterRequest, _: dict = Depends(get_current_user)
) -> DocumentIdentityResponse:
    registry = default_document_registry()
    try:
        identity = registry.register_file(request.path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return DocumentIdentityResponse(**identity.to_dict())


@router.get("")
def list_documents(_: dict = Depends(get_current_user)) -> list[dict]:
    return default_document_registry().list_documents()


@router.post("/reconcile")
def reconcile_documents(_: dict = Depends(get_current_user)) -> dict:
    changed = default_document_registry().reconcile_missing_files()
    return {"changed_count": len(changed), "changed": changed}


@router.get("/{document_id}/context", response_model=DocumentContextResponse)
def document_context(document_id: str, _: dict = Depends(get_current_user)) -> DocumentContextResponse:
    registry = default_document_registry()
    document = registry.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    hits = registry.context_from_old_chats(document_id)
    return DocumentContextResponse(document_id=document_id, document=document, conversation_hits=hits)
