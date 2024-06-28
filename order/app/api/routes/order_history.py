from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, OrderHistoryProducerDep
from app.models import (
    OrderHistoryPublic, OrderHistory, OrderHistoryCreate, OrderHistoryUpdate, Message
)
from app.crud import crud_order_history

router = APIRouter()

@router.post("/", response_model=OrderHistoryPublic)
async def create_order_history(*, session: SessionDep, order_history_in: OrderHistoryCreate, producer: OrderHistoryProducerDep, current_user: CurrentUser) -> Any:
    """
    Create new order history
    """
    order_history = crud_order_history.create(session=session, obj_in=order_history_in)
    await producer.order_history_created(order_history.dict())
    return order_history

@router.patch("/{order_history_id}", response_model=OrderHistoryPublic)
async def update_order_history(*, session: SessionDep, order_history_id: int, order_history_in: OrderHistoryUpdate, producer: OrderHistoryProducerDep, current_user: CurrentUser) -> Any:
    """
    Update order history
    """
    db_order_history = crud_order_history.get(session=session, id=order_history_id)
    if not db_order_history:
        raise HTTPException(status_code=404, detail="Order history not found")
    db_order_history = crud_order_history.update(session=session, db_obj=db_order_history, obj_in=order_history_in)
    await producer.order_history_updated(db_order_history.dict())
    return db_order_history

@router.get("/{order_history_id}", response_model=OrderHistoryPublic)
def get_order_history_by_id(order_history_id: int, session: SessionDep) -> Any:
    """
    Get specific order history by id.
    """
    order_history = crud_order_history.get(session=session, id=order_history_id)
    if not order_history:
        raise HTTPException(status_code=404, detail="Order history not found")
    return order_history

@router.delete("/{order_history_id}", response_model=Message)
async def delete_order_history(session: SessionDep, order_history_id: int, producer: OrderHistoryProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete order history
    """
    order_history = crud_order_history.get(session=session, id=order_history_id)
    if not order_history:
        raise HTTPException(status_code=404, detail="Order history not found")
    crud_order_history.remove(session=session, id=order_history_id)
    await producer.order_history_deleted(order_history.dict())
    return Message(message="Order history deleted successfully")
