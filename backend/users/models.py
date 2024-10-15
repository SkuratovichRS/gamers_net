from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    games: Mapped[List["Game"]] = relationship(secondary="users_games", back_populates="users")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    users: Mapped[List["User"]] = relationship(secondary="users_games", back_populates="games")


class UserGame(Base):
    __tablename__ = "users_games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("games.id"),
        nullable=False,
    )
