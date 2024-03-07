import uvicorn

from fastapi import FastAPI

from src.api.auth import auth as auth_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/auth")


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=5000, reload=True)