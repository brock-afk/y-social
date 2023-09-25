from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Cookie, Form, Depends
from y_social.server.dependencies import user_repository, templates
from y_social.user.interface import UserRepository, UserIn

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    user_id: str = Cookie(None),
):
    return templates.TemplateResponse(
        "index.jinja", {"request": request, "user": user_id}
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
            "posts/feed.jinja", {"request": request, "user": user}
        )


@router.post("/signin", response_class=HTMLResponse)
async def signin(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(templates)],
    user_repository: Annotated[UserRepository, Depends(user_repository)],
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
        response = templates.TemplateResponse(
            "posts/feed.jinja", {"request": request, "user_id": user}
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
