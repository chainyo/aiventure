"""Game router."""

import logging
from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.db import PlayerCRUD
from aiventure.dependencies import get_async_session_from_websocket
from aiventure.gcmanager import GameConnectionManager
from aiventure.models import PlayerDataResponse, User


logger = logging.getLogger("uvicorn.error")

game_connection_manager = GameConnectionManager()
router = APIRouter()


class GameAction(str, Enum):
    """Game action."""

    RETRIEVE_PLAYER_DATA = "retrieve-player-data"


class GameMessage(BaseModel):
    """Game message."""

    action: GameAction
    payload: dict[str, Any]


class GameMessageResponse(BaseModel):
    """Game message response."""

    action: GameAction
    payload: dict[str, Any]
    error: str | None = None


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
            message = GameMessage(**data)

            try:
                match message.action:
                    case GameAction.RETRIEVE_PLAYER_DATA:
                        async with PlayerCRUD(session) as crud:
                            player = await crud.get_by_user_id(user.id)
                            labs = player.labs if player else []
                            investments = player.investments if player else []

                        if player:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.RETRIEVE_PLAYER_DATA,
                                    payload=PlayerDataResponse(
                                        id=player.id,
                                        name=player.name,
                                        funds=player.funds,
                                        labs=[lab.model_dump() for lab in labs],
                                        investments=[investment.model_dump() for investment in investments],
                                    ).model_dump()
                                ).model_dump()
                            )
                        else:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.RETRIEVE_PLAYER_DATA,
                                    payload={},
                                    error="Player not found",
                                ).model_dump()
                            )
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
