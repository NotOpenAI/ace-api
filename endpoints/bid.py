from sqlalchemy.orm import Session
from crud import (
    contract,
    bid_type,
    bid_attribute_type,
    bid,
    user,
    bid_attribute,
    bid_attribute_option,
)
from fastapi import APIRouter, Depends, HTTPException
from core import deps
from schemas.contract import Contract, ContractCreate
from schemas.bid_type import BidType, BidTypeCreate
from schemas.bid_attribute_type import (
    BidAttributeTypeCreate,
    BidAttributeTypeUpdate,
    BidAttributeTypeFull,
)
from schemas.base import SuccessResponse
from schemas.bid import BidFull, BidCreate, BidUpdate, Bid
from schemas.bid_attribute import BidAttributeCreateDB
from schemas.bid_attribute_option import BidAttributeOptionCreateDB


router = APIRouter(prefix="/bids", tags=["bids"])


@router.post("/contracts", response_model=SuccessResponse[Contract])
def create_bid_contract_type(
    contract_in: ContractCreate, db: Session = Depends(deps.get_db)
):
    try:
        with db.begin_nested():
            new_contract_type = contract.create(db, contract_in)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, "Internal Server Error")
    db.refresh(new_contract_type)
    return SuccessResponse(data=new_contract_type)


@router.get("/contracts", response_model=SuccessResponse[list[Contract]])
def get_contract_types(db: Session = Depends(deps.get_db)):
    return SuccessResponse(data=contract.get(db))


@router.post("/types", response_model=SuccessResponse[BidType])
def create_bid_type(bid_type_in: BidTypeCreate, db: Session = Depends(deps.get_db)):
    new_bid_type = bid_type.create(db, bid_type_in)
    db.commit()
    db.refresh(new_bid_type)
    return SuccessResponse(data=new_bid_type)


@router.get("/types", response_model=SuccessResponse[list[BidType]])
def get_bid_types(db: Session = Depends(deps.get_db)):
    return SuccessResponse(data=bid_type.get(db))


@router.post("/attribute-types", response_model=SuccessResponse[BidAttributeTypeFull])
async def create_bid_attribute_type(
    attribute_type_in: BidAttributeTypeCreate, db: Session = Depends(deps.get_db)
):
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
    db: Session = Depends(deps.get_db),
):
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
async def get_bid_attribute_types(db: Session = Depends(deps.get_db)):
    bid_attribute_types = bid_attribute_type.get(db)
    return SuccessResponse(data=bid_attribute_types)


@router.post("", response_model=SuccessResponse[BidFull])
async def create_bid(bid_in: BidCreate, db: Session = Depends(deps.get_db)):
    # Validate bid manager
    bid_manager = user.get_by_id(db, bid_in.bid_manager_id)
    if not bid_manager:
        raise HTTPException(400, "Invalid bid manager id")
    bm_role = [role for role in bid_manager.roles if role.name == "Bid Manager"]
    if not len(bm_role):
        raise HTTPException(400, "Bid manager needs to have 'Bid Manager' role")

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
    bid_id: int, bid_in: BidUpdate, db: Session = Depends(deps.get_db)
):
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")

    try:
        with db.begin_nested():
            updated_bid = bid.update(db, bid_obj, bid_in)

            if (
                bid_in.approved is not None
                and bid_in.approved == False
                and bid_obj.project
            ):
                raise HTTPException(
                    400, "Cannot reject a bid after a project has been created"
                )

            if bid_in.estimated_data:
                bid.update_estimates(db, bid_obj.estimated_data, bid_in.estimated_data)

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
async def get_bid(bid_id: int, db: Session = Depends(deps.get_db)):
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")
    return SuccessResponse(data=bid_obj)


@router.get("", response_model=SuccessResponse[list[Bid]])
async def get_bids(db: Session = Depends(deps.get_db)):
    return SuccessResponse(data=bid.get(db))
