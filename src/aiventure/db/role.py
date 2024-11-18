"""Database operations for the roles and role_categories table."""

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Role, RoleBase, RoleCategory, RoleCategoryBase


class RoleCategoryCRUD(BaseCRUD):
    """CRUD operations for the role_categories table."""

    async def create(self, role_category: RoleCategoryBase) -> RoleCategory:
        """Create a new role category."""
        role_category = RoleCategory(**role_category.model_dump())

        self.session.add(role_category)
        await self.session.commit()
        await self.session.refresh(role_category)

        return role_category

    async def get_by_id(self, role_category_id: int) -> RoleCategory | None:
        """Get a role category by id."""
        role_category = await self.session.execute(select(RoleCategory).where(col(RoleCategory.id) == role_category_id))
        return role_category.scalar_one_or_none()

    async def update(self, role_category: RoleCategoryBase) -> RoleCategory | None:
        """Update a role category."""
        _role_category = await self.get_by_id(role_category.id)

        if _role_category is None:
            return None

        _role_category.name = role_category.name or _role_category.name
        _role_category.hex_color = role_category.hex_color or _role_category.hex_color

        self.session.add(_role_category)
        await self.session.commit()
        await self.session.refresh(_role_category)

        return _role_category


class RoleCRUD(BaseCRUD):
    """CRUD operations for the roles table."""

    async def create(self, role: RoleBase) -> Role:
        """Create a new role."""
        role = Role(**role.model_dump())

        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)

        return role

    async def get_by_id(self, role_id: int) -> Role | None:
        """Get a role by id."""
        role = await self.session.execute(select(Role).where(col(Role.id) == role_id))
        return role.scalar_one_or_none()

    async def update(self, role: RoleBase) -> Role | None:
        """Update a role."""
        _role = await self.get_by_id(role.id)

        if _role is None:
            return None

        _role.name = role.name or _role.name
        _role.description = role.description or _role.description
        _role.category_id = role.category_id or _role.category_id

        self.session.add(_role)
        await self.session.commit()
        await self.session.refresh(_role)

        return _role
