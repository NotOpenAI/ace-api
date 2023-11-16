from db.types import dt
from pydantic import BaseModel
from schemas.role import Role
from typing import Optional


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    roles: list[Role] = []
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
