from db.types import dt
from schemas.base import GlobalBase
from schemas.role import Role


class UserBase(GlobalBase):
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    role_ids: list[int] = []


class UserUpdate(GlobalBase):
    password: str | None = None
    username: str | None = None


class UserFull(UserBase):
    id: int
    roles: list[Role] = []
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
