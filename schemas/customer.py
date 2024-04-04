from db.types import dt
from schemas.base import GlobalBase
from pydantic_extra_types.phone_numbers import PhoneNumber
from schemas.customer_contact import (
    CustomerContactCreate,
    CustomerContact,
)
from typing import Optional


class CustomerBase(GlobalBase):
    name: str
    owner: Optional[str]
    market: Optional[str]
    reputation: Optional[int]
    fin_health: Optional[int]


class CustomerCreate(GlobalBase):
    name: str
    owner: Optional[str] = None
    market: Optional[str] = None
    reputation: Optional[int] = None
    fin_health: Optional[int] = None
    contacts: list[CustomerContactCreate] = []


class CustomerUpdate(GlobalBase):
    name: Optional[str] = None
    phone: Optional[PhoneNumber] = None
    owner: Optional[str] = None
    market: Optional[str] = None
    reputation: Optional[int] = None
    fin_health: Optional[int] = None
    contacts: Optional[list[CustomerContactCreate]] = None


class CustomerGet(GlobalBase):
    id: Optional[int] = None


class CustomerFull(CustomerBase):
    id: int
    contacts: list[CustomerContact] = []
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True


class Customer(CustomerBase):
    id: int
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
