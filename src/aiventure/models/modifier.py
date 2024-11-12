"""Modifiers models."""

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from aiventure.models.links import EmployeeModifierLink


if TYPE_CHECKING:
    from aiventure.models.employee import Employee


class ModifierTypeBase(SQLModel):
    """Modifier type model."""

    id: int = Field(primary_key=True)
    name: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "lab"}})


class ModifierType(ModifierTypeBase, table=True):
    """Modifier type model."""

    __tablename__ = "modifier_types"


MODIFIER_TYPE_MAPPING: dict[str, ModifierTypeBase] = {
    "employee": ModifierTypeBase(id=1, name="employee"),
    "lab": ModifierTypeBase(id=2, name="lab"),
    "location": ModifierTypeBase(id=3, name="location"),
}


class ModifierTypeEnum(str, Enum):
    """Modifier type enum."""

    EMPLOYEE = "employee"
    LAB = "lab"
    LOCATION = "location"

    @property
    def item(self) -> ModifierTypeBase:
        """Get the modifier type."""
        return MODIFIER_TYPE_MAPPING[self.value]


class ModifierBase(SQLModel):
    """Modifier base model."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    type_id: int = Field(foreign_key="modifier_types.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Boost model accuracy",
                "description": "Boost model accuracy by 10%",
                "type_id": 1,
            }
        }
    )


class Modifier(ModifierBase, table=True):
    """Modifier model."""

    __tablename__ = "modifiers"

    employees: list["Employee"] = Relationship(back_populates="modifiers", link_model=EmployeeModifierLink)


MODIFIER_MAPPING: dict[str, ModifierBase] = {
    # TODO: Add modifiers
}


class ModifierEnum(str, Enum):
    """Modifier enum."""

    # TODO: Add modifiers

    @property
    def item(self) -> ModifierBase:
        """Get the modifier."""
        return MODIFIER_MAPPING[self.value]


class ModifierRead(BaseModel):
    """Modifier read model."""

    id: int
    name: str
    description: str
    type_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Boost model accuracy",
                "description": "Boost model accuracy by 10%",
                "type_id": 1,
            }
        }
    )
