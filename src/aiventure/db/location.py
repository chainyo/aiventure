"""Location database."""

from sqlmodel import col, select

from aiventure.db.base import BaseCRUD
from aiventure.models import Location, LocationBase


class LocationCRUD(BaseCRUD):
    """CRUD operations for the location table."""

    async def create(self, location: LocationBase) -> Location:
        """Create a new location."""
        location = Location(**location.model_dump())

        self.session.add(location)
        await self.session.commit()
        await self.session.refresh(location)

        return location

    async def get_by_id(self, location_id: int) -> Location | None:
        """Get a location by id."""
        location = await self.session.execute(select(Location).where(col(Location.id) == location_id))
        return location.scalar_one_or_none()

    async def update(self, location: LocationBase) -> Location | None:
        """Update a location."""
        _location = await self.get_by_id(location.id)

        if _location is None:
            return None

        _location.name = location.name or _location.name
        _location.description = location.description or _location.description
        _location.modifier_id = location.modifier_id or _location.modifier_id

        self.session.add(_location)
        await self.session.commit()
        await self.session.refresh(_location)

        return _location
