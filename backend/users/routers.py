from typing import Annotated
from fastapi import APIRouter, Depends, Response

from backend.users.dependencies import get_service
from backend.users.schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema
from backend.users.service import Service

users_router = APIRouter()


@users_router.post("/api/v1/users", response_model=UserResponseSchema, status_code=201)
async def create_user(
    data: UserRequestSchema, service: Annotated[Service, Depends(get_service)]
) -> UserResponseSchema:
    response = await service.add_user(data)
    return response


@users_router.post("/api/v1/users/login", response_model=bool, status_code=201)
async def login(response: Response, data: UserLoginSchema, service: Annotated[Service, Depends(get_service)]) -> bool:
    token = await service.login_user(data)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="Lax")
    return True


@users_router.get("/api/v1/users", response_model=list[UserResponseSchema], status_code=200)
async def get_users(service: Annotated[Service, Depends(get_service)]) -> list[UserResponseSchema]:
    response = await service.get_users()
    return response


@users_router.post("/api/v1/users/logout", response_model=bool, status_code=201)
async def logout(response: Response) -> bool:
    response.delete_cookie(key="access_token")
    return True
