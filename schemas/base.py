from pydantic import BaseModel, ConfigDict
from typing import Optional, TypeVar, Generic

DataT = TypeVar("DataT")


class GlobalBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class BaseResponse(GlobalBase, Generic[DataT]):
    status: str
    data: Optional[DataT] = None


class SuccessResponse(BaseResponse, Generic[DataT]):
    status: str = "OK"
    data: Optional[DataT] = None
