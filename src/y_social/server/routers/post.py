from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Form, Depends
from y_social.post.interface import PostRepository, PostIn
from y_social.server.dependencies import templates, post_repository

router = APIRouter()


@router.post("/create-post/{user}", response_class=HTMLResponse)
async def create_post(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    post_repostiory: Annotated[PostRepository, Depends(post_repository)],
    user: int,
    content: str = Form(...),
):
    await post_repostiory.create_post(PostIn(text=content, created_by=user))
    posts = await post_repostiory.get_posts(user)
    return templates.TemplateResponse(
        "feed/posts.jinja", {"request": request, "user": user, "posts": posts}
    )
