from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from microgpt.api.auth.security import get_current_user
from microgpt.api.maturity import enforce_maturity_gate
from microgpt.api.safety.policy import safety_policy
from microgpt.api.schemas.common import ChatRequest, ChatResponse
from microgpt.platform.microlake.events import event_store
from microgpt.platform.runtime.errors import RuntimeUnavailableError
from microgpt.platform.runtime.factory import get_runtime
from microgpt.platform.runtime.no_model import NoModelRuntime

router = APIRouter(tags=["chat"])


def _check_input_and_log(request_id: str, username: str, message: str) -> None:
    event_store.append(
        "conversations",
        {
            "request_id": request_id,
            "username": username,
            "direction": "input",
            "message": message,
        },
    )

    decision = safety_policy.check(message)
    event_store.append(
        "safety_events",
        {
            "request_id": request_id,
            "username": username,
            "allowed": decision.allowed,
            "category": decision.category,
            "reason": decision.reason,
        },
    )

    if not decision.allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request blocked by MicroGPT safety gate",
        )


def _fallback_runtime(reason: str) -> NoModelRuntime:
    return NoModelRuntime(reason=reason)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user: dict = Depends(get_current_user)) -> ChatResponse:
    enforce_maturity_gate()
    request_id = str(uuid4())
    username = user["username"]
    _check_input_and_log(request_id, username, request.message)

    runtime = get_runtime()
    try:
        result = runtime.generate(request.message, max_tokens=request.max_tokens)
    except RuntimeUnavailableError as exc:
        runtime = _fallback_runtime(str(exc))
        result = runtime.generate(request.message, max_tokens=request.max_tokens)
    except Exception as exc:  # Defensive guard so a model process never takes down the API.
        runtime = _fallback_runtime(f"Unexpected generation error: {exc.__class__.__name__}: {exc}")
        result = runtime.generate(request.message, max_tokens=request.max_tokens)

    output_decision = safety_policy.check(result.text)
    if not output_decision.allowed:
        event_store.append(
            "safety_events",
            {
                "request_id": request_id,
                "username": username,
                "allowed": False,
                "category": output_decision.category,
                "reason": "Output blocked",
                "model_id": result.model_id,
                "runtime": result.runtime,
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
            "username": username,
            "direction": "output",
            "message": result.text,
            "model_id": result.model_id,
            "runtime": result.runtime,
            "tokens_generated": result.tokens_generated,
            "prompt_tokens": result.prompt_tokens,
            "fallback_used": result.fallback_used,
            "metadata": result.metadata,
        },
    )

    return ChatResponse(
        request_id=request_id,
        route=f"simple_chat/{runtime.runtime_name}",
        answer=result.text,
        model_id=result.model_id,
        runtime=result.runtime,
        safety_status="allowed",
        fallback_used=result.fallback_used,
    )


@router.post("/chat/stream")
def chat_stream(request: ChatRequest, user: dict = Depends(get_current_user)) -> StreamingResponse:
    enforce_maturity_gate()
    request_id = str(uuid4())
    username = user["username"]
    _check_input_and_log(request_id, username, request.message)
    runtime = get_runtime()

    def iterator():
        nonlocal runtime
        generated_parts: list[str] = []
        output_runtime = runtime.runtime_name
        try:
            try:
                for chunk in runtime.stream_generate(request.message, max_tokens=request.max_tokens):
                    generated_parts.append(chunk)
                    yield chunk
            except RuntimeUnavailableError as exc:
                fallback = _fallback_runtime(str(exc))
                output_runtime = fallback.runtime_name
                for chunk in fallback.stream_generate(request.message, max_tokens=request.max_tokens):
                    generated_parts.append(chunk)
                    yield chunk
            except Exception as exc:
                fallback = _fallback_runtime(f"Unexpected stream generation error: {exc.__class__.__name__}: {exc}")
                output_runtime = fallback.runtime_name
                for chunk in fallback.stream_generate(request.message, max_tokens=request.max_tokens):
                    generated_parts.append(chunk)
                    yield chunk
        finally:
            text = "".join(generated_parts)
            event_store.append(
                "conversations",
                {
                    "request_id": request_id,
                    "username": username,
                    "direction": "output_stream",
                    "message": text,
                    "runtime": output_runtime,
                },
            )

    return StreamingResponse(iterator(), media_type="text/plain; charset=utf-8")
