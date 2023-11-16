from db.types import dt
from pydantic import BaseModel
from schemas.customer_contact import CustomerContact


class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str
    owner: str
    market: str
    reputation: int
    fin_health: int


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    roles: list[CustomerContact] = []
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
