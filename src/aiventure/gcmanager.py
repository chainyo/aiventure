"""Game connection manager."""

from typing import Any

from fastapi import Depends, WebSocket
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.config import settings
from aiventure.db import UsersCRUD
from aiventure.dependencies import get_async_session_from_websocket
from aiventure.models import User


async def get_users_crud(session: AsyncSession = Depends(get_async_session_from_websocket)) -> UsersCRUD:
    return UsersCRUD(session=session)


class GameConnectionManager:
    """Game connection manager."""

    def __init__(self) -> None:
        """Initialize game connection manager."""
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, token: str, session: AsyncSession) -> User | None:
        """Connect to the websocket."""
        await websocket.accept()

        user = await self.get_websocket_user(token, session)
        if not user:
            await websocket.close(code=4001, reason="Unauthorized")
            return None

        self.active_connections[user.id] = websocket

        return user

    def disconnect(self, user_id: str) -> None:
        """Disconnect from the websocket."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict[str, Any], user_id: str) -> None:
        """Send a personal message to a user."""
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast(self, message: dict[str, Any], exclude: str | None = None) -> None:
        """Broadcast a message to all users except one."""
        for user_id, connection in self.active_connections.items():
            if user_id != exclude:
                await connection.send_json(message)

    async def get_websocket_user(self, token: str, session: AsyncSession) -> User | None:
        """Authenticate WebSocket connection and return user."""
        users_crud = UsersCRUD(session=session)
        try:
            payload = jwt.decode(token, settings.openssl_key, algorithms=[settings.algorithm])
            username = payload.get("sub")

            if username is None:
                return None

            user = await users_crud.get_by_email(username)
            if not user:
                return None

            return user

        except JWTError:
            return None

        except Exception:
            return None
