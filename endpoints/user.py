from schemas.user import User, UserCreate, UserUpdate
from schemas.user_role import UserRoleBulkCreate, UserRoleCreate
from sqlalchemy.orm import Session
from crud import user, user_role, role
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Body
from core import deps


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=User)
async def post_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user_exists = user.get_by_username(db, user_in.username)
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    return user.create(db, user_in)


@router.get("/", response_model=User)
async def get_user(username: str, db: Session = Depends(deps.get_db)):
    db_user = user.get_by_username(db, username)
    if db_user:
        return db_user
    raise HTTPException(status_code=400, detail="User not found")


@router.put("/", response_model=User)
async def update_user(
    user_id: int,
    username: str = Body(None),
    password: str = Body(None),
    db: Session = Depends(deps.get_db),
):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_in = UserUpdate(**jsonable_encoder(db_user))

    if username is not None:
        user_with_username = user.get_by_username(db, username)
        if user_with_username and user_with_username.id != db_user.id:
            raise HTTPException(
                status_code=400, detail="User with username already exists"
            )
        user_in.username = username

    if password is not None:
        user_in.password = password

    updated_user = user.update(db, db_user, user_in)
    return updated_user


@router.put("/roles", response_model=User)
async def manage_user_roles(
    user_id: int, user_role_in: UserRoleBulkCreate, db: Session = Depends(deps.get_db)
):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(400, "User not found")

    unique_role_ids = set(user_role_in.role_ids)
    db_roles = role.get_roles_by_ids(db, unique_role_ids)
    if len(db_roles) != len(unique_role_ids):
        raise HTTPException(400, "Invalid role id(s)")

    user_role.bulk_remove(db, user_id)
    user_role.bulk_create(
        db,
        [
            UserRoleCreate(user_id=user_id, role_id=role_id)
            for role_id in unique_role_ids
        ],
    )

    db.refresh(db_user)
    return db_user
