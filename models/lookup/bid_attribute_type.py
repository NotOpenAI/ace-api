from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, str_20
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .bid_attribute_option import BidAttributeOption


class BidAttributeType(Base):
    __tablename__ = "bid_attribute_type"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_20] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)
    required: Mapped[bool] = mapped_column(default=False)
    options: Mapped[List["BidAttributeOption"]] = relationship(
        back_populates="attribute_type"
    )
    __table_args__ = {"schema": "lookup"}
