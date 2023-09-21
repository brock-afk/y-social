import os
import asyncpg
import asyncpg.connection

from fastapi import Depends
from typing import Annotated
from y_social.user.interface import UserRepository
from y_social.user.impl import PostgresUserRepository


async def db_connection() -> asyncpg.connection.Connection:
    return await asyncpg.connect(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        database=os.environ.get("POSTGRES_DB"),
        host=os.environ.get("POSTGRES_HOST", "postgres"),
    )


def user_repository(
    db_connection: Annotated[asyncpg.connection.Connection, Depends(db_connection)]
) -> UserRepository:
    return PostgresUserRepository(db_connection)
