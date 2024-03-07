from typing import Annotated
from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class for our models"""

    __repr_cols__ = tuple("id")

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            if col in self.__repr_cols__:
                val = getattr(self, col)
                if isinstance(val, str) and len(val) > 20:
                    val = val[:20] + "..." + val[-1]
                cols.append(f"{col}={val}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


id_col = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at_col = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('utc', NOW())")
    ),
]
updated_at_col = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=datetime.utcnow,
    ),
]
