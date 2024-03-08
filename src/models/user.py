import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from passlib.context import CryptContext

from .base import id_col, updated_at_col, created_at_col, Base


if TYPE_CHECKING:
    from .advert import AdvertModel
    from .complaint import ComplaintModel
    from .session import SessionModel
    from .comment import CommentModel


pwd_ctx = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


class UserModel(Base):
    """Represents user in our system"""

    __tablename__ = "User"
    __repr_cols__ = ("id", "username", "shown_name")

    id: Mapped[id_col]
    username: Mapped[str] = mapped_column(String(128), unique=True)
    hashed_pass: Mapped[str]
    email: Mapped[str | None]
    phone: Mapped[str | None]
    shown_name: Mapped[str | None] = mapped_column(String(128))
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(server_default=text("false"))
    registered_at: Mapped[created_at_col]

    adverts: Mapped[list["AdvertModel"]] = relationship(back_populates="advertiser")

    complaints: Mapped[list["ComplaintModel"]] = relationship(
        back_populates="complainant"
    )
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="user")

    sessions: Mapped[list["SessionModel"]] = relationship(back_populates="user")

    @property
    def password(self):
        return self.hashed_pass

    @password.setter
    def password(self, val):
        self.hashed_pass = pwd_ctx.hash(val)

    def verify_password(self, password: str):
        return pwd_ctx.verify(password, self.hashed_pass)
