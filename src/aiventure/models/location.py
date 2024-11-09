"""Location models."""

from enum import Enum

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


class LocationBase(SQLModel):
    """Location model."""

    id: int = Field(primary_key=True)
    name: str
    description: str
    modifier_id: int = Field(foreign_key="modifiers.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "US",
                "description": "The United States of America",
                "modifier_id": 1,
            }
        }
    )


class Location(LocationBase, table=True):
    """Table for locations."""

    __tablename__ = "locations"


LOCATION_MAPPING: dict[str, LocationBase] = {
    "us": LocationBase(id=1, name="US", description="The United States of America", modifier_id=1),
    "eu": LocationBase(id=2, name="EU", description="The European Union", modifier_id=2),
    "asia": LocationBase(id=3, name="Asia", description="Asia", modifier_id=3),
}


class LocationEnum(str, Enum):
    """Location enum."""

    US = "us"
    EU = "eu"
    ASIA = "asia"

    @property
    def item(self) -> LocationBase:
        """Get the location."""
        return LOCATION_MAPPING[self.value]
