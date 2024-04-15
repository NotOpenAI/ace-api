from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.types import *
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User
    from .bid import Bid


class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[intpk] = mapped_column()
    text: Mapped[str_255] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"))
    bid: Mapped["Bid"] = relationship(back_populates="comments")
    created_at: Mapped[create_date] = mapped_column()
