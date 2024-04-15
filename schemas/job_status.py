from schemas.base import GlobalBase


class JobStatusBase(GlobalBase):
    value: str


class JobStatusCreate(JobStatusBase):
    pass


class JobStatus(JobStatusBase):
    id: int

    class Config:
        from_attributes = True
