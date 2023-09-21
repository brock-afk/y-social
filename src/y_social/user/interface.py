import datetime

from pydantic import BaseModel
from abc import ABC, abstractmethod


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_in: UserIn) -> UserOut:
        pass  # pragma: no cover
