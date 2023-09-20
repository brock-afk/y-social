from fastapi import FastAPI
from y_social.server.routers import user

app = FastAPI()

app.include_router(user.router)
