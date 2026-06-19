from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
from pathlib import Path
import secrets
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from microgpt.api.config import get_settings
from microgpt.platform.microlake.events import event_store

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str, salt: str | None = None) -> str:
    """Hash a password using the standard library.

    Format: pbkdf2_sha256$iterations$salt_hex$hash_hex
    """
    if not password:
        raise ValueError("password cannot be empty")
    iterations = 310_000
    salt_bytes = bytes.fromhex(salt) if salt else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, iterations)
    return f"pbkdf2_sha256${iterations}${salt_bytes.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations_raw, salt_hex, expected_hex = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_raw)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), iterations
        )
        return hmac.compare_digest(digest.hex(), expected_hex)
    except Exception:
        return False


def create_access_token(subject: str, role: str = "admin") -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    payload = decode_access_token(credentials.credentials)
    return {"username": payload.get("sub"), "role": payload.get("role", "viewer")}


def require_admin(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return user


def ensure_dev_user_file() -> Path:
    """Create a tiny local user file for Phase 1 development.

    This is deliberately simple. Phase 2/3 can replace it with SQLite/PostgreSQL.
    """
    settings = get_settings()
    users_dir = settings.data_dir / "auth"
    users_dir.mkdir(parents=True, exist_ok=True)
    users_file = users_dir / "users.jsonl"
    if not users_file.exists():
        encoded = hash_password(settings.admin_password)
        users_file.write_text(
            f'{{"username":"{settings.admin_username}","password_hash":"{encoded}","role":"admin"}}\n',
            encoding="utf-8",
        )
        event_store.append(
            "audit_events",
            {"action": "dev_admin_created", "username": settings.admin_username},
        )
    return users_file


def authenticate_user(username: str, password: str) -> dict[str, str] | None:
    import json

    users_file = ensure_dev_user_file()
    for line in users_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        user = json.loads(line)
        if user["username"] == username and verify_password(password, user["password_hash"]):
            return {"username": user["username"], "role": user.get("role", "viewer")}
    return None
