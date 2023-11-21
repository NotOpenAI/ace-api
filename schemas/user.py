from db.types import dt
from pydantic import BaseModel
from schemas.role import Role


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    role_ids: list[int] = []


class UserUpdate(BaseModel):
    password: str | None = None
    username: str | None = None


class User(UserBase):
    id: int
    roles: list[Role] = []
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
