from fastapi import Depends, FastAPI, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.security.auth import LoginRequest, TokenResponse, authenticate, create_access_token, require_user
from app.safety.maturity import check_maturity_gate
from app.safety.policy import evaluate_prompt
from app.runtime.llama_cpp_client import generate_answer

app = FastAPI(title="MicroGPT CPU-First Platform", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "microgpt-api"}


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    if not authenticate(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
    return TokenResponse(access_token=create_access_token(payload.username))


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, _user: str = Depends(require_user)) -> ChatResponse:
    maturity = check_maturity_gate()
    if not maturity.allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=maturity.reason)

    safety = evaluate_prompt(payload.message)
    if not safety.allowed:
        return ChatResponse(
            answer=safety.reason,
            safety_status=f"blocked:{safety.category}",
            maturity_status=maturity.status,
            model_backend="not_called",
        )

    answer, backend = await generate_answer(payload.message)
    return ChatResponse(
        answer=answer,
        safety_status=safety.category,
        maturity_status=maturity.status,
        model_backend=backend,
    )
