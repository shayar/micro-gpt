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
    max_tokens: int | None = Field(default=None, ge=1, le=4096)


class ChatResponse(BaseModel):
    request_id: str
    route: str
    answer: str
    model_id: str
    runtime: str
    safety_status: str
    fallback_used: bool = False


class MaturityRequest(BaseModel):
    level: str = Field(pattern="^(research|internal_alpha|private_beta|public)$")


class DocumentRegisterRequest(BaseModel):
    path: str = Field(min_length=1, description="Local path to a file that should be fingerprinted")


class DocumentIdentityResponse(BaseModel):
    document_id: str
    path: str
    canonical_path: str
    file_name: str
    extension: str
    size_bytes: int
    modified_time_utc: str
    md5: str
    sha256: str
    exists: bool = True


class DocumentContextResponse(BaseModel):
    document_id: str
    document: dict | None
    conversation_hits: list[dict]
