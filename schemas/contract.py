from schemas.base import GlobalBase


class ContractBase(GlobalBase):
    name: str


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase):
    id: int

    class Config:
        from_attributes = True
