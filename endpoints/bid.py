from sqlalchemy.orm import Session
from crud import (
    bid_attribute_type,
    bid,
    user,
    bid_attribute,
    bid_attribute_option,
    role,
    customer as customercrud,
)
from fastapi import APIRouter, Depends, HTTPException
from core import deps, security
from schemas.bid_attribute_type import (
    BidAttributeTypeCreate,
    BidAttributeTypeUpdate,
    BidAttributeTypeFull,
)
from schemas.base import SuccessResponse
from schemas.bid import BidFull, BidCreate, BidUpdate, Bid
from schemas.bid_attribute import BidAttributeCreateDB
from schemas.bid_attribute_option import BidAttributeOptionCreateDB
from typing import Annotated, Optional, List
from models.user import User


router = APIRouter(prefix="/bids", tags=["bids"])


@router.post("/attribute-types", response_model=SuccessResponse[BidAttributeTypeFull])
async def create_bid_attribute_type(
    attribute_type_in: BidAttributeTypeCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins can create bid attribute types")
    new_bid_attribute_type = bid_attribute_type.create(db, attribute_type_in)
    db.commit()
    db.refresh(new_bid_attribute_type)
    return SuccessResponse(data=new_bid_attribute_type)


@router.put(
    "/attribute-types/{attribute_type_id}",
    response_model=SuccessResponse[BidAttributeTypeFull],
)
async def update_bid_attribute_type(
    attribute_type_id: int,
    attribute_type_in: BidAttributeTypeUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins can create bid attribute types")
    db_attribute_type = bid_attribute_type.get_by_id(db, attribute_type_id)
    if not db_attribute_type:
        raise HTTPException(404, "Bid attribute type not found")

    updated_bid_attribute_type = bid_attribute_type.update(
        db, db_attribute_type, attribute_type_in
    )

    if attribute_type_in.options:
        if attribute_type_in.options.delete_options:
            bid_attribute_option.bulk_delete(
                db, attribute_type_in.options.delete_options
            )
        if attribute_type_in.options.update_options:
            for option in attribute_type_in.options.update_options:
                db_option = bid_attribute_option.get_by_value_id(
                    db, attribute_type_id, option.value
                )
                if db_option:
                    bid_attribute_option.update(db, db_option, option)
                else:
                    bid_attribute_option.create(
                        db,
                        BidAttributeOptionCreateDB(
                            attribute_type_id=attribute_type_id,
                            **option.model_dump(exclude_unset=True)
                        ),
                    )
    db.commit()
    db.refresh(updated_bid_attribute_type)
    return SuccessResponse(data=updated_bid_attribute_type)


@router.get(
    "/attribute-types", response_model=SuccessResponse[list[BidAttributeTypeFull]]
)
async def get_bid_attribute_types(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    bid_attribute_types = bid_attribute_type.get(db)
    return SuccessResponse(data=bid_attribute_types)


@router.post("", response_model=SuccessResponse[BidFull])
async def create_bid(
    bid_in: BidCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Bid Manager"):
        raise HTTPException(401, "Only bid managers can create bids")
    # Validate bid manager(s)
    if len(bid_in.bid_manager_ids):
        bm_role = role.get_role_by_name(db, "Bid Manager")
        valid_bid_managers = user.get_all(
            db, bid_in.bid_manager_ids, role_id=bm_role.id
        )
        if len(valid_bid_managers) != len(bid_in.bid_manager_ids):
            raise HTTPException(400, "Invalid bid manager id(s)")
    try:
        with db.begin_nested():
            new_bid = bid.create(db, bid_in)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, str(e))
    db.refresh(new_bid)
    return SuccessResponse(data=new_bid)


@router.put("/{bid_id}", response_model=SuccessResponse[BidFull])
async def update_bid(
    bid_id: int,
    bid_in: BidUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    """Update a bid's attributes"""
    if not current_user.has_role("Bid Manager"):
        raise HTTPException(401, "Only bid managers can update bids")
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")
    if not any(bm.id == current_user.id for bm in bid_obj.bid_managers):
        raise HTTPException(401, "You do not have permission to manage this bid")
    try:
        with db.begin_nested():
            if bid_in.bid_manager_ids and len(bid_in.bid_manager_ids):
                bm_role = role.get_role_by_name(db, "Bid Manager")
                valid_bid_managers = user.get_all(
                    db, bid_in.bid_manager_ids, role_id=bm_role.id
                )
                if len(valid_bid_managers) != len(bid_in.bid_manager_ids):
                    raise HTTPException(400, "Invalid bid manager id(s)")
            if bid_in.project_manager_ids and len(bid_in.project_manager_ids):
                pm_role = role.get_role_by_name(db, "Project Manager")
                valid_project_managers = user.get_all(
                    db, bid_in.project_manager_ids, role_id=pm_role.id
                )
                if len(valid_project_managers) != len(bid_in.project_manager_ids):
                    raise HTTPException(400, "Invalid project manager id(s)")
            updated_bid = bid.update(db, bid_obj, bid_in)
            if bid_in.attributes:
                if bid_in.attributes.deleted_attributes:
                    bid_attribute.bulk_remove(db, bid_in.attributes.deleted_attributes)
                if bid_in.attributes.updated_attributes:
                    for attribute in bid_in.attributes.updated_attributes:
                        db_attribute = bid_attribute.get_by_bid_type_id(
                            db, bid_id, attribute.type_id
                        )
                        if db_attribute:
                            # Update existing attribute
                            bid_attribute.update(db, db_attribute, attribute)
                        else:
                            # Create new attribute
                            bid_attribute.create(
                                db,
                                BidAttributeCreateDB(
                                    bid_id=bid_id,
                                    **attribute.model_dump(exclude_unset=True)
                                ),
                            )
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
    db.refresh(updated_bid)
    return SuccessResponse(data=updated_bid)


@router.get("/{bid_id}", response_model=SuccessResponse[BidFull])
async def get_bid(
    bid_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Bid Manager"):
        raise HTTPException(401, "Missing Bid Manager role")
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")
    return SuccessResponse(data=bid_obj)


@router.get("", response_model=SuccessResponse[list[Bid]])
async def get_bids(
    current_user: Annotated[User, Depends(security.get_current_user)],
    bid_manager_ids: Optional[List[int]] = None,
    customer: Optional[str] = None,
    db: Session = Depends(deps.get_db),
):
    customer_id = None
    if not current_user.has_role("Bid Manager"):
        raise HTTPException(401, "Missing Bid Manager role")

    if bid_manager_ids and len(bid_manager_ids):
        bm_role = role.get_role_by_name(db, "Bid Manager")
        valid_bms = user.get_all(db, user_ids=bid_manager_ids, role_id=bm_role.id)
        if valid_bms != len(bid_manager_ids):
            raise HTTPException(400, "Invalid bid manager id(s)")
    if customer:
        valid_customer = customercrud.get_by_name(db, customer)
        if not valid_customer:
            raise HTTPException(400, "Customer does not exist")
        customer_id = valid_customer.id
    return SuccessResponse(data=bid.get(db, customer_id, bid_manager_ids))
