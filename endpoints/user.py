from schemas.user import User, UserFull, UserCreate, UserUpdate
from schemas.user_role import UserRoleBulkUpdate, UserRoleCreate
from sqlalchemy.orm import Session
from crud import user, user_role, role
from fastapi import APIRouter, Depends, HTTPException
from core import deps
from schemas.base import SuccessResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=SuccessResponse[UserFull])
async def create_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    # Check that username is unique
    user_exists = user.get_by_username(db, user_in.username)
    if user_exists:
        raise HTTPException(400, "Username already exists")

    # Check that role ids are valid
    if len(user_in.role_ids):
        unique_role_ids = set(user_in.role_ids)
        db_roles = role.get_roles_by_ids(db, unique_role_ids)
        if len(db_roles) != len(unique_role_ids):
            raise HTTPException(400, "Invalid role id(s)")
    try:
        with db.begin_nested():
            new_user = user.create(db, user_in)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, str(e))

    db.refresh(new_user)
    return SuccessResponse(data=new_user)


@router.get("/{username}", response_model=SuccessResponse[UserFull])
async def get_user(username: str, db: Session = Depends(deps.get_db)):
    db_user = user.get_by_username(db, username)
    if db_user:
        return SuccessResponse(data=db_user)
    raise HTTPException(404, "User not found")


@router.get("", response_model=SuccessResponse[list[User]])
async def get_users(db: Session = Depends(deps.get_db)):
    return SuccessResponse(data=user.get_all(db))


@router.put("/{user_id}", response_model=SuccessResponse[UserFull])
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")

    if user_in.username is not None:
        user_with_username = user.get_by_username(db, user_in.username)
        if user_with_username and user_with_username.id != db_user.id:
            raise HTTPException(400, "User with username already exists")

    updated_user = user.update(db, db_user, user_in)
    db.commit()
    db.refresh(updated_user)
    return SuccessResponse(data=updated_user)


@router.put("/{user_id}/roles", response_model=SuccessResponse[UserFull])
async def manage_user_roles(
    user_id: int, user_roles: UserRoleBulkUpdate, db: Session = Depends(deps.get_db)
):
    # Check that user exists
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(400, "User not found")

    # Check that role ids are valid
    unique_role_ids = set(user_roles.role_ids)
    db_roles = role.get_roles_by_ids(db, unique_role_ids)
    if len(db_roles) != len(unique_role_ids):
        raise HTTPException(400, "Invalid role id(s)")

    try:
        with db.begin_nested():
            user_role.bulk_remove(db, user_id)
            user_role.bulk_create(
                db,
                [
                    UserRoleCreate(user_id=user_id, role_id=role_id)
                    for role_id in unique_role_ids
                ],
            )
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, "Internal Server Error")

    db.refresh(db_user)
    return SuccessResponse(data=db_user)
