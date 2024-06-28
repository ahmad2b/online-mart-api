import httpx
from typing import Annotated

from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_session
from app.models import AuthUserPublic, User
from app.kafka.producers.adjustment import get_adjustment_producer, AdjustmentProducer
from app.kafka.producers.inventory import get_inventory_producer, InventoryProducer
from app.kafka.producers.reservation import get_reservation_producer, ReservationProducer

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="http://localhost:8007/api/v1/login/access-token")
        

async def get_current_user(token: Annotated[str, Depends(reusable_oauth2)]) -> AuthUserPublic:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token_with_auth_service(token, credentials_exception)


async def verify_token_with_auth_service(token: str, credentials_exception: HTTPException) -> AuthUserPublic:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://auth-service:8000/api/v1/verify-token", json={"token": token})
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise credentials_exception
        return AuthUserPublic(**response.json())
    
CurrentUser = Annotated[User, Depends(get_current_user)]
SessionDep = Annotated[Session, Depends(get_session)]

AdjustmentProducerDep = Annotated[AdjustmentProducer, Depends(get_adjustment_producer)]
InventoryProducerDep = Annotated[InventoryProducer, Depends(get_inventory_producer)]
ReservationProducerDep = Annotated[ReservationProducer, Depends(get_reservation_producer)]