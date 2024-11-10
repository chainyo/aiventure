"""AI models models."""

from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from aiventure.models.core import UUIDModel
from aiventure.models.lab import Lab


class AIModelTypeBase(SQLModel):
    """AI model type base model."""

    id: int = Field(primary_key=True)
    name: str

    model_config = SQLModelConfig(json_schema_extra={"example": {"id": 1, "name": "NLP"}})


class AIModelType(AIModelTypeBase, table=True):
    """AI model type model."""

    __tablename__ = "ai_model_types"


AI_MODEL_TYPE_MAPPING: dict[str, AIModelTypeBase] = {
    "audio": AIModelTypeBase(id=1, name="Audio"),
    "cv": AIModelTypeBase(id=2, name="CV"),
    "nlp": AIModelTypeBase(id=3, name="NLP"),
    "multi_modal": AIModelTypeBase(id=4, name="Multi Modal"),
}


class AIModelTypeEnum(str, Enum):
    """AI model type enum."""

    AUDIO = "audio"
    CV = "cv"
    MULTI_MODAL = "multi_modal"
    NLP = "nlp"

    @property
    def item(self) -> AIModelTypeBase:
        """Get the item."""
        return AI_MODEL_TYPE_MAPPING[self]


class AIModelBase(UUIDModel):
    """AI model base model."""

    name: str
    model_type_id: int = Field(foreign_key="ai_model_types.id")
    tech_tree_id: str
    lab_id: str = Field(foreign_key="labs.id")

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {
                "name": "GPT-2",
                "model_type_id": 3,
                "tech_tree_id": "123e4567-e89b-12d3-a456-426614174000",
                "lab_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class AIModel(AIModelBase, table=True):
    """AI model model."""

    __tablename__ = "ai_models"

    lab: Lab = Relationship(back_populates="models")
