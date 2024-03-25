from db.db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = "fake user"
    return user
