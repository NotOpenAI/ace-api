from db.types import dt, currency
from schemas.base import GlobalBase
from schemas.user import User
from schemas.customer import Customer
from schemas.bid_estimate import BidEstimateCreate, BidEstimate, BidEstimateUpdate
from schemas.bid import Bid


class ProjectBase(GlobalBase):
    name: str
    foreman: str


class ProjectCreate(ProjectBase):
    project_manager_id: int
    bid_id: int


class ProjectCreateDB(ProjectCreate):
    customer_id: int


class ProjectUpdate(GlobalBase):
    name: str | None = None
    foreman: str | None = None
    project_manager_id: int | None = None
    percent_completed: int | None = None
    mat_expense: currency | None = None
    labor_expense: currency | None = None
    finish_date: dt | None = None
    num_change_mgt: int | None = None
    change_mgt_revenue: currency | None = None


class ProjectFull(ProjectBase):
    id: int
    percent_completed: int
    mat_expense: currency
    labor_expense: currency
    num_change_mgt: int
    change_mgt_revenue: currency
    total_expense: currency
    est_tot_completion_cost: currency
    est_cost_diff: currency
    contract_value: currency
    margin: int
    finish_date: dt | None
    finish_date_diff: int | None
    project_manager: User
    customer: Customer
    bid: Bid
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True


class Project(ProjectBase):
    id: int
    percent_completed: int
    finish_date: dt | None
    project_manager: User
    customer: Customer
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
