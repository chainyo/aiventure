"""Employees models."""

from uuid import UUID

from sqlmodel import Field
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel


class EmployeeBase(UUIDModel):
    """Employee model."""

    name: str
    salary: int
    image_url: str
    role_id: int = Field(foreign_key="roles.id")
    quality_id: int = Field(foreign_key="qualities.id")
    modifier_id_1: int | None = Field(foreign_key="modifiers.id", default=None)
    modifier_id_2: int | None = Field(foreign_key="modifiers.id", default=None)
    modifier_id_3: int | None = Field(foreign_key="modifiers.id", default=None)
    lab_id: UUID | None = Field(foreign_key="labs.id", default=None)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "bonuses": ["Free lunch", "Free gym"],
                "salary": 100000,
                "image_url": "https://example.com/image.png",
                "role_id": 1,
                "quality_id": 1,
                "modifier_id_1": 1,
                "modifier_id_2": 2,
                "modifier_id_3": 3,
                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class Employee(EmployeeBase, table=True):
    """Table for employees."""

    __tablename__ = "employees"
