from db.types import dt
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic_extra_types.phone_numbers import PhoneNumber


class CustomerContactBase(BaseModel):
    name: str
    email: EmailStr | None
    phone: PhoneNumber | None


class CustomerContactCreate(CustomerContactBase):
    pass


class CustomerContactCreateDB(CustomerContactBase):
    customer_id: int


class CustomerContact(CustomerContactBase):
    id: int
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
