from schemas.user import User, UserCreate, UserUpdate, UserFull
from schemas.user_role import UserRoleBulkUpdate, UserRoleCreate
from sqlalchemy.orm import Session
from crud import user, user_role, role
from fastapi import APIRouter, Depends, HTTPException
from core import deps, security
from schemas.base import SuccessResponse
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from models.user import User


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=SuccessResponse[UserFull])
async def create_user(
    user_in: UserCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins can create new users")
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


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(deps.get_db),
) -> Token:
    valid_user = security.authenticate_user(form_data.username, form_data.password, db)
    if not valid_user:
        raise security.credentials_exception
    access_token = security.create_access_token(data={"sub": valid_user.username})

    return Token(access_token=access_token, token_type="bearer")


@router.get("/{id}", response_model=SuccessResponse[UserFull])
async def get_user(
    id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    db_user = user.get_by_id(db, id)
    if db_user:
        return SuccessResponse(data=db_user)
    raise HTTPException(404, "User not found")


@router.get("", response_model=SuccessResponse[list[UserFull]])
async def get_users(
    current_user: Annotated[User, Depends(security.get_current_user)],
    role_name: Optional[str] = None,
    username: Optional[str] = None,
    db: Session = Depends(deps.get_db),
):
    role_id = None
    if role_name:
        valid_role = role.get_role_by_name(db, role_name)
        if not valid_role:
            raise HTTPException(400, "Invalid role filter")
        role_id = valid_role.id
    return SuccessResponse(data=user.get_all(db, username, role_id))


@router.put("/{id}", response_model=SuccessResponse[UserFull])
async def update_user(
    id: int,
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    print(current_user)
    if current_user.id != int(id):
        raise HTTPException(401, "No permission to update user")
    db_user = user.get_by_id(db, id)
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


@router.put("/{id}/roles", response_model=SuccessResponse[UserFull])
async def manage_user_roles(
    id: int,
    user_roles: UserRoleBulkUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins can manage user roles")
    # Check that user exists
    db_user = user.get_by_id(db, id)
    if not db_user:
        raise HTTPException(400, "User not found")

    # Check that role ids are valid
    unique_role_ids = set(user_roles.role_ids)
    db_roles = role.get_roles_by_ids(db, unique_role_ids)
    if len(db_roles) != len(unique_role_ids):
        raise HTTPException(400, "Invalid role id(s)")

    try:
        with db.begin_nested():
            user_role.bulk_remove(db, id)
            user_role.bulk_create(
                db,
                [
                    UserRoleCreate(user_id=id, role_id=role_id)
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
