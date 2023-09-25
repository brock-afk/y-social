import os
import pytest
import asyncpg
import asyncpg.connection

from y_social.server.main import app
from fastapi.testclient import TestClient
from y_social.user.impl import PostgresUserRepository
from y_social.post.impl import PostgresPostCollection
from tests.doubles.passwordhasher import PasswordHasherTestDouble


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
async def postgres_connection() -> asyncpg.connection.Connection:
    try:
        connection: asyncpg.connection.Connection = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database="test",
            host=os.getenv("POSTGRES_HOST", "postgres"),
            timeout=1,
        )
    except Exception:
        pytest.skip("Could not connect to Postgres")

    await connection.execute("DELETE FROM post")
    await connection.execute("DELETE FROM user_account")

    yield connection

    await connection.close()


@pytest.fixture
def password_hasher() -> PasswordHasherTestDouble:
    return PasswordHasherTestDouble()


@pytest.fixture
def user_repository(
    postgres_connection: asyncpg.connection.Connection,
    password_hasher: PasswordHasherTestDouble,
) -> PostgresUserRepository:
    return PostgresUserRepository(postgres_connection, password_hasher)


@pytest.fixture
def post_repostiory(
    postgres_connection: asyncpg.connection.Connection,
) -> PostgresPostCollection:
    return PostgresPostCollection(postgres_connection)


@pytest.fixture
async def test_user(postgres_connection: asyncpg.connection.Connection) -> int:
    result = await postgres_connection.fetchrow(
        """
        INSERT INTO user_account (username, password, created_at, updated_at)
        VALUES ('test', 'test', CLOCK_TIMESTAMP(), CLOCK_TIMESTAMP())
        RETURNING id
        """
    )

    yield result["id"]
