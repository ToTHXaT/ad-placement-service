from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import UserModel


class SessionModel(Base):
    """Represents a user logged into the system"""

    __tablename__ = "Session"
    __repr_cols__ = ("token", "user_id")

    token: Mapped[str] = mapped_column(primary_key=True)
    expires: Mapped[datetime]

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))
    user: Mapped['UserModel'] = relationship(back_populates="sessions")
