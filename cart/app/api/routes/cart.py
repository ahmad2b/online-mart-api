from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, CartProducerDep
from app.models import (
    Cart, CartCreate, CartUpdate, CartPublic, Message, CartsPublic
)
from app.crud import cart_crud

router = APIRouter()

@router.get("/", response_model=CartsPublic)
async def get_all_carts(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all carts
    """
    count_statement = select(func.count()).select_from(Cart)
    count = session.exec(count_statement).one()

    statement = select(Cart).offset(skip).limit(limit)
    carts = session.exec(statement).all()

    return CartsPublic(data=carts, count=count)

@router.post("/", response_model=CartPublic)
async def create_cart(*, session: SessionDep, cart_in: CartCreate, producer: CartProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new cart
    """
    cart = cart_crud.create(session=session, obj_in=cart_in)
    await producer.cart_created(cart.dict())
    return cart

@router.patch("/{cart_id}", response_model=CartPublic)
async def update_cart(*, session: SessionDep, cart_id: int, cart_in: CartUpdate, producer: CartProducerDep, current_user: CurrentUser) -> Any:
    """
    Update a cart
    """
    db_cart = cart_crud.get_by_id(session=session, id=cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_cart = cart_crud.update(session=session, obj_in=cart_in)
    await producer.cart_updated(db_cart.dict())
    return db_cart

@router.get("/{cart_id}", response_model=CartPublic)
def get_cart_by_id(cart_id: int, session: SessionDep) -> Any:
    """
    Get a specific cart by id.
    """
    cart = cart_crud.get_by_id(session=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.delete("/{cart_id}", response_model=Message)
async def delete_cart(session: SessionDep, cart_id: int, producer: CartProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete a cart
    """
    cart = cart_crud.get_by_id(session=session, id=cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_crud.remove(session=session, id=cart_id)
    await producer.cart_deleted(cart.dict())
    return Message(message="Cart deleted successfully")
