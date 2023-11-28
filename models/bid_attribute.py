from sqlalchemy import ForeignKey, CheckConstraint
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, create_date, update_date
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .lookup.attribute import Attribute


class BidAttribute(Base):
    __tablename__ = "bid_attribute"
    __table_args__ = (
        CheckConstraint(
            "(num_val is null AND attribute_option_id is not null) or (num_val is not null AND attribute_option_id is null)",
            name="one_required",
        ),
    )
    id: Mapped[intpk] = mapped_column()
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"))
    attribute_id: Mapped[int] = mapped_column(ForeignKey("lookup.attribute.id"))
    attribute: Mapped["Attribute"] = relationship()
    num_val: Mapped[Optional[int]] = mapped_column()
    attribute_option_id: Mapped[Optional[int]] = mapped_column()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
