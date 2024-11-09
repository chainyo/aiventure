"""Routing the requested endpoints to the API."""

from enum import Enum

from fastapi import APIRouter


api_router = APIRouter()

routers: list[tuple[APIRouter, str, list[str | Enum]]] = []

for items in routers:
    router, prefix, tags = items
    api_router.include_router(router, prefix=prefix, tags=tags)
