"""Game connection manager."""

from typing import Any

from fastapi import WebSocket


class GameConnectionManager:
    """Game connection manager."""

    def __init__(self) -> None:
        """Initialize game connection manager."""
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        """Connect to the websocket."""
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str) -> None:
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
