import asyncpg
import asyncpg.connection

from .interface import UserRepository, UserIn, UserOut


class PostgresUserRepository(UserRepository):
    def __init__(self, db_connection: asyncpg.connection.Connection) -> None:
        self.db_connection = db_connection

    async def create_user(self, user_in: UserIn) -> UserOut:
        try:
            result = await self.db_connection.fetchrow(
                """
                INSERT INTO user_accounts (username, password, created_at, updated_at)
                VALUES ($1, $2, CLOCK_TIMESTAMP(), CLOCK_TIMESTAMP())
                RETURNING username, created_at, updated_at
                """,
                user_in.username,
                user_in.password,
            )
        except asyncpg.exceptions.UniqueViolationError:
            raise self.UserExistsError(f"User {user_in.username} already exists")

        return UserOut(**result)
