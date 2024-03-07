from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at_col, id_col

if TYPE_CHECKING:
    from .advert import AdvertModel
    from .user import UserModel


class ComplaintModel(Base):
    """Represents a complaint left by a user on an advert"""

    __tablename__ = "Complaint"
    __repr_cols__ = ("id", "body", "created_at", "complainant_id", "advert_id")

    id: Mapped[id_col]
    body: Mapped[str] = mapped_column(Text())
    created_at: Mapped[created_at_col]

    complainant_id: Mapped[int | None] = mapped_column(
        ForeignKey("User.id", ondelete="SET NULL")
    )
    complainant: Mapped["UserModel"] = relationship(back_populates="complaints")

    advert_id: Mapped[int] = mapped_column(ForeignKey("Advert.id", ondelete="CASCADE"))
    advert: Mapped["AdvertModel"] = relationship(back_populates="complaints")
