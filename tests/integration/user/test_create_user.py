import pytest
import asyncpg.connection

from fastapi.testclient import TestClient
from y_social.user.interface import UserIn, UserOut
from y_social.user.impl import PostgresUserRepository


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_inserts_record_into_user_table(
    user_repository: PostgresUserRepository,
):
    await user_repository.create_user(UserIn(username="test", password="test"))

    result = await user_repository.db_connection.fetch(
        """
        SELECT id
        FROM user_account
        """
    )

    assert len(result) == 1


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_returns_user_out(user_repository: PostgresUserRepository):
    result = await user_repository.create_user(UserIn(username="test", password="test"))

    assert isinstance(result, UserOut)


@pytest.mark.user
@pytest.mark.integration
async def test_register_endpoint_inserts_user_into_database(
    postgres_connection: asyncpg.connection.Connection,
    test_client: TestClient,
):
    response = test_client.post(
        "/register", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 200
    result = await postgres_connection.fetch(
        """
        SELECT id
        FROM user_account
        """
    )

    assert len(result) == 1


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_raises_user_exists_error_if_user_already_exists(
    user_repository: PostgresUserRepository,
):
    await user_repository.create_user(UserIn(username="test", password="test"))

    with pytest.raises(PostgresUserRepository.UserExistsError):
        await user_repository.create_user(UserIn(username="test", password="test"))


@pytest.mark.user
@pytest.mark.integration
async def test_register_endpoint_returns_user_exists_error_if_user_already_exists(
    postgres_connection: asyncpg.connection.Connection,
    test_client: TestClient,
):
    _ = test_client.post("/register", data={"username": "test", "password": "test"})
    response = test_client.post(
        "/register", data={"username": "test", "password": "test"}
    )

    assert response.status_code == 200
    result = await postgres_connection.fetch(
        """
        SELECT id
        FROM user_account
        """
    )

    assert len(result) == 1


@pytest.mark.user
@pytest.mark.integration
async def test_create_user_hashes_password(user_repository: PostgresUserRepository):
    await user_repository.create_user(UserIn(username="test", password="test"))

    result = await user_repository.db_connection.fetchrow(
        """
        SELECT password
        FROM user_account
        """
    )

    assert result["password"] != "test"
