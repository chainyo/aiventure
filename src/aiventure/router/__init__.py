"""Router for the API."""

from .authentication import router as auth_router
from .core import router as core_router
from .game import router as game_router
from .web import router as web_router


__all__ = ["auth_router", "core_router", "game_router", "web_router"]
