import re
from pydantic import BaseModel, field_validator


class UserRequestSchema(BaseModel):
    nickname: str
    email: str
    password: str  

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("password must contain at least one special character")
        return password

class UserResponseSchema(BaseModel):
    id: int
    nickname: str
    email: str