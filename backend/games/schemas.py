from pydantic import BaseModel


class UserGameRequestSchema(BaseModel):
    name: str

class CreateUserGameResponseSchema(BaseModel):
    id: int
    user_id: int
    game_id: int


class GetUserGamesResponseSchema(BaseModel):
    id: int
    user_id: int
    game_id: int
    user_nickname: str
    game_name: str