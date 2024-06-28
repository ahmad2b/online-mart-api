from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, InventoryProducerDep
from app.models import (
    InventoryPublic, Inventory, InventoriesPublic, InventoryCreate, InventoryUpdate, Message
)
from app.crud import inventory_crud

router = APIRouter()

@router.get("/", response_model=InventoriesPublic)
async def get_all_inventory(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all inventory items
    """
    count_statement = select(func.count()).select_from(Inventory)
    count = session.exec(count_statement).one()

    statement = select(Inventory).offset(skip).limit(limit)
    inventory_items = session.exec(statement).all()

    return InventoriesPublic(data=inventory_items, count=count)

@router.post("/", response_model=InventoryPublic)
async def create_inventory(*, session: SessionDep, inventory_in: InventoryCreate, producer: InventoryProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new inventory item
    """
    inventory_item = inventory_crud.create(session=session, obj_in=inventory_in)
    await producer.inventory_created(inventory_item.dict())
    return inventory_item

@router.patch("/{inventory_id}", response_model=InventoryPublic)
async def update_inventory(*, session: SessionDep, inventory_id: int, inventory_in: InventoryUpdate, producer: InventoryProducerDep, current_user: CurrentUser) -> Any:
    """
    Update an inventory item
    """
    db_inventory = inventory_crud.get_by_id(session=session, id=inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    db_inventory = inventory_crud.update(session=session, db_obj=db_inventory, obj_in=inventory_in)
    await producer.inventory_updated(db_inventory.dict())
    return db_inventory

@router.get("/{inventory_id}", response_model=InventoryPublic)
def get_inventory_by_id(inventory_id: int, session: SessionDep) -> Any:
    """
    Get a specific inventory item by id.
    """
    inventory_item = inventory_crud.get_by_id(session=session, id=inventory_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory_item

@router.delete("/{inventory_id}", response_model=Message)
async def delete_inventory(session: SessionDep, inventory_id: int, producer: InventoryProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete an inventory item
    """
    inventory_item = inventory_crud.get_by_id(session=session, id=inventory_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    inventory_crud.remove(session=session, id=inventory_id)
    await producer.inventory_deleted(inventory_item.dict())
    return Message(message="Inventory item deleted successfully")

