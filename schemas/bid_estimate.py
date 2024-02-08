from schemas.base import GlobalBase
from db.types import dt, currency


class BidEstimateBase(GlobalBase):
    start_date: dt
    duration: int
    mat_cost: currency
    labor_cost: currency


class BidEstimateCreate(BidEstimateBase):
    pass


class BidEstimateUpdate(GlobalBase):
    start_date: dt | None = None
    duration: int | None = None
    mat_cost: currency | None = None
    labor_cost: currency | None = None
    quickbid_amt: currency | None = None


class BidEstimate(BidEstimateBase):
    id: int
    end_date: dt
    total_cost: currency
    quickbid_amt: currency | None
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
