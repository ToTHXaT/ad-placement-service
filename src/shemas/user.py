from datetime import datetime
from typing import Optional

from pydantic import Field
from .base import OrmModel


class UserLogin(OrmModel):
    username: str = Field(..., max_length=128)
    password: str


class UserCreate(UserLogin):
    shown_name: str | None = Field(..., max_length=128)
    email: str | None = None
    phone: str | None = None


class UserInfo(OrmModel):
    id: int
    username: str
    registered_at: datetime
    shown_name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_admin: bool
    is_banned: bool
