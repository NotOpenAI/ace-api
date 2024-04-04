from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from schemas.base import GlobalBase
from typing import Optional


class CustomerContactBase(GlobalBase):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[PhoneNumber] = None


class CustomerContactCreate(CustomerContactBase):
    pass


class CustomerContactCreateDB(CustomerContactBase):
    customer_id: int


class CustomerContact(CustomerContactBase):
    id: int

    class Config:
        from_attributes = True
