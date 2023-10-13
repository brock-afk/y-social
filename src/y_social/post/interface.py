import datetime

from pydantic import BaseModel
from abc import ABC, abstractmethod


class PostIn(BaseModel):
    text: str
    created_by: int


class PostOut(BaseModel):
    text: str
    username: str
    created_by: int
    created_at: datetime.datetime


class PostRepository(ABC):
    @abstractmethod
    async def create_post(self, post_in: PostIn) -> PostOut:
        pass  # pragma: no cover

    @abstractmethod
    async def get_posts(self, user_id: int) -> list[PostOut]:
        pass  # pragma: no cover
