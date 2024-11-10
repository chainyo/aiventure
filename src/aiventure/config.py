"""Configuration for the API."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    db_connection_str: str = Field(
        alias="DB_CONNECTION_STR",
        default="sqlite+aiosqlite:///aiventure.db",
        description="The connection string for the database.",
    )
    # Auth
    openssl_key: str = Field(
        alias="OPENSSL_KEY",
        default="secret",
        description="The key for the JWT token.",
    )
    algorithm: str = Field(
        alias="ALGORITHM",
        default="HS256",
        description="The algorithm for the JWT token.",
    )
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        default=30,
        description="The expiration time for the JWT token in minutes.",
    )


settings = Settings()
