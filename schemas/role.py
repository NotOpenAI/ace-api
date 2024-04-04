from schemas.base import GlobalBase
from typing import Optional


class RoleBase(GlobalBase):
    id: Optional[int] = None
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    class Config:
        from_attributes = True
