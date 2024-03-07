from datetime import datetime

from .base import OrmModel
from .user import UserInfo


class CommentCreation(OrmModel):
    body: str


class CommentInfo(OrmModel):
    id: int
    body: str
    created_at: datetime
    user: UserInfo
