from typing import Annotated

from fastapi import APIRouter, Depends, Request

from backend.games.dependencies import get_service
from backend.games.schemas import (CreateUserGameResponseSchema,
                                   GetUserGamesResponseSchema,
                                   UserGameRequestSchema)
from backend.games.service import Service

games_router = APIRouter(prefix="/api/v1/games", tags=["games"])


@games_router.post("", response_model=CreateUserGameResponseSchema, status_code=201)
async def create_user_game(
    request: Request, data: UserGameRequestSchema, service: Annotated[Service, Depends(get_service)]
) -> CreateUserGameResponseSchema:
    user_id = request.state.user_id
    response = await service.add_user_game(data, user_id)
    return response


@games_router.get("", response_model=list[GetUserGamesResponseSchema])
async def get_user_games(
    request: Request, service: Annotated[Service, Depends(get_service)]
) -> list[GetUserGamesResponseSchema]:
    user_id = request.state.user_id
    response = await service.get_user_games(user_id)
    return response
