import os
import asyncpg
import asyncpg.connection

from fastapi import Depends
from typing import Annotated
from y_social.user.impl import PostgresUserRepository
from argon2 import PasswordHasher as Argon2PasswordHasher
from y_social.user.interface import UserRepository, PasswordHasher


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DB"),
        host=os.environ.get("POSTGRES_HOST", "postgres"),
    )


def password_hasher() -> PasswordHasher:
    return Argon2PasswordHasher()


def user_repository(
    db_connection: Annotated[asyncpg.connection.Connection, Depends(db_connection)],
    password_hasher: Annotated[PasswordHasher, Depends(password_hasher)],
) -> UserRepository:
    return PostgresUserRepository(db_connection, password_hasher)
