import httpx
from typing import Annotated

from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_session
from app.models import AuthUserPublic, User
from app.kafka.producer.order import get_order_producer, OrderProducer
from app.kafka.producer.order_item import get_order_item_producer, OrderItemProducer
from app.kafka.producer.shipping_details import get_shipping_details_producer, ShippingDetailsProducer
from app.kafka.producer.order_history import get_order_history_producer, OrderHistoryProducer

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

OrderProducerDep = Annotated[OrderProducer, Depends(get_order_producer)]
OrderHistoryProducerDep = Annotated[OrderHistoryProducer, Depends(get_order_history_producer)]
OrderItemProducerDep = Annotated[OrderItemProducer, Depends(get_order_item_producer)]
ShippingDetailsProducerDep = Annotated[ShippingDetailsProducer, Depends(get_shipping_details_producer)]

