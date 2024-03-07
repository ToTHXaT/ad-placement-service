from fastapi import APIRouter, Security, Depends, Request, Response
from fastapi.security.api_key import APIKeyCookie

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config

from src.services import session_service
from src.services import user_service

from src.shemas import UserCreate, UserInfo

from src.db.db import make_session

api_key_refresh = APIKeyCookie(name=config.refresh_token_cookie_name, auto_error=False)
api_key_access = APIKeyCookie(name=config.access_token_cookie_name, auto_error=False)

auth = APIRouter()


@auth.post("/signup", response_model=UserInfo, status_code=201)
async def signup(
    user_c: UserCreate, res: Response, conn: AsyncSession = Depends(make_session)
) -> UserInfo:
    user = await user_service.signup(user_c, conn=conn)

    refresh_token, access_token = await session_service.issue_tokens(user.id, conn=conn)

    res.set_cookie(config.access_token_cookie_name, access_token)
    res.set_cookie(config.refresh_token_cookie_name, refresh_token)

    return user
