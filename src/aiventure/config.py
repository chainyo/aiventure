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


settings = Settings()
