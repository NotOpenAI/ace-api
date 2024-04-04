from schemas.base import GlobalBase
from db.types import dt
from typing import Optional


class UserRoleBase(GlobalBase):
    user_id: int
    role_id: int


class UserRoleBulkUpdate(GlobalBase):
    role_ids: list[int]


class UserRoleCreate(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    created_at: dt
    updated_at: Optional[dt]

    class Config:
        from_attributes = True
