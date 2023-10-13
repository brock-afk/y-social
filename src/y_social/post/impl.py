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

    async def get_posts(self, user_id: int) -> list[PostOut]:
        results = await self.db_connection.fetch(
            """
            SELECT post.text, post.created_by, user_account.username, post.created_at
            FROM post
            INNER JOIN user_account on post.created_by = user_account.id
            WHERE post.created_by = $1
            ORDER BY post.created_at DESC
            """,
            user_id,
        )

        return [PostOut(**result) for result in results]
