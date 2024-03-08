from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import comment_service
from src.shemas import CommentCreation, CommentInfo, UserInfo, Success

from src.api.auth import get_current_user
from src.db.db import make_session

router = APIRouter()


@router.post("/advert/{advert_id}/comment/new")
async def leave_a_comment(advert_id: int, comment_c: CommentCreation, user: UserInfo = Depends(get_current_user),
                        conn: AsyncSession = Depends(make_session)) -> CommentInfo:
    return await comment_service.leave_comment(advert_id, user, comment_c, conn=conn)


@router.get("/advert/{advert_id}/comments")
async def get_comments_of_the_advert(advert_id: int, conn: AsyncSession = Depends(make_session)) -> list[CommentInfo]:
    return await comment_service.get_comments_of_the_advert(advert_id=advert_id, conn=conn)


@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, user: UserInfo = Depends(get_current_user), conn: AsyncSession = Depends(make_session)) -> Success:
    return await comment_service.delete_comment(comment_id, user, conn=conn)
