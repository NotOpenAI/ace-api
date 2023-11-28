from sqlalchemy import ForeignKey
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, str_50
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..bid_attribute import BidAttribute
    from .bid_attribute_type import BidAttributeType


class BidAttributeOption(Base):
    __tablename__ = "bid_attribute_option"

    id: Mapped[intpk] = mapped_column()
    attribute_type_id: Mapped[int] = mapped_column(
        ForeignKey("lookup.bid_attribute_type.id")
    )
    attribute_type: Mapped["BidAttributeType"] = relationship(back_populates="options")
    active: Mapped[bool] = mapped_column(default=True)
    value: Mapped[str_50] = mapped_column()
    bid_attribute: Mapped["BidAttribute"] = relationship(back_populates="option")
    __table_args__ = {"schema": "lookup"}
