from datetime import datetime, date
from .base import OrmModel

from fastapi import Depends, Query
from pydantic import BaseModel

from src.models import AdvertType
from src.schemas import UserInfo


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


class UpdateAdvertType(OrmModel):
    new_type: AdvertType


class AdvertFiltration(BaseModel):
    title_includes: str | None = None
    body_includes: str | None = None
    type: AdvertType | None = None
    since: datetime | None = None
    before: datetime | None = None
    advertiser__id: int | None = None
