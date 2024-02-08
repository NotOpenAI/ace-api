from schemas.base import GlobalBase


class RoleBase(GlobalBase):
    id: int | None = None
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    class Config:
        from_attributes = True
