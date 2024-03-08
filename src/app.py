import logging
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI, Request

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.logger import logger

from src.api.auth import router as auth_router
from src.api.advert import router as advert_router
from src.api.comment import router as comment_router
from src.api.complaints import router as complaints_router
from src.api.user import router as user_router

from src.db.db import sessionmaker
from src.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with sessionmaker() as conn:
        try:
            await conn.execute(text("SELECT 1;"))
            logger.info("Connection to db established")
        except SQLAlchemyError as e:
            logger.critical("Failed to connect to db")
            raise e

    yield


app = FastAPI(title="Ad placement service API", lifespan=lifespan)


if config.telegram_bot_token and config.telegram_chat_id:
    @app.exception_handler(500)
    async def critical_error_handler(request: Request, e: Exception):
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage",
                data={
                    "chat_id": config.telegram_chat_id,
                    "text": f"Error on {request.url.path} - {e}",
                },
            )
            data = res.json()
            if not data.get('ok'):
                logger.critical(f"Was not able to send message to telegram due to {data.get('description')}")
        raise e


@app.get("/error")
async def error():
    raise ValueError("Something went wrong")


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(advert_router, prefix="/api/advert", tags=["advert"])
app.include_router(comment_router, prefix="/api", tags=["comment"])
app.include_router(complaints_router, prefix="/api", tags=["complaint"])


if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="localhost", port=5000, reload=True, log_level=logging.INFO
    )
