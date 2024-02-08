from schemas.base import GlobalBase
from db.types import dt


class UserRoleBase(GlobalBase):
    user_id: int
    role_id: int


class UserRoleBulkUpdate(GlobalBase):
    role_ids: list[int]


class UserRoleCreate(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
