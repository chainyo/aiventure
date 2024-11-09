"""Core models for the database and API."""

from pydantic import BaseModel, ConfigDict


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
