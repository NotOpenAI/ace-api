from db.types import dt, currency
from schemas.base import GlobalBase
from schemas.bid_attribute import (
    BidAttributeCreate,
    BidAttribute,
    BidAttributeBulkUpdate,
)
from schemas.user import User
from schemas.customer import Customer
from typing import Optional, List


class BidBase(GlobalBase):
    name: str


class BidCreate(BidBase):
    bid_manager_ids: List[int]
    customer_id: int
    original_contract: Optional[currency] = currency(0)
    original_cost: Optional[currency] = currency(0)
    lead: Optional[str] = None
    attributes: List[BidAttributeCreate] = []


class BidCreateTest(BidCreate):
    project_manager_ids: Optional[List[int]] = None
    start_date: Optional[dt] = None
    finish_date: Optional[dt] = None
    name: Optional[str] = None


class BidUpdate(GlobalBase):
    name: Optional[str] = None
    lead: Optional[str] = None
    bid_manager_ids: Optional[List[int]] = None
    project_manager_ids: Optional[List[int]] = None
    foreman: Optional[str] = None
    start_date: Optional[dt] = None
    original_contract: Optional[currency] = None
    original_cost: Optional[currency] = None
    attributes: Optional[BidAttributeBulkUpdate] = None


class ProjectUpdate(GlobalBase):
    project_manager_ids: Optional[List[int]] = None
    foreman: Optional[str] = None
    finish_date: Optional[dt] = None


class BidFull(BidBase):
    id: int
    bid_managers: List[User]
    project_managers: List[User]
    original_contract: Optional[currency]
    original_cost: Optional[currency]
    lead: Optional[str]
    foreman: Optional[str]
    customer: Customer
    start_date: Optional[dt]
    finish_date: Optional[dt]
    attributes: list[BidAttribute]
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True


class Bid(BidBase):
    id: int
    lead: Optional[str]
    original_contract: Optional[currency]
    original_cost: Optional[currency]
    bid_managers: List[User]
    project_managers: List[User]
    foreman: Optional[str]
    customer: Customer
    start_date: Optional[dt]
    finish_date: Optional[dt]
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
