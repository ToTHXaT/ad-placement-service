from fastapi import APIRouter, Security, Depends, Request, Response, HTTPException
from fastapi.security.api_key import APIKeyCookie

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from src.schemas import Success

from src.services import session_service
from src.services import user_service

from src.schemas import UserCreate, UserInfo, UserLogin

from src.db.db import make_session

api_key_refresh = APIKeyCookie(name=config.refresh_token_cookie_name, auto_error=False)
api_key_access = APIKeyCookie(name=config.access_token_cookie_name, auto_error=False)

router = APIRouter()


def get_current_user(
    access_token: str | None = Security(api_key_access),
) -> UserInfo:
    if access_token is None:
        raise HTTPException(401, "Not authenticated")

    user_info = session_service.authenticate_by_access_token(access_token)

    if user_info.is_banned:
        raise HTTPException(403, "User is banned")

    return user_info


def get_admin_user(
        user: UserInfo = Depends(get_current_user),
) -> UserInfo:
    if not user.is_admin:
        raise HTTPException(403, "Not an admin")

    return user


def set_cookie_tokens(refresh_token: str, access_token: str, res: Response):
    res.set_cookie(
        config.access_token_cookie_name,
        access_token,
        max_age=config.access_token_duration_minutes * 60,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    res.set_cookie(
        config.refresh_token_cookie_name,
        refresh_token,
        max_age=config.refresh_token_duration_days * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/auth/refresh_tokens"
    )


@router.post("/signup", status_code=201)
async def signup(
    user_c: UserCreate, req: Request, res: Response, conn: AsyncSession = Depends(make_session)
) -> UserInfo:
    user = await user_service.signup(user_c, conn=conn)

    refresh_token, access_token = await session_service.issue_tokens(user.id, conn=conn)

    set_cookie_tokens(refresh_token, access_token, res)

    return user


@router.post("/login", status_code=200)
async def login(
    user_l: UserLogin, res: Response, conn: AsyncSession = Depends(make_session)
) -> UserInfo:
    user = await user_service.login(user_l, conn=conn)

    refresh_token, access_token = await session_service.issue_tokens(user.id, conn=conn)

    set_cookie_tokens(refresh_token, access_token, res)

    return user


@router.get("/refresh_tokens")
async def refresh_tokens(
    res: Response,
    refresh_token: str | None = Security(api_key_refresh),
    conn: AsyncSession = Depends(make_session),
) -> Success:
    refresh_token, access_token = await session_service.refresh_tokens(
        refresh_token, conn=conn
    )
    set_cookie_tokens(refresh_token, access_token, res)

    return {"success": True}


