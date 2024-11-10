"""Utility functions."""

from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from jose import jwt

from aiventure.config import settings


class PasswordManager:
    """Password manager."""

    def __init__(self) -> None:
        """Initialization."""
        self.hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        """Hash password."""
        return self.hasher.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        """Verify password."""
        return self.hasher.verify(hash, password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create access token for user"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.openssl_key, algorithm=settings.algorithm)

    return token  # type: ignore[no-any-return]
