import jwt
from fastapi import HTTPException, Request
from passlib.context import CryptContext

from backend.core.settings import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_id_from_token(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        token_data = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        user_id = token_data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="unexpected error during token validation")
    

