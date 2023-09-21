from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter, Form, Depends
from y_social.server.dependencies import user_repository
from y_social.user.interface import UserRepository, UserIn

router = APIRouter()

templates = Jinja2Templates(directory="./src/y_social/server/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/toggle-signup", response_class=HTMLResponse)
def toggle_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/toggle-signin", response_class=HTMLResponse)
def toggle_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    user_repository: Annotated[UserRepository, Depends(user_repository)],
    username: str = Form(...),
    password: str = Form(...),
):
    user = await user_repository.create_user(
        UserIn(username=username, password=password, email="test@gmail.com")
    )

    return templates.TemplateResponse("feed.html", {"request": request, "user": user})
