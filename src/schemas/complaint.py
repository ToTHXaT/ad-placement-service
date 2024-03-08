from datetime import datetime

from pydantic import BaseModel

from .base import OrmModel


class ComplaintCreation(OrmModel):
    body: str


class ComplaintInfo(ComplaintCreation):
    id: int
    created_at: datetime
    complainant_id: int
    advert_id: int
