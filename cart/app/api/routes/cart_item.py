from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func


from app.api.deps import SessionDep, CurrentUser, CartItemProducerDep
from app.models import (
    CartItem, CartItemCreate, CartItemUpdate, Message, CartItemPublic, CartItemsPublic
)
from app.crud import cart_item_crud

router = APIRouter()

@router.get("/{cart_id}/items", response_model=CartItemsPublic)
async def get_all_cart_items(cart_id: int, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all cart items for a specific cart
    """
    count_statement = select(func.count()).select_from(CartItem).where(CartItem.cart_id == cart_id)
    count = session.exec(count_statement).one()

    statement = select(CartItem).where(CartItem.cart_id == cart_id).offset(skip).limit(limit)
    cart_items = session.exec(statement).all()

    return CartItemsPublic(data=cart_items, count=count)

@router.post("/{cart_id}/items", response_model=CartItemPublic)
async def create_cart_item(*, session: SessionDep, cart_id: int, cart_item_in: CartItemCreate, producer: CartItemProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new cart item
    """
    cart_item_in.cart_id = cart_id
    cart_item = cart_item_crud.create(session=session, obj_in=cart_item_in)
    await producer.cart_item_created(cart_item.dict())
    return cart_item

@router.patch("/{cart_id}/items/{cart_item_id}", response_model=CartItemPublic)
async def update_cart_item(*, session: SessionDep, cart_id: int, cart_item_id: int, cart_item_in: CartItemUpdate, producer: CartItemProducerDep, current_user: CurrentUser) -> Any:
    """
    Update a cart item
    """
    db_cart_item = cart_item_crud.get_by_id(session=session, id=cart_item_id)
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db_cart_item = cart_item_crud.update(session=session, db_obj=db_cart_item, obj_in=cart_item_in)
    await producer.cart_item_updated(db_cart_item.dict())
    return db_cart_item

@router.get("/{cart_id}/items/{cart_item_id}", response_model=CartItemPublic)
def get_cart_item_by_id(cart_id: int, cart_item_id: int, session: SessionDep) -> Any:
    """
    Get a specific cart item by id.
    """
    cart_item = cart_item_crud.get_by_id(session=session, id=cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item

@router.delete("/{cart_id}/items/{cart_item_id}", response_model=Message)
async def delete_cart_item(session: SessionDep, cart_id: int, cart_item_id: int, producer: CartItemProducerDep, current_user: CurrentUser) -> Message:
    """
    Remove an item from the cart
    """
    cart_item = cart_item_crud.get_by_id(session=session, id=cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart_item_crud.remove(session=session, id=cart_item_id)
    await producer.cart_item_deleted(cart_item.dict())
    return Message(message="Cart item deleted successfully")