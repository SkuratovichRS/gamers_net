# Dependencies for game-related operations will be defined here
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_session
from backend.games.repository import Repository
from backend.games.service import Service


def get_repository(session: AsyncSession = Depends(get_session)) -> Repository:
    return Repository(session)


def get_service(repo: Repository = Depends(get_repository)) -> Service:
    return Service(repo)
