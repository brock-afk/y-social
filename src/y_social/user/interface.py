import datetime

from typing import Protocol
from pydantic import BaseModel
from abc import ABC, abstractmethod


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        pass  # pragma: no cover

    def verify(self, password: str, hashed_password: str) -> bool:
        pass  # pragma: no cover


class UserRepository(ABC):
    class CreateUserError(Exception):
        pass

    class UserExistsError(CreateUserError):
        pass

    class LoginError(Exception):
        pass

    class UserDoesNotExistError(LoginError):
        pass

    class InvalidPasswordError(LoginError):
        pass

    @abstractmethod
    async def create_user(self, user_in: UserIn) -> UserOut:
        pass  # pragma: no cover

    @abstractmethod
    async def verify_user(self, user_in: UserIn) -> UserOut:
        pass  # pragma: no cover
