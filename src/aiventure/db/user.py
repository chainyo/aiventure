"""User database operations."""

from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, delete, select

from aiventure.db.base import BaseCRUD
from aiventure.db.utils import handle_crud_operation
from aiventure.models import User, UserCreate
from aiventure.utils import PasswordManager


class UsersCRUD(BaseCRUD):
    """Users CRUD."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialization."""
        super().__init__(session)
        self.pwmanager = PasswordManager()

    @handle_crud_operation
    async def create(self, data: UserCreate) -> User:
        """Create a user."""
        values = data.model_dump()
        values["password"] = self.pwmanager.hash_password(values["password"])

        user = User(**values)
        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    @handle_crud_operation
    async def get_by_id(self, user_id: str | UUID) -> User | None:
        """Get a user."""
        user = await self.session.execute(select(User).where(col(User.id) == str(user_id)))
        return user.scalar_one_or_none()

    @handle_crud_operation
    async def get_by_email(self, email: str) -> User | None:
        """Get a user."""
        user = await self.session.execute(select(User).where(col(User.email) == email))
        return user.scalar_one_or_none()

    @handle_crud_operation
    async def authenticate(self, email: str, password: str) -> User | None:
        """Verify a user."""
        user = await self.get_by_email(email)

        if user is None:
            return None

        try:
            self.pwmanager.verify_password(password, user.password)
            return user

        except VerifyMismatchError:
            return None

    @handle_crud_operation
    async def delete(self, email: str) -> bool | None:
        """Remove a user."""
        user = await self.get_by_email(email)

        if user is None:
            return None

        await self.session.execute(delete(User).where(col(User.email) == email))
        await self.session.commit()

        return True

    @handle_crud_operation
    async def promote_to_admin(self, email: str) -> User | None:
        """Promote a user to admin."""
        user = await self.get_by_email(email)

        if user is None:
            return None

        user.is_admin = True

        await self.session.commit()
        await self.session.refresh(user)

        return user

    @handle_crud_operation
    async def update(self) -> None:
        """Update a user."""
        pass
