import pytest
import asyncpg.connection

from fastapi.testclient import TestClient
from y_social.user.interface import UserIn, UserOut
from y_social.user.impl import PostgresUserRepository


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_inserts_record_into_user_table(
    postgres_connection: asyncpg.connection.Connection,
):
    user_repository = PostgresUserRepository(postgres_connection)
    await user_repository.create_user(
        UserIn(username="test", password="test", email="test@gmail.com")
    )

    result = await postgres_connection.fetch(
        """
        SELECT id
        FROM user_accounts
        """
    )

    assert len(result) == 1


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_returns_user_out(
    postgres_connection: asyncpg.connection.Connection,
):
    user_repository = PostgresUserRepository(postgres_connection)
    result = await user_repository.create_user(
        UserIn(username="test", password="test", email="test@gmail.com")
    )

    assert isinstance(result, UserOut)


@pytest.mark.user
@pytest.mark.integration
async def test_register_endpoint_inserts_user_into_database(
    postgres_connection: asyncpg.connection.Connection,
    test_client: TestClient,
):
    response = test_client.post(
        "/register",
        data={"username": "test", "password": "test", "email": "test@gmail.com"},
    )

    assert response.status_code == 200
    result = await postgres_connection.fetch(
        """
        SELECT id
        FROM user_accounts
        """
    )

    assert len(result) == 1
