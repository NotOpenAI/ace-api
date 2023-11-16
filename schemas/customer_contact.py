from db.types import dt
from pydantic import BaseModel
from typing import Optional


class CustomerContactBase(BaseModel):
    name: str


class CustomerContactCreate(CustomerContactBase):
    customer_id: int
    email: str | None
    phone: str | None


class CustomerContact(CustomerContactBase):
    id: int
    created_at: dt
    updated_at: dt

    class Config:
        from_attributes = True
