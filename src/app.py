import uvicorn

from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.advert import router as advert_router
from src.api.comment import router as comment_router
from src.api.complaints import router as complaints_router
from src.api.user import router as user_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(advert_router, prefix="/api/advert", tags=["advert"])
app.include_router(comment_router, prefix="/api", tags=["comment"])
app.include_router(complaints_router, prefix="/api", tags=["complaint"])


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=5000, reload=True)
