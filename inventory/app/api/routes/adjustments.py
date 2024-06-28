from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, AdjustmentProducerDep
from app.models import (
    AdjustmentPublic, Adjustment, AdjustmentsPublic, AdjustmentCreate, AdjustmentUpdate,
    Message
)
from app.crud import adjustment_crud

router = APIRouter()


@router.get("/", response_model=AdjustmentsPublic)
async def get_all_adjustments(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all adjustments
    """
    count_statement = select(func.count()).select_from(Adjustment)
    count = session.exec(count_statement).one()

    statement = select(Adjustment).offset(skip).limit(limit)
    adjustments = session.exec(statement).all()

    return AdjustmentsPublic(data=adjustments, count=count)

@router.post("/", response_model=AdjustmentPublic)
async def create_adjustment(*, session: SessionDep, adjustment_in: AdjustmentCreate, producer: AdjustmentProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new adjustment
    """
    adjustment = adjustment_crud.create(session=session, obj_in=adjustment_in)
    await producer.adjustment_made(adjustment.dict())
    return adjustment

@router.patch("/{adjustment_id}", response_model=AdjustmentPublic)
async def update_adjustment(*, session: SessionDep, adjustment_id: int, adjustment_in: AdjustmentUpdate, producer: AdjustmentProducerDep, current_user: CurrentUser) -> Any:
    """
    Update an adjustment
    """
    db_adjustment = adjustment_crud.get_by_id(session=session, id=adjustment_id)
    if not db_adjustment:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    db_adjustment = adjustment_crud.update(session=session, db_obj=db_adjustment, obj_in=adjustment_in)
    await producer.adjustment_made(db_adjustment.dict())
    return db_adjustment

@router.get("/{adjustment_id}", response_model=AdjustmentPublic)
def get_adjustment_by_id(adjustment_id: int, session: SessionDep) -> Any:
    """
    Get a specific adjustment by id.
    """
    adjustment = adjustment_crud.get_by_id(session=session, id=adjustment_id)
    if not adjustment:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adjustment

@router.delete("/{adjustment_id}", response_model=Message)
async def delete_adjustment(session: SessionDep, adjustment_id: int, producer: AdjustmentProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete an adjustment
    """
    adjustment = adjustment_crud.get_by_id(session=session, id=adjustment_id)
    if not adjustment:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    adjustment_crud.remove(session=session, id=adjustment_id)
    await producer.adjustment_made(adjustment.dict())
    return Message(message="Adjustment deleted successfully")
