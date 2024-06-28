from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, ReservationProducerDep
from app.models import (
    ReservationPublic, Reservation, ReservationsPublic, ReservationCreate, ReservationUpdate, Message
)
from app.crud import reservation_crud

router = APIRouter()

@router.get("/", response_model=ReservationsPublic)
async def get_all_reservations(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all reservations
    """
    count_statement = select(func.count()).select_from(Reservation)
    count = session.exec(count_statement).one()

    statement = select(Reservation).offset(skip).limit(limit)
    reservations = session.exec(statement).all()

    return ReservationsPublic(data=reservations, count=count)

@router.post("/", response_model=ReservationPublic)
async def create_reservation(*, session: SessionDep, reservation_in: ReservationCreate, producer: ReservationProducerDep, current_user: CurrentUser) -> Any:
    """
    Create a new reservation
    """
    reservation = reservation_crud.create(session=session, obj_in=reservation_in)
    await producer.reservation_created(reservation.dict())
    return reservation

@router.patch("/{reservation_id}", response_model=ReservationPublic)
async def update_reservation(*, session: SessionDep, reservation_id: int, reservation_in: ReservationUpdate, producer: ReservationProducerDep, current_user: CurrentUser) -> Any:
    """
    Update a reservation
    """
    db_reservation = reservation_crud.get_by_id(session=session, id=reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db_reservation = reservation_crud.update(session=session, db_obj=db_reservation, obj_in=reservation_in)
    await producer.reservation_updated(db_reservation.dict())
    return db_reservation

@router.get("/{reservation_id}", response_model=ReservationPublic)
def get_reservation_by_id(reservation_id: int, session: SessionDep) -> Any:
    """
    Get a specific reservation by id.
    """
    reservation = reservation_crud.get_by_id(session=session, id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/{reservation_id}", response_model=Message)
async def delete_reservation(session: SessionDep, reservation_id: int, producer: ReservationProducerDep, current_user: CurrentUser) -> Message:
    """
    Delete a reservation
    """
    reservation = reservation_crud.get_by_id(session=session, id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation_crud.remove(session=session, id=reservation_id)
    await producer.reservation_deleted(reservation.dict())
    return Message(message="Reservation deleted successfully")