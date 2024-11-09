"""Labs models."""

from uuid import UUID

from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.location import LocationEnum


class LabBase(UUIDModel):
    """Lab model."""

    name: str
    location: LocationEnum
    valuation: float
    income: float
    tech_tree_id: UUID

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "name": "Lab Zero",
                "location": "us",
                "valuation": 1000000,
                "income": 100000,
                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class Lab(LabBase, table=True):
    """Table for labs."""

    __tablename__ = "labs"
