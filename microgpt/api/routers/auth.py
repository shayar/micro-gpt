from fastapi import APIRouter, HTTPException, status

from microgpt.api.auth.security import authenticate_user, create_access_token
from microgpt.api.schemas.common import LoginRequest, TokenResponse
from microgpt.platform.microlake.events import event_store

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user = authenticate_user(request.username, request.password)
    if not user:
        event_store.append(
            "audit_events", {"action": "login_failed", "username": request.username}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(subject=user["username"], role=user["role"])
    event_store.append("audit_events", {"action": "login_success", "username": user["username"]})
    return TokenResponse(access_token=token)
