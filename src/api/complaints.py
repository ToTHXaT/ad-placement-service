from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_admin_user, get_current_user
from src.db.db import make_session
from src.services import complaint_service
from src.shemas import ComplaintCreation, ComplaintInfo, UserInfo


router = APIRouter()


@router.post("/advert/{advert_id}/complaint/new")
async def create_complaint(
    complaint_c: ComplaintCreation,
    advert_id: int,
    user: UserInfo = Depends(get_current_user),
    conn: AsyncSession = Depends(make_session),
) -> ComplaintInfo:
    return await complaint_service.create_complaint(
        complaint_c, advert_id, user.id, conn=conn
    )


@router.get("/advert/{advert_id}/complaints")
async def get_complaints_of_the_advert(
    advert_id: int,
    page: int = 1,
    per_page: int = 10,
    user: UserInfo = Depends(get_admin_user),
    conn: AsyncSession = Depends(make_session),
) -> list[ComplaintInfo]:
    return await complaint_service.get_complaints(page, per_page, advert_id=advert_id, conn=conn)


@router.get("/complaints")
async def get_complaints(
        page: int = 1,
        per_page: int = 10,
        user: UserInfo = Depends(get_admin_user),
        conn: AsyncSession = Depends(make_session),
) -> list[ComplaintInfo]:
    return await complaint_service.get_complaints(page, per_page, conn=conn)
