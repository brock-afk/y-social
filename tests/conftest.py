import os
import pytest
import asyncpg
import asyncpg.connection

from y_social.server.main import app
from fastapi.testclient import TestClient
from y_social.server.dependencies import db_connection


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

    await connection.execute("DELETE FROM user_accounts")

    yield connection

    await connection.close()


@pytest.fixture
def test_client():
    return TestClient(app)
