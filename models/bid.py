from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.types import intpk, str_100, create_date, update_date, dt, num_def_0
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
    bm_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bid_manager: Mapped["User"] = relationship()
    approved: Mapped[bool] = mapped_column(nullable=False, server_default="0")
    lead: Mapped[str_100] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("lookup.bid_type.id"))
    bid_type: Mapped["BidType"] = relationship()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="bids")
    margin: Mapped[int] = mapped_column()  # desired margin in %
    due_date: Mapped[dt] = mapped_column()
    final_amt: Mapped[num_def_0] = mapped_column()
    contract_id: Mapped[int] = mapped_column(ForeignKey("lookup.contract.id"))
    contract_type: Mapped["Contract"] = relationship()
    project: Mapped["Project"] = relationship(back_populates="bid")
    estimated_data: Mapped["BidEstimate"] = relationship(back_populates="bid")
    attributes: Mapped[List["BidAttribute"]] = relationship()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    # initial bid amount
    @hybrid_property
    def init_amt(self) -> num_def_0:
        return self.estimated_data.total_cost * num_def_0((self.margin / 100))
