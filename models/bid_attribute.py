from sqlalchemy import ForeignKey, CheckConstraint
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, create_date, update_date, currency
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .lookup.bid_attribute_type import BidAttributeType
    from .lookup.bid_attribute_option import BidAttributeOption


class BidAttribute(Base):
    __tablename__ = "bid_attribute"
    __table_args__ = (
        CheckConstraint(
            "(num_val IS NULL AND option_id IS NOT NULL) OR (num_val IS NOT NULL AND option_id IS NULL)",
            name="only_one_required",
        ),
    )
    bid_id: Mapped[intpk] = mapped_column(ForeignKey("bid.id"))
    type_id: Mapped[intpk] = mapped_column(ForeignKey("lookup.bid_attribute_type.id"))
    type: Mapped["BidAttributeType"] = relationship()
    num_val: Mapped[Optional[currency]] = mapped_column()
    option_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lookup.bid_attribute_option.id")
    )
    option: Mapped["BidAttributeOption"] = relationship(back_populates="bid_attribute")
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
