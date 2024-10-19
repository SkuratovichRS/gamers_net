from fastapi import Depends
from backend.core.dependencies import get_session
from backend.users.service import Service
from backend.users.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession


def get_repository(session: AsyncSession = Depends(get_session)) -> Repository:
    return Repository(session)


def get_service(repo: Repository = Depends(get_repository)) -> Service:
    return Service(repo)
