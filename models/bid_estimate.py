from sqlalchemy import ForeignKey
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, create_date, update_date, dt, currency
from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.hybrid import hybrid_property
from dateutil.relativedelta import relativedelta


if TYPE_CHECKING:
    from .bid import Bid


class BidEstimate(Base):
    __tablename__ = "bid_estimate"

    id: Mapped[intpk] = mapped_column()
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"), unique=True)
    bid: Mapped["Bid"] = relationship(back_populates="estimated_data")
    start_date: Mapped[dt] = mapped_column()
    duration: Mapped[int] = mapped_column()  # estimated # of months to complete
    mat_cost: Mapped[currency] = mapped_column()
    labor_cost: Mapped[currency] = mapped_column()
    quickbid_amt: Mapped[Optional[currency]] = mapped_column()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_property
    def end_date(self) -> dt:
        return self.start_date + relativedelta(months=self.duration)

    @hybrid_property
    def total_cost(self) -> currency:
        return self.labor_cost + self.mat_cost
