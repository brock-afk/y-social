import os
import pytest
import asyncpg
import asyncpg.connection


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
