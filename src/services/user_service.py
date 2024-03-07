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
            is_admin=False
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
