from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.types import intpk, str_100, create_date, update_date, dt, currency
from typing import TYPE_CHECKING, List
from sqlalchemy.ext.hybrid import hybrid_property


if TYPE_CHECKING:
    from .user import User
    from .customer import Customer
    from .lookup.bid_type import BidType
    from .lookup.contract import Contract
    from .project import Project
    from .bid_estimate import BidEstimate
    from .bid_attribute import BidAttribute


class Bid(Base):
    __tablename__ = "bid"
    id: Mapped[intpk] = mapped_column()
    bid_manager_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bid_manager: Mapped["User"] = relationship(back_populates="bids")
    approved: Mapped[bool] = mapped_column(default=False)
    lead: Mapped[str_100] = mapped_column()
    bid_type_id: Mapped[int] = mapped_column(ForeignKey("lookup.bid_type.id"))
    bid_type: Mapped["BidType"] = relationship()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="bids")
    margin: Mapped[int] = mapped_column()  # desired margin in %
    due_date: Mapped[dt] = mapped_column()
    final_amt: Mapped[currency] = mapped_column()
    contract_id: Mapped[int] = mapped_column(ForeignKey("lookup.contract.id"))
    contract_type: Mapped["Contract"] = relationship()
    project: Mapped["Project"] = relationship(back_populates="bid")
    estimated_data: Mapped["BidEstimate"] = relationship(back_populates="bid")
    attributes: Mapped[List["BidAttribute"]] = relationship()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_property
    def initial_bid_amt(self) -> currency:
        if not self.estimated_data:
            return currency(0)
        return (
            self.estimated_data.total_cost * currency((self.margin / 100) + 1)
        ).quantize(currency("1.00"))
