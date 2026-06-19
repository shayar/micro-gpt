from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_name: str
    maturity_level: str
    public_access: bool
    runtime_mode: str


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class ChatResponse(BaseModel):
    request_id: str
    route: str
    answer: str
    model_id: str
    safety_status: str


class MaturityRequest(BaseModel):
    level: str = Field(pattern="^(research|internal_alpha|private_beta|public)$")
