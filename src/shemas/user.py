from datetime import datetime

from pydantic import Field
from .base import OrmModel


class UserLogin(OrmModel):
    username: str = Field(..., max_length=128)
    password: str


class UserCreate(UserLogin):
    shown_name: str | None = Field(..., max_length=128)
    email: str | None
    phone: str | None


class UserInfo(OrmModel):
    id: int
    username: str
    registered_at: datetime
    shown_name: str | None
    email: str | None
    phone: str | None
    is_admin: bool
