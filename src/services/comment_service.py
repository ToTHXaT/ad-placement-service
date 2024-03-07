from typing import Literal

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete, asc, desc
from sqlalchemy.orm import joinedload

from src.models import AdvertModel, AdvertType, CommentModel
from src.shemas import (
    AdvertCreation,
    AdvertInfo,
    UserInfo,
    Success,
    CommentInfo,
    CommentCreation,
)


async def leave_comment(
    advert_id: int, user: UserInfo, comment_c: CommentCreation, *, conn: AsyncSession
) -> CommentInfo:
    async with conn.begin_nested():
        comment = CommentModel(
            **{**comment_c.dict(), "user_id": user.id, "advert_id": advert_id}
        )
        conn.add(comment)
        await conn.commit()

    await conn.refresh(comment, ["user"])

    return CommentInfo.from_orm(comment)


async def get_comments_of_the_advert(advert_id: int, *, conn: AsyncSession) -> list[CommentInfo]:
    q = select(CommentModel).where(CommentModel.advert_id == advert_id).options(joinedload(CommentModel.user))
    res = await conn.execute(q)

    return [CommentInfo.from_orm(comment) for comment in res.scalars()]


async def delete_comment(comment_id: int, user: UserInfo, *, conn: AsyncSession) -> Success:
    q = select(CommentModel).where(CommentModel.id == comment_id)
    res = await conn.execute(q)
    comment = res.scalar_one_or_none()

    if comment is None:
        raise HTTPException(404, "Comment not found")
    if comment.user_id != user.id and not user.is_admin:
        raise HTTPException(403, "Neither owner of the comment nor admin")

    async with conn.begin_nested():
        q = delete(CommentModel).where(CommentModel.id == comment_id).returning(CommentModel.id)
        res = await conn.execute(q)
        res = res.fetchone()

        if res[0] != comment_id:
            raise HTTPException(404, "Comment was already deleted")

        await conn.commit()

    return {"success": True}