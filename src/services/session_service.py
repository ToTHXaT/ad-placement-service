import uuid
from datetime import datetime, timedelta

import jwt

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload

from src.shemas import UserCreate, UserInfo, UserLogin
from src.models import UserModel, SessionModel

from src.config import config


def generate_refresh_token() -> str:
    return uuid.uuid4().hex


def authenticate_by_access_token(access_token: str) -> UserInfo:
    try:
        data = jwt.decode(
            access_token, config.jwt_secret, algorithms=[config.jwt_algorithm]
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, "Access token expired. Please login again.")

    return UserInfo(**data["user"])


async def refresh_tokens(refresh_token: str, *, conn: AsyncSession) -> tuple[str, str]:
    q = (
        select(SessionModel)
        .where(SessionModel.token == refresh_token)
        .options(joinedload(SessionModel.user))
    )
    data = await conn.execute(q)

    if not (session := data.scalar_one_or_none()):
        raise HTTPException(401, "Refresh token is invalid")
    if session.expires < datetime.utcnow():
        raise HTTPException(401, "Refresh token expired")

    user_info = UserInfo.from_orm(session.user).dict()
    user_info["registered_at"] = user_info["registered_at"].isoformat()

    async with conn.begin_nested():
        user_id = session.user_id
        await conn.delete(session)
        session = SessionModel(
            user_id=user_id,
            token=generate_refresh_token(),
            expires=datetime.utcnow()
            + timedelta(days=config.access_token_duration_minutes),
        )
        conn.add(session)
        refresh_token = session.token
        await conn.commit()

    access_token = jwt.encode(
        {
            "user": user_info,
            "exp": datetime.utcnow()
            + timedelta(minutes=config.access_token_duration_minutes),
        },
        config.jwt_secret,
        algorithm=config.jwt_algorithm,
    )

    return refresh_token, access_token


async def issue_tokens(user_id: int, *, conn: AsyncSession) -> tuple[str, str]:
    async with conn.begin_nested():
        session = SessionModel(
            user_id=user_id,
            token=generate_refresh_token(),
            expires=datetime.utcnow()
            + timedelta(days=config.access_token_duration_minutes),
        )
        conn.add(session)
        await conn.commit()
    await conn.refresh(session, ["user"])
    refresh_token = session.token

    user_info = UserInfo.from_orm(session.user).dict()
    user_info["registered_at"] = user_info["registered_at"].isoformat()

    access_token = jwt.encode(
        {
            "user": user_info,
            "exp": datetime.utcnow()
            + timedelta(minutes=config.access_token_duration_minutes),
        },
        config.jwt_secret,
        algorithm=config.jwt_algorithm,
    )

    return refresh_token, access_token
