"""Database operations for the ai_models and ai_model_types tables."""

from uuid import UUID

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import AIModel, AIModelBase, AIModelType, AIModelTypeBase


class AIModelTypeCRUD(BaseCRUD):
    """CRUD operations for the ai_model_types table."""

    async def create(self, ai_model_type: AIModelTypeBase) -> AIModelType:
        """Create a new AI model type."""
        ai_model_type = AIModelType(**ai_model_type.model_dump())

        self.session.add(ai_model_type)
        await self.session.commit()
        await self.session.refresh(ai_model_type)

        return ai_model_type

    async def get_by_id(self, ai_model_type_id: int) -> AIModelType | None:
        """Get an AI model type by ID."""
        ai_model_type = await self.session.execute(select(AIModelType).where(col(AIModelType.id) == ai_model_type_id))
        return ai_model_type.scalar_one_or_none()

    async def update(self, ai_model_type: AIModelTypeBase) -> AIModelType | None:
        """Update an AI model type."""
        _ai_model_type = await self.get_by_id(ai_model_type.id)

        if _ai_model_type is None:
            return None

        _ai_model_type.name = ai_model_type.name or _ai_model_type.name

        await self.session.commit()
        await self.session.refresh(_ai_model_type)

        return _ai_model_type


class AIModelCRUD(BaseCRUD):
    """CRUD operations for the ai_models table."""

    async def create(self, ai_model: AIModelBase) -> AIModel:
        """Create a new AI model."""
        ai_model = AIModel(**ai_model.model_dump())

        self.session.add(ai_model)
        await self.session.commit()
        await self.session.refresh(ai_model)

        return ai_model

    async def get_by_id(self, ai_model_id: str | UUID) -> AIModel | None:
        """Get an AI model by ID."""
        ai_model = await self.session.execute(select(AIModel).where(col(AIModel.id) == str(ai_model_id)))
        return ai_model.scalar_one_or_none()

    async def update(self, ai_model: AIModelBase) -> AIModel | None:
        """Update an AI model."""
        _ai_model = await self.get_by_id(ai_model.id)

        if _ai_model is None:
            return None

        _ai_model.name = ai_model.name or _ai_model.name

        await self.session.commit()
        await self.session.refresh(_ai_model)

        return _ai_model
