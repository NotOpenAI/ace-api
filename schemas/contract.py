from pydantic import BaseModel


class ContractBase(BaseModel):
    name: str


class ContractCreate(ContractBase):
    pass


class Contract(ContractBase):
    id: int

    class Config:
        from_attributes = True
