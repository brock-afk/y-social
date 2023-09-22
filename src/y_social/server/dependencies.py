import os
import asyncpg
import argon2.exceptions
import asyncpg.connection

from fastapi import Depends
from typing import Annotated
from functools import lru_cache
from y_social.user.impl import PostgresUserRepository
from argon2 import PasswordHasher as Argon2PasswordHasher
from y_social.user.interface import UserRepository, PasswordHasher


class Argon2PasswordHasherWrapper(PasswordHasher):
    def __init__(self) -> None:
        self.password_hasher = Argon2PasswordHasher()

    def hash(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            self.password_hasher.verify(hashed_password, password)
        except argon2.exceptions.VerificationError:
            return False
        else:
            return True


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DB"),
        host=os.environ.get("POSTGRES_HOST", "postgres"),
    )


@lru_cache
def password_hasher() -> PasswordHasher:
    return Argon2PasswordHasherWrapper()


def user_repository(
    db_connection: Annotated[asyncpg.connection.Connection, Depends(db_connection)],
    password_hasher: Annotated[PasswordHasher, Depends(password_hasher)],
) -> UserRepository:
    return PostgresUserRepository(db_connection, password_hasher)
