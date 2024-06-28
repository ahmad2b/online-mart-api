import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings

from app.kafka.consumer.order import OrderConsumer
from app.kafka.consumer.order_item  import OrderItemConsumer
from app.kafka.consumer.shipping_details import ShippingDetailsConsumer
from app.kafka.consumer.order_history import OrderHistoryConsumer


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    
    order_consumer = OrderConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="order_group")
    order_item_consumer = OrderItemConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="order_item_group")
    shipping_details_consumer = ShippingDetailsConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="shipping_details_group")
    order_history_consumer = OrderHistoryConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="order_history_group")
    
    await order_consumer.start()
    await order_item_consumer.start()
    await shipping_details_consumer.start()
    await order_history_consumer.start()

    order_task = asyncio.create_task(order_consumer.consume())
    order_item_task = asyncio.create_task(order_item_consumer.consume())
    shipping_details_task = asyncio.create_task(shipping_details_consumer.consume())
    order_history_task = asyncio.create_task(order_history_consumer.consume())
    
    try:
        yield
    finally:
        print("Stopping consumers...")
        await order_consumer.stop()
        await order_item_consumer.stop()
        await shipping_details_consumer.stop()
        await order_history_consumer.stop()
        order_task.cancel()
        order_item_task.cancel()
        shipping_details_task.cancel()
        order_history_task.cancel()
        print("Consumers stopped.")
        
        print("Stopping app..")


app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

app.include_router(api_router, prefix=settings.API_V1_STR)