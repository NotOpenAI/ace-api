from schemas.base import GlobalBase


class BidAttributeOptionBase(GlobalBase):
    value: str


class BidAttributeOptionCreate(BidAttributeOptionBase):
    pass


class BidAttributeOptionCreateDB(BidAttributeOptionCreate):
    attribute_type_id: int


class BidAttributeOptionUpdate(BidAttributeOptionBase):
    id: int | None = None
    active: bool = True


class BidAttributeOptionBulkUpdate(GlobalBase):
    update_options: list[BidAttributeOptionUpdate] | None = None
    delete_options: set[int] | None = None


class BidAttributeOption(BidAttributeOptionBase):
    id: int

    class Config:
        from_attributes = True


class BidAttributeOptionFull(BidAttributeOptionBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
