from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shemas import AdvertCreation, AdvertInfo, UserInfo
from src.services import advert_service
from src.services.advert_service import SortDir, SortField

from src.db.db import make_session
from src.api.auth import get_current_user

advert = APIRouter()


@advert.post("/new")
async def create_advert(
    advert_c: AdvertCreation,
    user: UserInfo = Depends(get_current_user),
    conn: AsyncSession = Depends(make_session),
):
    return await advert_service.create_advert(advert_c, user, conn=conn)


@advert.get("/get/{id}")
async def get_advert_details(
    id: int, conn: AsyncSession = Depends(make_session)
) -> AdvertInfo:
    return await advert_service.get_advert(id, conn=conn)


@advert.get("/all", response_model=list[AdvertInfo])
async def some(
    sort_dir: SortDir, sort_by: SortField, conn: AsyncSession = Depends(make_session),
        page: int = 1, per_page: int = 10
) -> list[AdvertInfo]:
    return await advert_service.list_adverts(
        sort_by=sort_by, sort_dir=sort_dir, conn=conn, page=page, per_page=per_page
    )
