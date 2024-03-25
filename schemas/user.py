from db.types import dt
from schemas.base import GlobalBase
from schemas.role import Role
from typing import Optional


class UserBase(GlobalBase):
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    role_ids: list[int] = []


class UserUpdate(GlobalBase):
    password: Optional[str] = None
    username: Optional[str] = None


class User(UserBase):
    id: int
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True


class UserFull(UserBase):
    id: int
    roles: list[Role] = []
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
