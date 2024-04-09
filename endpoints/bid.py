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
import models.bid
import models.bid_attribute
import models.bid_manager
import models.customer
import models.customer_contact
import models.lookup
import models.lookup.bid_attribute_option
import models.lookup.bid_attribute_type
import models.lookup.role
import models.project_manager
import models.user
import models.user_role
from schemas.bid_attribute_type import (
    BidAttributeTypeCreate,
    BidAttributeTypeUpdate,
    BidAttributeTypeFull,
)
from schemas.base import SuccessResponse
from schemas.bid import BidFull, BidCreate, BidUpdate, Bid, BidCreateTest
from schemas.bid_attribute import BidAttributeCreateDB
from schemas.bid_attribute_option import (
    BidAttributeOptionCreateDB,
)
from schemas.role import RoleCreate
from schemas.user import UserCreate
from schemas.customer import CustomerCreate
from schemas.customer_contact import CustomerContactCreate
from typing import Annotated, Optional, List
import models
import csv
from sqlalchemy import delete, text
from datetime import datetime
from db.types import currency

router = APIRouter(prefix="/bids", tags=["bids"])


@router.post("/attribute-types", response_model=SuccessResponse[BidAttributeTypeFull])
async def create_bid_attribute_type(
    attribute_type_in: BidAttributeTypeCreate,
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
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
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
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
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    bid_attribute_types = bid_attribute_type.get(db)
    return SuccessResponse(data=bid_attribute_types)


@router.post("", response_model=SuccessResponse[BidFull])
async def create_bid(
    bid_in: BidCreate,
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
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
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    """Update a bid's attributes"""
    if not current_user.has_role("Bid Manager"):
        raise HTTPException(401, "Only bid managers can update bids")
    bid_obj = bid.get_by_id(bid_id, db)
    if not bid_obj:
        raise HTTPException(404, "Bid not found")

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
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
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
    current_user: Annotated[models.user.User, Depends(security.get_current_user)],
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


@router.post("/test-data", response_model=SuccessResponse[list[BidFull]])
async def import_test_data(db: Session = Depends(deps.get_db)):
    # Delete existing data
    db.execute(delete(models.bid_attribute.BidAttribute))
    db.execute(delete(models.bid_manager.BidManager))
    db.execute(delete(models.project_manager.ProjectManager))
    db.execute(delete(models.user_role.UserRole))
    db.execute(delete(models.user.User))
    db.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1"))
    db.execute(delete(models.bid.Bid))
    db.execute(text("ALTER SEQUENCE bid_id_seq RESTART WITH 1"))
    db.execute(delete(models.customer_contact.CustomerContact))
    db.execute(text("ALTER SEQUENCE customer_contact_id_seq RESTART WITH 1"))
    db.execute(delete(models.customer.Customer))
    db.execute(text("ALTER SEQUENCE customer_id_seq RESTART WITH 1"))
    db.execute(delete(models.lookup.role.Role))
    db.execute(text("ALTER SEQUENCE lookup.role_id_seq RESTART WITH 1"))
    db.execute(delete(models.lookup.bid_attribute_option.BidAttributeOption))
    db.execute(text("ALTER SEQUENCE lookup.bid_attribute_option_id_seq RESTART WITH 1"))
    db.execute(delete(models.lookup.bid_attribute_type.BidAttributeType))
    db.execute(text("ALTER SEQUENCE lookup.bid_attribute_type_id_seq RESTART WITH 1"))

    # Create bid attribute types
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="project_class_desc",
            options=[
                {"value": "Residential"},
                {"value": "Commercial"},
                {"value": "Multi Family Housing"},
                {"value": "New Builds"},
                {"value": "General Contractor"},
                {"value": "Construction Manager"},
                {"value": "Health Care"},
            ],
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="job_status",
            options=[
                {"value": "Active"},
                {"value": "Completed"},
                {"value": "Rejected"},
            ],
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="tax_pr_desc", options=[{"value": "NY NO LOCAL TAX"}]
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="cost_basis", options=[{"value": "U"}, {"value": "L"}]
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="job_certified_payroll",
            options=[{"value": "N"}, {"value": "C"}, {"value": "Y"}],
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="framing", options=[{"value": "Wood"}, {"value": "Metal"}]
        ),
    )
    bid_attribute_type.create(db, BidAttributeTypeCreate(name="retainage_percent"))
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="drywall", options=[{"value": "No"}, {"value": "Yes"}]
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="insulation", options=[{"value": "No"}, {"value": "Yes"}]
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="ceiling", options=[{"value": "No"}, {"value": "Yes"}]
        ),
    )
    bid_attribute_type.create(
        db,
        BidAttributeTypeCreate(
            name="scope_clarity",
            options=[{"value": "Clear"}, {"value": "Some"}, {"value": "Vague"}],
        ),
    )
    bid_attribute_type.create(db, BidAttributeTypeCreate(name="margin"))

    # Create user roles
    admin_role = role.create(db, RoleCreate(name="Admin"))
    bm_role = role.create(db, RoleCreate(name="Bid Manager"))
    pm_role = role.create(db, RoleCreate(name="Project Manager"))
    db.commit()
    db.refresh(admin_role)
    db.refresh(bm_role)
    db.refresh(pm_role)

    # Create users
    user.create(
        db,
        UserCreate(
            username="kalford",
            first_name="Kellah",
            last_name="Alford",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="etesta",
            first_name="Ethan",
            last_name="Testa",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="mjohnston",
            first_name="Michael",
            last_name="Johnston",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="mgeska",
            first_name="Melissa",
            last_name="Geska",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="remmerson",
            first_name="Riley",
            last_name="Emmerson",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="mfitzgerald",
            first_name="Mike",
            last_name="Fitzgerald",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="egeska",
            first_name="Ed",
            last_name="Geska",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="galford",
            first_name="Geriann",
            last_name="Alford",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="gblack",
            first_name="Gary",
            last_name="Black",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="rcrowley",
            first_name="Ryan",
            last_name="Crowley",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="jcahill",
            first_name="John",
            last_name="Cahill",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="bosterling",
            first_name="Brad",
            last_name="Osterling",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="jcisneros",
            first_name="J",
            last_name="Cisneros",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="agarcia",
            first_name="Angel",
            last_name="Garcia",
            password="password",
            role_ids=[2, 3],
        ),
    )
    user.create(
        db,
        UserCreate(
            username="adminacc",
            first_name="admin",
            last_name="acc",
            password="password",
            role_ids=[1, 2, 3],
        ),
    )
    db.commit()

    customers = {}
    rows = []
    with open("USC_AI_Data.csv", newline="") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue

            # Update customers
            customer_name = row[3].strip()
            if not customer_name:
                customer_name = row[1].strip()
            customer_contact = row[16].strip()
            if customer_name not in customers:
                customers[customer_name] = {"name": customer_name, "contacts": []}
            if (
                customer_contact
                and customer_contact not in customers[customer_name]["contacts"]
            ):
                customers[customer_name]["contacts"].append(customer_contact)
            rows.append(row)

    for customer in customers.values():
        customercrud.create(
            db,
            CustomerCreate(
                name=customer["name"],
                contacts=[
                    CustomerContactCreate(name=contact)
                    for contact in customer["contacts"]
                ],
            ),
        )
    db.commit()

    def convert_currency_to_int(currency_str: str):
        return int(currency_str.strip().replace("$", "").replace(",", ""))

    def parse_datetime_string(date_str: str):
        split = date_str.split("/")
        return datetime(int(split[2]), int(split[0]), int(split[1]))

    bids = []
    for row in rows:
        customer_name = row[3].strip()
        if not customer_name:
            customer_name = row[1].strip()
        customer = customercrud.get_by_name(db, customer_name)
        bid_obj = {
            "name": row[1].strip(),
            "customer_id": customer.id,
            "original_contract": convert_currency_to_int(row[11]),
            "original_cost": convert_currency_to_int(row[12]),
        }

        start_date = row[14].strip()
        if start_date:
            bid_obj["start_date"] = parse_datetime_string(start_date)

        finish_date = row[15].strip()
        if finish_date:
            bid_obj["finish_date"] = parse_datetime_string(finish_date)

        project_managers = row[4].strip()
        bid_obj["project_manager_ids"] = []
        if project_managers:
            project_managers = project_managers.split("/")
            for pm in project_managers:
                split = pm.split(" ")
                project_manager = user.get_by_name(db, split[0], split[1])
                bid_obj["project_manager_ids"].append(project_manager.id)

        bid_manager = row[19].strip()
        bid_obj["bid_manager_ids"] = []
        if bid_manager:
            bid_obj["bid_manager_ids"] = [int(bid_manager)]

        bid_obj["attributes"] = []

        project_class_desc = row[6].strip()
        if project_class_desc:
            project_class_attr = bid_attribute_type.get_by_name(
                db, "project_class_desc"
            )
            option = next(
                opt
                for opt in project_class_attr.options
                if opt.value == project_class_desc
            )
            bid_obj["attributes"].append(
                {"type_id": project_class_attr.id, "option_id": option.id}
            )

        job_status = row[7].strip()
        job_status_attr = bid_attribute_type.get_by_name(db, "job_status")
        if job_status == "A":
            option = next(
                opt for opt in job_status_attr.options if opt.value == "Active"
            )
        else:
            option = next(
                opt for opt in job_status_attr.options if opt.value == "Completed"
            )
        bid_obj["attributes"].append(
            {"type_id": job_status_attr.id, "option_id": option.id}
        )

        tax_pr_desc = row[8].strip()
        if tax_pr_desc:
            tax_pr_attr = bid_attribute_type.get_by_name(db, "tax_pr_desc")
            bid_obj["attributes"].append(
                {"type_id": tax_pr_attr.id, "option_id": tax_pr_attr.options[0].id}
            )

        cost_basis = row[9].strip()
        cost_basis_attr = bid_attribute_type.get_by_name(db, "cost_basis")
        option = next(opt for opt in cost_basis_attr.options if opt.value == cost_basis)
        bid_obj["attributes"].append(
            {"type_id": cost_basis_attr.id, "option_id": option.id}
        )

        job_certified_payroll = row[10].strip()
        job_certified_payroll_attr = bid_attribute_type.get_by_name(
            db, "job_certified_payroll"
        )
        option = next(
            opt
            for opt in job_certified_payroll_attr.options
            if opt.value == job_certified_payroll
        )
        bid_obj["attributes"].append(
            {"type_id": job_certified_payroll_attr.id, "option_id": option.id}
        )

        retainage_percent = row[13].strip()
        retainage_percent_attr = bid_attribute_type.get_by_name(db, "retainage_percent")
        bid_obj["attributes"].append(
            {
                "type_id": retainage_percent_attr.id,
                "num_val": currency(retainage_percent),
            }
        )

        framing = row[21].strip()
        if framing and framing != "0" and framing != "3":
            framing_attr = bid_attribute_type.get_by_name(db, "framing")
            bid_obj["attributes"].append(
                {
                    "type_id": framing_attr.id,
                    "option_id": framing_attr.options[int(framing) - 1].id,
                }
            )

        drywall = row[22].strip()
        if drywall and drywall != "0":
            drywall_attr = bid_attribute_type.get_by_name(db, "drywall")
            bid_obj["attributes"].append(
                {
                    "type_id": drywall_attr.id,
                    "option_id": drywall_attr.options[int(drywall) - 1].id,
                }
            )

        insulation = row[23].strip()
        if insulation and insulation != "0":
            insulation_attr = bid_attribute_type.get_by_name(db, "insulation")
            bid_obj["attributes"].append(
                {
                    "type_id": insulation_attr.id,
                    "option_id": insulation_attr.options[int(insulation) - 1].id,
                }
            )

        ceiling = row[24].strip()
        if ceiling and ceiling != "0":
            ceiling_attr = bid_attribute_type.get_by_name(db, "ceiling")
            bid_obj["attributes"].append(
                {
                    "type_id": ceiling_attr.id,
                    "option_id": ceiling_attr.options[int(ceiling) - 1].id,
                }
            )

        scope = row[25].strip()
        if scope:
            scope_attr = bid_attribute_type.get_by_name(db, "scope_clarity")
            bid_obj["attributes"].append(
                {
                    "type_id": scope_attr.id,
                    "option_id": scope_attr.options[int(scope) - 1].id,
                }
            )

        margin = row[26].strip().replace("%", "")
        margin_attr = bid_attribute_type.get_by_name(db, "margin")
        bid_obj["attributes"].append(
            {"type_id": margin_attr.id, "num_val": currency(margin)}
        )
        bids.append(BidCreateTest(**bid_obj))

    for bid_obj in bids:
        new_bid = models.bid.Bid(
            **bid_obj.model_dump(
                exclude={
                    "attributes": True,
                    "bid_manager_ids": True,
                    "project_manager_ids": True,
                }
            ),
            attributes=[
                models.bid_attribute.BidAttribute(
                    **attribute.model_dump(exclude_unset=True)
                )
                for attribute in bid_obj.attributes
            ],
            bm_associations=[
                models.bid_manager.BidManager(manager_id=id)
                for id in bid_obj.bid_manager_ids
            ],
            pm_associations=[
                models.project_manager.ProjectManager(manager_id=id)
                for id in bid_obj.project_manager_ids
            ]
        )
        db.add(new_bid)
    db.commit()

    return SuccessResponse(data=bid.get(db))
