from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, id_col, created_at_col, updated_at_col

if TYPE_CHECKING:
    from .advert import AdvertModel
    from .user import UserModel


class CommentModel(Base):
    """Represents comments left by users under adverts"""

    __tablename__ = "Comment"
    __repr_cols__ = ("id", "body", "created_at", "advert_id")

    id: Mapped[id_col]
    created_at: Mapped[created_at_col]
    body: Mapped[str] = mapped_column(Text())

    advert_id: Mapped[int] = mapped_column(ForeignKey("Advert.id", ondelete="CASCADE"))
    advert: Mapped["AdvertModel"] = relationship(back_populates="comments")

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL")
    )
    user: Mapped["UserModel"] = relationship(back_populates="comments")
