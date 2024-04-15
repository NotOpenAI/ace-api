from db.types import dt, currency
from schemas.base import GlobalBase
from schemas.bid_attribute import (
    BidAttributeCreate,
    BidAttribute,
    BidAttributeBulkUpdate,
)
from schemas.user import User
from schemas.customer import Customer
from schemas.bid_status import BidStatus
from schemas.job_status import JobStatus
from typing import Optional, List


class BidBase(GlobalBase):
    name: str


class CommentBase(GlobalBase):
    text: str


class CommentCreate(CommentBase):
    bid_id: Optional[int] = None
    author_id: Optional[int] = None


class Comment(CommentBase):
    id: int
    author: User
    created_at: dt

    class Config:
        from_attributes = True


class BidCreate(BidBase):
    bid_manager_ids: List[int]
    project_manager_ids: List[int] = []
    customer_id: int
    original_contract: Optional[currency] = currency(0)
    final_cost: Optional[currency] = currency(0)
    bid_status_id: int
    job_status_id: Optional[int] = None
    lead: Optional[str] = None
    start_date: Optional[dt] = None
    new_comments: List[CommentCreate] = []
    finish_date: Optional[dt] = None
    name: Optional[str] = None
    foreman: Optional[str] = None
    attributes: List[BidAttributeCreate] = []


class BidUpdate(GlobalBase):
    name: Optional[str] = None
    lead: Optional[str] = None
    bid_manager_ids: Optional[List[int]] = None
    project_manager_ids: Optional[List[int]] = None
    foreman: Optional[str] = None
    start_date: Optional[dt] = None
    finish_date: Optional[dt] = None
    bid_status_id: Optional[int] = None
    job_status_id: Optional[int] = None
    original_contract: Optional[currency] = None
    new_comments: List[CommentCreate] = []
    final_cost: Optional[currency] = None
    attributes: Optional[BidAttributeBulkUpdate] = None


class ProjectUpdate(GlobalBase):
    project_manager_ids: Optional[List[int]] = None
    foreman: Optional[str] = None
    finish_date: Optional[dt] = None


class Bid(BidBase):
    id: int
    bid_status: BidStatus
    lead: Optional[str]
    original_contract: Optional[currency]
    final_cost: Optional[currency]
    bid_managers: List[User]
    project_managers: List[User]
    foreman: Optional[str]
    customer: Customer
    start_date: Optional[dt]
    finish_date: Optional[dt]
    desired_margin: Optional[currency]
    actual_margin: Optional[currency]
    job_status: Optional[JobStatus]
    comments: List[Comment]
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True


class BidFull(Bid):
    attributes: list[BidAttribute]

    class Config:
        from_attributes = True
