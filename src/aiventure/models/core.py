"""Core models for the database and API."""

import uuid

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


class Health(BaseModel):
    """Health model for the API."""

    status: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"status": "healthy"}},
    )


class Version(BaseModel):
    """Version model for the API."""

    version: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"version": "0.1.0"}},
    )


class UUIDModel(SQLModel):
    """Model with a UUID."""

    id: str = Field(
        # NOTE: This is a workaround to use UUIDs as primary keys in SQLite + aiosqlite and SQLModel/SQLAlchemy.
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True},
    )

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": "123e4567-e89b-12d3-a456-426614174000"}})
