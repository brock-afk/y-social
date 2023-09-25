import pytest

from y_social.post.impl import PostgresPostCollection, PostIn, PostOut


@pytest.mark.post
@pytest.mark.integration
async def test_create_post_updates_post_table(
    post_repostiory: PostgresPostCollection, test_user: int
):
    text = "Hello, world!"
    created_by = test_user
    post_in = PostIn(text=text, created_by=created_by)
    await post_repostiory.create_post(post_in)

    result = await post_repostiory.db_connection.fetch(
        """
        SELECT text, created_by, created_at
        FROM post
        WHERE text = $1 AND created_by = $2
        """,
        text,
        created_by,
    )

    assert len(result) == 1


@pytest.mark.post
@pytest.mark.integration
async def test_create_post_returns_post_out(
    post_repostiory: PostgresPostCollection, test_user: int
):
    text = "Hello, world!"
    created_by = test_user
    post_in = PostIn(text=text, created_by=created_by)
    post_out = await post_repostiory.create_post(post_in)

    assert isinstance(post_out, PostOut)
    assert post_out.text == text
    assert post_out.created_by == created_by
    assert post_out.created_at is not None
