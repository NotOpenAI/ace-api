from schemas.base import GlobalBase


class BidTypeBase(GlobalBase):
    name: str


class BidTypeCreate(BidTypeBase):
    pass


class BidType(BidTypeBase):
    id: int

    class Config:
        from_attributes = True
