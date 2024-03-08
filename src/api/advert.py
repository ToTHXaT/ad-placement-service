from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import AdvertCreation, AdvertInfo, UserInfo, UpdateAdvertType, Success
from src.schemas.advert import AdvertFiltration, AdvertSorting
from src.schemas.base import Pagination
from src.services import advert_service

from src.db.db import make_session
from src.api.auth import get_current_user

router = APIRouter()


@router.post("/new")
async def create_advert(
    advert_c: AdvertCreation,
    user: UserInfo = Depends(get_current_user),
    conn: AsyncSession = Depends(make_session),
):
    return await advert_service.create_advert(advert_c, user, conn=conn)


@router.get("/all", response_model=list[AdvertInfo])
async def list_all_adverts(
    conn: AsyncSession = Depends(make_session),
    advert_sorting: AdvertSorting = Depends(),
    pagination: Pagination = Depends(),
    advert_filtration: AdvertFiltration = Depends(),
) -> list[AdvertInfo]:
    return await advert_service.list_adverts(
        advert_filtration=advert_filtration,
        advert_sorting=advert_sorting,
        pagination=pagination,
        conn=conn
    )


@router.get("/{advert_id}")
async def get_advert_details(
    advert_id: int, conn: AsyncSession = Depends(make_session)
) -> AdvertInfo:
    return await advert_service.get_advert(advert_id, conn=conn)


@router.delete("/{advert_id}")
async def delete_advert(
    advert_id: int,
    user: UserInfo = Depends(get_current_user),
    conn: AsyncSession = Depends(make_session),
) -> Success:
    return await advert_service.delete_advert(advert_id, user, conn=conn)


@router.patch("/{advert_id}")
async def update_advert_type(
    advert_id: int,
    advert: UpdateAdvertType,
    user: UserInfo = Depends(get_current_user),
    conn: AsyncSession = Depends(make_session),
) -> AdvertInfo:
    return await advert_service.change_advert_type(advert_id, user, advert.new_type, conn=conn)

