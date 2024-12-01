"""Game connection manager."""

import asyncio
import logging
from enum import Enum
from typing import Any

from fastapi import WebSocket
from jose import JWTError, jwt
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.config import settings
from aiventure.constants import INCOME_TICK_RATE
from aiventure.db import PlayerCRUD, PlayerLabInvestmentLinkCRUD, UsersCRUD
from aiventure.models import FundsUpdate, GlobalGameState, User


logger = logging.getLogger("uvicorn.error")


class ConnectedUser(BaseModel):
    """A connected user."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    player_id: str | None = None
    websocket: WebSocket


class GameAction(str, Enum):
    """Game action."""

    CREATE_LAB = "create-lab"
    CREATE_MODEL = "create-model"
    CREATE_PLAYER = "create-player"
    RETRIEVE_LAB = "retrieve-lab"
    RETRIEVE_PLAYER_DATA = "retrieve-player-data"
    UPDATE_FUNDS = "update-funds"


class GameMessage(BaseModel):
    """Game message."""

    action: GameAction
    payload: dict[str, Any]


class GameMessageResponse(BaseModel):
    """Game message response."""

    action: GameAction
    payload: dict[str, Any]
    error: str | None = None


class GameManager:
    """Game manager that handles game connections and logic."""

    def __init__(self) -> None:
        """Initialize game manager."""
        self.active_connections: dict[str, ConnectedUser] = {}

        self._async_session = None
        self._running = False
        self._income_tick_rate = INCOME_TICK_RATE

    async def start(self, async_session: AsyncSession) -> None:
        """Start the game manager."""
        self._async_session = async_session
        self._running = True
        self._income_task = asyncio.create_task(self._income_loop())

    async def stop(self) -> None:
        """Stop the game manager."""
        self._running = False
        if self._income_task:
            self._income_task.cancel()
            try:
                await self._income_task
            except asyncio.CancelledError:
                pass

    async def connect(self, websocket: WebSocket, token: str, session: AsyncSession) -> User | None:
        """Connect to the websocket."""
        await websocket.accept()

        user = await self.get_websocket_user(token, session)
        if not user:
            await websocket.close(code=4001, reason="Unauthorized")
            return None

        self.active_connections[user.id] = ConnectedUser(websocket=websocket)

        _state = GlobalGameState(n_connected_players=len(self.active_connections))
        await self.broadcast(_state.model_dump())

        return user

    def disconnect(self, user_id: str) -> None:
        """Disconnect from the websocket."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict[str, Any], user_id: str) -> None:
        """Send a personal message to a user."""
        if user_id in self.active_connections:
            await self.active_connections[user_id].websocket.send_json(GameMessageResponse(**message).model_dump())

    async def broadcast(self, message: dict[str, Any], exclude: str | None = None) -> None:
        """Broadcast a message to all users except one if specified."""
        for user_id, connection in self.active_connections.items():
            if user_id != exclude:
                await connection.websocket.send_json(message)

    async def set_player_id(self, user_id: str, player_id: str) -> None:
        """Set the player ID for a user."""
        if user_id in self.active_connections:
            if self.active_connections[user_id].player_id is None:
                self.active_connections[user_id].player_id = player_id

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

        except (JWTError, Exception):
            return None

    async def _income_loop(self) -> None:
        """Income loop for all connected clients."""
        while self._running:
            try:
                await self._process_income()
                await asyncio.sleep(self._income_tick_rate)
            except Exception as e:
                logger.error(f"Error in income loop: {e}")
                raise e

    async def _process_income(self) -> None:
        """Process income for all connected clients."""
        for user_id, connection in self.active_connections.items():
            if connection.player_id is not None:
                async with PlayerLabInvestmentLinkCRUD(self._async_session) as player_lab_investment_link_crud:
                    income = await player_lab_investment_link_crud.get_income_for_player(connection.player_id)

                if income is not None:
                    income = income + 2
                    async with PlayerCRUD(self._async_session) as player_crud:
                        player = await player_crud.increment_funds(connection.player_id, income)

                    if player:
                        await self.send_personal_message(
                            {
                                "action": GameAction.UPDATE_FUNDS,
                                "payload": FundsUpdate(funds=player.funds, update_type="increment").model_dump(),
                            },
                            user_id,
                        )


game_manager = GameManager()
