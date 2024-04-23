from schemas.base import GlobalBase
from schemas.bid_attribute_option import (
    BidAttributeOptionCreate,
    BidAttributeOptionFull,
    BidAttributeOptionUpdate,
)
from typing import Optional


class BidAttributeTypeBase(GlobalBase):
    name: str


class BidAttributeTypeCreate(BidAttributeTypeBase):
    options: list[BidAttributeOptionCreate] = []
    required: bool = False


class BidAttributeTypeUpdate(GlobalBase):
    update_options: Optional[list[BidAttributeOptionUpdate]] = []
    active: Optional[bool] = None
    required: Optional[bool] = None


class BidAttributeTypeFull(BidAttributeTypeBase):
    id: int
    active: bool
    required: bool
    options: list[BidAttributeOptionFull]

    class Config:
        from_attributes = True


class BidAttributeType(BidAttributeTypeBase):
    id: int

    class Config:
        from_attributes = True
