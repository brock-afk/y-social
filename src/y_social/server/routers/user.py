from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="./src/y_social/server/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/toggle-signup", response_class=HTMLResponse)
def toggle_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/toggle-signin", response_class=HTMLResponse)
def toggle_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})
