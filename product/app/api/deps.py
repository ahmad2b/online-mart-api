from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.core.db import engine
from app.models import User
from app.kafka.producer.product import ProductProducer
from app.kafka.producer.category import CategoryProducer
from app.kafka.producer.brand import BrandProducer


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user(session: SessionDep, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


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