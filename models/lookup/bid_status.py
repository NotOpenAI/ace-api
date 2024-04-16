from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, str_50
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..bid import Bid


class BidStatus(Base):
    __tablename__ = "bid_status"

    id: Mapped[intpk] = mapped_column()
    value: Mapped[str_50] = mapped_column(unique=True)
    bid: Mapped["Bid"] = relationship(back_populates="bid_status")

    __table_args__ = {"schema": "lookup"}
