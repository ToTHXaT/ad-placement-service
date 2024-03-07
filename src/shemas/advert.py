from datetime import datetime
from .base import OrmModel

from src.models import AdvertType
from src.shemas import UserInfo


class AdvertCreation(OrmModel):
    title: str
    body: str
    compensation: str | None = None
    location: str | None = None
    type: AdvertType


class AdvertInfo(AdvertCreation):
    id: int
    created_at: datetime
    updated_at: datetime
    advertiser: UserInfo
