from sqlalchemy import ForeignKey
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from db.types import intpk, str_50, int_def_0, create_date, update_date, dt, currency
from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.hybrid import hybrid_property


if TYPE_CHECKING:
    from .user import User
    from .customer import Customer
    from .bid import Bid


class Project(Base):
    __tablename__ = "project"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_50] = mapped_column()
    percent_completed: Mapped[int_def_0] = mapped_column()
    project_manager_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    project_manager: Mapped["User"] = relationship()
    foreman: Mapped[str_50] = mapped_column()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="projects")
    mat_expense: Mapped[currency] = mapped_column()
    labor_expense: Mapped[currency] = mapped_column()
    num_change_mgt: Mapped[int_def_0] = mapped_column()
    change_mgt_revenue: Mapped[currency] = mapped_column()
    finish_date: Mapped[Optional[dt]] = mapped_column()
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"), unique=True)
    bid: Mapped["Bid"] = relationship(back_populates="project")
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_property
    def total_expense(self) -> currency:
        return self.labor_expense + self.mat_expense

    @hybrid_property
    def est_tot_completion_cost(self) -> currency:
        return (self.total_expense * 100 / self.bid.margin).quantize(currency("1.00"))

    @hybrid_property
    def est_cost_diff(self) -> currency:
        return self.bid.final_amt - self.est_tot_completion_cost

    @hybrid_property
    def contract_value(self) -> currency:
        return self.bid.final_amt + self.change_mgt_revenue

    @hybrid_property
    def finish_date_diff(self) -> int | None:
        if self.finish_date is None:
            return None
        return (self.finish_date - self.bid.estimated_data.end_date).days

    @hybrid_property
    def margin(self) -> int:
        return int((self.est_cost_diff / self.bid.final_amt) * 100)
