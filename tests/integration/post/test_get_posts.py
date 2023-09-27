import pytest

from y_social.post.impl import PostgresPostCollection, PostIn, PostOut


@pytest.mark.post
@pytest.mark.integration
async def test_get_posts_gets_post_created_by_user(
    post_repostiory: PostgresPostCollection, test_user: int
):
    post_in = PostIn(text="Hello world", created_by=test_user)
    await post_repostiory.create_post(post_in)

    posts = await post_repostiory.get_posts(test_user)

    assert len(posts) == 1
    assert posts[0].text == "Hello world"
    assert posts[0].created_by == test_user
    assert posts[0].created_at is not None


@pytest.mark.post
@pytest.mark.integration
async def test_get_posts_gets_posts_sorted_by_creation_date(
    post_repostiory: PostgresPostCollection, test_user: int
):
    post_in = PostIn(text="Hello world", created_by=test_user)
    await post_repostiory.create_post(post_in)

    post_in = PostIn(text="Hello world again", created_by=test_user)
    await post_repostiory.create_post(post_in)

    posts = await post_repostiory.get_posts(test_user)

    assert len(posts) == 2
    assert posts[0].text == "Hello world again"
    assert posts[1].text == "Hello world"
