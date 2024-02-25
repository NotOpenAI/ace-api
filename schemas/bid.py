from db.types import dt, currency
from schemas.base import GlobalBase
from schemas.bid_attribute import (
    BidAttributeCreate,
    BidAttribute,
    BidAttributeBulkUpdate,
)
from schemas.user import User
from schemas.customer import Customer
from schemas.bid_estimate import BidEstimateCreate, BidEstimate, BidEstimateUpdate


class BidBase(GlobalBase):
    lead: str
    margin: int
    due_date: dt


class BidCreate(BidBase):
    final_amt: currency = currency(0)
    bid_manager_id: int
    bid_type_id: int
    customer_id: int
    contract_id: int
    attributes: list[BidAttributeCreate] = []
    estimated_data: BidEstimateCreate


class BidUpdate(GlobalBase):
    approved: bool | None = None
    lead: str | None = None
    margin: int | None = None
    due_date: dt | None = None
    final_amt: currency | None = None
    contract_id: int | None = None
    attributes: BidAttributeBulkUpdate | None = None
    estimated_data: BidEstimateUpdate | None = None


class BidFull(BidBase):
    id: int
    approved: bool
    final_amt: currency
    initial_bid_amt: currency
    bid_manager: User
    customer: Customer
    estimated_data: BidEstimate
    attributes: list[BidAttribute]
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True


class Bid(BidBase):
    id: int
    approved: bool
    final_amt: currency
    initial_bid_amt: currency
    bid_manager: User
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
