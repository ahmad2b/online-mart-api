from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, ShippingDetailsProducerDep
from app.models import (
    ShippingDetailsPublic, ShippingDetails, ShippingDetailsCreate, ShippingDetailsUpdate, Message
)
from app.crud import crud_shipping_details

router = APIRouter()

@router.post("/", response_model=ShippingDetailsPublic)
async def create_shipping_details(*, session: SessionDep, shipping_details_in: ShippingDetailsCreate, producer: ShippingDetailsProducerDep, current_user: CurrentUser) -> Any:
    """
    Create new shipping details
    """
    shipping_details = crud_shipping_details.create(session=session, obj_in=shipping_details_in)
    await producer.shipping_details_created(shipping_details.dict())
    return shipping_details

@router.patch("/{shipping_details_id}", response_model=ShippingDetailsPublic)
async def update_shipping_details(*, session: SessionDep, shipping_details_id: int, shipping_details_in: ShippingDetailsUpdate, producer: ShippingDetailsProducerDep, current_user: CurrentUser) -> Any:
    """
    Update shipping details
    """
    db_shipping_details = crud_shipping_details.get(session=session, id=shipping_details_id)
    if not db_shipping_details:
        raise HTTPException(status_code=404, detail="Shipping details not found")
    db_shipping_details = crud_shipping_details.update(session=session, db_obj=db_shipping_details, obj_in=shipping_details_in)
    await producer.shipping_details_updated(db_shipping_details.dict())
    return db_shipping_details

@router.get("/{shipping_details_id}", response_model=ShippingDetailsPublic)
def get_shipping_details_by_id(shipping_details_id: int, session: SessionDep) -> Any:
    """
    Get specific shipping details by id.
    """
    shipping_details = crud_shipping_details.get(session=session, id=shipping_details_id)
    if not shipping_details:
        raise HTTPException(status_code=404, detail="Shipping details not found")
    return shipping_details

@router.delete("/{shipping_details_id}", response_model=Message)
async def delete_shipping_details(session: SessionDep, shipping_details_id: int, producer: ShippingDetailsProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete shipping details
    """
    shipping_details = crud_shipping_details.get(session=session, id=shipping_details_id)
    if not shipping_details:
        raise HTTPException(status_code=404, detail="Shipping details not found")
    crud_shipping_details.remove(session=session, id=shipping_details_id)
    await producer.shipping_details_deleted(shipping_details.dict())
    return Message(message="Shipping details deleted successfully")
