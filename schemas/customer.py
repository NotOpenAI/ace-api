from db.types import dt
from schemas.base import GlobalBase
from pydantic_extra_types.phone_numbers import PhoneNumber
from schemas.customer_contact import (
    CustomerContactCreate,
    CustomerContact,
)


class CustomerBase(GlobalBase):
    name: str
    phone: PhoneNumber
    address: str
    owner: str
    market: str
    reputation: int
    fin_health: int


class CustomerCreate(CustomerBase):
    contacts: list[CustomerContactCreate] = []


class CustomerUpdate(GlobalBase):
    name: str | None = None
    phone: PhoneNumber | None = None
    address: str | None = None
    owner: str | None = None
    market: str | None = None
    reputation: int | None = None
    fin_health: int | None = None
    contacts: list[CustomerContactCreate] | None = None


class CustomerGet(GlobalBase):
    id: int | None = None


class CustomerFull(CustomerBase):
    id: int
    contacts: list[CustomerContact] = []
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True


class Customer(CustomerBase):
    id: int
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
