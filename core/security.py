from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Annotated, Optional
from schemas.token import TokenData
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from crud import user
from core import deps
import os

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
router = APIRouter(prefix="")

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict, expires_delta: Optional[int] = int(ACCESS_TOKEN_EXPIRE_MINUTES)
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(deps.oauth2_scheme)],
    db: Session = Depends(deps.get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    valid_user = user.get_by_username(db, username=token_data.username)
    if valid_user is None:
        raise credentials_exception
    return valid_user


def authenticate_user(username: str, password: str, db: Session = Depends(deps.get_db)):
    valid_user = user.get_by_username(db, username)
    if not valid_user:
        return False
    if not verify_password(password, valid_user.hashed_password):
        return False
    return valid_user
