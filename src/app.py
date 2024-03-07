from fastapi import FastAPI

from src.api.auth import auth as auth_router


app = FastAPI()


app.include_router(auth_router, prefix="/auth")
