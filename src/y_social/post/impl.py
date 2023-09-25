import asyncpg.connection

from .interface import PostRepository, PostIn, PostOut


class PostgresPostCollection(PostRepository):
    def __init__(self, db_connection: asyncpg.connection.Connection) -> None:
        self.db_connection = db_connection

    async def create_post(self, post_in: PostIn) -> PostOut:
        result = await self.db_connection.fetchrow(
            """
            INSERT INTO post (text, created_by, created_at)
            VALUES ($1, $2, CLOCK_TIMESTAMP())
            RETURNING text, created_by, created_at
            """,
            post_in.text,
            post_in.created_by,
        )

        return PostOut(**result)
