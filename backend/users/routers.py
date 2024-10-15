from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
import jwt

from backend.settings import Settings
from backend.users.dependencies import create_service
from backend.users.schemas import UserRequestSchema, UserResponseSchema
from backend.users.security import get_user_id_from_token
from backend.users.service import Service


users_router = APIRouter()


@users_router.post("/api/v1/users", response_model=UserResponseSchema, status_code=201)
async def create_user(user_data: UserRequestSchema, service: Annotated[Service, Depends(create_service)]) -> UserResponseSchema:
    response = await service.add_user(user_data)
    return response


@users_router.post("/api/v1/users/login", response_model=bool, status_code=201)
async def login(
    response: Response, service: Annotated[Service, Depends(create_service)], username: str, password: str
) -> bool:
    user_id = await service.verify_user(username, password)
    token = jwt.encode({"user_id": user_id}, Settings.SECRET_KEY, Settings.ALGORITHM)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="Lax")
    return True


@users_router.get("/api/v1/users", response_model=list[UserResponseSchema], status_code=200)
async def get_users(request: Request, service: Annotated[Service, Depends(create_service)]) -> list[UserResponseSchema]:
    user_id = get_user_id_from_token(request)
    await service.check_user_existion(user_id)
    response = await service.get_users()
    return response

@users_router.post("/api/v1/users/logout", response_model=bool, status_code=201)
async def logout(response: Response) -> bool:
    response.delete_cookie(key="access_token")
    return True