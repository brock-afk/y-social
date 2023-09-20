from abc import ABC, abstractmethod
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_in: UserIn) -> UserInDB:
        pass  # pragma: no cover
