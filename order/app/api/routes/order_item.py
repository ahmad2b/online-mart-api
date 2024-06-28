from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, OrderItemProducerDep
from app.models import (
    OrderItemPublic, OrderItem, OrderItemsPublic, OrderItemCreate, OrderItemUpdate, Message
)
from app.crud import crud_order_item

router = APIRouter()

@router.get("/", response_model=OrderItemsPublic)
async def get_all_order_items(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all order items
    """
    count_statement = select(func.count()).select_from(OrderItem)
    count = session.exec(count_statement).one()

    statement = select(OrderItem).offset(skip).limit(limit)
    order_items = session.exec(statement).all()

    return OrderItemsPublic(data=order_items, count=count)

@router.post("/", response_model=OrderItemPublic)
async def create_order_item(*, session: SessionDep, order_item_in: OrderItemCreate, producer: OrderItemProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new order item
    """
    order_item = crud_order_item.create(session=session, obj_in=order_item_in)
    await producer.order_item_created(order_item.dict())
    return order_item

@router.patch("/{order_item_id}", response_model=OrderItemPublic)
async def update_order_item(*, session: SessionDep, order_item_id: int, order_item_in: OrderItemUpdate, producer: OrderItemProducerDep, current_user: CurrentUser) -> Any:
    """
    Update an order item
    """
    db_order_item = crud_order_item.get(session=session, id=order_item_id)
    if not db_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    db_order_item = crud_order_item.update(session=session, db_obj=db_order_item, obj_in=order_item_in)
    await producer.order_item_updated(db_order_item.dict())
    return db_order_item

@router.get("/{order_item_id}", response_model=OrderItemPublic)
def get_order_item_by_id(order_item_id: int, session: SessionDep) -> Any:
    """
    Get a specific order item by id.
    """
    order_item = crud_order_item.get(session=session, id=order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item

@router.delete("/{order_item_id}", response_model=Message)
async def delete_order_item(session: SessionDep, order_item_id: int, producer: OrderItemProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete an order item
    """
    order_item = crud_order_item.get(session=session, id=order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    crud_order_item.remove(session=session, id=order_item_id)
    await producer.order_item_deleted(order_item.dict())
    return Message(message="Order item deleted successfully")
