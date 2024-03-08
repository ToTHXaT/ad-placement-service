from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import ComplaintModel
from src.schemas import ComplaintCreation, ComplaintInfo, Pagination


async def create_complaint(complaint_c: ComplaintCreation, advert_id: int, complainant_id: int, *, conn: AsyncSession):
    async with conn.begin_nested():
        complaint = ComplaintModel(body=complaint_c.body, complainant_id=complainant_id, advert_id=advert_id)
        conn.add(complaint)
        await conn.flush()
        complaint_info = ComplaintInfo.from_orm(complaint)
        await conn.commit()

    return complaint_info


async def get_complaints(pagination: Pagination, *, advert_id: int | None = None, conn: AsyncSession) -> list[ComplaintInfo]:
    if advert_id is not None:
        q = (select(ComplaintModel).where(ComplaintModel.advert_id == advert_id)
             .order_by(ComplaintModel.created_at.asc()).limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page))
    else:
        q = (select(ComplaintModel)
             .order_by(ComplaintModel.created_at.asc()).limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page))

    res = await conn.execute(q)

    return [ComplaintInfo.from_orm(complaint) for complaint in res.scalars()]
