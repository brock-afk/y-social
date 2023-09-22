import datetime

from typing import Protocol
from pydantic import BaseModel
from abc import ABC, abstractmethod


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        pass  # pragma: no cover

    def verify(self, password: str, hashed_password: str) -> bool:
        pass  # pragma: no cover


class UserRepository(ABC):
    class UserExistsError(Exception):
        pass

    @abstractmethod
    async def create_user(self, user_in: UserIn) -> UserOut:
        pass  # pragma: no cover
