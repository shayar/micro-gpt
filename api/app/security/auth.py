import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET = os.getenv("MICROGPT_JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("MICROGPT_JWT_EXPIRE_MINUTES", "60"))
ADMIN_USERNAME = os.getenv("MICROGPT_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("MICROGPT_ADMIN_PASSWORD", "change-me-before-real-use")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_password(plain_password: str, expected_password: str) -> bool:
    # Phase 1 dev mode: env password. Production should switch to hashed password store.
    return plain_password == expected_password


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def authenticate(username: str, password: str) -> bool:
    return username == ADMIN_USERNAME and verify_password(password, ADMIN_PASSWORD)


def require_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_error
        return username
    except JWTError as exc:
        raise credentials_error from exc
