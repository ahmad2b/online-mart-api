import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.core.config import settings
from app.api.main import api_router

from app.kafka.consumer.cart import CartConsumer
from app.kafka.consumer.cart_item import CartItemConsumer


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    
    cart_consumer = CartConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="cart_group")
    cart_item_consumer = CartItemConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="cart_item_group")
    
    await cart_consumer.start()
    await cart_item_consumer.start()

    cart_task = asyncio.create_task(cart_consumer.consume())
    cart_item_task = asyncio.create_task(cart_item_consumer.consume())
    
    
    try:
        yield
    finally:
        print("Stopping consumers...")
       
        await cart_consumer.stop()
        await cart_item_consumer.stop()
        cart_task.cancel()
        cart_item_task.cancel()
        print("Consumers stopped.")        

        
        print("Stopping app..")


app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

app.get("/")(lambda: {"message": "Hello World"})

app.include_router(api_router, prefix=settings.API_V1_STR)