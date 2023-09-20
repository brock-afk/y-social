import asyncpg.connection

from .interface import UserRepository, UserIn, UserOut


class PostgresUserRepository(UserRepository):
    def __init__(self, db_connection: asyncpg.connection.Connection) -> None:
        self.db_connection = db_connection

    async def create_user(self, user_in: UserIn) -> UserOut:
        result = await self.db_connection.fetchrow(
            """
            INSERT INTO user_accounts (username, password, email, created_at, updated_at)
            VALUES ($1, $2, $3, CLOCK_TIMESTAMP(), CLOCK_TIMESTAMP())
            RETURNING username, email, created_at, updated_at
            """,
            user_in.username,
            user_in.password,
            user_in.email,
        )

        return UserOut(**result)
