"""Game router."""

import logging

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.config import settings
from aiventure.db import UsersCRUD
from aiventure.dependencies import get_async_session
from aiventure.gcmanager import GameConnectionManager
from aiventure.models import User


logger = logging.getLogger(__name__)

game_connection_manager = GameConnectionManager()
router = APIRouter()


async def get_users_crud(session: AsyncSession = Depends(get_async_session)) -> UsersCRUD:
    return UsersCRUD(session=session)


async def get_websocket_user(
    websocket: WebSocket,
    token: str = Query(...),
    users_crud: UsersCRUD = Depends(get_users_crud),
) -> User:
    """Authenticate WebSocket connection and return user."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        username = payload.get("sub")

        if username is None:
            await websocket.close(code=4001, reason="Invalid authentication token")
            return None

        user = await users_crud.get_by_email(username)
        if not user:
            await websocket.close(code=4001, reason="User not found")
            return None

        return user
    except JWTError:
        await websocket.close(code=4001, reason="Invalid authentication token")
        return None


@router.websocket("/ws")
async def game_ws(
    websocket: WebSocket,
    token: str = Query(...),
) -> None:
    """Websocket endpoint for game connections."""
    try:
        await websocket.accept()
        logger.info("WebSocket accepted")

        user = await get_websocket_user(websocket, token)
        logger.info(f"User: {user}")
        if not user:
            await websocket.close(code=4001, reason="Unauthorized")
            return

        await game_connection_manager.connect(websocket, user.id)

        try:
            while True:
                data = await websocket.receive_json()
                logger.info(f"Received: {data}")

                match data.get("command"):
                    case "test":
                        logger.info("Received test command")
                        await websocket.send_json({"response": "test"})
                    case _:
                        logger.info(data)

        except WebSocketDisconnect:
            await game_connection_manager.disconnect(user.id)

    except Exception as e:
        if not websocket.client_state.DISCONNECTED:
            await websocket.close(code=4000, reason=str(e))
