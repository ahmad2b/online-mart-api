from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, OrderProducerDep
from app.models import (
    OrderPublic, Order, OrdersPublic, OrderCreate, OrderUpdate, Message
)
from app.crud import crud_order

router = APIRouter()

@router.get("/", response_model=OrdersPublic)
async def get_all_orders(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all orders
    """
    count_statement = select(func.count()).select_from(Order)
    count = session.exec(count_statement).one()

    statement = select(Order).offset(skip).limit(limit)
    orders = session.exec(statement).all()

    return OrdersPublic(data=orders, count=count)

@router.post("/", response_model=OrderPublic)
async def create_order(*, session: SessionDep, order_in: OrderCreate, producer: OrderProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new order
    """
    order = crud_order.create(session=session, obj_in=order_in)
    await producer.order_created(order.dict())
    return order

@router.patch("/{order_id}", response_model=OrderPublic)
async def update_order(*, session: SessionDep, order_id: int, order_in: OrderUpdate, producer: OrderProducerDep, current_user: CurrentUser) -> Any:
    """
    Update an order
    """
    db_order = crud_order.get(session=session, id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order = crud_order.update(session=session, db_obj=db_order, obj_in=order_in)
    await producer.order_updated(db_order.dict())
    return db_order

@router.get("/{order_id}", response_model=OrderPublic)
def get_order_by_id(order_id: int, session: SessionDep) -> Any:
    """
    Get a specific order by id.
    """
    order = crud_order.get(session=session, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}", response_model=Message)
async def delete_order(session: SessionDep, order_id: int, producer: OrderProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete an order
    """
    order = crud_order.get(session=session, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.remove(session=session, id=order_id)
    await producer.order_deleted(order.dict())
    return Message(message="Order deleted successfully")
