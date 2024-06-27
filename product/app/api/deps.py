import httpx
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import engine
from app.models import User, AuthUserPublic
from app.kafka.producer.product import ProductProducer
from app.kafka.producer.category import CategoryProducer
from app.kafka.producer.brand import BrandProducer


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="http://localhost:8007/api/v1/login/access-token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]

async def get_current_user(token: Annotated[str, Depends(reusable_oauth2)]) -> AuthUserPublic:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token_with_auth_service(token, credentials_exception)

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_product_producer():
    producer = ProductProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()      

async def get_category_producer():
    producer = CategoryProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def get_brand_producer():
    producer = BrandProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
        

ProductProducerDep = Annotated[ProductProducer, Depends(get_product_producer)]
CategoryProducerDep = Annotated[CategoryProducer, Depends(get_category_producer)]
BrandProducerDep = Annotated[BrandProducer, Depends(get_brand_producer)]

async def verify_token_with_auth_service(token: str, credentials_exception: HTTPException) -> AuthUserPublic:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://auth-service:8000/api/v1/verify-token", json={"token": token})
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise credentials_exception
        return AuthUserPublic(**response.json())