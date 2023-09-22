import pytest
import asyncpg.connection

from y_social.user.interface import UserIn, UserOut
from y_social.user.impl import PostgresUserRepository


@pytest.mark.user
@pytest.mark.integration
async def test_verify_user_raises_user_does_not_exist_error_if_user_does_not_exist(
    user_repository: PostgresUserRepository,
):
    with pytest.raises(user_repository.UserDoesNotExistError):
        await user_repository.verify_user(UserIn(username="test", password="test"))


@pytest.mark.user
@pytest.mark.integration
async def test_verify_user_raises_invalid_password_error_if_password_is_invalid(
    user_repository: PostgresUserRepository,
):
    await user_repository.create_user(UserIn(username="test", password="test"))

    with pytest.raises(user_repository.InvalidPasswordError):
        await user_repository.verify_user(UserIn(username="test", password="invalid"))


@pytest.mark.user
@pytest.mark.integration
async def test_verify_user_returns_user_out_if_user_exists_and_password_is_valid(
    user_repository: PostgresUserRepository,
):
    await user_repository.create_user(UserIn(username="test", password="test"))

    result = await user_repository.verify_user(UserIn(username="test", password="test"))

    assert isinstance(result, UserOut)
    assert result.username == "test"
