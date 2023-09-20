import datetime

from abc import ABC, abstractmethod
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_in: UserIn) -> UserOut:
        pass  # pragma: no cover
