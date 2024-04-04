from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .bid import Bid


class BidManager(Base):
    __tablename__ = "bid_manager"
    manager_id: Mapped[intpk] = mapped_column(ForeignKey("user.id"))
    bid_id: Mapped[intpk] = mapped_column(ForeignKey("bid.id"))
    bid: Mapped["Bid"] = relationship(back_populates="bm_associations")
    manager: Mapped["User"] = relationship(back_populates="bid_associations")
