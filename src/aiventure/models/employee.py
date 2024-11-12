"""Employees models."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.lab import Lab
from aiventure.models.links import EmployeeModifierLink


if TYPE_CHECKING:
    from aiventure.models.modifier import Modifier, ModifierRead


class EmployeeBase(UUIDModel):
    """Employee model."""

    name: str
    salary: int
    image_url: str
    role_id: int = Field(foreign_key="roles.id")
    quality_id: int = Field(foreign_key="qualities.id")
    lab_id: str | None = Field(foreign_key="labs.id", default=None)

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "bonuses": ["Free lunch", "Free gym"],
                "salary": 100000,
                "image_url": "https://avatar.iran.liara.run/public",
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

    modifiers: list["Modifier"] = Relationship(back_populates="employees", link_model=EmployeeModifierLink)
    lab: Lab | None = Relationship(back_populates="employees")


class EmployeeRead(BaseModel):
    """Employee read model."""

    id: str
    name: str
    salary: int
    image_url: str
    role_id: int
    quality_id: int
    modifiers: list["ModifierRead"]
    lab_id: str | None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "salary": 100000,
                "image_url": "https://avatar.iran.liara.run/public",
                "role_id": 1,
                "quality_id": 1,
                "modifiers": [
                    {
                        "id": 1,
                        "name": "Boost model accuracy",
                        "description": "Boost model accuracy by 10%",
                        "type_id": 1,
                    }
                ],
                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )
