from schemas.user import User, UserCreate, UserUpdate
from schemas.user_role import UserRoleBulkUpdate, UserRoleCreate
from sqlalchemy.orm import Session
from crud import user, user_role, role
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from core import deps


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=User)
async def create_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    # Check that username is unique
    user_exists = user.get_by_username(db, user_in.username)
    if user_exists:
        raise HTTPException(400, "Username already exists")

    # Check that role ids are valid
    if user_in.role_ids and len(user_in.role_ids) > 0:
        unique_role_ids = set(user_in.role_ids)
        db_roles = role.get_roles_by_ids(db, unique_role_ids)
        if len(db_roles) != len(unique_role_ids):
            raise HTTPException(400, "Invalid role id(s)")
    try:
        with db.begin_nested():
            new_user = user.create(db, user_in)
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

    db.refresh(new_user)
    return new_user


@router.get("/", response_model=User)
async def get_user(username: str, db: Session = Depends(deps.get_db)):
    db_user = user.get_by_username(db, username)
    if db_user:
        return db_user
    raise HTTPException(status_code=400, detail="User not found")


@router.put("/", response_model=User)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.username is not None:
        user_with_username = user.get_by_username(db, user_in.username)
        if user_with_username and user_with_username.id != db_user.id:
            raise HTTPException(
                status_code=400, detail="User with username already exists"
            )

    updated_user = user.update(db, db_user, user_in)
    db.commit()
    return updated_user


@router.put("/roles", response_model=User)
async def manage_user_roles(
    user_role_in: UserRoleBulkUpdate, db: Session = Depends(deps.get_db)
):
    # check that user exists
    db_user = user.get_by_id(db, user_role_in.user_id)
    if not db_user:
        raise HTTPException(400, "User not found")

    # check that role ids are valid
    unique_role_ids = set(user_role_in.role_ids)
    db_roles = role.get_roles_by_ids(db, unique_role_ids)
    if len(db_roles) != len(unique_role_ids):
        raise HTTPException(400, "Invalid role id(s)")

    try:
        with db.begin_nested():
            # delete existing role associations
            user_role.bulk_remove(db, user_role_in.user_id)

            # create role associations
            user_role.bulk_create(
                db,
                [
                    UserRoleCreate(user_id=user_role_in.user_id, role_id=role_id)
                    for role_id in unique_role_ids
                ],
            )
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

    db.refresh(db_user)
    return db_user
