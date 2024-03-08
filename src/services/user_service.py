from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from fastapi import HTTPException

from src.shemas import UserCreate, UserInfo, UserLogin
from src.models import UserModel


async def signup(user_c: UserCreate, *, conn: AsyncSession) -> UserInfo:
    async with conn.begin():
        user = UserModel(
            username=user_c.username,
            password=user_c.password,
            email=user_c.email,
            phone=user_c.phone,
            shown_name=user_c.shown_name,
            is_admin=False,
        )
        conn.add(user)
        await conn.commit()
    await conn.refresh(user)

    return UserInfo.from_orm(user)


async def login(user_l: UserLogin, *, conn: AsyncSession) -> UserInfo:
    q = select(UserModel).where(UserModel.username == user_l.username)
    res = await conn.execute(q)

    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(401, f"User with {user_l.username=} does not exists")

    if not user.verify_password(user_l.password):
        raise HTTPException(401, f"Invalid credentials for login")

    return UserInfo.from_orm(user)


async def grant_admin(grantor: UserInfo, grantee_id: int, *, conn: AsyncSession) -> UserInfo:
    if not grantor.is_admin:
        raise HTTPException(403, "Grantor is not admin")

    q = select(UserModel).where(UserModel.id == grantee_id)
    res = await conn.execute(q)
    grantee = res.scalar_one_or_none()

    if grantee is None:
        raise HTTPException(404, "User not found")
    if grantee.is_admin:
        raise HTTPException(400, "User is already admin")

    async with conn.begin_nested():
        grantee.is_admin = True
        conn.add(grantee)
        await conn.commit()
    await conn.refresh(grantee)

    return UserInfo.from_orm(grantee)


async def ban_user(user_id, *, conn: AsyncSession) -> UserInfo:
    q = select(UserModel).where(UserModel.id == user_id)
    res = await conn.execute(q)
    user = res.scalar_one_or_none()

    if user is None:
        raise HTTPException(404, "User not found")
    if user.is_banned:
        raise HTTPException(400, "User is already banned")

    async with conn.begin_nested():
        user.is_banned = True
        conn.add(user)
        user_info = UserInfo.from_orm(user)
        await conn.commit()

    return user_info


async def unban_user(user_id, *, conn: AsyncSession) -> UserInfo:
    q = select(UserModel).where(UserModel.id == user_id)
    res = await conn.execute(q)
    user = res.scalar_one_or_none()

    if user is None:
        raise HTTPException(404, "User not found")
    if not user.is_banned:
        raise HTTPException(400, "User is not banned")

    async with conn.begin_nested():
        user.is_banned = False
        conn.add(user)
        user_info = UserInfo.from_orm(user)
        await conn.commit()

    return user_info
