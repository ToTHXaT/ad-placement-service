import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, id_col, created_at_col, updated_at_col

if TYPE_CHECKING:
    from .user import UserModel
    from .comment import CommentModel
    from .complaint import ComplaintModel


class AdvertType(enum.StrEnum):
    purchase = "purchase"
    sell = "sell"
    service = "service"


class AdvertModel(Base):
    """Represents advert placed by user"""

    __tablename__ = "Advert"
    __repr_cols__ = ("id", "title", "type", "created_at", "advertiser_id")

    id: Mapped[id_col]
    title: Mapped[str]
    body: Mapped[str] = mapped_column(Text())
    created_at: Mapped[created_at_col]
    updated_at: Mapped[updated_at_col]
    compensation: Mapped[str | None]
    location: Mapped[str | None]
    type: Mapped[AdvertType]
    is_hidden: Mapped[bool] = mapped_column(default=False)

    advertiser_id: Mapped[int] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE")
    )
    advertiser: Mapped["UserModel"] = relationship(back_populates="adverts")

    comments: Mapped[list["CommentModel"]] = relationship(back_populates="advert")

    complaints: Mapped[list["ComplaintModel"]] = relationship(back_populates="advert")
