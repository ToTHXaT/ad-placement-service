from typing import Literal

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete, asc, desc
from sqlalchemy.orm import joinedload

from src.models import AdvertModel, AdvertType
from src.schemas import AdvertCreation, AdvertInfo, UserInfo, Success


async def create_advert(
    advert_c: AdvertCreation, user: UserInfo, *, conn: AsyncSession
) -> AdvertInfo:
    async with conn.begin_nested():
        advert = AdvertModel(**{**advert_c.dict(), "advertiser_id": user.id})
        conn.add(advert)
        await conn.commit()

    await conn.refresh(advert, ["advertiser"])
    return AdvertInfo.from_orm(advert)


async def get_advert(advert_id: int, *, conn: AsyncSession) -> AdvertInfo:
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


# class Filter(BaseModel)


async def list_adverts(
    page: int,
    per_page: int,
    sort_by: SortField = "created_at",
    sort_dir: SortDir = "desc",
    *,
    conn: AsyncSession,
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


async def delete_advert(
    advert_id: int, user: UserInfo, *, conn: AsyncSession
) -> Success:
    q = select(AdvertModel.advertiser_id).where(AdvertModel.id == advert_id)
    res = await conn.execute(q)
    advert = res.one_or_none()

    if advert is None:
        raise HTTPException(404, "Advert not found")
    if advert[0] != user.id:
        raise HTTPException(403, "Not the advert owner")

    async with conn.begin_nested():
        q = delete(AdvertModel).where(AdvertModel.id == advert_id)
        await conn.execute(q)
        await conn.commit()

    return {"success": True}


async def change_advert_type(advert_id: int, user: UserInfo, new_type: AdvertType, *, conn: AsyncSession) -> AdvertInfo:
    q = select(AdvertModel).where(AdvertModel.id == advert_id).options(joinedload(AdvertModel.advertiser))
    res = await conn.execute(q)
    advert = res.scalar_one_or_none()

    if advert is None:
        raise HTTPException(404, "Advert not found")
    if advert.advertiser_id != user.id and not user.is_admin:
        raise HTTPException(403, "Neither owner nor admin")
    if advert.type == new_type:
        raise HTTPException(400, "Advert already has this type")

    async with conn.begin_nested():
        advert.type = new_type
        conn.add(advert)
        advert_info = AdvertInfo.from_orm(advert)
        await conn.commit()

    return advert_info
