from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from backend.users.models import User
from backend.users.schemas import UserRequestSchema, UserResponseSchema
from backend.users.security import get_password_hash, verify_password

class Service:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_data: UserRequestSchema) -> UserResponseSchema:
        async with self.session as session:
            user_data_dict = user_data.model_dump()
            user_data_dict['password'] = get_password_hash(user_data_dict['password'])
            user = User(**user_data_dict)
            try:    
                session.add(user)
                await session.commit()
                await session.refresh(user) 
                return UserResponseSchema.model_validate(user, from_attributes=True)
            except IntegrityError as e:
                await session.rollback()
                if 'users_nickname_key' in str(e.orig):  
                    raise HTTPException(status_code=409, detail="username already exists")
                elif 'users_email_key' in str(e.orig): 
                    raise HTTPException(status_code=409, detail="email already exists")
                else:
                    raise HTTPException(status_code=409, detail="an unknown integrity error occurred")
        
    async def get_users(self) -> list[UserResponseSchema]:
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return [UserResponseSchema.model_validate(user, from_attributes=True) for user in users]
    
    async def verify_user(self, username: str, password: str) -> int:
        async with self.session as session:
            result = await session.execute(select(User).where(User.nickname == username))
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=400, detail="user does not exist")
            if not verify_password(password, user.password):
                raise HTTPException(status_code=400, detail="wrong password")
            return user.id
        
    async def check_user_existion(self, user_id: str) -> bool:
        async with self.session as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=403, detail="not authorized")
            return True