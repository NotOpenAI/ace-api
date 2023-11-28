from schemas.base import GlobalBase
from db.types import dt
from schemas.bid_attribute_type import BidAttributeType
from schemas.bid_attribute_option import BidAttributeOption


class BidAttributeBase(GlobalBase):
    num_val: int | None = None


class BidAttributeCreate(BidAttributeBase):
    option_id: int | None = None
    type_id: int


class BidAttributeCreateDB(BidAttributeCreate):
    bid_id: int


class BidAttributeUpdate(BidAttributeBase):
    type_id: int
    option_id: int | None = None


class BidAttributeBulkUpdate(GlobalBase):
    updated_attributes: list[BidAttributeUpdate] | None = None
    deleted_attributes: set[int] | None = None


class BidAttribute(BidAttributeBase):
    id: int
    type: BidAttributeType
    option: BidAttributeOption | None
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
