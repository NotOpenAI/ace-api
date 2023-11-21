from pydantic import BaseModel
from db.types import dt


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleBulkUpdate(BaseModel):
    user_id: int
    role_ids: list[int]


class UserRoleCreate(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    created_at: dt
    updated_at: dt | None

    class Config:
        from_attributes = True
