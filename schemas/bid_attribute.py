from schemas.base import GlobalBase
from db.types import dt, currency
from schemas.bid_attribute_type import BidAttributeType
from schemas.bid_attribute_option import BidAttributeOption
from typing import Optional, List, Set


class BidAttributeBase(GlobalBase):
    num_val: Optional[currency] = None


class BidAttributeCreate(BidAttributeBase):
    option_id: Optional[int] = None
    type_id: int


class BidAttributeCreateDB(BidAttributeCreate):
    bid_id: int


class BidAttributeUpdate(BidAttributeBase):
    type_id: int
    option_id: Optional[int] = None


class BidAttributeBulkUpdate(GlobalBase):
    updated_attributes: Optional[List[BidAttributeUpdate]] = None
    deleted_attributes: Optional[Set[int]] = None


class BidAttribute(BidAttributeBase):
    type: BidAttributeType
    option: Optional[BidAttributeOption]
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
