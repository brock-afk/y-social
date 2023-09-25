from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from y_social.post.interface import PostRepository
from y_social.user.interface import UserRepository, UserIn
from fastapi import Request, APIRouter, Cookie, Form, Depends
from y_social.server.dependencies import user_repository, post_repository, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    post_repository: Annotated[PostRepository, Depends(post_repository)],
    user_id: str = Cookie(None),
):
    if user_id is not None:
        posts = await post_repository.get_posts(int(user_id))
    return templates.TemplateResponse(
        "index.jinja", {"request": request, "user": user_id, "posts": posts}
    )


@router.get("/toggle-signup", response_class=HTMLResponse)
def toggle_signup(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
):
    return templates.TemplateResponse("forms/signup.jinja", {"request": request})


@router.get("/toggle-signin", response_class=HTMLResponse)
def toggle_signin(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
):
    return templates.TemplateResponse("forms/signin.jinja", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    user_repository: Annotated[UserRepository, Depends(user_repository)],
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        user = await user_repository.create_user(
            UserIn(username=username, password=password)
        )
    except user_repository.CreateUserError as e:
        return templates.TemplateResponse(
            "forms/signup.jinja",
            {
                "request": request,
                "error": str(e),
                "username": username,
                "password": password,
            },
        )
    else:
        return templates.TemplateResponse(
            "posts/feed.jinja", {"request": request, "user": user, "posts": []}
        )


@router.post("/signin", response_class=HTMLResponse)
async def signin(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    user_repository: Annotated[UserRepository, Depends(user_repository)],
    post_repository: Annotated[PostRepository, Depends(post_repository)],
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        user = await user_repository.verify_user(
            UserIn(username=username, password=password)
        )
    except user_repository.LoginError as e:
        return templates.TemplateResponse(
            "forms/signin.jinja",
            {
                "request": request,
                "error": str(e),
                "username": username,
                "password": password,
            },
        )
    else:
        posts = await post_repository.get_posts(user.id)
        response = templates.TemplateResponse(
            "posts/feed.jinja", {"request": request, "user_id": user, "posts": posts}
        )
        response.set_cookie(
            "user_id", str(user.id), httponly=True, secure=True, samesite="strict"
        )
        response.set_cookie(
            key="username",
            value=str(user.username),
            httponly=True,
            secure=True,
            samesite="strict",
        )

        return response


@router.post("/signout", response_class=HTMLResponse)
async def signout(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
):
    response = templates.TemplateResponse("forms/signin.jinja", {"request": request})
    response.delete_cookie(key="user_id")

    return response
