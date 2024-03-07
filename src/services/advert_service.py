from typing import Literal

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, asc, desc
from sqlalchemy.orm import joinedload

from src.models import AdvertModel, AdvertType
from src.shemas import AdvertCreation, AdvertInfo, UserInfo


async def create_advert(
    advert_c: AdvertCreation, user: UserInfo, conn: AsyncSession
) -> AdvertInfo:
    async with conn.begin_nested():
        advert = AdvertModel(**{**advert_c.dict(), "advertiser_id": user.id})
        conn.add(advert)
        await conn.commit()

    await conn.refresh(advert, ["advertiser"])
    return AdvertInfo.from_orm(advert)


async def get_advert(advert_id: int, conn: AsyncSession) -> AdvertInfo:
    q = (
        select(AdvertModel)
        .where(AdvertModel.id == advert_id)
        .options(joinedload(AdvertModel.advertiser))
    )
    res = await conn.execute(q)
    advert = res.scalar_one_or_none()
    if advert is None:
        raise HTTPException(404, "Advert with this id not found")

    return AdvertInfo.from_orm(advert)


SortField = Literal[
    "created_at",
    "updated_at",
    "id",
    "title",
    "body",
]
SortDir = Literal["asc", "desc"]
FilterField = Literal[""]


async def list_adverts(
    conn: AsyncSession, page: int, per_page: int, sort_by: SortField = "created_at", sort_dir: SortDir = "desc"
) -> list[AdvertInfo]:
    match sort_dir:
        case "asc":
            sort_func = asc
        case "desc":
            sort_func = desc

    q = (
        select(AdvertModel)
        .options(joinedload(AdvertModel.advertiser))
        .order_by(sort_func(AdvertModel.__table__.c[sort_by]))
        .limit(per_page)
        .offset((page - 1) * per_page)
    )

    res = await conn.execute(q)

    return [AdvertInfo.from_orm(adv) for adv in res.scalars()]


