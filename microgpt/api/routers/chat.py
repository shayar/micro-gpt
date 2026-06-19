from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from microgpt.api.auth.security import get_current_user
from microgpt.api.maturity import enforce_maturity_gate
from microgpt.api.safety.policy import safety_policy
from microgpt.api.schemas.common import ChatRequest, ChatResponse
from microgpt.platform.microlake.events import event_store
from microgpt.platform.runtime.factory import get_runtime

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user: dict = Depends(get_current_user)) -> ChatResponse:
    enforce_maturity_gate()
    request_id = str(uuid4())
    event_store.append(
        "conversations",
        {
            "request_id": request_id,
            "username": user["username"],
            "direction": "input",
            "message": request.message,
        },
    )

    decision = safety_policy.check(request.message)
    event_store.append(
        "safety_events",
        {
            "request_id": request_id,
            "username": user["username"],
            "allowed": decision.allowed,
            "category": decision.category,
            "reason": decision.reason,
        },
    )

    if not decision.allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request blocked by MicroGPT Phase 1 safety gate",
        )

    runtime = get_runtime()
    result = runtime.generate(request.message)

    output_decision = safety_policy.check(result.text)
    if not output_decision.allowed:
        event_store.append(
            "safety_events",
            {
                "request_id": request_id,
                "username": user["username"],
                "allowed": False,
                "category": output_decision.category,
                "reason": "Output blocked",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Generated output blocked by MicroGPT safety gate",
        )

    event_store.append(
        "conversations",
        {
            "request_id": request_id,
            "username": user["username"],
            "direction": "output",
            "message": result.text,
            "model_id": result.model_id,
        },
    )

    return ChatResponse(
        request_id=request_id,
        route="simple_chat/no_model",
        answer=result.text,
        model_id=result.model_id,
        safety_status="allowed",
    )
