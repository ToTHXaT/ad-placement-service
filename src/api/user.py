from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import user_service
from src.api.auth import get_current_user, get_admin_user
from src.schemas import UserInfo
from src.db.db import make_session


router = APIRouter()


@router.post("/{user_id}/grant-admin")
async def grant_admin(user_id: int, grantor: UserInfo = Depends(get_current_user), conn: AsyncSession = Depends(make_session)) -> UserInfo:
    return await user_service.grant_admin(grantor, user_id, conn=conn)


@router.post("/{user_id/ban")
async def ban_user(user_id: int, _admin: UserInfo = Depends(get_admin_user), conn: AsyncSession = Depends(make_session)) -> UserInfo:
    return await user_service.ban_user(user_id, conn=conn)


@router.post("/{user_id}/unban")
async def ban_user(user_id: int, _admin: UserInfo = Depends(get_admin_user), conn: AsyncSession = Depends(make_session)) -> UserInfo:
    return await user_service.unban_user(user_id, conn=conn)
