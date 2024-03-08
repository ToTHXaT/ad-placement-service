from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import ComplaintModel
from src.shemas import ComplaintCreation, ComplaintInfo


async def create_complaint(complaint_c: ComplaintCreation, advert_id: int, complainant_id: int, *, conn: AsyncSession):
    async with conn.begin_nested():
        complaint = ComplaintModel(body=complaint_c.body, complainant_id=complainant_id, advert_id=advert_id)
        conn.add(complaint)
        await conn.commit()

    await conn.refresh(complaint)
    return ComplaintInfo.from_orm(complaint)


async def get_complaints(page: int, per_page: int, *, advert_id: int | None = None, conn: AsyncSession) -> list[ComplaintInfo]:
    if advert_id is not None:
        q = (select(ComplaintModel).where(ComplaintModel.advert_id == advert_id)
             .order_by(ComplaintModel.created_at.asc()).limit(per_page).offset((page - 1) * per_page))
    else:
        q = (select(ComplaintModel)
             .order_by(ComplaintModel.created_at.asc()).limit(per_page).offset((page - 1) * per_page))

    res = await conn.execute(q)

    return [ComplaintInfo.from_orm(complaint) for complaint in res.scalars()]
