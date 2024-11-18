"""Database operations for the modifiers table."""

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Modifier, ModifierBase, ModifierType, ModifierTypeBase


class ModifierTypeCRUD(BaseCRUD):
    """CRUD operations for the modifier_types table."""

    async def create(self, modifier_type: ModifierTypeBase) -> ModifierType:
        """Create a new modifier type."""
        modifier_type = ModifierType(**modifier_type.model_dump())

        self.session.add(modifier_type)
        await self.session.commit()
        await self.session.refresh(modifier_type)

        return modifier_type

    async def get_by_id(self, modifier_type_id: int) -> ModifierType | None:
        """Get a modifier type by id."""
        modifier_type = await self.session.execute(select(ModifierType).where(col(ModifierType.id) == modifier_type_id))
        return modifier_type.scalar_one_or_none()

    async def update(self, modifier_type: ModifierTypeBase) -> ModifierType | None:
        """Update a modifier type."""
        _modifier_type = await self.get_by_id(modifier_type.id)

        if _modifier_type is None:
            return None

        _modifier_type.name = modifier_type.name

        await self.session.commit()
        await self.session.refresh(_modifier_type)

        return _modifier_type


class ModifierCRUD(BaseCRUD):
    """CRUD operations for the modifiers table."""

    async def create(self, modifier: ModifierBase) -> Modifier:
        """Create a new modifier."""
        modifier = Modifier(**modifier.model_dump())

        self.session.add(modifier)
        await self.session.commit()
        await self.session.refresh(modifier)

        return modifier

    async def get_by_id(self, modifier_id: int) -> Modifier | None:
        """Get a modifier by id."""
        modifier = await self.session.execute(select(Modifier).where(col(Modifier.id) == modifier_id))
        return modifier.scalar_one_or_none()

    async def update(self, modifier: ModifierBase) -> Modifier | None:
        """Update a modifier."""
        _modifier = await self.get_by_id(modifier.id)

        if _modifier is None:
            return None

        _modifier.name = modifier.name
        _modifier.description = modifier.description
        _modifier.type_id = modifier.type_id

        await self.session.commit()
        await self.session.refresh(_modifier)

        return _modifier
