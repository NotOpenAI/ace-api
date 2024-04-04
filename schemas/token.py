from schemas.base import GlobalBase
from typing import Optional


class Token(GlobalBase):
    access_token: str
    token_type: str


class TokenData(GlobalBase):
    username: Optional[str] = None
