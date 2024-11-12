"""Game router."""

import logging

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.db import PlayerCRUD
from aiventure.dependencies import get_async_session_from_websocket
from aiventure.gcmanager import GameConnectionManager
from aiventure.models import User


logger = logging.getLogger("uvicorn.error")

game_connection_manager = GameConnectionManager()
router = APIRouter()


@router.websocket("/ws")
async def game_ws(
    websocket: WebSocket,
    token: str = Query(...),
    session: AsyncSession = Depends(get_async_session_from_websocket),
) -> None:
    """Websocket endpoint for game connections."""
    try:
        user: User | None = await game_connection_manager.connect(websocket, token, session)
        if not user:
            return

        while True:
            data = await websocket.receive_json()

            try:
                match data.get("command"):
                    case "retrieve-player-data":
                        player = await PlayerCRUD(session).read_by_user_id(user.id)
                        if player:
                            await websocket.send_json(player)
                        else:
                            await websocket.send_json({"error": "Player not found"})
                    case "test":
                        await websocket.send_json({"response": "test"})
                    case _:
                        logger.info(data)
            except Exception as e:
                logger.error(e)
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        if user:
            game_connection_manager.disconnect(user.id)

    except Exception as e:
        if not websocket.client_state.DISCONNECTED:
            await websocket.close(code=4000, reason=str(e))
