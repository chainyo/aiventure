"""Game router."""

import logging
import uuid
from enum import Enum
from typing import Any

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.constants import CREATE_MODEL_COST
from aiventure.db import AIModelCRUD, LabCRUD, PlayerCRUD
from aiventure.dependencies import get_async_session_from_websocket
from aiventure.gcmanager import GameConnectionManager
from aiventure.models import (
    AI_MODEL_TYPE_MAPPING,
    AIModelBase,
    AIModelDataResponse,
    AIModelTypeBase,
    Investment,
    Investor,
    LabBase,
    LabDataResponse,
    Player,
    PlayerBase,
    PlayerDataResponse,
    User,
)


logger = logging.getLogger("uvicorn.error")

game_connection_manager = GameConnectionManager()
router = APIRouter()


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

        player: Player | None = None

        while True:
            data = await websocket.receive_json()
            message = GameMessage(**data)

            try:
                match message.action:
                    case GameAction.CREATE_LAB:
                        async with LabCRUD(session) as crud:
                            lab = await crud.create(
                                LabBase(
                                    name=message.payload["name"],
                                    location=message.payload["location"],
                                    valuation=0,
                                    income=0,
                                    tech_tree_id=str(uuid.uuid4()),
                                    player_id=player.id,
                                ),
                                player,
                            )
                            if lab:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_LAB,
                                        payload=LabDataResponse(
                                            id=lab.id,
                                            name=lab.name,
                                            location=lab.location,
                                            valuation=lab.valuation,
                                            income=lab.income,
                                            tech_tree_id=lab.tech_tree_id,
                                            player_id=lab.player_id,
                                            employees=[],
                                            models=[],
                                            investors=[
                                                Investor(
                                                    player=investor.player,
                                                    part=investor.part,
                                                )
                                                for investor in lab.investors
                                            ],
                                            player=lab.player,
                                        ).model_dump(),
                                    ).model_dump()
                                )
                            else:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_LAB,
                                        payload={},
                                        error="Failed to create lab",
                                    ).model_dump()
                                )
                    case GameAction.CREATE_MODEL:
                        # Check if funds are sufficient
                        if player.funds < CREATE_MODEL_COST:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.CREATE_MODEL,
                                    payload={},
                                    error="Insufficient funds",
                                ).model_dump()
                            )
                            continue
                        # Check if lab is the user's lab
                        _lab = next((lab for lab in player.labs if lab.id == message.payload["lab_id"]), None)
                        if not _lab:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.CREATE_MODEL,
                                    payload={},
                                    error="You can only create a model for your lab.",
                                ).model_dump()
                            )
                            continue
                        # Get the ai model type id
                        ai_model_type: AIModelTypeBase | None = AI_MODEL_TYPE_MAPPING.get(
                            message.payload["category"], None
                        )
                        if not ai_model_type:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.CREATE_MODEL,
                                    payload={},
                                    error="Model category not found",
                                ).model_dump()
                            )
                            continue
                        # Check if model name is available or create new model
                        async with AIModelCRUD(session) as crud:
                            if await crud.get_by_name(message.payload["name"]):
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_MODEL,
                                        payload={},
                                        error="Model name already exists",
                                    ).model_dump()
                                )
                                continue
                            # Create AI Model
                            model = await crud.create(
                                AIModelBase(
                                    name=message.payload["name"],
                                    ai_model_type_id=ai_model_type.id,
                                    tech_tree_id=str(uuid.uuid4()),
                                    lab_id=_lab.id,
                                ),
                                _lab,
                            )

                            if model:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_MODEL,
                                        payload=AIModelDataResponse(
                                            id=model.id,
                                            name=model.name,
                                            ai_model_type_id=model.ai_model_type_id,
                                            tech_tree_id=model.tech_tree_id,
                                            lab_id=model.lab_id,
                                        ).model_dump(),
                                    ).model_dump()
                                )
                            else:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_MODEL,
                                        payload={},
                                        error="Failed to create model",
                                    ).model_dump()
                                )
                                continue
                        # Decrement funds
                        async with PlayerCRUD(session) as crud:
                            _player = await crud.decrement_funds(player.id, CREATE_MODEL_COST)
                            if _player:
                                player.funds = _player.funds
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.UPDATE_FUNDS,
                                        payload={
                                            "funds": player.funds
                                        },
                                    ).model_dump()
                                )
                            else:
                                # TODO: Handle error
                                continue

                    case GameAction.CREATE_PLAYER:
                        async with PlayerCRUD(session) as crud:
                            player = await crud.create(
                                PlayerBase(
                                    name=message.payload["name"],
                                    avatar=message.payload["avatar"],
                                    user_id=user.id,
                                )
                            )
                            if player:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_PLAYER,
                                        payload=PlayerDataResponse(
                                            id=player.id,
                                            name=player.name,
                                            avatar=player.avatar,
                                            funds=player.funds,
                                            labs=[],
                                            investments=[
                                                Investment(
                                                    lab=investment.lab,
                                                    part=investment.part,
                                                )
                                                for investment in player.investments
                                            ],
                                        ).model_dump(),
                                    ).model_dump()
                                )
                            else:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.CREATE_PLAYER,
                                        payload={},
                                        error="Failed to create player",
                                    ).model_dump()
                                )
                    case GameAction.RETRIEVE_LAB:
                        async with LabCRUD(session) as crud:
                            lab = await crud.read_by_id(message.payload["id"])

                            if lab:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.RETRIEVE_LAB,
                                        payload=LabDataResponse(
                                            id=lab.id,
                                            name=lab.name,
                                            location=lab.location,
                                            valuation=lab.valuation,
                                            income=lab.income,
                                            tech_tree_id=lab.tech_tree_id,
                                            player_id=lab.player_id,
                                            employees=lab.employees,
                                            models=lab.models,
                                            investors=[
                                                Investor(
                                                    player=investor.player,
                                                    part=investor.part,
                                                )
                                                for investor in lab.investors
                                            ],
                                            player=lab.player,
                                        ).model_dump(),
                                    ).model_dump()
                                )
                            else:
                                await websocket.send_json(
                                    GameMessageResponse(
                                        action=GameAction.RETRIEVE_LAB,
                                        payload={},
                                        error="Lab not found",
                                    ).model_dump()
                                )
                    case GameAction.RETRIEVE_PLAYER_DATA:
                        async with PlayerCRUD(session) as crud:
                            if not player:
                                player = await crud.read_player_data_by_user_id(user.id)
                            else:
                                player = await crud.read_player_data_by_id(player.id)
                        if player:
                            await websocket.send_json(
                                GameMessageResponse(
                                    action=GameAction.RETRIEVE_PLAYER_DATA,
                                    payload=PlayerDataResponse(
                                        id=player.id,
                                        name=player.name,
                                        avatar=player.avatar,
                                        funds=player.funds,
                                        labs=player.labs,
                                        investments=[
                                            Investment(
                                                lab=investment.lab,
                                                part=investment.part,
                                            )
                                            for investment in player.investments
                                        ],
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
