"""Quality models."""

from enum import Enum

from sqlmodel import Field, SQLModel
from sqlmodel._compat import SQLModelConfig


class QualityBase(SQLModel):
    """Quality model."""

    id: int = Field(primary_key=True)
    name: str
    hex_color: str

    model_config = SQLModelConfig(
        json_schema_extra={
            "example": {"id": 1, "name": "Poor", "hex_color": "#9d9d9d"}
        }
    )


class Quality(QualityBase, table=True):
    """Quality model."""

    __tablename__ = "qualities"


QUALITY_MAPPING: dict[str, QualityBase] = {
    "poor": QualityBase(id=1, name="Poor", hex_color="#9d9d9d"),
    "common": QualityBase(id=2, name="Common", hex_color="#ffffff"),
    "uncommon": QualityBase(id=3, name="Uncommon", hex_color="#1eff00"),
    "rare": QualityBase(id=4, name="Rare", hex_color="#0070dd"),
    "epic": QualityBase(id=5, name="Epic", hex_color="#a335ee"),
    "legendary": QualityBase(id=6, name="Legendary", hex_color="#ff8000"),
    "star": QualityBase(id=7, name="Star", hex_color="#e6cc80"),
}


class QualityEnum(str, Enum):
    """Quality enum."""

    POOR = "poor"
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    STAR = "star"

    @property
    def item(self) -> QualityBase:
        """Get the quality."""
        return QUALITY_MAPPING[self.value]
